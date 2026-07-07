#!/usr/bin/env python3
"""Unit tests for _sync_changelog.py"""

import json
import os
import sys
import tempfile
import unittest
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _changelog_utils import (
    load_site_info, save_site_info,
    build_tool_entry, append_changelog, sync_metadata
)


class TestSyncChangelog(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.orig_site_info = os.environ.get('SITE_INFO_TEST')

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _make_tmp_site_info(self, data):
        path = os.path.join(self.tmpdir, 'site-info.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return path

    def test_scan_appends_missing_tools(self):
        data = {
            "version": "2.0.0",
            "lastUpdated": "2026-01-01",
            "toolCount": 10,
            "changelog": []
        }
        self._make_tmp_site_info(data)

        entries = [build_tool_entry("测试工具", "Test Tool", "テストツール", "Test Tool")]
        result = append_changelog(data, entries)

        self.assertEqual(len(result['changelog']), 1)
        self.assertIn("新增工具：测试工具", result['changelog'][0]['items']['zh'])

    def test_reset_rebuilds_metadata(self):
        data = {
            "version": "1.0.0",
            "lastUpdated": "2020-01-01",
            "toolCount": 5,
            "changelog": [{"version": "1.0.0", "date": "2020-01-01",
                           "zh": "旧", "en": "Old", "ja": "旧", "vi": "Cũ",
                           "items": {"zh": ["旧条目"], "en": ["Old"], "ja": ["旧"], "vi": ["Cũ"]}}]
        }

        result = sync_metadata(data, tool_count=50)
        self.assertEqual(result['lastUpdated'], date.today().isoformat())
        self.assertEqual(result['toolCount'], 50)
        self.assertEqual(len(result['changelog']), 1)


if __name__ == '__main__':
    unittest.main()
