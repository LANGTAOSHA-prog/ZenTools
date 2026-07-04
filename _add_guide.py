#!/usr/bin/env python3
"""生成评测/指南/行业专题页面 HTML 骨架。"""

import argparse
import json
import os
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(SCRIPT_DIR, 'guides')

GUIDE_TYPES = {
    'core':     ('核心指南',     '📘'),
    'case':     ('案例研究',     '⭐'),
    'review':   ('对比评测',     '⚖️'),
    'industry': ('行业专题',     '🏭'),
}


def build_guide_html(slug, title_zh, guide_type, desc_zh, sections_zh, word_count,
                     read_minutes,
                     title_en='', title_ja='', title_vi='',
                     desc_en='', desc_ja='', desc_vi=''):
    today = date.today().isoformat()
    type_label = GUIDE_TYPES[guide_type][0]
    type_icon = GUIDE_TYPES[guide_type][1]
    type_en = {'core': 'Core Guide', 'case': 'Case Study', 'review': 'Review', 'industry': 'Industry'}[guide_type]

    title_en = title_en or title_zh
    title_ja = title_ja or title_zh
    title_vi = title_vi or title_zh
    desc_en = desc_en or desc_zh
    desc_ja = desc_ja or desc_zh
    desc_vi = desc_vi or desc_zh

    sections_html_zh = ''
    toc_html = '<p>目录</p>\n<ol>\n'
    for i, sec in enumerate(sections_zh, 1):
        anchor = f'section-{i}'
        toc_html += f'<li><a href="#{anchor}">{sec["title"]}</a></li>\n'
        body = ''
        for para in sec.get('paragraphs', []):
            body += f'<p>{para}</p>\n'
        if sec.get('list'):
            body += '<ul>\n'
            for li in sec['list']:
                body += f'<li>{li}</li>\n'
            body += '</ul>\n'
        if sec.get('tip'):
            body += f'<div class="tip-box"><strong>💡 提示：</strong>{sec["tip"]}</div>\n'
        sections_html_zh += f'<h2 id="{anchor}">{sec["title"]}</h2>\n{body}\n'
    toc_html += '</ol>\n'

    related_html = f'''<div class="related-section">
<h3>相关推荐</h3>
<div class="related-links">
<a href="/guides/">返回深度指南</a>
<a href="/tools.html">查看全部工具</a>
</div>
</div>'''

    zh_page = {
        'pageTitle': f'{title_zh} - ZenTools',
        'pageHeader': title_zh,
        'pageDesc': desc_zh,
        'wordCount': f'{word_count}+ 字',
        'readTime': f'{read_minutes} 分钟阅读',
        'backToGuides': f'← 返回{type_label}',
        'typeLabel': type_label,
    }
    en_page = {
        'pageTitle': f'{title_en} - ZenTools',
        'pageHeader': title_en,
        'pageDesc': desc_en,
        'wordCount': f'{word_count}+ words',
        'readTime': f'{read_minutes} min read',
        'backToGuides': f'← Back to Guides',
        'typeLabel': type_en,
    }
    ja_page = {
        'pageTitle': f'{title_ja} - ZenTools',
        'pageHeader': title_ja,
        'pageDesc': desc_ja,
        'wordCount': f'{word_count}+ 語',
        'readTime': f'{read_minutes}分で読める',
        'backToGuides': f'← ガイドに戻る',
        'typeLabel': type_label,
    }
    vi_page = {
        'pageTitle': f'{title_vi} - ZenTools',
        'pageHeader': title_vi,
        'pageDesc': desc_vi,
        'wordCount': f'{word_count}+ từ',
        'readTime': f'{read_minutes} phút đọc',
        'backToGuides': f'← Quay lại',
        'typeLabel': type_label,
    }

    zh_json = json.dumps(zh_page, ensure_ascii=False)
    en_json = json.dumps(en_page, ensure_ascii=False)
    ja_json = json.dumps(ja_page, ensure_ascii=False)
    vi_json = json.dumps(vi_page, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n-page="pageTitle">{title_zh} - ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="canonical" href="https://zentools.xyz/guides/{slug}.html"/>
<link rel="manifest" href="/manifest.json"/>
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.guide-hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; text-align: center; color: #fff; margin-bottom: 40px; }}
.guide-hero-title, .guide-hero h1 {{ font-size: 42px; margin-bottom: 16px; font-weight: 700; }}
.guide-hero p {{ font-size: 18px; opacity: 0.9; max-width: 800px; margin: 0 auto; line-height: 1.6; }}
.guide-meta {{ display: flex; gap: 24px; justify-content: center; margin-top: 20px; font-size: 14px; opacity: 0.85; }}
.guide-type {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 999px; font-size: 12px; font-weight: 600; letter-spacing: 0.5px; }}
.guide-back {{ max-width: 1200px; margin: 0 auto 30px; padding: 0 20px; }}
.back-link {{ display: inline-flex; align-items: center; gap: 8px; color: #667eea; text-decoration: none; font-weight: 600; padding: 10px 0; }}
.back-link:hover {{ color: #764ba2; }}
.guide-container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px 60px; }}
.guide-body {{ background: #fff; border-radius: 20px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); color: #333; }}
.guide-body h2 {{ font-size: 28px; margin: 40px 0 20px; color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }}
.guide-body h3 {{ font-size: 22px; margin: 30px 0 15px; color: #444; }}
.guide-body p {{ line-height: 1.8; color: #555; margin-bottom: 16px; }}
.guide-body ul, .guide-body ol {{ margin: 16px 0; padding-left: 24px; }}
.guide-body li {{ margin-bottom: 8px; line-height: 1.6; color: #555; }}
.guide-body a {{ color: #667eea; text-decoration: none; }}
.guide-body a:hover {{ text-decoration: underline; }}
.tip-box {{ background: linear-gradient(135deg, rgba(102,126,234,0.1) 0%, rgba(118,75,162,0.1) 100%); border-left: 4px solid #667eea; padding: 20px 24px; border-radius: 8px; margin: 24px 0; }}
.tip-box strong {{ color: #667eea; font-weight: 700; }}
.related-section {{ background: #f8f9fa; border-radius: 12px; padding: 24px; margin-top: 40px; }}
.related-section h3 {{ margin-top: 0; color: #333; }}
.related-links {{ display: flex; flex-wrap: wrap; gap: 12px; }}
.related-links a {{ color: #667eea; text-decoration: none; padding: 8px 16px; background: #fff; border-radius: 6px; border: 1px solid #e0e0e0; transition: all 0.2s; }}
.related-links a:hover {{ background: #667eea; color: #fff; border-color: #667eea; }}
@media(max-width: 768px) {{
  .guide-hero {{ padding: 40px 20px; }}
  .guide-hero-title, .guide-hero h1 {{ font-size: 28px; }}
  .guide-body {{ padding: 24px; }}
  .guide-meta {{ flex-direction: column; gap: 8px; }}
}}
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{title_zh}",
  "description": "{desc_zh}",
  "datePublished": "{today}",
  "author": {{ "@type": "Organization", "name": "ZenTools" }},
  "publisher": {{ "@type": "Organization", "name": "ZenTools" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://zentools.xyz/guides/{slug}.html" }}
}}
</script>
</head>
<body>

<div class="guide-hero">
<span class="guide-type">{type_icon} {type_label}</span>
<div class="guide-hero-title" data-i18n-page="pageHeader">{title_zh}</div>
<p data-i18n-page="pageDesc">{desc_zh}</p>
<div class="guide-meta">
<span data-i18n-page="wordCount">{word_count}+ 字</span>
<span data-i18n-page="readTime">{read_minutes} 分钟阅读</span>
<span>📅 {today}</span>
</div>
</div>

<div class="guide-back">
<a href="/guides/" class="back-link" data-i18n-page="backToGuides">← 返回深度指南</a>
</div>

<div class="guide-container">
<div class="guide-body">
<div id="toc">{toc_html}</div>
{sections_html_zh}
{related_html}
</div>
</div>

<footer style="max-width:1200px;margin:0 auto;padding:40px 20px;text-align:center;border-top:1px solid #e0e0e0;">
<div style="font-size:14px;color:#666;">&copy; 2026 ZenTools. 免费在线工具箱。</div>
</footer>

<script>
window.ZT_PAGE = {{
  zh: {zh_json},
  en: {en_json},
  ja: {ja_json},
  vi: {vi_json}
}};
</script>
<script src="../assets/js/common-i18n.min.js"></script>
<script src="../assets/js/tool-ui.min.js"></script>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description='生成 ZenTools 评测/指南页面')
    parser.add_argument('--slug', required=True, help='URL 友好标识')
    parser.add_argument('--title-zh', required=True, help='中文标题')
    parser.add_argument('--title-en', default='', help='英文标题')
    parser.add_argument('--title-ja', default='', help='日文标题')
    parser.add_argument('--title-vi', default='', help='越南文标题')
    parser.add_argument('--desc-zh', required=True, help='中文描述')
    parser.add_argument('--desc-en', default='', help='英文描述')
    parser.add_argument('--desc-ja', default='', help='日文描述')
    parser.add_argument('--desc-vi', default='', help='越南文描述')
    parser.add_argument('--type', required=True, choices=GUIDE_TYPES.keys(),
                        help='指南类型: core(核心指南)/case(案例)/review(评测)/industry(行业)')
    parser.add_argument('--word-count', type=int, default=2000, help='字数 (默认 2000)')
    parser.add_argument('--read-minutes', type=int, default=15, help='阅读时间 (分钟)')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')

    args = parser.parse_args()

    os.makedirs(GUIDES_DIR, exist_ok=True)
    out_path = os.path.join(GUIDES_DIR, f'{args.slug}.html')

    if os.path.exists(out_path) and not args.overwrite:
        print(f'✗ 文件已存在: {out_path}')
        sys.exit(1)

    default_sections = [
        {
            'title': '概述',
            'paragraphs': [
                f'{args.title_zh}的详细介绍。在这里添加该{GUIDE_TYPES[args.type][0]}的核心内容。',
                '说明本文的目标读者和适用场景。',
            ],
        },
        {
            'title': '核心内容',
            'paragraphs': ['在此处添加主要分析或步骤说明。'],
            'list': ['要点 1', '要点 2', '要点 3'],
        },
        {
            'title': '实际案例',
            'paragraphs': ['通过具体案例展示实际应用场景。'],
            'tip': '这里可以添加一个实用的技巧提醒。',
        },
        {
            'title': '常见问题',
            'paragraphs': ['总结读者常问的问题及解答。'],
        },
        {
            'title': '总结与下一步',
            'paragraphs': ['总结本文要点，建议下一步操作。'],
        },
    ]

    html = build_guide_html(
        slug=args.slug,
        title_zh=args.title_zh,
        guide_type=args.type,
        desc_zh=args.desc_zh,
        sections_zh=default_sections,
        word_count=args.word_count,
        read_minutes=args.read_minutes,
        title_en=args.title_en,
        title_ja=args.title_ja,
        title_vi=args.title_vi,
        desc_en=args.desc_en,
        desc_ja=args.desc_ja,
        desc_vi=args.desc_vi,
    )

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)

    print(f'✓ {GUIDE_TYPES[args.type][0]}页面已生成: {out_path}')
    print(f'\n📝 下一步：编辑 {out_path} 填写完整内容')
    print(f'  当前是骨架模板，需要补充至 {args.word_count}+ 字的完整内容')
    print(f'  建议替换 guide-body 内的默认章节为真实内容')


if __name__ == '__main__':
    main()
