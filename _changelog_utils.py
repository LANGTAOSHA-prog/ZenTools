#!/usr/bin/env python3
"""changelog 公共操作模块：读取/写入 site-info.json，构建变更项，当日聚合追加。"""

import json
import os
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SITE_INFO_PATH = os.path.join(SCRIPT_DIR, 'data', 'site-info.json')
TOOLS_DATA_PATH = os.path.join(SCRIPT_DIR, 'data', 'tools-data.json')


def _default_site_info():
    return {
        "version": "1.0.0",
        "lastUpdated": date.today().isoformat(),
        "toolCount": 0,
        "changelog": []
    }


def load_site_info():
    if not os.path.exists(SITE_INFO_PATH):
        return _default_site_info()
    with open(SITE_INFO_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_site_info(data):
    os.makedirs(os.path.dirname(SITE_INFO_PATH), exist_ok=True)
    with open(SITE_INFO_PATH, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def build_tool_entry(name_zh, name_en, name_ja, name_vi):
    return {
        "zh": "新增工具：" + name_zh,
        "en": "New tool: " + name_en,
        "ja": "新規ツール：" + name_ja,
        "vi": "Công cụ mới: " + name_vi
    }


def build_tutorial_entry(title_zh, title_en, title_ja, title_vi):
    return {
        "zh": "新增教程：" + title_zh,
        "en": "New tutorial: " + title_en,
        "ja": "新規チュートリアル：" + title_ja,
        "vi": "Hướng dẫn mới: " + title_vi
    }


def build_guide_entry(title_zh, title_en, title_ja, title_vi):
    return {
        "zh": "新增指南：" + title_zh,
        "en": "New guide: " + title_en,
        "ja": "新規ガイド：" + title_ja,
        "vi": "Hướng dẫn chuyên sâu mới: " + title_vi
    }


def sync_metadata(data, tool_count=None):
    data['lastUpdated'] = date.today().isoformat()
    if tool_count is not None:
        data['toolCount'] = tool_count
    elif os.path.exists(TOOLS_DATA_PATH):
        with open(TOOLS_DATA_PATH, 'r', encoding='utf-8') as f:
            tools_data = json.load(f)
        data['toolCount'] = len(tools_data.get('tools', []))
    return data


def append_changelog(data, entries):
    if not entries:
        return data

    data = sync_metadata(data)
    today = date.today().isoformat()

    latest = data['changelog'][0] if data.get('changelog') else None

    if latest and latest.get('date') == today:
        for entry in entries:
            for lang in ['zh', 'en', 'ja', 'vi']:
                item_text = entry.get(lang, '')
                if item_text and item_text not in latest['items'][lang]:
                    latest['items'][lang].append(item_text)
    else:
        first = entries[0]
        new_entry = {
            "version": data.get("version", "1.0.0"),
            "date": today,
            "zh": first.get("zh", ""),
            "en": first.get("en", ""),
            "ja": first.get("ja", ""),
            "vi": first.get("vi", ""),
            "items": {lang: [] for lang in ['zh', 'en', 'ja', 'vi']}
        }
        for entry in entries:
            for lang in ['zh', 'en', 'ja', 'vi']:
                item_text = entry.get(lang, '')
                if item_text:
                    new_entry['items'][lang].append(item_text)
        data['changelog'].insert(0, new_entry)

    return data
