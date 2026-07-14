#!/usr/bin/env python3
"""
独立 changelog 同步脚本。

模式:
  --scan          扫描 tools-data.json 中的 new 标记和 HTML 文件，将缺失项追加到 changelog
  --from-commits 从提交消息文件中提取 `cl:` 标记行，追加为 changelog 条目
  --reset         以 tools-data.json 为基准重建 site-info.json 元数据，保留已有 changelog 条目
"""

import argparse
import json
import os
import re
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

from _changelog_utils import (
    load_site_info, save_site_info,
    build_tool_entry, build_tutorial_entry, build_guide_entry, build_cl_entry,
    append_changelog, sync_metadata
)

TOOLS_DATA_PATH = os.path.join(SCRIPT_DIR, 'data', 'tools-data.json')
SITE_INFO_PATH = os.path.join(SCRIPT_DIR, 'data', 'site-info.json')


def scan_mode():
    print("=== changelog 扫描模式 ===")
    data = load_site_info()

    entries = []

    if os.path.exists(TOOLS_DATA_PATH):
        with open(TOOLS_DATA_PATH, 'r', encoding='utf-8') as f:
            tools_data = json.load(f)

        new_tools = [t for t in tools_data.get('tools', []) if t.get('new')]
        current_items = set()
        for entry in data.get('changelog', []):
            for lang in ['zh', 'en', 'ja', 'vi']:
                for item in entry.get('items', {}).get(lang, []):
                    current_items.add(item)

        for tool in new_tools:
            entry = build_tool_entry(
                tool.get('name', ''),
                tool.get('name__en', tool.get('name', '')),
                tool.get('name__ja', tool.get('name', '')),
                tool.get('name__vi', tool.get('name', ''))
            )
            if entry['zh'] not in current_items:
                entries.append(entry)
                print(f"  发现新工具: {entry['zh']}")

    if entries:
        data = append_changelog(data, entries)
        save_site_info(data)
        print(f"✓ 已追加 {len(entries)} 条变更记录")
    else:
        print("  没有发现新的变更记录")

    print(f"  工具总数: {data.get('toolCount', 'N/A')}")
    print(f"  更新日期: {data.get('lastUpdated', 'N/A')}")


def from_commits_mode(path):
    print("=== changelog 从 commit 标记提取 ===")
    data = load_site_info()
    entries = []
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^\s*cl:\s*(.*)$', line, re.IGNORECASE)
                if m:
                    text = m.group(1).strip()
                    if text:
                        entries.append(build_cl_entry(text))
                        print(f"  发现标记: {text}")
    if entries:
        data = append_changelog(data, entries)
        save_site_info(data)
        print(f"✓ 已追加 {len(entries)} 条变更记录")
    else:
        print("  没有发现 cl: 标记")


def reset_mode():
    print("=== changelog 重置模式 ===")
    data = load_site_info()

    if os.path.exists(TOOLS_DATA_PATH):
        with open(TOOLS_DATA_PATH, 'r', encoding='utf-8') as f:
            tools_data = json.load(f)
        data['version'] = tools_data.get('version', data.get('version', '1.0.0'))
        data = sync_metadata(data)
        print(f"  版本: {data['version']}")
        print(f"  工具总数: {data['toolCount']}")
        print(f"  更新日期: {data['lastUpdated']}")

    save_site_info(data)
    print("✓ site-info.json 元数据已重建（changelog 条目已保留）")


def main():
    parser = argparse.ArgumentParser(description='同步 site-info.json changelog 数据')
    parser.add_argument('--scan', action='store_true', help='扫描新工具并追加到 changelog')
    parser.add_argument('--from-commits', metavar='FILE', help='从提交消息文件提取 cl: 标记并追加')
    parser.add_argument('--reset', action='store_true', help='重建 site-info.json 元数据')

    args = parser.parse_args()
    if not args.scan and not args.reset and not args.from_commits:
        parser.print_help()
        sys.exit(1)
    if args.scan:
        scan_mode()
    if args.from_commits:
        from_commits_mode(args.from_commits)
    if args.reset:
        reset_mode()


if __name__ == '__main__':
    main()
