#!/usr/bin/env python3
"""Unit tests for _changelog_utils.py"""

import json
import os
import sys
import tempfile
import unittest
from datetime import date, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _changelog_utils import (
    build_tool_entry,
    build_tutorial_entry,
    build_guide_entry,
    append_changelog,
    load_site_info,
    sync_metadata,
    _default_site_info,
)


class TestBuildEntries(unittest.TestCase):

    def test_build_tool_entry_four_langs(self):
        entry = build_tool_entry("PDF OCR", "PDF OCR", "PDF OCR", "PDF OCR")
        for lang in ['zh', 'en', 'ja', 'vi']:
            self.assertIn(lang, entry)
            self.assertIsInstance(entry[lang], str)
            self.assertTrue(len(entry[lang]) > 0)

    def test_build_tutorial_entry_four_langs(self):
        entry = build_tutorial_entry("教程", "Tutorial", "チュートリアル", "Hướng dẫn")
        for lang in ['zh', 'en', 'ja', 'vi']:
            self.assertIn(lang, entry)

    def test_build_guide_entry_four_langs(self):
        entry = build_guide_entry("指南", "Guide", "ガイド", "Hướng dẫn")
        for lang in ['zh', 'en', 'ja', 'vi']:
            self.assertIn(lang, entry)


class TestAppendChangelog(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def _make_data(self, changelog=None):
        return {
            "version": "3.0.0",
            "lastUpdated": "2026-07-01",
            "toolCount": 100,
            "changelog": changelog or []
        }

    def test_same_day_aggregation(self):
        today = date.today().isoformat()
        data = self._make_data([{
            "version": "3.0.0",
            "date": today,
            "zh": "已有内容",
            "en": "Existing",
            "ja": "既存",
            "vi": "Hiện có",
            "items": {
                "zh": ["已有条目A"],
                "en": ["Existing item A"],
                "ja": ["既存A"],
                "vi": ["Hiện có A"]
            }
        }])

        entry = build_tool_entry("新工具", "New Tool", "新ツール", "Công cụ mới")
        result = append_changelog(data, [entry])

        self.assertEqual(len(result['changelog']), 1)
        latest = result['changelog'][0]
        self.assertEqual(latest['date'], today)
        self.assertIn("已有条目A", latest['items']['zh'])
        self.assertIn("新增工具：新工具", latest['items']['zh'])

    def test_cross_day_new_entry(self):
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        data = self._make_data([{
            "version": "3.0.0",
            "date": yesterday,
            "zh": "昨天的内容",
            "en": "Yesterday",
            "ja": "昨日",
            "vi": "Hôm qua",
            "items": {
                "zh": ["旧条目"],
                "en": ["Old item"],
                "ja": ["旧"],
                "vi": ["Cũ"]
            }
        }])

        entry = build_tool_entry("新工具", "New Tool", "新ツール", "Công cụ mới")
        result = append_changelog(data, [entry])

        self.assertEqual(len(result['changelog']), 2)
        today_entry = result['changelog'][0]
        self.assertEqual(today_entry['date'], date.today().isoformat())
        self.assertIn("新增工具：新工具", today_entry['items']['zh'])

    def test_empty_changelog_creates_first_entry(self):
        data = self._make_data([])
        entry = build_tutorial_entry("教程A", "Tutorial A", "チュートリアルA", "HD A")
        result = append_changelog(data, [entry])

        self.assertEqual(len(result['changelog']), 1)
        self.assertEqual(result['changelog'][0]['date'], date.today().isoformat())

    def test_duplicate_entry_not_added(self):
        today = date.today().isoformat()
        data = self._make_data([{
            "version": "3.0.0",
            "date": today,
            "zh": "测试",
            "en": "Test",
            "ja": "テスト",
            "vi": "Test",
            "items": {
                "zh": ["新增工具：测试工具"],
                "en": ["New tool: Test Tool"],
                "ja": ["新規ツール：テストツール"],
                "vi": ["Công cụ mới: Test Tool"]
            }
        }])

        entry = build_tool_entry("测试工具", "Test Tool", "テストツール", "Test Tool")
        result = append_changelog(data, [entry])

        zh_items = result['changelog'][0]['items']['zh']
        self.assertEqual(zh_items.count("新增工具：测试工具"), 1)


class TestSyncMetadata(unittest.TestCase):

    def test_sync_updates_last_updated(self):
        data = {"version": "1.0", "lastUpdated": "2020-01-01", "toolCount": 0, "changelog": []}
        result = sync_metadata(data, tool_count=50)
        self.assertEqual(result['lastUpdated'], date.today().isoformat())
        self.assertEqual(result['toolCount'], 50)


if __name__ == '__main__':
    unittest.main()
