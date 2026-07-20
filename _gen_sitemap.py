#!/usr/bin/env python3
"""重新生成 sitemap.xml 和 sitemap.txt，包含所有 .html 文件。

P0 修复要点：
  - 排除内部/非内容目录与页面（避免稀释抓取预算）
  - lastmod 优先取「该文件最近一次 git 提交日期」（反映真实内容变更，
    且跨克隆/部署稳定），git 不可用时回退到文件 mtime
"""

import os
import subprocess
import time
import xml.etree.ElementTree as ET

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_URL = 'https://zentools.xyz'

# 非内容 / 内部目录：整目录不进 sitemap
EXCLUDE_DIRS = {
    '.git', '.github', '.vscode', '.atomcode', '.claude',
    '.monkeycode', 'node_modules', 'pdf_tools', 'chrome-extension',
    '__pycache__', 'json', 'pdf', 'design',
}

# 非内容 / 内部页：验证文件、测试页、统计 / 恢复控制台、示例草稿
# —— 不进 sitemap，避免稀释抓取预算（同时由 robots.txt 的 Disallow 屏蔽）
EXCLUDE_FILES = {
    'examples.html', 'notes.html', 'recovery-console.html', 'stats.html',
    'test-ui.html', 'test-auto-changelog.html',
    'googlec2f7e3dbccb44280.html',   # Google Search Console 站点验证文件
}

# 优先级规则：根目录 > 分类页 > 工具页 > 教程 / 指南
PRIORITY_RULES = {
    '/index.html':            ('daily',  '1.0'),
    '/about.html':            ('weekly', '0.8'),
    '/changelog.html':        ('daily',  '0.9'),
    '/privacy.html':          ('monthly', '0.5'),
    '/terms.html':            ('monthly', '0.5'),
    '/tools.html':            ('daily',  '0.9'),
    '/categories.html':       ('weekly', '0.7'),
    '/contact.html':          ('monthly', '0.6'),
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
    if rel_path in PRIORITY_RULES:
        return PRIORITY_RULES[rel_path]
    if rel_path in CATEGORY_INDEXES:
        return ('weekly', '0.8')
    return ('weekly', '0.6')


def _lastmod(rel_path: str, abs_path: str) -> str:
    """lastmod 优先取 git 最近提交日期，失败回退 mtime。"""
    try:
        r = subprocess.run(
            ['git', '-C', SCRIPT_DIR, 'log', '-1', '--format=%cI', '--', rel_path],
            capture_output=True, text=True, timeout=15,
        )
        d = r.stdout.strip()
        if d:
            return d[:10]   # 'YYYY-MM-DD'
    except Exception:
        pass
    return time.strftime('%Y-%m-%d', time.gmtime(os.path.getmtime(abs_path)))


def main():
    root = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    now = time.strftime('%Y-%m-%dT%H:%M:%S+08:00')
    count = 0
    txt_lines = []

    for dirpath, dirnames, filenames in os.walk(SCRIPT_DIR):
        dirnames[:] = [d for d in dirnames
                       if d not in EXCLUDE_DIRS and not d.startswith('.')]
        for fn in filenames:
            if fn.endswith('.html'):
                abs_path = os.path.join(dirpath, fn)
                rel = os.path.relpath(abs_path, SCRIPT_DIR).replace('\\', '/')
                if rel in EXCLUDE_FILES or fn in EXCLUDE_FILES:
                    continue
                lastmod = _lastmod(rel, abs_path)
                changefreq, priority = _priority('/' + rel)

                u = ET.SubElement(root, 'url')
                ET.SubElement(u, 'loc').text = f'{BASE_URL}/{rel}'
                ET.SubElement(u, 'lastmod').text = lastmod
                ET.SubElement(u, 'changefreq').text = changefreq
                ET.SubElement(u, 'priority').text = priority

                txt_lines.append(f'{BASE_URL}/{rel}')
                count += 1

    # 写入 sitemap.xml（单行紧凑，与既有格式一致）
    out_xml = os.path.join(SCRIPT_DIR, 'sitemap.xml')
    with open(out_xml, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write(ET.tostring(root, encoding='unicode'))
        f.write('\n')
    print(f'✓ sitemap.xml 已生成: {count} 个 URL (lastmod 取自 git 提交日期)')

    # 同步写入 sitemap.txt
    out_txt = os.path.join(SCRIPT_DIR, 'sitemap.txt')
    with open(out_txt, 'w', encoding='utf-8') as f:
        f.write('\n'.join(txt_lines))
        f.write('\n')
    print(f'✓ sitemap.txt 已生成: {count} 个 URL')


if __name__ == '__main__':
    main()
