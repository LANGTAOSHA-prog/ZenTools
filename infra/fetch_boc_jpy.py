#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取中国银行 (Bank of China) 实时日元汇率，写入 data/jpy-rate.json。

说明：
  - 中国银行外汇牌价页：https://www.boc.cn/sourcedb/whpj/
  - 日元按「100 JPY = X CNY」报价，字段顺序为：
      现汇买入价 / 现钞买入价 / 现汇卖出价 / 现钞卖出价 / 中行折算价 / 发布时间
  - 本工具换算统一采用「中行折算价」(reference rate) 作为参考汇率：
      1 CNY = 100 / 中行折算价 JPY
  - 纯静态站无后端，由 GitHub Actions 定时任务每 30 分钟运行本脚本并提交 JSON，
    前端同源拉取该 JSON 自动填充汇率，规避浏览器 CORS 限制。
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

URL = "https://www.boc.cn/sourcedb/whpj/"
OUT = "data/jpy-rate.json"
TZ_BEIJING = timezone(timedelta(hours=8))  # 北京时间


def fetch_html():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read().decode("utf-8", "ignore")


def parse(html):
    m = re.search(r"<tr data-currency='日元'>(.*?)</tr>", html, re.S)
    if not m:
        raise ValueError("未找到日元汇率行")
    cells = re.findall(r"<td[^>]*>([^<]*)</td>", m.group(1))
    # cells: [货币名, 现汇买入, 现钞买入, 现汇卖出, 现钞卖出, 中行折算价, 发布时间, 时间]
    buy = float(cells[1])
    cash_buy = float(cells[2])
    sell = float(cells[3])
    cash_sell = float(cells[4])
    ref = float(cells[5])
    published = cells[6].strip()
    if ref <= 0:
        raise ValueError("中行折算价异常: %r" % ref)
    cny_to_jpy = round(100.0 / ref, 4)
    return {
        "source": "中国银行 (Bank of China)",
        "sourceUrl": URL,
        "fetchedAt": datetime.now(TZ_BEIJING).strftime("%Y-%m-%d %H:%M:%S"),
        "publishedAt": published,
        "currency": "JPY",
        "quoteUnit": "100 JPY",
        "refRate": ref,        # 中行折算价: 100 JPY = ref CNY
        "buyRate": buy,        # 现汇买入价: 100 JPY = buy CNY
        "sellRate": sell,      # 现汇卖出价: 100 JPY = sell CNY
        "cnyToJpy": cny_to_jpy,  # 1 CNY = cnyToJpy JPY（CNY→JPY 用）
        "jpyToCny100": ref,      # 100 JPY = ref CNY（JPY→CNY 用）
    }


def main():
    try:
        html = fetch_html()
        data = parse(html)
    except Exception as e:  # 抓取/解析失败时保留旧文件，避免前端断流
        print("FETCH/PARSE FAILED:", e, file=sys.stderr)
        if os.path.exists(OUT):
            print("保留上一次成功的汇率文件。")
            sys.exit(0)
        sys.exit(1)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print("OK 发布时间=%s | 1 CNY = %s JPY | 100 JPY = %s CNY"
          % (data["publishedAt"], data["cnyToJpy"], data["jpyToCny100"]))


if __name__ == "__main__":
    main()
