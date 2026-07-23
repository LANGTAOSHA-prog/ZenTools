#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
百度普通收录主动推送脚本（zentools.xyz）

前置条件：
  1. 在 https://ziyuan.baidu.com 添加站点 zentools.xyz 并完成所有权验证
     （文件验证：把 baidu_verify_xxxx.html 放到仓库根目录，经部署上线即可）。
  2. 在「普通收录」页获取接口调用 token（接口地址里 ?token= 后面的那段）。
  3. 把 token 设为环境变量 BAIDU_ZIYUAN_TOKEN —— 切勿写入仓库或脚本本身。

用法：
  # Windows PowerShell
  $env:BAIDU_ZIYUAN_TOKEN = "你的token"
  python infra/submit_baidu.py                # 全量推送
  python infra/submit_baidu.py --limit 10     # 自测前 10 条
  python infra/submit_baidu.py --batch 500    # 每批 500 条（官方上限 2000/次）
  python infra/submit_baidu.py --dry-run      # 只解析打印，不推送

接口：POST http://data.zz.baidu.com/urls?site=https://zentools.xyz&token=TOKEN
请求体：Content-Type: text/plain，每行一个 URL
返回  ：{"remain":剩余配额,"success":成功数,"not_valid":非法数,
         "not_same_site":非本站数,"error":错误码,"message":"..."}

说明：
  - 百度仅对"已验证站点"的 URL 受理，未验证或跨站会被 not_same_site 计入。
  - 普通收录是"加速发现"，不保证收录；与 IndexNow(Bing系) 互补。
  - Google 不支持此类实时推送，请继续用 sitemap + 前50手动清单。
"""
import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "zentools.xyz"
ENDPOINT = "http://data.zz.baidu.com/urls"
BATCH_DEFAULT = 1000


def normalize_url(loc):
    """把 URL 主机归一到 zentools.xyz（去 www），协议强制 https。"""
    m = re.match(r"^(https?)://([^/]+)(/.*)?$", loc.strip())
    if not m:
        return None
    path = m.group(3) or "/"
    return f"https://{HOST}{path}"


def load_urls_from_sitemap():
    sm = os.path.join(ROOT, "sitemap.xml")
    if not os.path.exists(sm):
        print(f"[ERR] 找不到 sitemap.xml: {sm}", file=sys.stderr)
        sys.exit(1)
    tree = ET.parse(sm)
    urls = []
    for loc in tree.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc"):
        if loc.text:
            u = normalize_url(loc.text)
            if u:
                urls.append(u)
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def post_batch(api_url, chunk):
    body = "\n".join(chunk).encode("utf-8")
    req = urllib.request.Request(
        api_url,
        data=body,
        headers={"Content-Type": "text/plain"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:  # noqa
        return 0, str(e)


def main():
    ap = argparse.ArgumentParser(description="百度普通收录主动推送（zentools.xyz）")
    ap.add_argument("--dry-run", action="store_true", help="只解析打印，不推送")
    ap.add_argument("--limit", type=int, default=0, help="仅提交前 N 条（自测用）")
    ap.add_argument("--batch", type=int, default=BATCH_DEFAULT, help="每批条数(≤2000)")
    args = ap.parse_args()

    token = os.environ.get("BAIDU_ZIYUAN_TOKEN")
    if not token:
        print("[ERR] 未检测到 BAIDU_ZIYUAN_TOKEN 环境变量。", file=sys.stderr)
        print("      请先在百度搜索资源平台验证站点并获取 token，然后：", file=sys.stderr)
        print('      $env:BAIDU_ZIYUAN_TOKEN = "你的token"', file=sys.stderr)
        sys.exit(1)
    api_url = f"{ENDPOINT}?site=https://{HOST}&token={token}"
    print(f"[OK] 站点: https://{HOST}")
    print(f"[OK] 接口: {ENDPOINT}?site=https://{HOST}&token=***(已隐藏)")

    urls = load_urls_from_sitemap()
    print(f"[OK] sitemap 解析到 {len(urls)} 条 URL（已归一到 {HOST}）")

    if args.limit > 0:
        urls = urls[: args.limit]
        print(f"[*] --limit 生效，仅推送前 {len(urls)} 条")

    if args.dry_run:
        print("[DRY-RUN] 不实际推送。前 5 条示例：")
        for u in urls[:5]:
            print("   ", u)
        print(f"[DRY-RUN] 共 {len(urls)} 条，分 { (len(urls) + args.batch - 1)//args.batch } 批")
        return

    batch_size = min(max(1, args.batch), 2000)
    total = len(urls)
    success_total = 0
    not_valid_total = 0
    not_same_site_total = 0
    fail = 0
    for i in range(0, total, batch_size):
        chunk = urls[i : i + batch_size]
        status, body = post_batch(api_url, chunk)
        if status == 200:
            try:
                rj = json.loads(body)
            except Exception:
                rj = {}
            s = rj.get("success", 0)
            nv = rj.get("not_valid", 0)
            nss = rj.get("not_same_site", 0)
            success_total += s
            not_valid_total += nv
            not_same_site_total += nss
            remain = rj.get("remain", "?")
            print(f"  批次 {i//batch_size + 1}: 200 OK  success={s} not_valid={nv} "
                  f"not_same_site={nss} remain={remain}")
        else:
            fail += len(chunk)
            print(f"  批次 {i//batch_size + 1}: {status} FAIL  body={body[:200]}")
    print(f"\n[完成] 成功 {success_total} 条 / 非法 {not_valid_total} 条 / "
          f"非本站 {not_same_site_total} 条 / 推送失败 {fail} 条 / 总计 {total} 条")


if __name__ == "__main__":
    main()
