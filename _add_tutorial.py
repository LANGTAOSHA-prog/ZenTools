#!/usr/bin/env python3
"""生成教程页面 HTML 骨架，遵循 ZenTools 多语言模板。"""

import argparse
import os
import sys
from datetime import date

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TUTORIALS_DIR = os.path.join(SCRIPT_DIR, 'tutorials')

CATEGORY_LABELS = {
    'AI工具':   ('🤖 AI工具',    '🤖 AI Tools',     '🤖 AIツール',     '🤖 Công cụ AI'),
    '图片工具': ('🖼️ 图片工具',  '🖼️ Image Tools',  '🖼️ 画像ツール',   '🖼️ Công cụ hình ảnh'),
    'PDF工具':  ('📄 PDF工具',   '📄 PDF Tools',    '📄 PDFツール',    '📄 Công cụ PDF'),
    '文本工具': ('📝 文本工具',  '📝 Text Tools',   '📝 テキストツール', '📝 Công cụ văn bản'),
    '视频工具': ('🎬 视频工具',  '🎬 Video Tools',  '🎬 動画ツール',   '🎬 Công cụ video'),
    '音频工具': ('🎵 音频工具',  '🎵 Audio Tools',  '🎵 音声ツール',   '🎵 Công cụ âm thanh'),
    '开发工具': ('💻 开发工具',  '💻 Dev Tools',     '💻 開発ツール',   '💻 Công cụ phát triển'),
    'SEO工具':  ('🔍 SEO工具',  '🔍 SEO Tools',    '🔍 SEOツール',    '🔍 Công cụ SEO'),
    '生活工具': ('🌍 生活工具',  '🌍 Life Tools',   '🌍 生活ツール',   '🌍 Công cụ đời sống'),
    '金融工具': ('💰 金融工具',  '💰 Finance Tools', '💰 金融ツール',   '💰 Công cụ tài chính'),
}


def build_tutorial_html(slug, title_zh, category, tool_url, desc_zh, steps_zh,
                        tips_zh, faqs_zh, related,
                        title_en='', title_ja='', title_vi='',
                        desc_en='', desc_ja='', desc_vi=''):
    cat_label = CATEGORY_LABELS[category][0]
    cat_en = CATEGORY_LABELS[category][1]
    cat_ja = CATEGORY_LABELS[category][2]
    cat_vi = CATEGORY_LABELS[category][3]
    today = date.today().isoformat()

    def build_steps(keys_zh, keys_en, keys_ja, keys_vi, steps):
        html_zh = ''
        html_en = ''
        html_ja = ''
        html_vi = ''
        for i, step in enumerate(steps, 1):
            title = step['title']
            body = step['body']
            title_en_s = step.get('title_en', title)
            title_ja_s = step.get('title_ja', title)
            title_vi_s = step.get('title_vi', title)
            body_en = step.get('body_en', body)
            body_ja = step.get('body_ja', body)
            body_vi = step.get('body_vi', body)
            html_zh += f'''<h3 data-i18n="step{i}T">{i}. {title}</h3>
<p data-i18n="step{i}B">{body}</p>
'''
            html_en += f'''<h3 data-i18n="step{i}T">{i}. {title_en_s}</h3>
<p data-i18n="step{i}B">{body_en}</p>
'''
            html_ja += f'''<h3 data-i18n="step{i}T">{i}. {title_ja_s}</h3>
<p data-i18n="step{i}B">{body_ja}</p>
'''
            html_vi += f'''<h3 data-i18n="step{i}T">{i}. {title_vi_s}</h3>
<p data-i18n="step{i}B">{body_vi}</p>
'''
        return html_zh, html_en, html_ja, html_vi

    steps_zh_html = ''
    steps_data_zh = {}
    steps_data_en = {}
    steps_data_ja = {}
    steps_data_vi = {}
    for i, step in enumerate(steps_zh, 1):
        t = step['title']
        b = step['body']
        t_en = step.get('title_en', t)
        b_en = step.get('body_en', b)
        t_ja = step.get('title_ja', t)
        b_ja = step.get('body_ja', b)
        t_vi = step.get('title_vi', t)
        b_vi = step.get('body_vi', b)
        steps_zh_html += f'<h3 data-i18n="step{i}T">{i}. {t}</h3>\n<p data-i18n="step{i}B">{b}</p>\n'
        steps_data_zh[f'step{i}T'] = t
        steps_data_zh[f'step{i}B'] = b
        steps_data_en[f'step{i}T'] = t_en
        steps_data_en[f'step{i}B'] = b_en
        steps_data_ja[f'step{i}T'] = t_ja
        steps_data_ja[f'step{i}B'] = b_ja
        steps_data_vi[f'step{i}T'] = t_vi
        steps_data_vi[f'step{i}B'] = b_vi

    tips_html = ''
    for i, tip in enumerate(tips_zh, 1):
        tips_html += f'<div class="tip"><strong data-i18n="tip{i}Label">{tip["label"]}</strong><br/><span data-i18n="tip{i}Text">{tip["text"]}</span></div>\n'

    faq_html = ''
    for i, faq in enumerate(faqs_zh, 1):
        faq_html += f'<p><strong data-i18n="faq{i}Q">{faq["q"]}</strong><br/><span data-i18n="faq{i}A">{faq["a"]}</span></p>\n'

    related_html = ' · '.join(f'<a href="{r[0]}">{r[1]}</a>' for r in related)

    zh_page = {
        'pageTitle': f'{title_zh} - ZenTools',
        'title': title_zh,
        'desc': desc_zh,
        'catLabel': cat_label,
        'date': f'📅 {today}',
        'readTime': '⏱ 2 分钟阅读',
        'introTitle': '功能介绍',
        'openTitle': '打开工具',
        'openBody': f'访问 <a href="{tool_url}">{title_zh.split("：")[0]}</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。',
        'stepTitle': '操作步骤',
        'tipTitle': '实用技巧',
        'faqTitle': '常见问题',
        'relTitle': '相关工具：',
        'backToIndex': '← 返回教程中心',
        'navHome': '首页', 'navAll': '全部工具', 'navPrivacy': '隐私政策',
        'footerCopy': '© 2026 ZenTools. 免费在线工具箱。',
        **steps_data_zh,
        **{f'tip{i+1}Label': t['label'] for i, t in enumerate(tips_zh)},
        **{f'tip{i+1}Text': t['text'] for i, t in enumerate(tips_zh)},
        **{f'faq{i+1}Q': f['q'] for i, f in enumerate(faqs_zh)},
        **{f'faq{i+1}A': f['a'] for i, f in enumerate(faqs_zh)},
    }

    en_page = dict(zh_page)
    en_page.update({
        'pageTitle': f'{title_en or title_zh} - ZenTools',
        'title': title_en or title_zh,
        'desc': desc_en or desc_zh,
        'catLabel': cat_en,
        'readTime': '⏱ 2 min read',
        'introTitle': 'Introduction',
        'openTitle': 'Open the Tool',
        'openBody': f'Visit <a href="{tool_url}">{title_en or title_zh}</a>. All processing happens locally in your browser — no installation needed.',
        'stepTitle': 'Steps',
        'tipTitle': 'Tips',
        'faqTitle': 'FAQ',
        'relTitle': 'Related Tools:',
        'backToIndex': '← Back to Tutorials',
        'navHome': 'Home', 'navAll': 'All Tools', 'navPrivacy': 'Privacy',
        'footerCopy': '© 2026 ZenTools. Free Online Toolbox.',
        **steps_data_en,
    })
    for i, t in enumerate(tips_zh, 1):
        en_page[f'tip{i}Label'] = t.get('label_en', t['label'])
        en_page[f'tip{i}Text'] = t.get('text_en', t['text'])
    for i, f in enumerate(faqs_zh, 1):
        en_page[f'faq{i}Q'] = f.get('q_en', f['q'])
        en_page[f'faq{i}A'] = f.get('a_en', f['a'])

    ja_page = dict(zh_page)
    ja_page.update({
        'pageTitle': f'{title_ja or title_zh} - ZenTools',
        'title': title_ja or title_zh,
        'desc': desc_ja or desc_zh,
        'catLabel': cat_ja,
        'readTime': '⏱ 2分',
        'introTitle': '機能紹介',
        'openTitle': 'ツールを開く',
        'openBody': f'<a href="{tool_url}">{title_ja or title_zh}</a>にアクセスしてください。すべての操作はブラウザ内で完了します。',
        'stepTitle': '操作手順',
        'tipTitle': 'ヒント',
        'faqTitle': 'よくある質問',
        'relTitle': '関連ツール：',
        'backToIndex': '← チュートリアルに戻る',
        'navHome': 'ホーム', 'navAll': 'すべてのツール', 'navPrivacy': 'プライバシー',
        'footerCopy': '© 2026 ZenTools. 無料オンラインツールボックス。',
        **steps_data_ja,
    })
    for i, t in enumerate(tips_zh, 1):
        ja_page[f'tip{i}Label'] = t.get('label_ja', t['label'])
        ja_page[f'tip{i}Text'] = t.get('text_ja', t['text'])
    for i, f in enumerate(faqs_zh, 1):
        ja_page[f'faq{i}Q'] = f.get('q_ja', f['q'])
        ja_page[f'faq{i}A'] = f.get('a_ja', f['a'])

    vi_page = dict(zh_page)
    vi_page.update({
        'pageTitle': f'{title_vi or title_zh} - ZenTools',
        'title': title_vi or title_zh,
        'desc': desc_vi or desc_zh,
        'catLabel': cat_vi,
        'readTime': '⏱ 2 phút đọc',
        'introTitle': 'Giới thiệu',
        'openTitle': 'Mở Công cụ',
        'openBody': f'Truy cập <a href="{tool_url}">{title_vi or title_zh}</a>. Tất cả xử lý được thực hiện cục bộ trong trình duyệt.',
        'stepTitle': 'Các bước',
        'tipTitle': 'Mẹo',
        'faqTitle': 'Câu hỏi thường gặp',
        'relTitle': 'Công cụ liên quan:',
        'backToIndex': '← Quay lại Hướng dẫn',
        'navHome': 'Trang chủ', 'navAll': 'Tất cả', 'navPrivacy': 'Quyền riêng tư',
        'footerCopy': '© 2026 ZenTools. Hộp công cụ trực tuyến miễn phí.',
        **steps_data_vi,
    })
    for i, t in enumerate(tips_zh, 1):
        vi_page[f'tip{i}Label'] = t.get('label_vi', t['label'])
        vi_page[f'tip{i}Text'] = t.get('text_vi', t['text'])
    for i, f in enumerate(faqs_zh, 1):
        vi_page[f'faq{i}Q'] = f.get('q_vi', f['q'])
        vi_page[f'faq{i}A'] = f.get('a_vi', f['a'])

    import json
    zh_json = json.dumps(zh_page, ensure_ascii=False)
    en_json = json.dumps(en_page, ensure_ascii=False)
    ja_json = json.dumps(ja_page, ensure_ascii=False)
    vi_json = json.dumps(vi_page, ensure_ascii=False)

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">{title_zh} - ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="canonical" href="https://zentools.xyz/tutorials/{slug}.html"/>
<link rel="manifest" href="/manifest.json"/>
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.page-tutorial {{ max-width:920px; margin:0 auto; padding:20px 16px 60px; }}
.page-tutorial .back-link {{ display:inline-flex; align-items:center; gap:6px; font-size:14px; color:var(--muted); margin-bottom:20px; transition:color 0.2s; text-decoration:none; }}
.page-tutorial .back-link:hover {{ color:var(--cyan); }}
.page-tutorial .page-eyebrow {{ font-size:12px; font-weight:700; color:var(--cyan); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; display:block; }}
.page-tutorial h1 {{ font-size:28px; font-weight:800; margin-bottom:8px; }}
.page-tutorial .meta {{ font-size:13px; color:var(--muted); display:flex; gap:16px; margin-bottom:24px; }}
.article-body {{ max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; }}
.article-body h2 {{ font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }}
.article-body h3 {{ font-size:16px; font-weight:600; color:var(--cyan); margin:24px 0 8px; }}
.article-body p, .article-body li {{ font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:10px; }}
.article-body a {{ color:var(--cyan); text-decoration:none; }}
.article-body a:hover {{ text-decoration:underline; }}
.tip {{ background:rgba(0,229,255,0.06); border-left:3px solid var(--cyan); padding:14px 18px; border-radius:0 10px 10px 0; margin:16px 0; font-size:14px; color:var(--text); }}
.rel-tools {{ font-size:13px; color:var(--muted); margin-top:12px; }}
.rel-tools a {{ color:var(--cyan); }}
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "TechArticle",
  "headline": "{title_zh}",
  "description": "{desc_zh}",
  "datePublished": "{today}",
  "author": {{ "@type": "Organization", "name": "ZenTools" }},
  "publisher": {{ "@type": "Organization", "name": "ZenTools" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "https://zentools.xyz/tutorials/{slug}.html" }}
}}
</script>
</head>
<body>
<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="z-wrap">
<nav>
<div class="nav-inner">
<a class="logo" href="/">ZenTools<span>2.0</span></a>
<div class="nav-links">
<a href="/" data-i18n="navHome">首页</a>
<a href="/tools.html" data-i18n="navAll">全部工具</a>
<select id="langSelect" class="lang-select">
<option value="zh">中文</option>
<option value="en">English</option>
<option value="ja">日本語</option>
<option value="vi">Tiếng Việt</option>
</select>
</div>
</div>
</nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/" data-i18n="backToIndex">← 返回教程中心</a>
<span class="page-eyebrow" data-i18n="catLabel">{cat_label}</span>
<h1 data-i18n="title">{title_zh}</h1>
<div class="meta">
<span data-i18n="date">📅 {today}</span>
<span data-i18n="readTime">⏱ 2 分钟阅读</span>
</div>

<div class="article-body">
<h2 data-i18n="introTitle">功能介绍</h2>
<p data-i18n="desc">{desc_zh}</p>

<h2 data-i18n="openTitle">打开工具</h2>
<p data-i18n="openBody">访问工具页面，在浏览器中直接使用。</p>

<h2 data-i18n="stepTitle">操作步骤</h2>
{steps_zh_html}

<h2 data-i18n="tipTitle">实用技巧</h2>
{tips_html}

<h2 data-i18n="faqTitle">常见问题</h2>
{faq_html}

<div class="rel-tools"><strong data-i18n="relTitle">相关工具：</strong>{related_html}</div>
</div>
</div>

<footer>
<div class="footer-inner">
<div class="footer-logo">ZenTools</div>
<div class="footer-links">
<a href="/" data-i18n="navHome">首页</a>
<a href="/tools.html" data-i18n="navAll">全部工具</a>
<a href="/privacy.html" data-i18n="navPrivacy">隐私政策</a>
</div>
<p class="footer-copy" data-i18n="footerCopy">© 2026 ZenTools. 免费在线工具箱。</p>
</div>
</footer>
</div>

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
<script>
if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('/sw.js');
}}
</script>
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description='生成 ZenTools 教程页面')
    parser.add_argument('--slug', required=True, help='URL 友好标识')
    parser.add_argument('--title-zh', required=True, help='中文标题')
    parser.add_argument('--title-en', default='', help='英文标题')
    parser.add_argument('--title-ja', default='', help='日文标题')
    parser.add_argument('--title-vi', default='', help='越南文标题')
    parser.add_argument('--desc-zh', required=True, help='中文描述')
    parser.add_argument('--desc-en', default='', help='英文描述')
    parser.add_argument('--desc-ja', default='', help='日文描述')
    parser.add_argument('--desc-vi', default='', help='越南文描述')
    parser.add_argument('--category', required=True, choices=list(CATEGORY_LABELS.keys()),
                        help='工具分类')
    parser.add_argument('--tool-url', required=True, help='对应工具的 URL')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在的文件')

    args = parser.parse_args()

    os.makedirs(TUTORIALS_DIR, exist_ok=True)
    out_path = os.path.join(TUTORIALS_DIR, f'{args.slug}.html')

    if os.path.exists(out_path) and not args.overwrite:
        print(f'✗ 文件已存在: {out_path}')
        sys.exit(1)

    default_steps = [
        {'title': '打开工具', 'title_en': 'Open the Tool', 'title_ja': 'ツールを開く', 'title_vi': 'Mở công cụ',
         'body': f'访问<a href="{args.tool_url}">{args.tool_url}</a>，在浏览器中打开工具。',
         'body_en': f'Visit <a href="{args.tool_url}">{args.tool_url}</a> to open the tool in your browser.',
         'body_ja': f'<a href="{args.tool_url}">{args.tool_url}</a>にアクセスしてください。',
         'body_vi': f'Truy cập <a href="{args.tool_url}">{args.tool_url}</a>.',
        },
        {'title': '上传/输入内容', 'title_en': 'Upload/Enter Content', 'title_ja': 'アップロード/入力', 'title_vi': 'Tải lên/Nhập nội dung',
         'body': '上传文件或手动输入需要处理的内容。',
         'body_en': 'Upload files or manually enter content to process.',
         'body_ja': 'ファイルをアップロードまたは内容を入力してください。',
         'body_vi': 'Tải tệp lên hoặc nhập nội dung cần xử lý.',
        },
        {'title': '处理结果', 'title_en': 'View Result', 'title_ja': '結果を確認', 'title_vi': 'Xem kết quả',
         'body': '处理完成后查看或下载结果。',
         'body_en': 'View or download the result after processing.',
         'body_ja': '処理完了後に結果を確認またはダウンロードしてください。',
         'body_vi': 'Xem hoặc tải xuống kết quả sau khi xử lý.',
        },
    ]
    default_tips = [
        {'label': '提示 1：', 'label_en': 'Tip 1:', 'label_ja': 'ヒント1:', 'label_vi': 'Mẹo 1:',
         'text': '所有处理均在浏览器本地完成，文件不上传服务器。',
         'text_en': 'All processing is done locally in your browser.',
         'text_ja': 'すべての処理はブラウザ内で完了します。',
         'text_vi': 'Tất cả xử lý được thực hiện cục bộ.'},
        {'label': '提示 2：', 'label_en': 'Tip 2:', 'label_ja': 'ヒント2:', 'label_vi': 'Mẹo 2:',
         'text': '无需注册账号，完全免费使用。',
         'text_en': 'No registration required, completely free.',
         'text_ja': '登録不要、完全無料で使用可能。',
         'text_vi': 'Không cần đăng ký, hoàn toàn miễn phí.'},
    ]
    default_faqs = [
        {'q': f'需要安装软件吗？', 'q_en': 'Do I need to install software?', 'q_ja': 'ソフトウェアをインストールする必要がありますか？', 'q_vi': 'Cần cài đặt phần mềm không?',
         'a': '不需要。直接在浏览器中使用。', 'a_en': 'No. Use it directly in your browser.', 'a_ja': 'いいえ。ブラウザで直接使用できます。', 'a_vi': 'Không. Sử dụng trực tiếp trong trình duyệt.'},
    ]

    html = build_tutorial_html(
        slug=args.slug,
        title_zh=args.title_zh,
        category=args.category,
        tool_url=args.tool_url,
        desc_zh=args.desc_zh,
        steps_zh=default_steps,
        tips_zh=default_tips,
        faqs_zh=default_faqs,
        related=[],
        title_en=args.title_en,
        title_ja=args.title_ja,
        title_vi=args.title_vi,
        desc_en=args.desc_en,
        desc_ja=args.desc_ja,
        desc_vi=args.desc_vi,
    )

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f'✓ 教程页面已生成: {out_path}')
    print(f'\n📝 下一步：编辑 {out_path} 填写具体内容（步骤、技巧、FAQ）')


if __name__ == '__main__':
    main()
