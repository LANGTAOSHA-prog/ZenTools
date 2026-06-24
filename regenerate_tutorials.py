#!/usr/bin/env python3
"""Regenerate all tutorial pages with full i18n (data-i18n on all body elements + 4-language ZT_PAGE)."""
import os, re, subprocess, json

# ── Load card data from current index.html ──
with open('/workspace/tutorials/index.html', 'r') as f:
    index = f.read()

cards = []
for m in re.finditer(
    r'<!-- Article \d+: .+? -->\s*\n<a class="article-card" href="([^"]+)">\s*\n<div class="cat"[^>]*data-i18n="(cat\w+)"[^>]*>([^<]+)</div>\s*\n<h3[^>]*data-i18n="(a\d+)Title"[^>]*>([^<]+)</h3>\s*\n<div class="meta"><span[^>]*data-i18n="(a\d+)Date"[^>]*>([^<]+)</span><span[^>]*data-i18n="(a\d+)Read"[^>]*>([^<]+)</span></div>\s*\n<div class="summary"[^>]*data-i18n="(a\d+)Sum"[^>]*>([^<]*)</div>',
    index
):
    slug = m.group(1).replace('/tutorials/', '').replace('.html', '')
    cards.append(dict(
        slug=slug, cat_key=m.group(2), cat_text=m.group(3),
        a_key=m.group(4), a_title=m.group(5),
        date_key=m.group(6), date_text=m.group(7),
        read_key=m.group(8), read_text=m.group(9),
        sum_key=m.group(10), summary=m.group(11),
    ))

seen = set()
unique_cards = []
for c in cards:
    if c['slug'] not in seen:
        seen.add(c['slug'])
        unique_cards.append(c)

# ── Load git ZT_PAGE for existing translations ──
result = subprocess.run(['git', 'show', '56e7a38:tutorials/index.html'], capture_output=True, text=True)
orig = result.stdout
start = orig.find('window.ZT_PAGE={')
end = orig.find('\n<script', start)
zt_raw = orig[start:end]

def parse_git_lang(text, lang):
    m = re.search(rf'{lang}:\{{([^}}]+)\}}', text)
    if not m:
        return {}
    return {k: v for k, v in re.findall(r"(\w+):'((?:[^'\\]|\\.)*)'", m.group(1))}

git_langs = {lang: parse_git_lang(zt_raw, lang) for lang in ['zh', 'en', 'ja', 'vi']}

# ── Shared structural translations (4 languages) ──
SHARED = {
    'introTitle': ['功能介绍', 'Introduction', '機能紹介', 'Giới thiệu'],
    'openTitle': ['打开工具', 'Open the Tool', 'ツールを開く', 'Mở công cụ'],
    'stepTitle': ['操作步骤', 'How to Use', '使い方', 'Các bước thực hiện'],
    'tipTitle': ['实用技巧', 'Tips', 'ヒント', 'Mẹo'],
    'faqTitle': ['常见问题', 'FAQ', 'よくある質問', 'FAQ'],
    'relTitle': ['相关工具：', 'Related Tools: ', '関連ツール：', 'Công cụ liên quan: '],
    'backToIndex': ['返回教程中心', 'Back to Tutorials', 'チュートリアルに戻る', 'Quay lại hướng dẫn'],
    'tipLabel': ['提示', 'Tip', 'ヒント', 'Mẹo'],
}

def tr(key, lang_idx):
    """Get translation for shared key (0=zh,1=en,2=ja,3=vi)."""
    return SHARED[key][lang_idx]

# ── SVG availability ──
svgs = set(os.listdir('/workspace/guides/img/'))

def svg_for(slug, step):
    name = f'{slug}-step{step}.svg'
    return f'/guides/img/{name}' if name in svgs else None

# ── Content templates per category ──
# Each template step is (zh_title, zh_body, en_title, en_body, ja_title, ja_body, vi_title, vi_body)
def T(zh, en, ja, vi):
    return [zh, en, ja, vi]

def S(zh_s, en_s, ja_s, vi_s, zh_b, en_b, ja_b, vi_b):
    return [zh_s, en_s, ja_s, vi_s, zh_b, en_b, ja_b, vi_b]

catPdf_steps = [
    S('打开工具', 'Open the Tool', 'ツールを開く', 'Mở công cụ',
      '访问{tool_link}，所有处理在浏览器本地完成，无需上传文件到服务器。',
      'Visit {tool_link}. All processing happens locally in your browser, no files are uploaded.',
      '{tool_link}にアクセス。すべての処理はブラウザ内で完結します。',
      'Truy cập {tool_link}. Mọi xử lý đều diễn ra trong trình duyệt.'),
    S('选择文件', 'Select Files', 'ファイルを選択', 'Chọn tệp',
      '点击上传区域选择需要处理的 PDF 文件，或直接拖拽文件到上传区域。',
      'Click the upload area to select PDF files, or drag and drop files directly.',
      'アップロードエリアをクリックしてPDFファイルを選択するか、ドラッグ＆ドロップしてください。',
      'Nhấp vào khu vực tải lên để chọn tệp PDF, hoặc kéo thả trực tiếp.'),
    S('设置参数', 'Adjust Settings', 'パラメータを設定', 'Cài đặt thông số',
      '根据需要调整处理参数，工具会实时显示预览效果。',
      'Adjust settings as needed. The tool shows a live preview of the result.',
      '必要に応じてパラメータを調整。リアルタイムでプレビュー表示。',
      'Điều chỉnh thông số theo nhu cầu. Công cụ hiển thị xem trước theo thời gian thực.'),
    S('下载结果', 'Download Result', '結果をダウンロード', 'Tải xuống',
      '处理完成后点击「下载」按钮保存文件。',
      'Click the "Download" button to save your file when done.',
      '処理完了後、「ダウンロード」ボタンをクリックして保存。',
      'Nhấp nút "Tải xuống" để lưu tệp sau khi hoàn tất.'),
]
catPdf_tips = [
    T('处理大文件时请耐心等待，速度取决于电脑性能。', 'Processing large files may take time depending on your computer performance.',
      '大きなファイルの処理には時間がかかる場合があります。', 'Xử lý tệp lớn có thể mất thời gian.'),
    T('所有操作在浏览器本地完成，文件不会上传到服务器。', 'All processing is local in your browser. Files never leave your computer.',
      'すべての処理はブラウザ内で実行され、ファイルはサーバーに送信されません。', 'Mọi xử lý đều trong trình duyệt, tệp không rời khỏi máy bạn.'),
]
catPdf_faqs = [
    (T('支持多大的文件？', 'What file size is supported?', '対応ファイルサイズは？', 'Kích thước tệp hỗ trợ?'),
     T('取决于浏览器内存，通常 100MB 以内。', 'Depends on browser memory, typically up to 100MB.', 'ブラウザのメモリに依存しますが、通常100MBまで。', 'Phụ thuộc vào bộ nhớ trình duyệt, thường dưới 100MB.')),
    (T('需要注册吗？', 'Do I need to sign up?', '登録は必要ですか？', 'Cần đăng ký không?'),
     T('不需要。完全免费，无需注册。', 'No. Completely free, no sign-up needed.', '不要です。完全無料で登録不要。', 'Không. Hoàn toàn miễn phí, không cần đăng ký.')),
    (T('文件会上传吗？', 'Are files uploaded?', 'ファイルはアップロードされますか？', 'Tệp có được tải lên không?'),
     T('不会。所有处理在浏览器本地完成。', 'No. All processing is done locally in your browser.', 'いいえ。すべてブラウザ内で処理されます。', 'Không. Mọi xử lý đều trong trình duyệt.')),
]

catImg_steps = [
    S('打开工具', 'Open the Tool', 'ツールを開く', 'Mở công cụ',
      '访问{tool_link}，所有处理在浏览器本地完成。',
      'Visit {tool_link}. All processing happens locally in your browser.',
      '{tool_link}にアクセス。すべての処理はブラウザ内で完結します。',
      'Truy cập {tool_link}. Mọi xử lý đều trong trình duyệt.'),
    S('上传图片', 'Upload Image', '画像をアップロード', 'Tải ảnh lên',
      '点击上传区域选择图片，或拖拽文件到上传区域。',
      'Click the upload area to select an image, or drag and drop.',
      'アップロードエリアをクリックするか、ドラッグ＆ドロップ。',
      'Nhấp vào khu vực tải lên hoặc kéo thả ảnh.'),
    S('调整参数', 'Adjust Settings', 'パラメータを調整', 'Điều chỉnh thông số',
      '根据需要调整参数，所有效果实时预览。',
      'Adjust settings as needed. All effects preview in real time.',
      '必要に応じてパラメータを調整。リアルタイムプレビュー。',
      'Điều chỉnh thông số, xem trước theo thời gian thực.'),
    S('下载保存', 'Download & Save', 'ダウンロードして保存', 'Tải xuống và lưu',
      '确认效果满意后点击「下载」按钮保存。',
      'Click "Download" to save your result.',
      '「ダウンロード」ボタンをクリックして保存。',
      'Nhấp "Tải xuống" để lưu kết quả.'),
]
catImg_tips = [
    T('支持 JPG、PNG、WebP、BMP 等常见格式。', 'Supports JPG, PNG, WebP, BMP and more.',
      'JPG、PNG、WebP、BMPなどに対応。', 'Hỗ trợ JPG, PNG, WebP, BMP...'),
    T('所有处理均在浏览器本地完成。', 'All processing is local in your browser.',
      'すべてブラウザ内で処理。', 'Mọi xử lý đều trong trình duyệt.'),
]
catImg_faqs = [
    (T('支持哪些图片格式？', 'What image formats are supported?', '対応画像形式は？', 'Định dạng ảnh hỗ trợ?'),
     T('JPG、PNG、WebP、BMP、GIF 等。', 'JPG, PNG, WebP, BMP, GIF and more.', 'JPG、PNG、WebP、BMP、GIFなど。', 'JPG, PNG, WebP, BMP, GIF...')),
    (T('需要安装软件吗？', 'Do I need to install software?', 'ソフトウェアのインストールは必要？', 'Cần cài đặt phần mềm không?'),
     T('不需要。直接在浏览器中使用。', 'No. Use it directly in your browser.', '不要。ブラウザで直接使用可能。', 'Không. Sử dụng trực tiếp trong trình duyệt.')),
]

# Category → template mapping
CONTENT_TPL = {}
for cat_key in ['catPdf', 'catImg', 'catVideo', 'catAudio', 'catAI', 'catDev', 'catFinance', 'catSEO']:
    CONTENT_TPL[cat_key] = dict(
        steps=catPdf_steps if cat_key in ['catPdf', 'catVideo', 'catAudio', 'catFinance', 'catSEO'] else catImg_steps,
        tips=catPdf_tips if cat_key in ['catPdf', 'catVideo', 'catAudio', 'catFinance'] else catImg_tips,
        faqs=catPdf_faqs if cat_key in ['catPdf', 'catVideo', 'catAudio', 'catFinance'] else catImg_faqs,
    )

CAT_MAP = {
    'catPdf': 'catPdf', 'catImg': 'catImg', 'catVideo': 'catVideo',
    'catAudio': 'catAudio', 'catAI': 'catAI', 'catDev': 'catDev',
    'catFinance': 'catFinance', 'catSEO': 'catSEO', 'catQR': 'catImg',
}

LANG_NAMES = ['zh', 'en', 'ja', 'vi']

def esc(val):
    """Escape a value for JS string."""
    return val.replace("'", "\\'").replace('\n', '\\n')

def gen_body_tpl(c):
    """Generate body HTML + translations for a tutorial page."""
    tpl_key = CAT_MAP.get(c['cat_key'], 'catDev')
    tpl = CONTENT_TPL.get(tpl_key, CONTENT_TPL['catDev'])
    a = c['a_key']  # e.g., 'a1'
    slug = c['slug']
    tool_url = f'/{slug.replace("-","/")}.html'
    tool_name = c['a_title'].split('教程：')[0] if '教程：' in c['a_title'] else c['a_title']
    tool_link = f'<a href="{tool_url}" target="_blank">{tool_name}</a>'
    
    # ── Build body HTML with data-i18n ──
    steps = tpl['steps']
    tips = tpl['tips']
    faqs = tpl['faqs']
    
    related = [t for t in unique_cards if t['slug'] != slug and t['cat_key'] == c['cat_key']][:4]
    
    lines = []
    lang_zt = {lang: {} for lang in LANG_NAMES}
    
    # Helper: add translation for a key
    def add_tr(key, zh_text, en_text=None, ja_text=None, vi_text=None):
        lang_zt['zh'][key] = zh_text
        lang_zt['en'][key] = en_text or zh_text
        lang_zt['ja'][key] = ja_text or zh_text
        lang_zt['vi'][key] = vi_text or zh_text
    
    # intro
    intro_key = f'{a}Intro'
    add_tr(intro_key, c['summary'])
    add_tr(f'{a}OpenBody',
           f'访问 {tool_link}，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件，文件不会上传到服务器。',
           f'Visit {tool_link}. All processing happens locally in your browser — no installation needed, files never leave your device.',
           f'{tool_link} にアクセス。すべての処理はブラウザ内で完結し、ファイルがサーバーに送信されることはありません。',
           f'Truy cập {tool_link}. Mọi xử lý đều trong trình duyệt — không cần cài đặt, tệp không rời khỏi máy bạn.')

    lines.append(f'<p data-i18n="{intro_key}">{c["summary"]}</p>')
    lines.append(f'<h2 data-i18n="introTitle">{tr("introTitle", 0)}</h2>')
    # Actually h2 first, then p
    lines = []
    lines.append(f'<h2 data-i18n="introTitle">{tr("introTitle", 0)}</h2>')
    lines.append(f'<p data-i18n="{intro_key}">{c["summary"]}</p>')
    lines.append(f'')
    lines.append(f'<h2 data-i18n="openTitle">{tr("openTitle", 0)}</h2>')
    lines.append(f'<p data-i18n="{a}OpenBody">访问 {tool_link}，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件，文件不会上传到服务器。</p>')
    lines.append(f'')
    lines.append(f'<h2 data-i18n="stepTitle">{tr("stepTitle", 0)}</h2>')
    
    for idx, step in enumerate(steps, 1):
        s_titles = step[:4]  # [zh_title, en_title, ja_title, vi_title]
        s_bodies = step[4:]  # [zh_body, en_body, ja_body, vi_body]
        
        sk = f'{a}Step{idx}T'
        bk = f'{a}Step{idx}B'
        
        add_tr(sk, s_titles[0], s_titles[1], s_titles[2], s_titles[3])
        
        # Body: insert tool_link into template
        zh_body = s_bodies[0].replace('{tool_link}', tool_link)
        en_body = s_bodies[1].replace('{tool_link}', tool_name)
        ja_body = s_bodies[2].replace('{tool_link}', tool_name)
        vi_body = s_bodies[3].replace('{tool_link}', tool_name)
        add_tr(bk, zh_body, en_body, ja_body, vi_body)
        
        idx_text = f'{idx}. '
        lines.append(f'<h3 data-i18n="{sk}">{idx_text}{s_titles[0]}</h3>')
        lines.append(f'<p data-i18n="{bk}">{zh_body}</p>')
        
        svg = svg_for(slug, idx)
        if svg:
            lines.append(f'<div class="screenshot-wrap"><img src="{svg}" alt="{c["a_title"]} - {s_titles[0]}" style="max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);"></div>')
    
    lines.append(f'')
    lines.append(f'<h2 data-i18n="tipTitle">{tr("tipTitle", 0)}</h2>')
    for i, tip in enumerate(tips, 1):
        tk = f'{a}Tip{i}'
        add_tr(tk, tip[0], tip[1], tip[2], tip[3])
        lines.append(f'<div class="tip"><strong data-i18n="tipLabel">{tr("tipLabel", 0)} {i}：</strong><span data-i18n="{tk}">{tip[0]}</span></div>')
    
    lines.append(f'')
    lines.append(f'<h2 data-i18n="faqTitle">{tr("faqTitle", 0)}</h2>')
    for i, (faq_q, faq_a) in enumerate(faqs, 1):
        qk = f'{a}Faq{i}Q'
        ak = f'{a}Faq{i}A'
        add_tr(qk, faq_q[0], faq_q[1], faq_q[2], faq_q[3])
        add_tr(ak, faq_a[0], faq_a[1], faq_a[2], faq_a[3])
        lines.append(f'<p><strong data-i18n="{qk}">{faq_q[0]}</strong><br/><span data-i18n="{ak}">{faq_a[0]}</span></p>')
    
    if related:
        items = ' · '.join(f'<a href="/tutorials/{t["slug"]}.html">{t["a_title"].split("教程：")[0] if "教程：" in t["a_title"] else t["a_title"]}</a>' for t in related)
        lines.append(f'')
        lines.append(f'<div class="rel-tools"><strong data-i18n="relTitle">{tr("relTitle", 0)}</strong>\n{items}\n</div>')
    
    body_html = '\n'.join(lines)
    
    # ── Build ZT_PAGE ──
    # Add shared keys
    for key in ['introTitle', 'openTitle', 'stepTitle', 'tipTitle', 'faqTitle', 'relTitle', 'backToIndex', 'tipLabel']:
        t = SHARED[key]
        for li, lang in enumerate(LANG_NAMES):
            lang_zt[lang][key] = t[li]
    
    # Add page-specific header keys
    for li, lang in enumerate(LANG_NAMES):
        git = git_langs.get(lang, {})
        lp = lang_zt[lang]
        
        lp['pageTitle'] = f"{git.get(c['a_key']+'Title', c['a_title'])} - ZenTools" if lang != 'zh' else f"{c['a_title']} - ZenTools"
        lp[c['cat_key']] = git.get(c['cat_key'], c['cat_text']) if lang != 'zh' else c['cat_text']
        lp[c['a_key'] + 'Title'] = git.get(c['a_key'] + 'Title', c['a_title']) if lang != 'zh' else c['a_title']
        lp[c['date_key']] = git.get(c['date_key'], c['date_text']) if lang != 'zh' else c['date_text']
        lp[c['read_key']] = git.get(c['read_key'], c['read_text']) if lang != 'zh' else c['read_text']
    
    # Build JS
    lang_blocks = []
    for li, lang in enumerate(LANG_NAMES):
        pairs = lang_zt[lang]
        p_str = ','.join(f"{k}:'{esc(v)}'" for k, v in pairs.items())
        lang_blocks.append(f"{lang}:{{{p_str}}}")
    
    zt_js = 'window.ZT_PAGE={' + ','.join(lang_blocks) + '};'
    
    return body_html, zt_js

def gen_one(c):
    body_html, zt_js = gen_body_tpl(c)
    
    slug = c['slug']; a_key = c['a_key']; cat_key = c['cat_key']
    a_title = c['a_title']; date_text = c['date_text']
    read_text = c['read_text']; summary = c['summary']
    
    page_title = a_title.replace("'", "\\'")
    page_summary = summary.replace("'", "\\'")
    page_date = date_text.replace('📅 ', '')
    
    # Build nav/footer with data-i18n for shared translations
    nav_html = '<a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/tools.html" data-i18n="navAll">全部工具</a>'
    footer_links = '<a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/privacy.html" data-i18n="navPrivacy">隐私政策</a>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">{page_title} - ZenTools</title>
<meta name="description" content="{page_summary}"/>
<link rel="canonical" href="https://zentools.xyz/tutorials/{slug}.html"/>
<link rel="manifest" href="/manifest.json" />
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.article-body {{ max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; }}
.article-body h2 {{ font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }}
.article-body h3 {{ font-size:16px; font-weight:600; color:var(--cyan); margin:24px 0 8px; }}
.article-body p, .article-body li {{ font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:10px; }}
.article-body .tip {{ background:rgba(0,229,255,0.06); border-left:3px solid var(--cyan); padding:14px 18px; border-radius:0 10px 10px 0; margin:16px 0; font-size:14px; color:var(--text); }}
.article-body .rel-tools {{ font-size:13px; color:var(--muted); margin-top:12px; }}
.article-body .rel-tools a {{ color:var(--cyan); text-decoration:none; }}
.article-body .rel-tools a:hover {{ text-decoration:underline; }}
.page-tutorial {{ max-width:920px; margin:0 auto; padding:20px 16px 60px; }}
.page-tutorial .back-link {{ display:inline-flex; align-items:center; gap:6px; font-size:14px; color:var(--muted); margin-bottom:20px; transition:color 0.2s; }}
.page-tutorial .back-link:hover {{ color:var(--cyan); }}
.page-tutorial .page-eyebrow {{ font-size:12px; font-weight:700; color:var(--cyan); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; display:block; }}
.page-tutorial h1 {{ font-size:28px; font-weight:800; margin-bottom:8px; }}
.page-tutorial .meta {{ font-size:13px; color:var(--muted); display:flex; gap:16px; margin-bottom:24px; }}
.screenshot-wrap img {{ max-width:100%; border-radius:12px; border:1px solid rgba(255,255,255,0.08); margin:12px 0; box-shadow:0 8px 24px rgba(0,0,0,0.3); }}
</style>
<meta name="google-adsense-account" content="ca-pub-1955887568822472">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1955887568822472" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"{page_title}","description":"{page_summary}","datePublished":"{page_date}","author":{{"@type":"Organization","name":"ZenTools"}},"publisher":{{"@type":"Organization","name":"ZenTools"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://zentools.xyz/tutorials/{slug}.html"}}}}</script>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links">{nav_html}<select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">← <span data-i18n="backToIndex">{tr("backToIndex", 0)}</span></a>
<span class="page-eyebrow" data-i18n="{cat_key}">{c['cat_text']}</span>
<h1 data-i18n="{a_key}Title">{a_title}</h1>
<div class="meta"><span data-i18n="{c['date_key']}">{date_text}</span><span data-i18n="{c['read_key']}">{read_text}</span></div>

<div class="article-body">
{body_html}
</div>
</div>

<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links">{footer_links}</div><p class="footer-copy" data-i18n="footerCopy">© 2026 ZenTools. 免费在线工具箱。</p></div></footer>
</div>

<script>
{zt_js}
</script>
<script src="../assets/js/tool-ui.min.js"></script>
<button class="bookmark-float" onclick="prompt('复制链接收藏本站','https://zentools.xyz')">⭐ 收藏本站，下次办公快人一步</button>
<script>
if ('serviceWorker' in navigator) {{
  window.addEventListener('load', () => {{
    navigator.serviceWorker.register('/service-worker.js').catch(() => {{}});
  }});
}}
</script>
</body>
</html>'''
    
    return html

# ── Generate all pages ──
count = 0
for c in unique_cards:
    if c['slug'] == 'qr-generator':
        continue
    html = gen_one(c)
    path = f'/workspace/tutorials/{c["slug"]}.html'
    with open(path, 'w') as f:
        f.write(html)
    count += 1
    print(f"OK {c['slug']}")

print(f"\nDone! Generated {count} pages with full i18n support")
