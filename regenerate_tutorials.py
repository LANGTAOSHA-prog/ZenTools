#!/usr/bin/env python3
"""Regenerate all tutorial pages with i18n ZT_PAGE support."""
import os, re, subprocess, json

# ── Load card data from current index.html ──
with open('/workspace/tutorials/index.html', 'r') as f:
    index = f.read()

# Parse cards
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

# Deduplicate
seen = set()
unique_cards = []
for c in cards:
    if c['slug'] not in seen:
        seen.add(c['slug'])
        unique_cards.append(c)

# ── Load ZT_PAGE translations from git ──
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

# ── SVG availability ──
svgs = set(os.listdir('/workspace/guides/img/'))

def svg_for(slug, step):
    name = f'{slug}-step{step}.svg'
    return f'/guides/img/{name}' if name in svgs else None

# ── Content templates per category ──
CONTENT_TEMPLATES = {}

CONTENT_TEMPLATES['catPdf'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成，无需上传文件到服务器。'),
        ('选择文件', '点击上传区域选择需要处理的 PDF 文件，或直接拖拽文件到上传区域。'),
        ('设置参数', '根据需要调整处理参数，工具会实时显示预览效果。'),
        ('下载结果', '处理完成后点击「下载」按钮保存文件。'),
    ],
    tips=['处理大文件时请耐心等待，处理速度取决于本地电脑性能。', '所有操作在浏览器本地完成，文件不会上传到服务器。'],
    faqs=[
        ('Q：支持多大的文件？', 'A：取决于浏览器内存限制，通常支持 100MB 以内的文件。'),
        ('Q：需要注册账号吗？', 'A：不需要。所有工具完全免费，无需注册。'),
        ('Q：文件会上传到服务器吗？', 'A：不会。所有处理在浏览器本地完成。'),
    ],
)

CONTENT_TEMPLATES['catImg'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成。'),
        ('上传图片', '点击上传区域选择需要处理的图片，或拖拽文件到上传区域。'),
        ('调整参数', '根据需求调整处理参数，所有效果实时预览。'),
        ('下载保存', '确认效果满意后点击「下载」按钮保存处理后的图片。'),
    ],
    tips=['支持 JPG、PNG、WebP、BMP 等常见图片格式。', '所有处理均在浏览器本地完成。'],
    faqs=[
        ('Q：支持哪些图片格式？', 'A：支持 JPG、PNG、WebP、BMP、GIF 等常见格式。'),
        ('Q：需要安装软件吗？', 'A：不需要。直接在浏览器中使用。'),
    ],
)

CONTENT_TEMPLATES['catVideo'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成。'),
        ('上传视频', '选择视频文件。支持 MP4、WebM、AVI 等常见格式。'),
        ('设置参数', '根据需要设置处理参数。'),
        ('下载结果', '处理完成后点击「下载」按钮获取结果。'),
    ],
    tips=['建议使用 MP4 格式以获得最佳兼容性。', '视频处理速度取决于文件大小和电脑性能。'],
    faqs=[
        ('Q：支持哪些视频格式？', 'A：支持 MP4、WebM、AVI、MOV 等常见格式。'),
        ('Q：需要付费吗？', 'A：完全免费使用。'),
    ],
)

CONTENT_TEMPLATES['catAudio'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中处理。'),
        ('上传音频', '选择音频文件。支持 MP3、WAV、OGG 等常见格式。'),
        ('编辑处理', '根据需要调整参数。'),
        ('下载保存', '处理完成后点击下载按钮获取结果。'),
    ],
    tips=['所有处理在浏览器本地完成。', '建议使用 MP3 格式。'],
    faqs=[
        ('Q：支持哪些音频格式？', 'A：支持 MP3、WAV、OGG、AAC、FLAC 等。'),
        ('Q：处理后的音质会下降吗？', 'A：工具保持原始音频质量。'),
    ],
)

CONTENT_TEMPLATES['catAI'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。'),
        ('输入内容', '在输入框中输入你的需求或问题。'),
        ('等待AI处理', 'AI 会自动处理并生成结果。'),
        ('查看结果', '不满意可以重新生成或微调输入。'),
    ],
    tips=['输入描述越详细，AI 生成的结果越精准。', '可以多次尝试不同输入。'],
    faqs=[
        ('Q：AI 生成的内容准确吗？', 'A：AI 生成内容仅供参考，重要信息建议人工核实。'),
        ('Q：需要联网吗？', 'A：需要联网使用 AI 服务。'),
        ('Q：使用需要付费吗？', 'A：完全免费。'),
    ],
)

CONTENT_TEMPLATES['catDev'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。'),
        ('输入数据', '粘贴或输入你需要处理的数据内容。'),
        ('自动处理', '工具会自动分析并处理数据。'),
        ('复制结果', '点击「复制」按钮将结果复制到剪贴板。'),
    ],
    tips=['所有处理在浏览器本地完成，数据不会上传到服务器。', '支持键盘快捷键操作。'],
    faqs=[
        ('Q：数据会被保存吗？', 'A：不会。数据仅在浏览器内存中处理。'),
        ('Q：支持大数据量吗？', 'A：取决于浏览器内存限制。'),
    ],
)

CONTENT_TEMPLATES['catFinance'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中计算。'),
        ('输入参数', '填写相关的财务参数。'),
        ('查看结果', '工具会自动计算并展示详细结果。'),
        ('调整方案', '修改任意参数重新计算。'),
    ],
    tips=['计算结果仅供参考，实际以金融机构为准。', '可以对比不同方案下的差异。'],
    faqs=[
        ('Q：计算结果准确吗？', 'A：工具使用标准财务公式计算。'),
        ('Q：数据会上传到服务器吗？', 'A：不会。所有计算在浏览器本地完成。'),
    ],
)

CONTENT_TEMPLATES['catSEO'] = dict(
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。'),
        ('输入网址或内容', '输入需要分析的网址或文本。'),
        ('查看分析结果', '工具会自动分析并展示优化建议。'),
        ('优化调整', '根据分析建议调整内容。'),
    ],
    tips=['SEO 是持续优化的过程，建议定期检查和调整。', '结合多种工具一起使用效果更佳。'],
    faqs=[
        ('Q：分析结果准确吗？', 'A：工具模拟搜索引擎的常见规则，结果有参考价值。'),
        ('Q：需要付费吗？', 'A：完全免费。'),
    ],
)

CAT_TEMPLATE_KEYS = {
    'catPdf': 'catPdf', 'catImg': 'catImg', 'catVideo': 'catVideo',
    'catAudio': 'catAudio', 'catAI': 'catAI', 'catDev': 'catDev',
    'catFinance': 'catFinance', 'catSEO': 'catSEO', 'catQR': 'catImg',
}

def gen_one(c):
    slug = c['slug']; a_key = c['a_key']; cat_key = c['cat_key']
    a_title = c['a_title']; cat_text = c['cat_text']
    date_text = c['date_text']; read_text = c['read_text']
    summary = c['summary']
    
    tpl = CONTENT_TEMPLATES.get(CAT_TEMPLATE_KEYS.get(cat_key, 'catDev'), CONTENT_TEMPLATES['catDev'])
    tool_url = f'/{slug.replace("-","/")}.html'
    tool_name = a_title.split('教程：')[0] if '教程：' in a_title else a_title
    tool_link = f'<a href="{tool_url}" target="_blank">{tool_name}</a>'
    
    # Build steps
    steps_html = ''
    for idx, (stitle, sbody) in enumerate(tpl['steps'], 1):
        steps_html += f'<h3>{idx}. {stitle}</h3>\n<p>{sbody.replace("{tool_link}", tool_link)}</p>\n'
        svg = svg_for(slug, idx)
        if svg:
            steps_html += f'<div class="screenshot-wrap"><img src="{svg}" alt="{a_title} - {stitle}" style="max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);"></div>\n'
    
    # Tips
    tips_html = ''.join(f'<div class="tip"><strong>提示 {i}：</strong><span>{t}</span></div>\n' for i, t in enumerate(tpl['tips'], 1))
    # FAQ
    faqs_html = ''.join(f'<p><strong>{q}</strong><br/><span>{a}</span></p>\n' for q, a in tpl['faqs'])
    # Related
    related = [t for t in unique_cards if t['slug'] != slug and t['cat_key'] == cat_key][:4]
    rel_html = ''
    if related:
        items = ' · '.join(f'<a href="/tutorials/{t["slug"]}.html">{t["a_title"].split("教程：")[0] if "教程：" in t["a_title"] else t["a_title"]}</a>' for t in related)
        rel_html = f'<div class="rel-tools">🔗 <strong>相关工具：</strong>\n{items}\n</div>\n'
    
    # Build ZT_PAGE for this page
    page_keys = ['pageTitle', 'backToIndex', cat_key, a_key + 'Title', c['date_key'], c['read_key']]
    lang_blocks = []
    for lang in ['zh', 'en', 'ja', 'vi']:
        pairs = {}
        for pk in page_keys:
            if lang == 'zh':
                # From our card data
                if pk == 'pageTitle':
                    pairs[pk] = f"{a_title} - ZenTools"
                elif pk == 'backToIndex':
                    pairs[pk] = '返回教程中心'
                elif pk == cat_key:
                    pairs[pk] = cat_text
                elif pk == a_key + 'Title':
                    pairs[pk] = a_title
                elif pk == c['date_key']:
                    pairs[pk] = date_text
                elif pk == c['read_key']:
                    pairs[pk] = read_text
            else:
                # Try git translations, fallback to zh
                git_pairs = git_langs.get(lang, {})
                if pk == 'pageTitle':
                    en_title = git_pairs.get(a_key + 'Title', a_title) if lang == 'en' else a_title
                    pairs[pk] = f"{en_title} - ZenTools" if lang == 'en' else f"{a_title} - ZenTools"
                elif pk == 'backToIndex':
                    pairs[pk] = git_pairs.get('backToIndex', '返回教程中心') if lang == 'en' else {'en': 'Back to Tutorials', 'ja': 'チュートリアルに戻る', 'vi': 'Quay lại hướng dẫn'}.get(lang, a_title)
                elif pk == cat_key:
                    pairs[pk] = git_pairs.get(cat_key, cat_text)
                elif pk == a_key + 'Title':
                    pairs[pk] = git_pairs.get(pk, a_title)
                elif pk == c['date_key']:
                    pairs[pk] = git_pairs.get(pk, date_text)
                elif pk == c['read_key']:
                    pairs[pk] = git_pairs.get(pk, read_text)
        
        # Build block
        p_str = ','.join(f"{k}:'{v.replace(chr(39), chr(39)+chr(39))}'" for k, v in pairs.items())
        lang_blocks.append(f"{lang}:{{{p_str}}}")
    
    zt_js = 'window.ZT_PAGE={' + ','.join(lang_blocks) + '};'
    
    page_title = a_title.replace("'", "\\'")
    page_summary = summary.replace("'", "\\'")
    page_date = date_text.replace('📅 ', '')

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
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/" data-i18n="navHome">\u9996\u9875</a><a href="/dev/" data-i18n="navDev">\u5f00\u53d1\u5de5\u5177</a><a href="/tools.html" data-i18n="navAll">\u5168\u90e8\u5de5\u5177</a><select id="langSelect" class="lang-select"><option value="zh">\u4e2d\u6587</option><option value="en">English</option><option value="ja">\u65e5\u672c\u8a9e</option><option value="vi">Ti\u1ebfng Vi\u1ec7t</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">\u2190 <span data-i18n="backToIndex">\u8fd4\u56de\u6559\u7a0b\u4e2d\u5fc3</span></a>
<span class="page-eyebrow" data-i18n="{cat_key}">{cat_text}</span>
<h1 data-i18n="{a_key}Title">{a_title}</h1>
<div class="meta"><span data-i18n="{c['date_key']}">{date_text}</span><span data-i18n="{c['read_key']}">{read_text}</span></div>

<div class="article-body">
<h2>\u529f\u80fd\u4ecb\u7ecd</h2>
<p>{summary}</p>

<h2>\u6253\u5f00\u5de5\u5177</h2>
<p>\u8bbf\u95ee {tool_link}\uff0c\u5728\u6d4f\u89c8\u5668\u4e2d\u76f4\u63a5\u4f7f\u7528\u3002\u6240\u6709\u64cd\u4f5c\u5728\u6d4f\u89c8\u5668\u672c\u5730\u5b8c\u6210\uff0c\u65e0\u9700\u5b89\u88c5\u4efb\u4f55\u8f6f\u4ef6\uff0c\u6587\u4ef6\u4e0d\u4f1a\u4e0a\u4f20\u5230\u670d\u52a1\u5668\u3002</p>

<h2>\u64cd\u4f5c\u6b65\u9aa4</h2>
{steps_html}
<h2>\u5b9e\u7528\u6280\u5de7</h2>
{tips_html}
<h2>\u5e38\u89c1\u95ee\u9898</h2>
{faqs_html}
{rel_html}
</div>
</div>

<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links"><a href="/" data-i18n="navHome">\u9996\u9875</a><a href="/dev/" data-i18n="navDev">\u5f00\u53d1\u5de5\u5177</a><a href="/privacy.html" data-i18n="navPrivacy">\u9690\u79c1\u653f\u7b56</a></div><p class="footer-copy" data-i18n="footerCopy">\u00a9 2026 ZenTools. \u514d\u8d39\u5728\u7ebf\u5de5\u5177\u7bb1\u3002</p></div></footer>
</div>

<script>
{zt_js}
</script>
<script src="../assets/js/tool-ui.min.js"></script>
<button class="bookmark-float" onclick="prompt('\u590d\u5236\u94fe\u63a5\u6536\u85cf\u672c\u7ad9','https://zentools.xyz')">\u2b50 \u6536\u85cf\u672c\u7ad9\uff0c\u4e0b\u6b21\u529e\u516c\u5feb\u4eba\u4e00\u6b65</button>
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

# Generate
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

print(f"\nDone! Generated {count} pages with i18n support")
