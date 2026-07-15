#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SEO 长尾词优化脚本：
1. 为缺少 meta keywords 的工具页补齐（基于 name+keywords+category+问答长尾）
2. 为已有 meta keywords 的工具页追加 2 条问答式长尾（若缺失）
3. 去重 tools-data.json keywords 字段中的冗余 "在线免费"（保留 "免费在线"）
4. 同步重生成 assets/js/tools-data.js
幂等：重复运行不会重复追加。
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT, 'data', 'tools-data.json')
JS_PATH = os.path.join(ROOT, 'assets', 'js', 'tools-data.js')

# 兼容 name-first / content-first 两种属性顺序
KW_RE = re.compile(r'<meta\s+name=["\']keywords["\']\s+content=["\']([^"\']*)["\']\s*/?>', re.I)
KW_RE2 = re.compile(r'<meta\s+content=["\']([^"\']*)["\']\s+name=["\']keywords["\']\s*/?>', re.I)
DESC_RE = re.compile(r'(<meta\s+name=["\']description["\'][^>]*>)', re.I)
TITLE_RE = re.compile(r'(</title>)', re.I)


def compact(name):
    return re.sub(r'\s+', '', name or '')


def longtail(name):
    """2 条问答式长尾"""
    nc = compact(name)
    return [nc + '在线使用', nc + '怎么用']


def build_missing_keywords(t):
    """为缺失页构造完整 meta keywords"""
    nc = compact(t['name'])
    cat = t.get('category', '') or '工具'
    core = [w for w in re.split(r'[,\s]+', t.get('keywords', '') or '') if w][:3]
    parts = [nc, t['name'] + '工具']
    for w in core:
        if w not in parts and w != nc:
            parts.append(w)
    parts.append(cat)
    parts += longtail(t['name'])
    parts.append('ZenTools')
    seen = set()
    out = []
    for p in parts:
        if p and p not in seen:
            seen.add(p)
            out.append(p)
    return ','.join(out[:8])


def detect_eol(text):
    return '\r\n' if '\r\n' in text[:4000] else '\n'


def optimize_html(t):
    url = t.get('url', '')
    if not url or not url.startswith('/') or url.endswith('/'):
        return 'skip-url'
    p = ROOT + url
    if not os.path.isfile(p):
        return 'skip-nofile'
    html = open(p, 'r', encoding='utf-8', errors='ignore', newline='').read()
    head = html[:8000]
    m = KW_RE.search(head) or KW_RE2.search(head)
    if m:
        # 已有：追加缺失的问答长尾
        content = m.group(1)
        toks = [c.strip() for c in content.split(',') if c.strip()]
        add = [x for x in longtail(t['name']) if x not in toks]
        if not add:
            return 'ok-present'
        new_content = ','.join(toks + add)
        new_tag = m.group(0).replace(content, new_content)
        html = html.replace(m.group(0), new_tag, 1)
        open(p, 'w', encoding='utf-8', newline='').write(html)
        return 'appended'
    else:
        # 缺失：在 description 后插入
        kw_str = build_missing_keywords(t)
        eol = detect_eol(html)
        new_tag = '<meta name="keywords" content="' + kw_str + '" />'
        dm = DESC_RE.search(head)
        if dm:
            html = html.replace(dm.group(1), dm.group(1) + eol + '  ' + new_tag, 1)
        else:
            tm = TITLE_RE.search(head)
            if not tm:
                return 'skip-noinsert'
            html = html.replace(tm.group(1), tm.group(1) + eol + '  ' + new_tag, 1)
        open(p, 'w', encoding='utf-8', newline='').write(html)
        return 'inserted'


def dedup_json_keywords(t):
    kw = t.get('keywords', '') or ''
    # 按逗号分组，去重 "在线免费"（与 "免费在线" 冗余），组内/组间去重
    groups = [g.strip() for g in re.split(r'[,，]', kw) if g.strip()]
    out = []
    seen = set()
    for g in groups:
        if g == '在线免费':  # 冗余反序词，丢弃
            continue
        if g not in seen:
            seen.add(g)
            out.append(g)
    t['keywords'] = ', '.join(out)


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tools = data['tools']

    # 1+2: HTML meta 优化
    stats = {'inserted': 0, 'appended': 0, 'ok-present': 0, 'skip-url': 0, 'skip-nofile': 0, 'skip-noinsert': 0}
    for t in tools:
        r = optimize_html(t)
        stats[r] = stats.get(r, 0) + 1

    # 3: JSON keywords 去重
    removed_count = 0
    for t in tools:
        before = (t.get('keywords', '') or '').count('在线免费')
        dedup_json_keywords(t)
        after = (t.get('keywords', '') or '').count('在线免费')
        removed_count += (before - after)

    # 4: 同步 tools-data.js
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write('const toolsData = ')
        json.dump(tools, f, ensure_ascii=False, indent=2)
        f.write(';\n')

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    print('=== HTML meta 优化 ===')
    print('  新增 keywords(原缺失):', stats['inserted'])
    print('  追加问答长尾(原有):', stats['appended'])
    print('  已有且完整:', stats['ok-present'])
    print('  跳过(url/文件):', stats['skip-url'] + stats['skip-nofile'])
    print('=== JSON keywords 去重 ===')
    print('  移除冗余"在线免费"次数:', removed_count)
    print('  已同步 tools-data.js:', JS_PATH)


if __name__ == '__main__':
    main()
