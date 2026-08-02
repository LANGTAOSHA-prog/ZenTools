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
JS_TOOLS_DATA_PATH = os.path.join(ROOT, 'assets', 'js', 'tools-data.js')
REQUIRED_LANG_KEYS = ('zh', 'en', 'ja', 'vi')
LANG_PATTERN = re.compile(r'(?:(?:"|\')?(zh|en|ja|vi)(?:"|\')?\s*:)', re.IGNORECASE)

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


def read_text(path: str) -> str:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except FileNotFoundError:
        fail(f'file not found: {path}')


def find_matching_brace(text: str, start_index: int) -> int:
    depth = 0
    for idx in range(start_index, len(text)):
        char = text[idx]
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                return idx
    return -1


def extract_translation_map(text: str):
    patterns = [
        re.compile(r'window\.ZT_PAGE\s*=\s*\{', re.IGNORECASE),
        re.compile(r'window\.pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'window\.ZT_PAGE\s*=\s*translations\s*;', re.IGNORECASE),
        re.compile(r'window\.ZT_PAGE\s*=\s*pageTranslations\s*;', re.IGNORECASE),
        re.compile(r'var\s+pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'const\s+pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'let\s+pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'var\s+translations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'const\s+translations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'let\s+translations\s*=\s*\{', re.IGNORECASE),
    ]

    for pattern in patterns:
        match = pattern.search(text)
        if not match:
            continue

        if 'translations' in pattern.pattern or 'pageTranslations' in pattern.pattern:
            alias_name = 'translations' if 'translations' in pattern.pattern else 'pageTranslations'
            alias_decl = re.search(rf'(?:var|const|let)\s+{alias_name}\s*=\s*\{{', text, re.IGNORECASE)
            if alias_decl:
                open_brace = text.find('{', alias_decl.start())
                if open_brace != -1:
                    close_brace = find_matching_brace(text, open_brace)
                    if close_brace != -1:
                        return text[open_brace + 1:close_brace]

        open_brace = text.find('{', match.start())
        if open_brace == -1:
            continue
        close_brace = find_matching_brace(text, open_brace)
        if close_brace == -1:
            continue
        return text[open_brace + 1:close_brace]

    alias_match = re.search(r'window\.ZT_PAGE\s*=\s*([A-Za-z_$][A-Za-z0-9_$]*)\s*;', text, re.IGNORECASE)
    if alias_match:
        alias_name = alias_match.group(1)
        alias_decl = re.search(rf'(?:var|const|let)\s+{re.escape(alias_name)}\s*=\s*\{{', text, re.IGNORECASE)
        if alias_decl:
            open_brace = text.find('{', alias_decl.start())
            if open_brace != -1:
                close_brace = find_matching_brace(text, open_brace)
                if close_brace != -1:
                    return text[open_brace + 1:close_brace]

    return None


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
    slug_mismatches = []

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

        file_name = os.path.basename(url).rsplit('.html', 1)[0]
        parent_dir = os.path.basename(os.path.dirname(url))
        if file_name == 'index':
            continue

        accepted_slugs = {file_name}
        if parent_dir:
            accepted_slugs.add(f'{parent_dir}-{file_name}')
            accepted_slugs.add(f'{parent_dir}_{file_name}')
            accepted_slugs.add(f'{parent_dir}.{file_name}')

        if slug not in accepted_slugs:
            slug_mismatches.append((index, slug, url, file_name, sorted(accepted_slugs)))

    if slug_mismatches:
        print(f'⚠ slug/file-name mismatch count: {len(slug_mismatches)}')
        for index, slug, url, file_name, accepted in slug_mismatches[:12]:
            print(f'  - tool #{index}: slug={slug} url={url} file-name={file_name} accepted={accepted}')

    return len(tools)


def validate_runtime_data_sync(data):
    js_text = read_text(JS_TOOLS_DATA_PATH)
    match = re.search(r'const\s+toolsData\s*=\s*(\[[\s\S]*?\])\s*;', js_text)
    if not match:
        fail(f'could not locate toolsData export in {JS_TOOLS_DATA_PATH}')

    try:
        js_tools = json.loads(match.group(1))
    except json.JSONDecodeError as exc:
        fail(f'invalid JS data export in {JS_TOOLS_DATA_PATH}: {exc}')

    json_tools = data['tools']
    if js_tools != json_tools:
        fail('assets/js/tools-data.js is out of sync with data/tools-data.json')

    print('✓ assets/js/tools-data.js matches data/tools-data.json')


def validate_zt_page_maps():
    checked_pages = 0
    page_errors = []

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in {'.git', '.github', '.atomcode', '.agent', '.claude', '.vscode', '__pycache__'}]
        for filename in filenames:
            if not filename.lower().endswith('.html'):
                continue
            full_path = os.path.join(dirpath, filename)
            html_text = read_text(full_path)

            if 'window.ZT_PAGE' not in html_text and 'pageTranslations' not in html_text:
                continue

            translation_map = extract_translation_map(html_text)
            if translation_map is None:
                page_errors.append(f'{full_path}: could not extract ZT_PAGE / pageTranslations object')
                continue

            checked_pages += 1
            found_langs = {match.group(1).lower() for match in LANG_PATTERN.finditer(translation_map)}
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
    validate_runtime_data_sync(data)
    validate_zt_page_maps()
    print(f'✓ tools-data.json validation passed ({tool_count} tools)')


if __name__ == '__main__':
    main()
