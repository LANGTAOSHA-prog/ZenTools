#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow 批量提交脚本（zentools.xyz）

工作流程：
  1. 在仓库根目录找到密钥文件（命名形如 <32位十六进制>.txt，内容为密钥本身）
  2. 解析 sitemap.xml 拿到全站 URL
  3. 把 URL 主机统一归一到 zentools.xyz（去掉 www 前缀，与 keyLocation 所在主机一致）
  4. 按每批 100 条 POST 到 https://api.indexnow.org/indexnow

用法：
  python infra/submit_indexnow.py --dry-run            # 只解析+打印，不实际提交
  python infra/submit_indexnow.py --limit 10          # 仅提交前 10 条（自测）
  python infra/submit_indexnow.py                     # 全量提交
  python infra/submit_indexnow.py --batch 50          # 每批 50 条

说明：
  - 密钥文件必须已经过部署上线到 https://zentools.xyz/<key>.txt 才能提交成功，
    否则 IndexNow 返回 403（key not found）。
  - IndexNow 仅被 Bing / Yandex / Naver / Seznam 等支持，Google 不支持。
"""
import argparse
import glob
import json
import os
import re
import sys
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "zentools.xyz"
KEY_FILE_RE = re.compile(r"^[0-9a-f]{32}\.txt$")
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH_DEFAULT = 100


def find_key():
    """在仓库根目录找 IndexNow 密钥文件（32位十六进制.txt）。"""
    for p in glob.glob(os.path.join(ROOT, "*.txt")):
        name = os.path.basename(p)
        if KEY_FILE_RE.match(name):
            with open(p, "r", encoding="utf-8") as f:
                key = f.read().strip()
            if re.fullmatch(r"[0-9a-f]{32}", key):
                return key, name
    return None, None


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
    # 去重保序
    seen = set()
    uniq = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            uniq.append(u)
    return uniq


def post_batch(payload):
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
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
    ap = argparse.ArgumentParser(description="IndexNow 批量提交（zentools.xyz）")
    ap.add_argument("--dry-run", action="store_true", help="只解析打印，不提交")
    ap.add_argument("--limit", type=int, default=0, help="仅提交前 N 条（自测用）")
    ap.add_argument("--batch", type=int, default=BATCH_DEFAULT, help="每批条数")
    args = ap.parse_args()

    key, key_file = find_key()
    if not key:
        print("[ERR] 根目录未找到 IndexNow 密钥文件（应为 32 位十六进制命名的 .txt）",
              file=sys.stderr)
        sys.exit(1)
    key_location = f"https://{HOST}/{key_file}"
    print(f"[OK] 密钥文件: {key_file}")
    print(f"[OK] keyLocation: {key_location}")

    urls = load_urls_from_sitemap()
    print(f"[OK] sitemap 解析到 {len(urls)} 条 URL（已归一到 {HOST}）")

    if args.limit > 0:
        urls = urls[: args.limit]
        print(f"[*] --limit 生效，仅提交前 {len(urls)} 条")

    if args.dry_run:
        print("[DRY-RUN] 不实际提交。前 5 条示例：")
        for u in urls[:5]:
            print("   ", u)
        print(f"[DRY-RUN] 共 {len(urls)} 条，分 { (len(urls) + args.batch - 1)//args.batch } 批")
        return

    batch_size = max(1, args.batch)
    total = len(urls)
    ok = 0
    fail = 0
    for i in range(0, total, batch_size):
        chunk = urls[i : i + batch_size]
        payload = {
            "host": HOST,
            "key": key,
            "keyLocation": key_location,
            "urlList": chunk,
        }
        status, body = post_batch(payload)
        if status == 200:
            ok += len(chunk)
            print(f"  批次 {i//batch_size + 1}: {status} OK  ({len(chunk)} 条)")
        else:
            fail += len(chunk)
            print(f"  批次 {i//batch_size + 1}: {status} FAIL  body={body[:200]}")
    print(f"\n[完成] 成功 {ok} 条 / 失败 {fail} 条 / 总计 {total} 条")


if __name__ == "__main__":
    main()
