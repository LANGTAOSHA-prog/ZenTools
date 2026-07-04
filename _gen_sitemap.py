#!/usr/bin/env python3
"""重新生成 sitemap.xml，包含所有 .html 文件。"""

import os
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://zentools.xyz'
EXCLUDE_DIRS = {'.git', '.github', '.vscode', '.atomcode', '.claude',
                '.monkeycode', 'node_modules', 'pdf_tools', '__pycache__',
                'json', 'pdf', 'design'}


def main():
    root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    count = 0

    for dirpath, dirnames, filenames in os.walk(SCRIPT_DIR):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith('.html'):
                rel = os.path.relpath(os.path.join(dirpath, fn), SCRIPT_DIR)
                u = ET.SubElement(root, 'url')
                ET.SubElement(u, 'loc').text = f'{BASE_URL}/{rel}'
                count += 1

    out = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(out, 'w', encoding='utf-8') as f:
        f.write(ET.tostring(root, encoding='unicode'))
    print(f'✓ sitemap.xml 已生成: {count} 个 URL')


if __name__ == '__main__':
    main()