#!/usr/bin/env python3
"""重新生成 sitemap.xml 和 sitemap.txt，包含所有 .html 文件。"""

import os
import time
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://zentools.xyz'
EXCLUDE_DIRS = {
    '.git', '.github', '.vscode', '.atomcode', '.claude',
    '.monkeycode', 'node_modules', 'pdf_tools', '__pycache__',
    'json', 'pdf', 'design'
}

# 优先级规则：根目录 > 分类页 > 工具页 > 教程/指南
PRIORITY_RULES = {
    '/index.html':            ('daily',  '1.0'),
    '/about.html':            ('weekly', '0.8'),
    '/changelog.html':        ('daily',  '0.9'),
    '/privacy.html':          ('monthly','0.5'),
    '/terms.html':            ('monthly','0.5'),
    '/tools.html':            ('daily',  '0.9'),
    '/categories.html':       ('weekly', '0.7'),
    '/contact.html':          ('monthly','0.6'),
}

CATEGORY_INDEXES = {
    '/ai/index.html', '/audio/index.html', '/compare/index.html',
    '/dev/index.html', '/finance/index.html', '/guides/index.html',
    '/image/index.html', '/knowledge/index.html', '/life/index.html',
    '/qr/index.html', '/seo/index.html', '/text/index.html',
    '/tools/index.html', '/tutorials/index.html', '/video/index.html',
    '/yunchuang/index.html',
}


def _priority(rel_path: str) -> tuple:
    """根据路径返回 (changefreq, priority)。"""
    # 精确匹配根目录页面
    if rel_path in PRIORITY_RULES:
        return PRIORITY_RULES[rel_path]
    # 分类索引页
    if rel_path in CATEGORY_INDEXES:
        return ('weekly', '0.8')
    # 其他工具页面
    return ('weekly', '0.6')


def main():
    root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    now = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    count = 0
    txt_lines = []

    for dirpath, dirnames, filenames in os.walk(SCRIPT_DIR):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith('.html'):
                abs_path = os.path.join(dirpath, fn)
                rel = os.path.relpath(abs_path, SCRIPT_DIR)
                mtime = os.path.getmtime(abs_path)
                lastmod = time.strftime('%Y-%m-%d', time.gmtime(mtime))
                changefreq, priority = _priority('/' + rel)

                u = ET.SubElement(root, 'url')
                ET.SubElement(u, 'loc').text = f'{BASE_URL}/{rel}'
                ET.SubElement(u, 'lastmod').text = lastmod
                ET.SubElement(u, 'changefreq').text = changefreq
                ET.SubElement(u, 'priority').text = priority

                txt_lines.append(f'{BASE_URL}/{rel}')
                count += 1

    # 写入 sitemap.xml（加 XML 声明）
    out_xml = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(out_xml, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(root, encoding='unicode'))
        f.write('\n')
    print(f'✓ sitemap.xml 已生成: {count} 个 URL (含 lastmod/changefreq/priority)')

    # 同步写入 sitemap.txt
    out_txt = os.path.join(SCRIPT_DIR, 'sitemap.txt')
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_lines))
        f.write('\n')
    print(f'✓ sitemap.txt 已生成: {count} 个 URL')


if __name__ == '__main__':
    main()