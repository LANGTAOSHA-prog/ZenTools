#!/usr/bin/env python3
"""生成评测/指南/行业专题页面 HTML 骨架，含 4 语 i18n。"""

import argparse
import json
import os
import sys
from datetime import date
from _changelog_utils import build_guide_entry, append_changelog, load_site_info, save_site_info

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GUIDES_DIR = os.path.join(SCRIPT_DIR, 'guides')

GUIDE_TYPES = {
    'core':     ('核心指南',     '📘'),
    'case':     ('案例研究',     '⭐'),
    'review':   ('对比评测',     '⚖️'),
    'industry': ('行业专题',     '🏭'),
}

FIXED_I18N = {
    'zh': {
        'guideBack': '← 返回深度指南',
        'relatedTitle': '相关推荐',
        'backToGuides': '返回深度指南',
        'viewAllTools': '查看全部工具',
        'footerCopy': '© 2026 ZenTools. 免费在线工具箱。',
        'navHome': '首页',
        'navAll': '全部工具',
        'navPrivacy': '隐私政策',
        'breadcrumbGuides': '深度指南',
    },
    'en': {
        'guideBack': '← Back to Guides',
        'relatedTitle': 'Related',
        'backToGuides': 'Back to Guides',
        'viewAllTools': 'View All Tools',
        'footerCopy': '© 2026 ZenTools. Free Online Toolbox.',
        'navHome': 'Home',
        'navAll': 'All Tools',
        'navPrivacy': 'Privacy',
        'breadcrumbGuides': 'Guides',
    },
    'ja': {
        'guideBack': '← ガイドに戻る',
        'relatedTitle': '関連',
        'backToGuides': 'ガイドに戻る',
        'viewAllTools': 'すべてのツール',
        'footerCopy': '© 2026 ZenTools. 無料オンラインツールボックス。',
        'navHome': 'ホーム',
        'navAll': 'すべてのツール',
        'navPrivacy': 'プライバシー',
        'breadcrumbGuides': 'ガイド',
    },
    'vi': {
        'guideBack': '← Quay lại Guides',
        'relatedTitle': 'Liên quan',
        'backToGuides': 'Quay lại Guides',
        'viewAllTools': 'Xem tất cả công cụ',
        'footerCopy': '© 2026 ZenTools. Hộp công cụ miễn phí.',
        'navHome': 'Trang chủ',
        'navAll': 'Tất cả',
        'navPrivacy': 'Quyền riêng tư',
        'breadcrumbGuides': 'Guides',
    },
}


def build_section_html(sections, lang):
    html = ''
    for i, sec in enumerate(sections, 1):
        lang_key = f'__{lang}' if lang != 'zh' else ''
        title = sec.get(f'title{lang_key}', sec['title'])
        anchor = f'section-{i}'
        html += f'<h2 id="{anchor}" data-i18n="sec{i}Title">{title}</h2>\n'
        for j, para in enumerate(sec.get(f'paragraphs{lang_key}', sec.get('paragraphs', [])), 1):
            html += f'<p data-i18n="sec{i}p{j}">{para}</p>\n'
        if sec.get(f'list{lang_key}', sec.get('list')):
            html += '<ul>\n'
            for k, li in enumerate(sec.get(f'list{lang_key}', sec.get('list', [])), 1):
                html += f'<li data-i18n="sec{i}li{k}">{li}</li>\n'
            html += '</ul>\n'
        if sec.get(f'tip{lang_key}', sec.get('tip')):
            tip_label = {'zh': '提示', 'en': 'Tip', 'ja': 'ヒント', 'vi': 'Mẹo'}.get(lang, '提示')
            html += f'<div class="tip-box"><strong>{tip_label}：</strong><span data-i18n="sec{i}Tip">{sec.get(f"tip{lang_key}", sec["tip"])}</span></div>\n'
    return html


def build_toc_html(sections, lang):
    lang_key = f'__{lang}' if lang != 'zh' else ''
    html = {'zh': '<p>目录</p>', 'en': '<p>Table of Contents</p>',
            'ja': '<p>目次</p>', 'vi': '<p>Mục lục</p>'}.get(lang, '<p>目录</p>')
    html += '\n<ol>\n'
    for i, sec in enumerate(sections, 1):
        title = sec.get(f'title{lang_key}', sec['title'])
        html += f'<li><a href="#section-{i}" data-i18n="sec{i}Title">{title}</a></li>\n'
    html += '</ol>\n'
    return html


def build_i18n_dict(sections, lang, extra):
    lang_key = f'__{lang}' if lang != 'zh' else ''
    d = dict(extra)
    for i, sec in enumerate(sections, 1):
        title = sec.get(f'title{lang_key}', sec['title'])
        d[f'sec{i}Title'] = title
        paragraphs = sec.get(f'paragraphs{lang_key}', sec.get('paragraphs', []))
        for j, para in enumerate(paragraphs, 1):
            d[f'sec{i}p{j}'] = para
        lst = sec.get(f'list{lang_key}', sec.get('list', []))
        for k, li in enumerate(lst, 1):
            d[f'sec{i}li{k}'] = li
        tip = sec.get(f'tip{lang_key}', sec.get('tip'))
        if tip:
            d[f'sec{i}Tip'] = tip
    return d


def build_guide_html(slug, title_zh, guide_type, desc_zh, sections, word_count,
                     read_minutes, title_en, title_ja, title_vi,
                     desc_en, desc_ja, desc_vi):
    today = date.today().isoformat()
    type_label = GUIDE_TYPES[guide_type][0]
    type_icon = GUIDE_TYPES[guide_type][1]
    type_label_en = {'core': 'Core Guide', 'case': 'Case Study', 'review': 'Review', 'industry': 'Industry'}[guide_type]

    title_en = title_en or title_zh
    title_ja = title_ja or title_zh
    title_vi = title_vi or title_zh
    desc_en = desc_en or desc_zh
    desc_ja = desc_ja or desc_zh
    desc_vi = desc_vi or desc_zh

    page_extra = {
        'zh': {
            'pageTitle': f'{title_zh} - ZenTools',
            'pageHeader': title_zh,
            'pageDesc': desc_zh,
            'wordCount': f'{word_count}+ 字',
            'readTime': f'{read_minutes} 分钟阅读',
            'typeLabel': f'{type_icon} {type_label}',
            'today': f'📅 {today}',
            'tocTitle': '目录',
        },
        'en': {
            'pageTitle': f'{title_en} - ZenTools',
            'pageHeader': title_en,
            'pageDesc': desc_en,
            'wordCount': f'{word_count}+ words',
            'readTime': f'{read_minutes} min read',
            'typeLabel': f'{type_icon} {type_label_en}',
            'today': f'📅 {today}',
            'tocTitle': 'Table of Contents',
        },
        'ja': {
            'pageTitle': f'{title_ja} - ZenTools',
            'pageHeader': title_ja,
            'pageDesc': desc_ja,
            'wordCount': f'{word_count}+ 語',
            'readTime': f'{read_minutes}分で読める',
            'typeLabel': f'{type_icon} {type_label}',
            'today': f'📅 {today}',
            'tocTitle': '目次',
        },
        'vi': {
            'pageTitle': f'{title_vi} - ZenTools',
            'pageHeader': title_vi,
            'pageDesc': desc_vi,
            'wordCount': f'{word_count}+ từ',
            'readTime': f'{read_minutes} phút đọc',
            'typeLabel': f'{type_icon} {type_label}',
            'today': f'📅 {today}',
            'tocTitle': 'Mục lục',
        },
    }

    zh = build_i18n_dict(sections, 'zh', {**FIXED_I18N['zh'], **page_extra['zh']})
    en = build_i18n_dict(sections, 'en', {**FIXED_I18N['en'], **page_extra['en']})
    ja = build_i18n_dict(sections, 'ja', {**FIXED_I18N['ja'], **page_extra['ja']})
    vi = build_i18n_dict(sections, 'vi', {**FIXED_I18N['vi'], **page_extra['vi']})

    zh_json = json.dumps(zh, ensure_ascii=False)
    en_json = json.dumps(en, ensure_ascii=False)
    ja_json = json.dumps(ja, ensure_ascii=False)
    vi_json = json.dumps(vi, ensure_ascii=False)

    sections_zh_html = build_section_html(sections, 'zh')

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">{title_zh} - ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="canonical" href="https://zentools.xyz/guides/{slug}.html"/>
<link rel="manifest" href="/manifest.json"/>
<meta name="theme-color" content="#00e5ff"/>
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.guide-hero {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 60px 20px; text-align: center; color: #fff; margin-bottom: 40px; }}
.guide-hero-title {{ font-size: 42px; margin-bottom: 16px; font-weight: 700; }}
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
.guide-body ul, .guide-body ol {{ margin: 16px 0; padding-left: 24px; color: #555; }}
.guide-body li {{ margin-bottom: 8px; line-height: 1.6; }}
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
  .guide-hero-title {{ font-size: 28px; }}
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
<span class="guide-type" data-i18n="typeLabel">{type_icon} {type_label}</span>
<div class="guide-hero-title" data-i18n="pageHeader">{title_zh}</div>
<p data-i18n="pageDesc">{desc_zh}</p>
<div class="guide-meta">
<span data-i18n="wordCount">{word_count}+ 字</span>
<span data-i18n="readTime">{read_minutes} 分钟阅读</span>
<span data-i18n="today">📅 {today}</span>
</div>
</div>

<div class="guide-back">
<a href="/guides/" class="back-link" data-i18n="guideBack">← 返回深度指南</a>
</div>

<div class="guide-container">
<div class="guide-body">
<div id="toc">
<p data-i18n="tocTitle">目录</p>
<ol>
{build_toc_html(sections, 'zh')}
</ol>
</div>
{sections_zh_html}
<div class="related-section">
<h3 data-i18n="relatedTitle">相关推荐</h3>
<div class="related-links">
<a href="/guides/" data-i18n="backToGuides">返回深度指南</a>
<a href="/tools.html" data-i18n="viewAllTools">查看全部工具</a>
</div>
</div>
</div>
</div>

<footer style="max-width:1200px;margin:0 auto;padding:40px 20px;text-align:center;border-top:1px solid #e0e0e0;">
<div style="font-size:14px;color:#666;" data-i18n="footerCopy">&copy; 2026 ZenTools. 免费在线工具箱。</div>
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


def build_default_sections(args):
    type_label = GUIDE_TYPES[args.type][0]
    return [
        {
            'title': '概述',
            'title__en': 'Overview',
            'title__ja': '概要',
            'title__vi': 'Tổng quan',
            'paragraphs': [
                f'{args.title_zh}的详细介绍。在这里添加该{type_label}的核心内容。',
                '说明本文的目标读者和适用场景。',
            ],
            'paragraphs__en': [
                f'Detailed introduction to {args.title_en or args.title_zh}. Add core content of this {type_label} here.',
                'Describe the target audience and applicable scenarios.',
            ],
            'paragraphs__ja': [
                f'{args.title_ja or args.title_zh}の詳細な紹介。{type_label}のコアコンテンツを追加してください。',
                '対象読者と適用シナリオを説明します。',
            ],
            'paragraphs__vi': [
                f'Giới thiệu chi tiết về {args.title_vi or args.title_zh}. Thêm nội dung cốt lõi của {type_label} vào đây.',
                'Mô tả đối tượng độc giả và các kịch bản áp dụng.',
            ],
        },
        {
            'title': '核心内容',
            'title__en': 'Core Content',
            'title__ja': 'コアコンテンツ',
            'title__vi': 'Nội dung chính',
            'paragraphs': ['在此处添加主要分析或步骤说明。'],
            'paragraphs__en': ['Add main analysis or step-by-step instructions here.'],
            'paragraphs__ja': ['主な分析または手順の説明を追加してください。'],
            'paragraphs__vi': ['Thêm phân tích chính hoặc hướng dẫn từng bước tại đây.'],
            'list': ['要点 1', '要点 2', '要点 3'],
            'list__en': ['Key Point 1', 'Key Point 2', 'Key Point 3'],
            'list__ja': ['ポイント 1', 'ポイント 2', 'ポイント 3'],
            'list__vi': ['Điểm chính 1', 'Điểm chính 2', 'Điểm chính 3'],
        },
        {
            'title': '实际案例',
            'title__en': 'Practical Examples',
            'title__ja': '実践事例',
            'title__vi': 'Ví dụ thực tế',
            'paragraphs': ['通过具体案例展示实际应用场景。'],
            'paragraphs__en': ['Demonstrate practical application scenarios through specific cases.'],
            'paragraphs__ja': ['具体的な事例を通じて実際の応用シーンを示します。'],
            'paragraphs__vi': ['Trình bày các kịch bản ứng dụng thực tế qua ví dụ cụ thể.'],
            'tip': '这里可以添加一个实用的技巧提醒。',
            'tip__en': 'You can add a practical tip reminder here.',
            'tip__ja': 'ここに実用的なヒントを追加できます。',
            'tip__vi': 'Bạn có thể thêm một mẹo thực tế ở đây.',
        },
        {
            'title': '常见问题',
            'title__en': 'FAQ',
            'title__ja': 'よくある質問',
            'title__vi': 'Câu hỏi thường gặp',
            'paragraphs': [
                'Q1: 这是常见问题 1',
                'A1: 这是答案 1',
                'Q2: 这是常见问题 2',
                'A2: 这是答案 2',
            ],
            'paragraphs__en': [
                'Q1: This is FAQ question 1',
                'A1: This is answer 1',
                'Q2: This is FAQ question 2',
                'A2: This is answer 2',
            ],
            'paragraphs__ja': [
                'Q1: よくある質問 1',
                'A1: 回答 1',
                'Q2: よくある質問 2',
                'A2: 回答 2',
            ],
            'paragraphs__vi': [
                'Q1: Câu hỏi thường gặp 1',
                'A1: Câu trả lời 1',
                'Q2: Câu hỏi thường gặp 2',
                'A2: Câu trả lời 2',
            ],
        },
        {
            'title': '总结与下一步',
            'title__en': 'Summary & Next Steps',
            'title__ja': 'まとめと次のステップ',
            'title__vi': 'Tóm tắt & Bước tiếp theo',
            'paragraphs': ['总结本文要点，给出后续行动建议。'],
            'paragraphs__en': ['Summarize key points and suggest next actions.'],
            'paragraphs__ja': ['要点をまとめ、次のアクションを提案します。'],
            'paragraphs__vi': ['Tóm tắt các điểm chính và đề xuất hành động tiếp theo.'],
        },
    ]


def main():
    parser = argparse.ArgumentParser(description='生成 ZenTools 评测/指南页面 (含 4 语 i18n)')
    parser.add_argument('--slug', required=True, help='URL 友好标识')
    parser.add_argument('--title-zh', required=True, help='中文标题')
    parser.add_argument('--title-en', default='', help='英文标题')
    parser.add_argument('--title-ja', default='', help='日文标题')
    parser.add_argument('--title-vi', default='', help='越南文标题')
    parser.add_argument('--desc-zh', required=True, help='中文描述')
    parser.add_argument('--desc-en', default='', help='英文描述')
    parser.add_argument('--desc-ja', default='', help='日文描述')
    parser.add_argument('--desc-vi', default='', help='越南文描述')
    parser.add_argument('--type', required=True, choices=list(GUIDE_TYPES.keys()),
                        help='指南类型: core/case/review/industry')
    parser.add_argument('--word-count', type=int, default=2000, help='字数 (默认 2000)')
    parser.add_argument('--read-minutes', type=int, default=15, help='阅读时间 (分钟)')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在文件')

    args = parser.parse_args()

    os.makedirs(GUIDES_DIR, exist_ok=True)
    out_path = os.path.join(GUIDES_DIR, f'{args.slug}.html')

    if os.path.exists(out_path) and not args.overwrite:
        print(f'✗ 文件已存在: {out_path}')
        sys.exit(1)

    sections = build_default_sections(args)

    html = build_guide_html(
        slug=args.slug,
        title_zh=args.title_zh,
        guide_type=args.type,
        desc_zh=args.desc_zh,
        sections=sections,
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

    print(f'✓ {GUIDE_TYPES[args.type][0]}页面已生成 (含 4 语 i18n): {out_path}')
    try:
        data = load_site_info()
        changelog_entries = [
            build_guide_entry(args.title_zh,
                              args.title_en or args.title_zh,
                              args.title_ja or args.title_zh,
                              args.title_vi or args.title_zh)
        ]
        data = append_changelog(data, changelog_entries)
        save_site_info(data)
        print(f'✓ site-info.json changelog 已更新')
    except Exception as e:
        print(f'⚠ changelog 更新失败 (非致命): {e}')
    print(f'\n📝 下一步：编辑 {out_path} 填充真实内容')
    print(f'  每个章节在 ZT_PAGE 中都有 sec{{N}}Title / sec{{N}}p{{M}} / sec{{N}}li{{K}} / sec{{N}}Tip')
    print(f'  的 4 语翻译键，替换默认占位文本即可')


if __name__ == '__main__':
    main()