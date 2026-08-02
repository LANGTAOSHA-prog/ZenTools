#!/usr/bin/env python3
"""Validate tools-data.json integrity for the ZenTools static site.

This script performs a lightweight structural validation so that:
- categories remain aligned across languages
- every tool has a required metadata shape
- duplicate slugs and broken URLs are caught early
- HTML pages expose a complete ZT_PAGE multi-language map
"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT, 'data', 'tools-data.json')
REQUIRED_LANG_KEYS = ('zh', 'en', 'ja', 'vi')
LANG_PATTERN = re.compile(r'\b(zh|en|ja|vi)\s*:', re.IGNORECASE)

REQUIRED_TOOL_KEYS = [
    'name',
    'name__en',
    'name__ja',
    'name__vi',
    'slug',
    'category',
    'url',
    'description',
    'description__en',
    'description__ja',
    'description__vi',
    'icon',
    'featured',
    'new',
    'keywords',
]


def fail(message: str) -> None:
    print(f'ERROR: {message}')
    sys.exit(1)


def load_json(path: str):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        fail(f'file not found: {path}')
    except json.JSONDecodeError as exc:
        fail(f'invalid JSON in {path}: {exc}')


def validate_top_level(data):
    required_root = ['version', 'lastUpdated', 'categories', 'categories__en', 'categories__ja', 'categories__vi', 'tools']
    for key in required_root:
        if key not in data:
            fail(f'missing top-level key: {key}')

    if not isinstance(data['tools'], list):
        fail('top-level "tools" must be a list')

    lang_arrays = {
        'categories': data['categories'],
        'categories__en': data['categories__en'],
        'categories__ja': data['categories__ja'],
        'categories__vi': data['categories__vi'],
    }

    base_len = len(data['categories'])
    for lang_name, arr in lang_arrays.items():
        if len(arr) != base_len:
            fail(f'{lang_name} length mismatch: expected {base_len}, got {len(arr)}')


def validate_tools(data):
    tools = data['tools']
    seen_slugs = Counter()
    seen_urls = Counter()

    for index, tool in enumerate(tools):
        if not isinstance(tool, dict):
            fail(f'tool #{index} must be an object')

        for key in REQUIRED_TOOL_KEYS:
            if key not in tool:
                fail(f'tool #{index} missing key: {key} (slug={tool.get("slug", "<unknown>")})')

        for key in ('featured', 'new'):
            if key not in tool or not isinstance(tool[key], bool):
                fail(f'tool #{index} field {key} must be boolean')

        for key in ('name', 'name__en', 'name__ja', 'name__vi', 'slug', 'category', 'url', 'description', 'description__en', 'description__ja', 'description__vi', 'icon', 'keywords'):
            if not isinstance(tool[key], str) or not tool[key].strip():
                fail(f'tool #{index} field {key} must be a non-empty string')

        slug = tool['slug']
        seen_slugs[slug] += 1
        if seen_slugs[slug] > 1:
            fail(f'duplicate slug detected: {slug}')

        url = tool['url']
        if not url.startswith('/') or not url.endswith('.html'):
            fail(f'tool #{index} has invalid url: {url}')

        target_path = os.path.join(ROOT, url.lstrip('/'))
        if not os.path.exists(target_path):
            fail(f'tool #{index} broken url target missing: {url}')

        seen_urls[url] += 1
        if seen_urls[url] > 1:
            fail(f'duplicate url detected: {url}')

        category = tool['category']
        if category not in data['categories']:
            fail(f'tool #{index} category not found in categories list: {category}')

        if not slug.replace('-', '').replace('_', '').isalnum():
            fail(f'tool #{index} slug must be URL-safe: {slug}')

    return len(tools)


def validate_zt_page_maps():
    checked_pages = 0
    page_errors = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {'.git', '.github', '.atomcode', '.agent', '.claude', '.vscode', '__pycache__'}]
        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue
            full_path = os.path.join(dirpath, filename)
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                html_text = f.read()

            if 'window.ZT_PAGE' not in html_text and 'pageTranslations' not in html_text:
                continue

            checked_pages += 1
            found_langs = {match.group(1).lower() for match in LANG_PATTERN.finditer(html_text)}
            missing = [lang for lang in REQUIRED_LANG_KEYS if lang not in found_langs]
            if missing:
                page_errors.append(f'{full_path}: missing ZT_PAGE language keys: {missing}')

    if page_errors:
        for message in page_errors[:10]:
            print(f'ERROR: {message}')
        if len(page_errors) > 10:
            print(f'ERROR: ... and {len(page_errors) - 10} more ZT_PAGE issues')
        sys.exit(1)

    print(f'✓ ZT_PAGE language map check passed across {checked_pages} HTML pages')


def main():
    data = load_json(JSON_PATH)
    validate_top_level(data)
    tool_count = validate_tools(data)
    validate_zt_page_maps()
    print(f'✓ tools-data.json validation passed ({tool_count} tools)')


if __name__ == '__main__':
    main()
