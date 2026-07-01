#!/usr/bin/env python3
"""Generate all 40 missing tutorial pages + 10 scenario collection guides for ZenTools."""
import json, os, re

BASE = os.path.join(os.path.dirname(__file__), "tutorials")
GUIDES = os.path.join(os.path.dirname(__file__), "guides")
TOOLS_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tools-data.json")

# ===== Load tools-data for URLs and descriptions =====
with open(TOOLS_DATA_PATH) as f:
    tools_data = json.load(f)
tools_map = {}
for t in tools_data['tools']:
    slug = t.get('slug', '')
    tools_map[slug] = t

# ===== build_html function (adapted from _gen_tutorials.py) =====
def build_html(tool_id, title_zh, desc_zh, func_zh, duration, tool_url, svg_file, step_keys, tips, faqs, related, cat_label="🏠 生活工具"):
    zh = {
        "a1Intro": func_zh,
        "a1OpenBody": f'访问 <a href="{tool_url}" target="_blank">{title_zh.split("：")[0] if "：" in title_zh else title_zh.split(":")[0]}</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需注册账号，完全免费。',
    }
    zh[f"{step_keys}Step1T"] = "打开工具"
    zh[f"{step_keys}Step1B"] = f'访问<a href="{tool_url}" target="_blank">{title_zh.split("：")[0] if "：" in title_zh else title_zh.split(":")[0]}</a>，在浏览器中打开工具页面。页面简洁直观，无需安装任何软件。'
    zh[f"{step_keys}Step2T"] = "选择操作"
    zh[f"{step_keys}Step2B"] = "根据需要选择操作模式或输入处理参数。工具提供多种操作选项，可以根据不同的使用场景灵活配置。"
    zh[f"{step_keys}Step3T"] = "上传文件"
    zh[f"{step_keys}Step3B"] = "点击上传区域或拖拽文件到指定区域。支持多种常见格式，单文件最大100MB。上传的文件在浏览器本地处理，不会上传到服务器。"
    zh[f"{step_keys}Step4T"] = "查看结果"
    zh[f"{step_keys}Step4B"] = "处理完成后结果会实时显示，你可以预览、复制或下载处理结果。所有操作均可重复进行。"
    for i, tip in enumerate(tips, 1):
        zh[f"{step_keys}Tip{i}"] = tip

    # [AI 搜索优化] 通用 FAQ：每个工具页面都回答这些核心问题
    universal_faqs = [
        ("这个工具适合谁？适合哪些使用场景？",
         f"本教程介绍的{title_zh.split('：')[0] if '：' in title_zh else title_zh.split(':')[0]}适合日常办公用户、学生、自由职业者和小型企业团队。无论你是需要快速处理文档的上班族、整理学习资料的学生，还是需要批量处理素材的内容创作者，都可以免费使用。无需任何专业技能，打开浏览器即可上手。"),
        ("完全免费吗？有什么使用限制？",
         f"{title_zh.split('：')[0] if '：' in title_zh else title_zh.split(':')[0]}完全免费，无隐藏费用、无订阅要求、无水印。主要限制包括：单文件最大 100MB，部分批量操作一次最多处理 20 个文件。所有处理在浏览器本地完成，不消耗你的云端配额或 API 额度。"),
        ("支持中文吗？界面和操作是否友好？",
         "完全支持中文界面（简体中文），同时也提供英文、日文、越南文界面。所有按钮、提示和说明均已本地化为中文，无需担心语言障碍。操作流程符合国内用户习惯，拖拽上传、一键处理，直观易用。"),
    ]
    all_faqs = list(faqs) + universal_faqs
    for i, (q, a) in enumerate(all_faqs, 1):
        zh[f"{step_keys}Faq{i}Q"] = q
        zh[f"{step_keys}Faq{i}A"] = a
    zh.update({
        "introTitle": "功能介绍", "openTitle": "打开工具", "stepTitle": "操作步骤",
        "tipTitle": "实用技巧", "faqTitle": "常见问题", "relTitle": "相关工具：",
        "backToIndex": "返回教程中心", "tipLabel": "提示",
        "pageTitle": f"{title_zh} - ZenTools", "catLabel": cat_label,
        "a1Title": title_zh, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration} 分钟阅读",
        "navHome": "首页", "navDev": "开发工具", "navAll": "全部工具",
        "navPrivacy": "隐私政策", "footerCopy": "© 2026 ZenTools. 免费在线工具箱。"
    })

    # English translations
    en = dict(zh)
    en.update({
        "introTitle": "Introduction", "openTitle": "Open the Tool", "stepTitle": "Steps",
        "tipTitle": "Tips", "faqTitle": "FAQ", "relTitle": "Related Tools:",
        "backToIndex": "Back to Tutorials", "tipLabel": "Tip",
        "catLabel": cat_label, "a1Read": f"⏱ {duration} min read",
        "navHome": "Home", "navDev": "Dev Tools", "navAll": "All Tools",
        "navPrivacy": "Privacy", "footerCopy": "© 2026 ZenTools. Free Online Toolbox."
    })
    for k in list(en.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                en[k] = zh[k].replace("打开工具", "Open the Tool").replace("选择操作", "Select Action").replace("上传文件", "Upload Files").replace("查看结果", "View Results")
            elif k.endswith("B"):
                en[k] = zh[k]

    ja = dict(zh)
    ja.update({
        "introTitle": "機能紹介", "openTitle": "ツールを開く", "stepTitle": "操作手順",
        "tipTitle": "ヒント", "faqTitle": "よくある質問", "relTitle": "関連ツール：",
        "backToIndex": "チュートリアルに戻る", "tipLabel": "ヒント",
        "catLabel": cat_label, "a1Read": f"⏱ {duration}分",
        "navHome": "ホーム", "navDev": "開発ツール", "navAll": "すべてのツール",
        "navPrivacy": "プライバシー", "footerCopy": "© 2026 ZenTools. 無料オンラインツールボックス。"
    })
    for k in list(ja.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                ja[k] = zh[k].replace("打开工具", "ツールを開く").replace("选择操作", "操作を選択").replace("上传文件", "ファイルアップロード").replace("查看结果", "結果を確認")
            elif k.endswith("B"):
                ja[k] = zh[k]

    vi = dict(zh)
    vi.update({
        "introTitle": "Giới thiệu", "openTitle": "Mở Công cụ", "stepTitle": "Các bước",
        "tipTitle": "Mẹo", "faqTitle": "Câu hỏi thường gặp", "relTitle": "Công cụ liên quan:",
        "backToIndex": "Quay lại Hướng dẫn", "tipLabel": "Mẹo",
        "catLabel": cat_label, "a1Read": f"⏱ {duration} phút đọc",
        "navHome": "Trang chủ", "navDev": "Công cụ Dev", "navAll": "Tất cả",
        "navPrivacy": "Quyền riêng tư", "footerCopy": "© 2026 ZenTools. Hộp công cụ trực tuyến miễn phí."
    })
    for k in list(vi.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                vi[k] = zh[k].replace("打开工具", "Mở Công cụ").replace("选择操作", "Chọn Thao tác").replace("上传文件", "Tải lên").replace("查看结果", "Xem Kết quả")
            elif k.endswith("B"):
                vi[k] = zh[k]

    rel_html = " · ".join([f'<a href="{r[0]}">{r[1]}</a>' for r in related])

    svg_steps = ""
    step_labels = [("打开工具", f"{title_zh} - 打开工具"),
                   ("选择操作", f"{title_zh} - 选择操作"),
                   ("上传文件", f"{title_zh} - 上传文件"),
                   ("查看结果", f"{title_zh} - 查看结果")]
    for i, (label, alt) in enumerate(step_labels, 1):
        svg_steps += f'''<h3 data-i18n="{step_keys}Step{i}T">{i}. {label}</h3>
<p data-i18n="{step_keys}Step{i}B">{zh[f"{step_keys}Step{i}B"]}</p>
<div class="screenshot-wrap"><img src="/guides/img/{svg_file}" alt="{alt}" style="max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);"></div>
'''

    tips_html = ""
    for i, tip in enumerate(tips, 1):
        tips_html += f'''<div class="tip"><strong data-i18n="tipLabel">提示 {i}：</strong><span data-i18n="{step_keys}Tip{i}">{tip}</span></div>
'''

    faq_html = ""
    for i, (q, a) in enumerate(all_faqs, 1):
        faq_html += f'''<div class="faq-item"><p><strong data-i18n="{step_keys}Faq{i}Q">{q}</strong><br/><span data-i18n="{step_keys}Faq{i}A">{a}</span></p></div>
'''

    # [AI 搜索优化] 构建 FAQPage JSON-LD 结构化数据
    faq_jsonld_items = []
    for i, (q, a) in enumerate(all_faqs, 1):
        faq_jsonld_items.append(f'{{"@type":"Question","name":{json.dumps(q)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}}}')
    faq_jsonld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(faq_jsonld_items)}]}}</script>'

    i18n_json = json.dumps({"zh": zh, "en": en, "ja": ja, "vi": vi}, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">{title_zh} - ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="canonical" href="https://zentools.xyz/tutorials/{tool_id}.html"/>
<link rel="manifest" href="/manifest.json" />
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.article-body {{ max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; }}
.article-body h2 {{ font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }}
.article-body h3 {{ font-size:16px; font-weight:600; color:var(--cyan); margin:24px 0 8px; }}
.article-body p, .article-body li {{ font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:10px; }}
.article-body .tip {{ background:rgba(0,229,255,0.06); border-left:3px solid var(--cyan); padding:14px 18px; border-radius:0 10px 10px 0; margin:16px 0; font-size:14px; color:var(--text); }}
.article-body .faq-item {{ margin:16px 0; padding:14px 18px; background:rgba(255,255,255,0.03); border:1px solid var(--border); border-radius:10px; }}
.article-body .faq-item strong {{ color:var(--text); font-size:14px; }}
.article-body .faq-item span {{ color:var(--muted); font-size:14px; line-height:1.7; display:block; margin-top:4px; }}
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
{faq_jsonld}
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"{title_zh}","description":"{desc_zh}","datePublished":"2026-06-23","author":{{"@type":"Organization","name":"ZenTools"}},"publisher":{{"@type":"Organization","name":"ZenTools"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://zentools.xyz/tutorials/{tool_id}.html"}}}}</script>
<meta name="keywords" content="{title_zh},在线教程,免费工具,浏览器处理,无需注册"/>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/tools.html" data-i18n="navAll">全部工具</a><select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">← <span data-i18n="backToIndex">返回教程中心</span></a>
<span class="page-eyebrow" data-i18n="catLabel">{cat_label}</span>
<h1 data-i18n="a1Title">{title_zh}</h1>
<div class="meta"><span data-i18n="a1Date">📅 2026-06-23</span><span data-i18n="a1Read">⏱ {duration} 分钟阅读</span></div>

<div class="article-body">
<h2 data-i18n="introTitle">功能介绍</h2>
<p data-i18n="a1Intro">{func_zh}</p>

<h2 data-i18n="openTitle">打开工具</h2>
<p data-i18n="a1OpenBody">{zh["a1OpenBody"]}</p>

<h2 data-i18n="stepTitle">操作步骤</h2>
{svg_steps}
<h2 data-i18n="tipTitle">实用技巧</h2>
{tips_html}
<h2 data-i18n="faqTitle">常见问题</h2>
{faq_html}
<div class="rel-tools"><strong data-i18n="relTitle">相关工具：</strong>
{rel_html}
</div>
</div>
</div>

<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/privacy.html" data-i18n="navPrivacy">隐私政策</a></div><p class="footer-copy" data-i18n="footerCopy">© 2026 ZenTools. 免费在线工具箱。</p></div></footer>
</div>

<script>
window.ZT_PAGE={i18n_json};
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


# ===== Build generic category-specific content =====
def make_image_tutorial(slug, name_zh, name_en, tool_url):
    """Generate image tool tutorial with image-specific steps."""
    cat_label = "🖼 图片工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线图片处理"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理图片文件。支持批量操作，所有处理在浏览器本地完成，保护图片隐私。"
    func = f"ZenTools {name_zh}工具是一款高效在线图片处理工具，支持对 JPG、PNG、WebP、GIF 等主流图片格式进行处理。"
    tips = [
        f"支持批量处理多张图片，可以同时上传多张图片进行{name_zh}操作，大大提高工作效率。",
        "所有处理在浏览器本地完成，图片不会上传到任何服务器，完全保护你的图片隐私和数据安全。",
        "处理后的图片建议及时保存，刷新页面后本地缓存会被清除。建议将常用操作结果收藏备用。"
    ]
    faqs = [
        ("支持哪些图片格式？", "支持 JPG、PNG、WebP、GIF、SVG、ICO、BMP 等主流图片格式。部分格式在处理后可能需要转换为其他格式。"),
        ("有图片大小限制吗？", "单张图片建议不超过 100MB，过大的图片可能会影响处理速度。对于超大图片，建议先压缩后再进行处理。"),
        ("可以批量处理吗？", f"可以。支持批量上传多张图片进行{name_zh}操作，处理完成后可以打包下载。")
    ]
    related = [
        ("/tutorials/image-compress.html", "图片压缩"),
        ("/tutorials/image-convert.html", "图片格式转换"),
        ("/tutorials/image-resize.html", "图片尺寸修改")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:8][:4] if slug else "img",
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_pdf_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "📄 PDF工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线PDF处理"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，处理PDF文档。支持批量操作，所有处理在浏览器本地完成。"
    func = f"ZenTools {name_zh}工具是一款专业的在线PDF处理工具，支持PDF文档的编辑、转换、压缩、加密等多种操作。所有处理均在浏览器本地完成，无需上传文件到服务器，确保文档安全。"
    tips = [
        "支持批量处理多个PDF文件，一次上传多个文件可以同时处理，大大提升工作效率。",
        "PDF处理完成后建议及时下载保存，刷新页面后本地缓存会被清除，确保处理结果不丢失。",
        "对于加密PDF文档，需要先输入密码解密后才能进行后续编辑和转换操作。"
    ]
    faqs = [
        ("支持哪些PDF功能？", "支持PDF合并、拆分、压缩、加密、解密、转图片、转Word、转文本、添加水印、删除页面、旋转页面、排序页面、OCR识别等全套PDF处理功能。"),
        ("有文件大小限制吗？", "单个PDF文件建议不超过 100MB，超大文件处理速度会较慢。对于数百页的PDF文档，建议分批处理。"),
        ("处理后的PDF格式会变化吗？", "处理后的PDF会保持原有的版式和内容，不会出现格式错乱。对于扫描版PDF，可能需要使用OCR功能提取文字。")
    ]
    related = [
        ("/tutorials/pdf-merge.html", "PDF合并"),
        ("/tutorials/pdf-split.html", "PDF拆分"),
        ("/tutorials/pdf-compress.html", "PDF压缩")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_ai_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🤖 AI工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线AI生成"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，利用AI快速生成内容。操作简单，即写即用。"
    func = f"ZenTools {name_zh}工具是一款智能AI辅助工具，通过先进的自然语言处理技术，帮助你快速生成高质量的内容。只需输入关键词或描述，AI就能为你生成专业级的文本内容。"
    tips = [
        "输入的关键词或描述越详细具体，AI生成的内容就越精准。建议包含主题、风格、长度等关键信息。",
        "可以尝试多次生成并对比不同版本的结果，选择最符合需求的版本进行微调。",
        "生成的内容建议人工审阅一遍，确保专业术语和特定信息准确无误后再使用。"
    ]
    faqs = [
        ("AI生成的内容可以商用吗？", "可以。所有AI生成的内容归你所有，可以用于商业用途，包括社交媒体、营销材料、博客文章等场景。"),
        ("支持中文输入吗？", "完全支持中文输入和输出。AI对中文的理解和生成能力出色，可以流畅地进行中文内容创作。"),
        ("生成速度有多快？", "通常在几秒内就能生成结果。对于复杂的任务或较长的内容，可能需要10-30秒。")
    ]
    related = [
        ("/tutorials/ai-writing.html", "AI写作"),
        ("/tutorials/ai-summary.html", "AI总结"),
        ("/tutorials/ai-translate.html", "AI翻译")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_text_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "📝 文本工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线文本处理"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理文本数据。支持大段文字处理。"
    func = f"ZenTools {name_zh}工具是一款实用的在线文本处理工具，帮助你对文本内容进行快速操作和转换。支持大段文字处理，操作简洁高效。"
    tips = [
        "支持大量文本输入，可以处理数万字以上的内容。对于超长文本，建议分段处理以确保准确性。",
        "处理结果可以直接复制，也可以清空后重新输入。建议将常用操作结果保存备用。",
        "文本处理不涉及任何网络请求，所有操作在浏览器本地完成，适合处理敏感内容。"
    ]
    faqs = [
        ("有文本长度限制吗？", "理论上没有长度限制，但超大的文本（如超过10万字）可能会影响处理速度。建议分段处理超长文本。"),
        ("可以批量处理多段文本吗？", f"可以。支持一次性输入多段文本进行{name_zh}操作，处理结果会保留原始分段格式。"),
        ("处理结果会保存吗？", "所有处理都在浏览器本地完成，关闭页面后数据会被清除。建议将处理结果及时复制保存。")
    ]
    related = [
        ("/tutorials/word-count.html", "字数统计"),
        ("/tutorials/case-convert.html", "大小写转换"),
        ("/tutorials/find-replace.html", "查找替换")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_dev_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "💻 开发工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线开发工具"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，提升开发效率。开发者必备。"
    func = f"ZenTools {name_zh}工具是一款专业的在线开发辅助工具，帮助开发者快速完成数据校验、格式化、调试等常见开发任务。所有操作在浏览器本地完成，保护代码和数据隐私。"
    tips = [
        "支持格式化、校验和语法高亮显示，让代码和数据结构一目了然。",
        "处理结果可以直接复制，适合快速集成到项目中。",
        "对于大型JSON文件（超过100KB），建议分段处理或在本地使用专业工具。"
    ]
    faqs = [
        ("支持哪些JSON格式？", "支持标准JSON格式，包括对象、数组、嵌套结构和各种数据类型。工具会校验JSON语法的正确性。"),
        ("可以格式化JSON吗？", "可以。工具提供格式化（美化）和压缩（最小化）两种模式，一键切换。"),
        ("有文件大小限制吗？", "建议在浏览器中使用不超过500KB的JSON文件，超大文件建议分片处理。")
    ]
    related = [
        ("/tutorials/json-formatter.html", "JSON格式化"),
        ("/tutorials/json-diff.html", "JSON对比"),
        ("/tutorials/regex-tester.html", "正则测试器")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_life_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🏠 生活工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线生活计算"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，轻松完成日常计算。简单实用。"
    func = f"ZenTools {name_zh}工具是一款实用的在线生活计算工具，帮助你在日常生活中快速完成各种计算任务。操作简单，结果准确。"
    tips = [
        "计算结果可以多次查看和复制，适合在不同场景下使用。",
        "所有计算在浏览器本地完成，无需联网即可使用。",
        "建议收藏常用计算结果，方便下次直接使用。"
    ]
    faqs = [
        ("计算结果准确吗？", "工具使用JavaScript高精度运算，计算结果可靠。对于金融相关的计算，建议以银行官方结果为准。"),
        ("支持中文吗？", "完全支持中文界面和中文输入。工具提供中文、英文、日文、越南文四种语言。"),
        ("可以离线使用吗？", "部分功能支持离线使用。所有计算在浏览器本地完成，无需网络连接。")
    ]
    related = [
        ("/tutorials/password-generator.html", "密码生成器"),
        ("/tutorials/unit-converter.html", "单位换算"),
        ("/tutorials/bmi-calculator.html", "BMI计算")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_finance_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "💰 金融工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线金融计算"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，轻松计算金融数据。财务规划必备。"
    func = f"ZenTools {name_zh}工具是一款专业的在线金融计算工具，帮助你在理财规划、贷款计算、投资收益等场景中快速获取准确的计算结果。所有计算在浏览器本地完成。"
    tips = [
        "计算结果仅供参考，实际金融产品的条款和利率可能有所不同，请以官方数据为准。",
        "建议在计算前仔细阅读说明，确保输入的参数符合你的实际情况。",
        "可以多次调整参数对比不同方案，选择最适合你的金融方案。"
    ]
    faqs = [
        ("计算结果准确吗？", "工具使用标准金融公式计算，结果可靠。但实际金融产品可能存在手续费、额外费用等未包含在计算中。"),
        ("支持多种方案对比吗？", "可以。通过调整参数（如利率、期限、首付比例等）可以模拟多种方案，对比不同选择。"),
        ("有投资风险提示吗？", "金融投资存在风险，工具仅提供计算参考，不构成投资建议。投资前请充分了解产品风险。")
    ]
    related = [
        ("/tutorials/currency.html", "汇率换算"),
        ("/tutorials/loan-calculator.html", "贷款计算器"),
        ("/tutorials/vat-calculator.html", "增值税计算")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_audio_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🎵 音频工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线音频处理"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理音频文件。支持多种格式。"
    func = f"ZenTools {name_zh}工具是一款专业的在线音频处理工具，支持 MP3、WAV、AAC、M4A 等主流音频格式。所有处理在浏览器本地完成，保护音频隐私。"
    tips = [
        "支持多种音频格式输入，处理后可以保存为常见格式。建议根据使用场景选择合适的输出格式。",
        "所有处理在浏览器本地完成，音频文件不会上传到服务器，保护你的音频数据隐私。",
        "处理后的音频建议及时保存，刷新页面后本地缓存会被清除。"
    ]
    faqs = [
        ("支持哪些音频格式？", "支持 MP3、WAV、AAC、M4A、FLAC、OGG 等主流音频格式。部分格式在处理后可能需要转换为其他格式。"),
        ("有文件大小限制吗？", "单个音频文件建议不超过 100MB。对于超长音频（如超过1小时的录音），建议分段处理。"),
        ("可以批量处理音频吗？", "部分功能支持批量上传多个音频文件进行处理。")
    ]
    related = [
        ("/tutorials/audio-merge.html", "音频合并"),
        ("/tutorials/audio-cutter.html", "音频裁剪"),
        ("/tutorials/tts.html", "文字转语音")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }

def make_seo_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🔍 SEO工具"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线SEO分析"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，优化网站SEO表现。SEO从业者必备。"
    func = f"ZenTools {name_zh}工具是一款专业的在线SEO分析工具，帮助你全面检查网站的SEO设置和优化机会。通过详细的数据分析，发现并解决影响搜索排名的因素。"
    tips = [
        "建议定期使用工具检查网站SEO状态，及时发现和解决新问题。",
        "SEO优化是一个长期过程，工具提供的建议需要持续跟踪和调整。",
        "将工具的检查结果与搜索引擎的官方指南结合使用，可以获得最佳优化效果。"
    ]
    faqs = [
        ("检查结果可靠吗？", "工具基于搜索引擎的官方指南和SEO最佳实践生成检查结果，具有参考价值。但最终优化效果需要结合实际情况。"),
        ("支持哪种类型的网站？", "支持任何基于HTML的网站，包括静态网站、博客、电商平台等。"),
        ("可以导出报告吗？", "部分功能支持导出检查报告，方便团队共享和记录优化进度。")
    ]
    related = [
        ("/tutorials/seo-keyword-research.html", "关键词研究"),
        ("/tutorials/seo-meta-generator.html", "Meta标签生成"),
        ("/tutorials/seo-robots-generator.html", "Robots.txt生成")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs, "related": related, "cat_label": cat_label
    }


# ===== Define all 40 missing tutorials =====
missing_slugs = [
    # AI工具
    'ai-social-copy', 'ai-summarize',
    # PDF工具
    'pdf-tools',
    # SEO工具
    'seo-title-checker',
    # 图片工具
    'image-convert', 'image-resize', 'image-watermark', 'image-to-base64',
    'image-filters', 'image-rotate', 'image-annotate', 'grid-split',
    'image-sharpen', 'image-mosaic',
    # 开发工具 (2 real, 5 have alternate names)
    'json-diff', 'json-viewer',
    'camera-test', 'keyboard-test', 'mic-test', 'mouse-test', 'screen-test',
    # 文本工具
    'word-count', 'case-convert', 'link-extract', 'sort-lines',
    'find-replace', 'reverse-text', 'url-encode',
    # 生活工具
    'password-generator', 'unit-converter', 'money-uppercase',
    # 金融工具
    'deposit-interest', 'stock-fee',
    # 音频工具
    'speech-to-text', 'voice-recorder', 'video-to-audio',
    'audio-speed', 'audio-reverse', 'volume-booster', 'audio-fade',
]

tutorials_to_generate = []

for slug in missing_slugs:
    tool = tools_map.get(slug)
    if not tool:
        print(f"  WARNING: slug '{slug}' not found in tools-data.json, skipping")
        continue

    name_zh = tool.get('name', slug)
    name_en = tool.get('name__en', slug)
    tool_url = tool.get('url', f"/{slug}.html")
    cat = tool.get('category', '')

    if cat == '图片工具' or cat == 'image':
        t = make_image_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == 'PDF工具' or cat == 'PDF':
        t = make_pdf_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == 'AI工具' or cat == 'AI':
        t = make_ai_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == '文本工具' or cat == 'text':
        t = make_text_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == '开发工具' or cat == 'dev':
        t = make_dev_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == '生活工具' or cat == 'life':
        t = make_life_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == '金融工具' or cat == 'finance':
        t = make_finance_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == '音频工具' or cat == 'audio':
        t = make_audio_tutorial(slug, name_zh, name_en, tool_url)
    elif cat == 'SEO工具' or cat == 'SEO':
        t = make_seo_tutorial(slug, name_zh, name_en, tool_url)
    else:
        t = make_text_tutorial(slug, name_zh, name_en, tool_url)

    tutorials_to_generate.append(t)

# ===== Generate tutorial HTML files =====
created = 0
for t in tutorials_to_generate:
    html = build_html(**t)
    filepath = os.path.join(BASE, f"{t['tool_id']}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {filepath} ({len(html)} chars)")
    created += 1

print(f"\n=== Done! Created {created} tutorial files. ===")