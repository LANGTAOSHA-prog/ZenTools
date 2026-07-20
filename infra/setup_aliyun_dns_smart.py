#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 DNS 智能解析 - 自动添加「境外」线路记录（Cloudflare 加速，备案合规版）
========================================================================
纯标准库实现（无需 pip install 任何包），直接调用阿里云 OpenAPI(RPC 签名)。

在现有 @/www 默认指向阿里云 39.96.10.135 的基础上，
新增「境外/国外」线路，把海外用户分流到 Cloudflare 边缘。

⚠️ 合规前提（详见 dns-smart-resolution-draft.md）：
   - DNS 权威始终留在阿里云(hichina)，**绝不把 NS 交给 Cloudflare**。
   - Cloudflare 侧必须用「CNAME 接入 / Partial setup」，不是改 NS。
   - CF_TARGET = Cloudflare CNAME 接入时给 www.zentools.xyz 的 CNAME 目标
     （形如 www.zentools.xyz.cdn.cloudflare.net 或 xxxx.cloudflare.net）。
   - Cloudflare 怎么服务该 Host：方案① CDN 回源 ECS(推荐, 内容一致) /
     方案② Route 到 Worker(zentools.taojianghu.workers.dev)。

用法：
  # 只读检查现有记录（验证凭证 + 看当前 zone），需要凭证：
  export ALIBABACLOUD_ACCESS_KEY_ID=xxxx
  export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx
  python setup_aliyun_dns_smart.py --check

  # 预览将要添加的境外记录（无需凭证，只需 CF_TARGET）：
  export CF_TARGET=www.zentools.xyz.cdn.cloudflare.net
  python setup_aliyun_dns_smart.py

  # 真实写入：
  export ALIBABACLOUD_ACCESS_KEY_ID=xxxx
  export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx
  export CF_TARGET=www.zentools.xyz.cdn.cloudflare.net
  export CF_APEX_IP=104.16.x.x,172.67.x.x   # 国外 @ 的 A 目标(可选; 不填则 @ 始终走阿里云)
  python setup_aliyun_dns_smart.py --apply

  # GCP 自建节点方案（国外 -> 谷歌云 IP，国内仍走阿里云 39.96.10.135）：
  export ALIBABACLOUD_ACCESS_KEY_ID=xxxx
  export ALIBABACLOUD_ACCESS_KEY_SECRET=xxxx
  export GCP_IP=34.143.64.123               # 谷歌云实例外部 IP
  python setup_aliyun_dns_smart.py --gcp --apply     # 真实写入「境外」线路
  python setup_aliyun_dns_smart.py --gcp            # 仅预览(不改动)
"""
import os
import sys
import ssl
import json
import uuid
import hmac
import hashlib
import base64
import urllib.parse
import urllib.request
from datetime import datetime, timezone

DOMAIN = "zentools.xyz"
ENDPOINT = "https://dns.aliyuncs.com/"

# 仅新增「境外」线路。阿里云 Line="overseas" 即智能解析的「境外/国外」。
# 国内外默认线路(@/www)保持指向阿里云 39.96.10.135，本脚本不改动它。
#
# 国外目标有两种可选方案（由 --gcp / 默认 CF 决定）：
#   CF 方案 : www->CNAME(CF_TARGET)  @->A(CF_APEX_IP)  走 Cloudflare 边缘
#   GCP 方案: www->A(GCP_IP)  @->A(GCP_IP)             走谷歌云自建节点(代码 git 同步, 内容一致)

GCP_IP = os.environ.get("GCP_IP", "34.143.64.123")


def build_records(target):
    """按 target 返回要添加的「境外」线路记录列表。"""
    if target == "gcp":
        ip = os.environ.get("GCP_IP", "34.143.64.123").strip()
        return [
            {
                "rr": "www", "type": "A", "value": ip,
                "line": "overseas", "ttl": 600, "required": True,
                "desc": "国外 www -> 谷歌云节点 A 记录(代码 git 同步, 与国内内容一致)",
            },
            {
                "rr": "@", "type": "A", "value": ip,
                "line": "overseas", "ttl": 600, "required": True,
                "desc": "国外 @ -> 谷歌云节点 A 记录(根域只能用 A)",
            },
        ]
    # 默认 Cloudflare 方案
    return [
        {
            "rr": "www", "type": "CNAME", "value_env": "CF_TARGET",
            "line": "overseas", "ttl": 600, "required": True,
            "desc": "国外 www -> Cloudflare 自定义域 CNAME (最终指向 zentools.taojianghu.workers.dev)",
        },
        {
            "rr": "@", "type": "A", "value_env": "CF_APEX_IP",
            "line": "overseas", "ttl": 600, "required": False,
            "desc": "国外 @ -> Cloudflare 任播 IP (根域不能用 CNAME; 不填则 @ 始终走阿里云)",
        },
    ]


def percent_encode(s):
    """阿里云风格 percent-encode：字母数字及 -_.~ 不编码，其余 UTF-8 字节 %XX。"""
    return urllib.parse.quote(str(s), safe="-_.~")


def sign(params, secret):
    # 1) 按 key 字典序拼接 canonical query
    items = sorted(params.items())
    canon = "&".join(f"{percent_encode(k)}={percent_encode(v)}" for k, v in items)
    # 2) StringToSign = HTTPMethod & percentEncode("/") & percentEncode(canon)
    string_to_sign = "GET&" + percent_encode("/") + "&" + percent_encode(canon)
    # 3) HMAC-SHA1，key = secret + "&"
    key = (secret + "&").encode("utf-8")
    dig = hmac.new(key, string_to_sign.encode("utf-8"), hashlib.sha1).digest()
    return base64.b64encode(dig).decode("ascii")


def call_api(action, secret_id, secret, **kwargs):
    params = {
        "Action": action,
        "Format": "JSON",
        "Version": "2015-01-09",
        "AccessKeyId": secret_id,
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": uuid.uuid4().hex,
        "Timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    params.update(kwargs)
    params["Signature"] = sign(params, secret)
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    ctx = ssl.create_default_context()
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")


def do_check(secret_id, secret):
    try:
        data = call_api("DescribeDomainRecords", secret_id, secret, DomainName=DOMAIN, PageSize=100)
    except Exception as e:
        print(f"✗ 查询失败: {e}")
        return
    recs = (data.get("DomainRecords") or {}).get("Record", [])
    print(f"阿里云 zone 现有记录数: {len(recs)}")
    for r in recs:
        print(f"  RR={r.get('RR')!r} Type={r.get('Type')!r} Line={r.get('Line')!r} "
              f"Value={r.get('Value')!r} TTL={r.get('TTL')} Status={r.get('Status')}")


def main():
    args = sys.argv[1:]
    check = "--check" in args
    apply = "--apply" in args
    target = "gcp" if "--gcp" in args else "cf"
    secret_id = os.environ.get("ALIBABACLOUD_ACCESS_KEY_ID")
    secret = os.environ.get("ALIBABACLOUD_ACCESS_KEY_SECRET")

    if check:
        if not secret_id or not secret:
            sys.exit("✗ --check 需要凭证: 请先 export ALIBABACLOUD_ACCESS_KEY_ID / ALIBABACLOUD_ACCESS_KEY_SECRET")
        do_check(secret_id, secret)
        return

    if apply and (not secret_id or not secret):
        sys.exit("✗ 缺少凭证: 请先 export ALIBABACLOUD_ACCESS_KEY_ID / ALIBABACLOUD_ACCESS_KEY_SECRET")

    records = build_records(target)
    print(f"域名: {DOMAIN}")
    print(f"国外目标方案: {'GCP(谷歌云自建节点)' if target == 'gcp' else 'Cloudflare'}")
    print(f"模式: {'【真实写入】' if apply else '【预览 dry-run】'}")
    print("-" * 60)

    for r in records:
        val = r.get("value") or os.environ.get(r.get("value_env", ""), "")
        if not val:
            if r["required"]:
                sys.exit(f"✗ 缺少目标值 (用于 {r['rr']} {r['type']} | {r['desc']})")
            else:
                print(f"跳过(可选): {r['rr']} {r['type']} {r['line']}")
                continue
        values = [v.strip() for v in val.split(",") if v.strip()]
        for v in values:
            label = f"{r['rr']} / {r['line']} / {r['type']} -> {v} (TTL {r['ttl']})"
            if not apply:
                print(f"[预览] 将添加: {label}  # {r['desc']}")
                continue
            try:
                call_api("AddDomainRecord", secret_id, secret,
                         DomainName=DOMAIN, RR=r["rr"], Type=r["type"],
                         Value=v, Line=r["line"], TTL=r["ttl"])
                print(f"[已添加] {label}")
            except Exception as e:
                print(f"[失败] {label}: {e}")

    print("-" * 60)
    print("完成。" if apply else "预览结束(未做任何改动)。加 --apply 真正写入。")


if __name__ == "__main__":
    main()
