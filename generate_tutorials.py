#!/usr/bin/env python3
"""Batch generate standalone tutorial pages for all tools."""
import os, re, json

# ── Read card metadata from index.html ──
with open('/workspace/tutorials/index.html', 'r') as f:
    index_content = f.read()

sections = re.split(r'<!-- (Article \d+: .+?) -->', index_content)
cards = []
for i in range(1, len(sections), 2):
    block = sections[i+1] if i+1 < len(sections) else ''
    href_m = re.search(r'<a class="article-card" href="([^"]+)"', block)
    if not href_m: continue
    slug = href_m.group(1).replace('/tutorials/', '').replace('.html', '')
    title_m = re.search(r'<h3[^>]*>([^<]+)</h3>', block)
    cat_m = re.search(r'<div class="cat"[^>]*>([^<]+)</div>', block)
    date_m = re.search(r'data-i18n="([^"]*Date)"[^>]*>([^<]+)<', block)
    read_m = re.search(r'data-i18n="([^"]*Read)"[^>]*>([^<]+)<', block)
    sum_m = re.search(r'<div class="summary"[^>]*>([^<]*)</div>', block)
    a_key_m = re.search(r'data-i18n="(a\d+)Title"', block)
    cat_key_m = re.search(r'data-i18n="(cat\w+)"', block)
    tags = re.findall(r'data-i18n="(tag\w+)"[^>]*>([^<]+)<', block)
    tag_keys = [t[0] for t in tags]
    tag_texts = [t[1] for t in tags]

    cards.append(dict(
        slug=slug, title=title_m.group(1) if title_m else '',
        cat_text=cat_m.group(1) if cat_m else '',
        date_key=date_m.group(1) if date_m else 'a1Date',
        date_text=date_m.group(2) if date_m else '',
        read_key=read_m.group(1) if read_m else 'a1Read',
        read_text=read_m.group(2) if read_m else '',
        summary=sum_m.group(1) if sum_m else '',
        a_key=a_key_m.group(1) if a_key_m else 'a1',
        cat_key=cat_key_m.group(1) if cat_key_m else 'catDev',
        tag_keys=tag_keys, tag_texts=tag_texts,
    ))

# Deduplicate
seen = set()
unique_cards = []
for c in cards:
    if c['slug'] not in seen:
        seen.add(c['slug'])
        unique_cards.append(c)

# ── SVG availability ──
svgs = set(os.listdir('/workspace/guides/img/'))

def svg_for(slug, step):
    """Check if a specific SVG exists for this tool+step."""
    for ext in ['.svg']:
        name = f'{slug}-step{step}{ext}'
        if name in svgs: return f'/guides/img/{name}'
        alt = slug.replace('-', '_') + f'_step{step}' + ext
        if alt in svgs: return f'/guides/img/{alt}'
    return None

def has_any_svg(slug):
    """Check if any SVG exists for this tool."""
    return any(f.startswith(slug) for f in svgs)

# ── Content templates per category ──
CONTENT_TEMPLATES = {}

CONTENT_TEMPLATES['catPdf'] = dict(
    why_tip='PDF是日常办公中最常见的文档格式。',
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成，无需上传文件到服务器。', True),
        ('选择文件', '点击上传区域选择需要处理的 PDF 文件，或直接拖拽文件到上传区域。支持批量选择多个文件。', True),
        ('设置参数', '根据需要调整处理参数，工具会实时显示预览效果，方便你确认输出结果。', False),
        ('下载结果', '处理完成后点击「下载」按钮保存文件。所有文件仅在浏览器本地处理，不会上传到服务器。', True),
    ],
    tips=['处理大文件时请耐心等待，处理速度取决于本地电脑性能。', '所有操作在浏览器本地完成，文件不会上传到服务器，保护隐私安全。'],
    faqs=[
        ('Q：支持多大的文件？', 'A：取决于浏览器内存限制，通常支持 100MB 以内的文件。超大文件建议分批处理。'),
        ('Q：需要注册账号吗？', 'A：不需要。所有工具完全免费，无需注册，打开即用。'),
        ('Q：文件会上传到服务器吗？', 'A：不会。所有处理在浏览器本地完成，文件不会离开你的电脑。'),
    ],
)

CONTENT_TEMPLATES['catImg'] = dict(
    why_tip='图片处理是日常办公和设计中常见的需求。',
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成，无需上传文件。', True),
        ('上传图片', '点击上传区域选择需要处理的图片，或拖拽图片文件到上传区域。支持 JPG、PNG 等常见格式。', True),
        ('调整参数', '根据需求调整处理参数，所有效果实时预览，所见即所得。', False),
        ('下载保存', '确认效果满意后点击「下载」按钮保存处理后的图片。', True),
    ],
    tips=['支持常见图片格式：JPG、PNG、WebP、BMP 等。', '所有处理均在浏览器本地完成，保护你的图片隐私安全。'],
    faqs=[
        ('Q：支持哪些图片格式？', 'A：支持 JPG、PNG、WebP、BMP、GIF 等常见图片格式。'),
        ('Q：处理后的图片质量会降低吗？', 'A：不会。工具使用无损处理算法，确保输出质量。'),
        ('Q：需要安装软件吗？', 'A：不需要。直接在浏览器中使用，无需下载安装任何软件。'),
    ],
)

CONTENT_TEMPLATES['catVideo'] = dict(
    why_tip='视频处理是内容创作中常见的需求。',
    steps=[
        ('打开工具', '访问 {tool_link}，所有处理在浏览器本地完成。', True),
        ('上传视频', '点击上传区域选择视频文件。支持 MP4、WebM、AVI 等常见视频格式。', True),
        ('设置处理参数', '根据需要设置处理参数，工具提供实时预览功能。', False),
        ('下载结果', '处理完成后点击「下载」按钮获取结果文件。', True),
    ],
    tips=['建议使用 MP4 格式以获得最佳兼容性。', '视频处理速度取决于文件大小和电脑性能。'],
    faqs=[
        ('Q：支持哪些视频格式？', 'A：支持 MP4、WebM、AVI、MOV 等常见格式。'),
        ('Q：视频文件有大小限制吗？', 'A：取决于浏览器内存，建议 500MB 以内的文件。'),
        ('Q：处理速度如何？', 'A：速度取决于视频大小和电脑性能，小文件几秒即可完成。'),
    ],
)

CONTENT_TEMPLATES['catAudio'] = dict(
    why_tip='音频编辑是内容创作中的常见需求。',
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中处理音频。', True),
        ('上传音频', '选择或拖拽音频文件到上传区域。支持 MP3、WAV、OGG 等常见音频格式。', True),
        ('编辑处理', '根据需要调整音频处理参数，可试听效果。', False),
        ('下载保存', '处理完成后点击下载按钮获取结果文件。', True),
    ],
    tips=['所有处理在浏览器本地完成，保护隐私。', '建议使用 MP3 格式以获得最佳兼容性。'],
    faqs=[
        ('Q：支持哪些音频格式？', 'A：支持 MP3、WAV、OGG、AAC、FLAC 等格式。'),
        ('Q：音频文件有大小限制吗？', 'A：取决于浏览器内存，通常 200MB 以内可正常处理。'),
        ('Q：处理后的音质会下降吗？', 'A：工具保持原始音频质量，不会额外压缩降低音质。'),
    ],
)

CONTENT_TEMPLATES['catAI'] = dict(
    why_tip='AI 工具正在改变我们的工作方式。',
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。', True),
        ('输入内容', '在输入框中输入你的需求或问题，尽可能描述清楚以获得最佳结果。', True),
        ('等待AI处理', 'AI 会自动处理你的请求并生成结果，过程可能需要几秒钟。', False),
        ('查看结果', '浏览 AI 生成的内容，不满意可以重新生成或微调输入。', True),
    ],
    tips=['输入描述越详细，AI 生成的结果越精准。', '可以多次尝试不同输入，获得最满意的结果。'],
    faqs=[
        ('Q：AI 生成的内容准确吗？', 'A：AI 生成内容仅供参考，重要信息建议人工核实。'),
        ('Q：需要联网吗？', 'A：需要联网使用 AI 服务。'),
        ('Q：使用需要付费吗？', 'A：目前完全免费，无需注册即可使用。'),
    ],
)

CONTENT_TEMPLATES['catDev'] = dict(
    why_tip='开发者工具帮助提高编码和工作效率。',
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。', True),
        ('输入数据', '粘贴或输入你需要处理的数据内容。', True),
        ('自动处理', '工具会自动分析并处理数据，实时显示结果。', False),
        ('复制结果', '查看处理结果，点击「复制」按钮将结果复制到剪贴板。', True),
    ],
    tips=['所有处理在浏览器本地完成，数据不会上传到服务器。', '支持键盘快捷键操作，提高效率。'],
    faqs=[
        ('Q：数据会被保存吗？', 'A：不会。数据仅在浏览器内存中处理，关闭页面即清除。'),
        ('Q：支持大数据量吗？', 'A：取决于浏览器内存限制，一般可处理数 MB 的数据。'),
        ('Q：开源吗？', 'A：工具完全免费使用，详情可查看网站说明。'),
    ],
)

CONTENT_TEMPLATES['catFinance'] = dict(
    why_tip='理财计算帮助做出明智的财务决策。',
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中计算。', True),
        ('输入参数', '填写相关的财务参数，如金额、利率、期限等。', True),
        ('查看结果', '工具会自动计算并展示详细的还款计划或财务分析。', False),
        ('调整方案', '修改任意参数重新计算，对比不同方案的差异。', True),
    ],
    tips=['计算结果仅供参考，实际以金融机构为准。', '可以对比不同利率和期限下的还款差异。'],
    faqs=[
        ('Q：计算结果准确吗？', 'A：工具使用标准财务公式计算，结果准确可靠。'),
        ('Q：数据会上传到服务器吗？', 'A：不会。所有计算在浏览器本地完成。'),
        ('Q：需要注册吗？', 'A：不需要，打开即用。'),
    ],
)

CONTENT_TEMPLATES['catSEO'] = dict(
    why_tip='SEO 优化帮助提升网站在搜索引擎中的排名。',
    steps=[
        ('打开工具', '访问 {tool_link}，直接在浏览器中使用。', True),
        ('输入网址或内容', '输入需要分析的网址或文本内容。', True),
        ('查看分析结果', '工具会自动分析并展示优化建议。', False),
        ('优化调整', '根据分析建议调整内容，再次验证效果。', True),
    ],
    tips=['SEO 是持续优化的过程，建议定期检查和调整。', '结合多种工具一起使用效果更佳。'],
    faqs=[
        ('Q：分析结果准确吗？', 'A：工具模拟搜索引擎的常见规则，结果有参考价值。'),
        ('Q：需要付费吗？', 'A：完全免费使用。'),
        ('Q：数据安全吗？', 'A：分析过程在浏览器中进行，不会存储你的数据。'),
    ],
)

CAT_TEMPLATE_KEYS = {
    'catPdf': 'catPdf', 'catImg': 'catImg', 'catVideo': 'catVideo',
    'catAudio': 'catAudio', 'catAI': 'catAI', 'catDev': 'catDev',
    'catFinance': 'catFinance', 'catSEO': 'catSEO', 'catQR': 'catImg',
}

def gen_tutorial_pages(cards):
    for c in cards:
        if c['slug'] == 'qr-generator':
            print(f"SKIP {c['slug']} (already exists)")
            continue
        
        gen_one_page(c)
        print(f"OK   {c['slug']}")

def gen_one_page(c):
    slug = c['slug']
    title = c['title']
    cat_text = c['cat_text']
    date_text = c['date_text']
    read_text = c['read_text']
    summary = c['summary']
    a_key = c['a_key']
    cat_key = c['cat_key']
    tag_keys = c['tag_keys']
    tag_texts = c['tag_texts']
    
    # Determine category template
    tpl_key = CAT_TEMPLATE_KEYS.get(cat_key, 'catDev')
    tpl = CONTENT_TEMPLATES.get(tpl_key, CONTENT_TEMPLATES['catDev'])
    
    # Tool link (infer from slug)
    tool_link = f'<a href="/{slug.replace("-","/")}.html" target="_blank">{title.split("教程：")[0] if "教程：" in title else title}</a>'
    tool_url = f'/{slug.replace("-","/")}.html'
    
    # Build step HTML
    steps_html = ''
    for idx, (step_title, step_body, has_svg) in enumerate(tpl['steps'], 1):
        step_body_filled = step_body.replace('{tool_link}', tool_link)
        svg_path = svg_for(slug, idx)
        steps_html += f'<h3>{idx}. {step_title}</h3>\n<p>{step_body_filled}</p>\n'
        if has_svg and svg_path:
            steps_html += f'''<div class="screenshot-wrap">
  <img src="{svg_path}" alt="{title} - {step_title}" style="max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);">
</div>\n'''
    
    # Build tips HTML
    tips_html = ''
    for i, tip in enumerate(tpl['tips'], 1):
        tips_html += f'<div class="tip"><strong>提示 {i}：</strong><span>{tip}</span></div>\n'
    
    # Build FAQ HTML
    faqs_html = ''
    for q, a in tpl['faqs']:
        faqs_html += f'<p><strong>{q}</strong><br/><span>{a}</span></p>\n'
    
    # Related tools (tools in same category)
    related_tools = [t for t in unique_cards if t['slug'] != slug and t['cat_key'] == cat_key][:4]
    rel_html = ''
    if related_tools:
        rel_list = ' · '.join(
            f'<a href="/tutorials/{t["slug"]}.html">{t["title"].split("教程：")[0] if "教程：" in t["title"] else t["title"]}</a>'
            for t in related_tools
        )
        rel_html = f'<div class="rel-tools">🔗 <strong>相关工具：</strong>\n{rel_list}\n</div>\n'
    
    # Build HTML
    page_html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{title} - ZenTools</title>
<meta name="description" content="{summary}"/>
<link rel="canonical" href="https://zentools.xyz/tutorials/{slug}.html"/>
<link rel="manifest" href="/manifest.json" />
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.article-body {{ max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; transition:border-color 0.3s,box-shadow 0.3s; }}
.article-body h2 {{ font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }}
.article-body h3 {{ font-size:16px; font-weight:600; color:var(--cyan); margin:24px 0 8px; }}
.article-body p, .article-body li {{ font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:10px; }}
.article-body ul, .article-body ol {{ padding-left:20px; }}
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
.screenshot-wrap p {{ text-align:center; font-size:12px; color:#6b7a9f; margin-top:4px; }}
</style>
<meta name="google-adsense-account" content="ca-pub-1955887568822472">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1955887568822472" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"{title}","description":"{summary}","datePublished":"{date_text.replace('📅 ','')}","author":{{"@type":"Organization","name":"ZenTools"}},"publisher":{{"@type":"Organization","name":"ZenTools"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://zentools.xyz/tutorials/{slug}.html"}},"about":"{title.split("教程：")[0] if "教程：" in title else title}"}}</script>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/">首页</a><a href="/dev/">开发工具</a><a href="/tools.html">全部工具</a><select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">← 返回教程中心</a>
<span class="page-eyebrow">{cat_text}</span>
<h1>{title}</h1>
<div class="meta"><span>{date_text}</span><span>{read_text}</span></div>

<div class="article-body">

<h2>功能介绍</h2>
<p>{summary} {tpl.get('why_tip', '')}</p>

<h2>打开工具</h2>
<p>访问 {tool_link}，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件，文件不会上传到服务器。</p>

<h2>操作步骤</h2>

{steps_html}
<h2>实用技巧</h2>
{tips_html}
<h2>常见问题</h2>
{faqs_html}
{rel_html}
</div>
</div>

<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links"><a href="/">首页</a><a href="/dev/">开发工具</a><a href="/privacy.html">隐私政策</a></div><p class="footer-copy">© 2026 ZenTools. 免费在线工具箱。</p></div></footer>
</div>

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
    
    path = f'/workspace/tutorials/{slug}.html'
    with open(path, 'w') as f:
        f.write(page_html)

# Run
gen_tutorial_pages(unique_cards)
print(f"\nDone! Generated {len(unique_cards) - 1} pages (skipped qr-generator)")