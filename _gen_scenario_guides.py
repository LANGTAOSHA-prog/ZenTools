#!/usr/bin/env python3
"""Generate 10 scenario collection guides for ZenTools."""
import json, os

BASE = "/workspace/guides"
TOOLS_DATA_PATH = "/workspace/data/tools-data.json"

with open(TOOLS_DATA_PATH) as f:
    tools_data = json.load(f)
tools_map = {}
for t in tools_data['tools']:
    slug = t.get('slug', '')
    tools_map[slug] = t

os.makedirs(BASE, exist_ok=True)


def get_tool_link(slug, label=None):
    """Get a tool's URL and a nice label."""
    tool = tools_map.get(slug)
    if not tool:
        return "", label or slug
    url = tool.get('url', '')
    return url, label or tool.get('name', slug)


def make_scenario_html(slug, title_zh, title_en, desc_zh, intro_zh,
                       sections, tools_list, related_tools, cat_emoji=""):
    """Build a scenario collection guide page."""

    zh = {
        "pageTitle": f"{title_zh} - ZenTools",
        "navHome": "首页", "navDev": "开发工具", "navAll": "全部工具",
        "navPrivacy": "隐私政策", "footerCopy": "© 2026 ZenTools. 免费在线工具箱。",
        "introTitle": "导语", "sceneTitle": "使用场景", "tipTitle": "实用建议",
        "faqTitle": "常见问题", "relTitle": "更多推荐工具：",
        "backToIndex": "返回指南中心",
    }
    zh["a1Intro"] = intro_zh

    en = dict(zh)
    en.update({
        "pageTitle": f"{title_en} - ZenTools",
        "navHome": "Home", "navDev": "Dev Tools", "navAll": "All Tools",
        "navPrivacy": "Privacy", "footerCopy": "© 2026 ZenTools. Free Online Toolbox.",
        "introTitle": "Introduction", "sceneTitle": "Use Cases", "tipTitle": "Tips",
        "faqTitle": "FAQ", "relTitle": "More Tools:",
        "backToIndex": "Back to Guides",
    })
    en["a1Intro"] = desc_zh

    ja = dict(zh)
    ja.update({
        "pageTitle": f"{title_zh} - ZenTools",
        "navHome": "ホーム", "navDev": "開発ツール", "navAll": "すべてのツール",
        "navPrivacy": "プライバシー", "footerCopy": "© 2026 ZenTools. 無料オンラインツールボックス。",
        "introTitle": "はじめに", "sceneTitle": "利用シーン", "tipTitle": "ヒント",
        "faqTitle": "よくある質問", "relTitle": "関連ツール：",
        "backToIndex": "ガイドに戻る",
    })

    vi = dict(zh)
    vi.update({
        "pageTitle": f"{title_zh} - ZenTools",
        "navHome": "Trang chủ", "navDev": "Công cụ Dev", "navAll": "Tất cả",
        "navPrivacy": "Quyền riêng tư", "footerCopy": "© 2026 ZenTools. Hộp công cụ trực tuyến miễn phí.",
        "introTitle": "Giới thiệu", "sceneTitle": "Ứng dụng", "tipTitle": "Mẹo",
        "faqTitle": "Câu hỏi thường gặp", "relTitle": "Công cụ khác:",
        "backToIndex": "Quay lại Hướng dẫn",
    })

    # Build sections HTML
    sections_html = ""
    for sec in sections:
        sec_title = sec.get("title", "")
        sec_body = sec.get("body", "")
        sec_tools = sec.get("tools", [])
        sections_html += f'<h2 data-i18n="sceneTitle">{sec_title}</h2>\n<p>{sec_body}</p>\n'
        for t_slug, t_label in sec_tools:
            t_url, _ = get_tool_link(t_slug)
            if t_url:
                sections_html += f'<div class="guide-card"><a href="{t_url}" target="_blank" class="guide-card-link"><strong>{t_label}</strong></a></div>\n'

    # Tips section
    tips_html = ""
    for tip in sections[-1].get("tips", []) if sections else []:
        tips_html += f'<div class="guide-tip">{tip}</div>\n'

    # Tools sidebar
    tools_html = ""
    for t_slug, t_label in tools_list:
        t_url, _ = get_tool_link(t_slug)
        if t_url:
            tools_html += f'<a href="{t_url}" target="_blank">{t_label}</a>\n'

    # Related tools
    related_html = ""
    for r_slug, r_label in related_tools:
        r_url, _ = get_tool_link(r_slug)
        if r_url:
            related_html += f'<a href="{r_url}" target="_blank">{r_label}</a>\n'

    i18n_json = json.dumps({"zh": zh, "en": en, "ja": ja, "vi": vi}, ensure_ascii=False)

    cat_label = f"{cat_emoji} 场景指南"

    # Generate FAQ
    faq_html = """
<div class="faq-item"><p><strong>这些工具需要注册吗？</strong><br/>不需要。所有工具均无需注册即可使用，完全免费。</p></div>
<div class="faq-item"><p><strong>数据安全吗？</strong><br/>所有文件处理均在浏览器本地完成，不会上传到服务器，数据完全安全。</p></div>
<div class="faq-item"><p><strong>支持哪些设备？</strong><br/>支持桌面浏览器和移动端浏览器。推荐使用 Chrome、Edge 或 Safari。</p></div>
<div class="faq-item"><p><strong>可以批量使用吗？</strong><br/>多数工具支持批量操作，可以一次处理多个文件，提高效率。</p></div>
"""

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">{title_zh} - ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="canonical" href="https://zentools.xyz/guides/{slug}.html"/>
<link rel="manifest" href="/manifest.json" />
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.guide-body {{ max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; }}
.guide-body h2 {{ font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }}
.guide-body p {{ font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:12px; }}
.guide-card {{ background:rgba(0,229,255,0.05); border:1px solid rgba(0,229,255,0.2); border-radius:10px; padding:14px 18px; margin:12px 0; }}
.guide-card-link {{ color:var(--cyan); text-decoration:none; font-weight:600; }}
.guide-card-link:hover {{ text-decoration:underline; }}
.guide-tip {{ background:rgba(0,229,255,0.04); border-left:3px solid var(--cyan); padding:10px 16px; border-radius:0 8px 8px 0; margin:10px 0; font-size:14px; color:var(--text); }}
.faq-item {{ margin:16px 0; padding:12px 16px; background:rgba(255,255,255,0.02); border-radius:8px; border:1px solid rgba(255,255,255,0.06); }}
.faq-item p {{ margin:0; }}
.tools-list {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0; }}
.tools-list a {{ background:rgba(0,229,255,0.1); color:var(--cyan); padding:6px 12px; border-radius:6px; text-decoration:none; font-size:13px; }}
.tools-list a:hover {{ background:rgba(0,229,255,0.2); }}
.page-guide {{ max-width:920px; margin:0 auto; padding:20px 16px 60px; }}
.page-guide .back-link {{ display:inline-flex; align-items:center; gap:6px; font-size:14px; color:var(--muted); margin-bottom:20px; }}
.page-guide .back-link:hover {{ color:var(--cyan); }}
.page-guide .page-eyebrow {{ font-size:12px; font-weight:700; color:var(--cyan); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; display:block; }}
.page-guide h1 {{ font-size:28px; font-weight:800; margin-bottom:8px; }}
.page-guide .meta {{ font-size:13px; color:var(--muted); display:flex; gap:16px; margin-bottom:24px; }}
</style>
<meta name="google-adsense-account" content="ca-pub-1955887568822472">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1955887568822472" crossorigin="anonymous"></script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Article","headline":"{title_zh}","description":"{desc_zh}","datePublished":"2026-07-01","author":{{"@type":"Organization","name":"ZenTools"}},"publisher":{{"@type":"Organization","name":"ZenTools"}}}}</script>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{{"@type":"Question","name":"这些工具需要注册吗？","acceptedAnswer":{{"@type":"Answer","text":"不需要。所有工具均无需注册即可使用，完全免费。"}}}},{{"@type":"Question","name":"数据安全吗？","acceptedAnswer":{{"@type":"Answer","text":"所有文件处理均在浏览器本地完成，不会上传到服务器，数据完全安全。"}}}},{{"@type":"Question","name":"支持哪些设备？","acceptedAnswer":{{"@type":"Answer","text":"支持桌面浏览器和移动端浏览器。推荐使用 Chrome、Edge 或 Safari。"}}}},{{"@type":"Question","name":"可以批量使用吗？","acceptedAnswer":{{"@type":"Answer","text":"多数工具支持批量操作，可以一次处理多个文件，提高效率。"}}}}]}}</script>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/tools.html" data-i18n="navAll">全部工具</a><select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-guide">
<a class="back-link" href="/tutorials/">← <span data-i18n="backToIndex">返回指南中心</span></a>
<span class="page-eyebrow" data-i18n="sceneTitle">{cat_label}</span>
<h1 data-i18n="a1Title">{title_zh}</h1>
<div class="meta"><span>📅 2026-07-01</span><span>⏱ 8 分钟阅读</span></div>

<div class="guide-body">
<h2 data-i18n="introTitle">导语</h2>
<p data-i18n="a1Intro">{intro_zh}</p>

{sections_html}

<h2 data-i18n="tipTitle">实用建议</h2>
{tips_html}

<h2 data-i18n="faqTitle">常见问题</h2>
{faq_html}

<div class="tools-list" style="margin-top:24px;">
<strong data-i18n="relTitle">本指南涉及工具：</strong>
{tools_html}
</div>

<div class="tools-list" style="margin-top:16px;">
<strong data-i18n="relTitle">更多推荐工具：</strong>
{related_html}
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


# ===== Define 10 scenario collection guides =====

scenarios = []

# 1. 出差日本必用工具
scenarios.append({
    "slug": "travel-japan-tools",
    "title_zh": "出差日本必用的 10 个在线工具",
    "title_en": "10 Essential Tools for Business Trips to Japan",
    "desc_zh": "出差日本必备在线工具清单：PDF 处理、图片压缩、AI 翻译、证件照制作等。所有工具无需注册，浏览器直接使用。",
    "cat_emoji": "✈️",
    "intro_zh": "出差日本前，你需要处理大量文件和资料。本指南精选了 10 个 ZenTools 工具，覆盖证件照制作、PDF 文件处理、图片格式转换、文字翻译、合同扫描等常见出差场景，全部免费且无需注册，在浏览器中即可使用。",
    "sections": [
        {
            "title": "一、证件与文档准备",
            "body": "出差前需要准备护照扫描件、签证材料、合同文件等。以下工具帮助你快速处理各类文档。",
            "tools": [
                ("pdf-compress", "PDF压缩工具：压缩护照、合同等PDF文件，方便邮件发送"),
                ("pdf-merge", "PDF合并工具：将多份材料合并为一个PDF，便于整理"),
                ("pdf-split", "PDF拆分工具：从大文件中提取特定页面"),
                ("pdf-converter", "PDF转图片工具：将PDF合同扫描成图片格式"),
            ]
        },
        {
            "title": "二、证件照与图片处理",
            "body": "签证申请和商务场合可能需要标准证件照，以下工具帮你快速制作和修改图片。",
            "tools": [
                ("id-photo", "证件照制作：快速生成标准尺寸证件照，支持多种规格"),
                ("image-resize", "图片尺寸修改：调整照片尺寸以符合签证要求"),
                ("image-compress", "图片压缩工具：压缩图片大小，节省存储空间"),
            ]
        },
        {
            "title": "三、语言与交流",
            "body": "在日本出差，语言沟通是重要环节。以下工具辅助你完成翻译和文字处理。",
            "tools": [
                ("ai-translate", "AI翻译工具：中文、英文、日文互译，准确自然"),
                ("ai-summarize", "AI文本总结：快速总结长篇日文文件或邮件要点"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "使用这些工具前，请确保网络稳定。所有工具均在浏览器本地运行，无需联网即可完成文件处理，适合在酒店或移动场景中使用。",
            "tools": [],
            "tips": [
                "提前在国内整理好所有文件，到达日本后再调整格式会更高效。",
                "建议将常用工具收藏到浏览器书签栏，到达目的地后可随时使用。",
                "证件照建议准备多种尺寸规格，以应对不同的申请要求。",
                "所有处理结果请及时下载保存，关闭页面后本地缓存会被清除。"
            ]
        }
    ],
    "tools_list": [
        ("pdf-compress", "PDF压缩"), ("pdf-merge", "PDF合并"), ("pdf-split", "PDF拆分"),
        ("pdf-converter", "PDF转图片"), ("id-photo", "证件照"), ("image-resize", "图片尺寸"),
        ("image-compress", "图片压缩"), ("ai-translate", "AI翻译"), ("ai-summarize", "AI总结")
    ],
    "related_tools": [
        ("pdf-tools", "PDF工具集"), ("image-tools", "图片工具集")
    ]
})

# 2. 学生党PDF处理合集
scenarios.append({
    "slug": "student-pdf-guide",
    "title_zh": "学生党 PDF 处理合集：论文、笔记、考试资料管理",
    "title_en": "Student PDF Guide: Managing Papers, Notes & Exam Materials",
    "desc_zh": "学生必备 PDF 处理指南：合并论文、压缩文献、OCR 识别扫描件、提取考试重点。ZenTools 全免费，支持批量操作。",
    "cat_emoji": "📚",
    "intro_zh": "大学生活中，PDF 文件无处不在——论文、课件、教材、文献、考试资料。本指南精选 9 个 ZenTools 工具，帮你高效管理所有 PDF 资料。无论是合并多篇论文、压缩大体积文献，还是从扫描件中提取文字，这里都能找到合适的工具。",
    "sections": [
        {
            "title": "一、论文与作业处理",
            "body": "写论文时需要合并不同部分的文档，或将多个附件整合为一个 PDF 提交。",
            "tools": [
                ("pdf-merge", "PDF合并：将论文各部分合并为一个文件"),
                ("pdf-split", "PDF拆分：从大文件中提取特定章节"),
                ("pdf-converter", "PDF转Word：将PDF论文转为可编辑的Word文档"),
            ]
        },
        {
            "title": "二、文献与资料管理",
            "body": "收集了大量文献后，需要压缩体积便于存储，或从扫描件中提取关键文字。",
            "tools": [
                ("pdf-compress", "PDF压缩：大幅压缩PDF文献体积，节省硬盘空间"),
                ("pdf-ocr", "PDF OCR：从扫描版PDF中提取文字，便于搜索和引用"),
                ("image-ocr", "图片OCR：从图片中提取文字，适用于纸质笔记扫描"),
            ]
        },
        {
            "title": "三、考试与复习工具",
            "body": "考试前需要整理重点资料，以下工具可以帮助你快速制作复习笔记。",
            "tools": [
                ("pdf-converter", "PDF转图片：将重点章节转成图片格式，方便手机复习"),
                ("text-diff", "文本对比：对比不同版本的笔记和答案"),
                ("word-count", "字数统计：快速统计论文和作业字数"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "学生党使用这些工具，可以显著提高学习效率。建议按场景将工具分组收藏。",
            "tools": [],
            "tips": [
                "建议按课程或论文项目分组保存 PDF 文件，配合合并工具管理。",
                "扫描版教材使用 OCR 功能提取文字后，可以用 Ctrl+F 搜索关键词。",
                "压缩后的 PDF 文件大小建议控制在 10MB 以内，便于邮件发送和云端同步。",
                "所有工具均支持批量操作，可以同时处理多份文献或作业。"
            ]
        }
    ],
    "tools_list": [
        ("pdf-merge", "PDF合并"), ("pdf-split", "PDF拆分"), ("pdf-compress", "PDF压缩"),
        ("pdf-converter", "PDF转换"), ("pdf-ocr", "PDF OCR"), ("image-ocr", "图片OCR"),
        ("text-diff", "文本对比"), ("word-count", "字数统计")
    ],
    "related_tools": [
        ("tutorials/pdf-merge.html", "PDF合并教程"), ("tutorials/pdf-compress.html", "PDF压缩教程")
    ]
})

# 3. 开发者效率工具清单
scenarios.append({
    "slug": "developer-efficiency-tools",
    "title_zh": "开发者效率工具清单：JSON、正则、代码调试必备",
    "title_en": "Developer Efficiency Toolkit: JSON, Regex & Code Debugging",
    "desc_zh": "开发者必备在线工具合集：JSON格式化、正则测试、时间戳转换、图片Base64编码等。无需安装，打开即用。",
    "cat_emoji": "💻",
    "intro_zh": "作为开发者，日常工作中需要频繁处理 JSON 数据、调试正则表达式、转换时间戳、编码图片资源。本指南精选 9 个 ZenTools 开发工具，覆盖 API 调试、数据格式化、文件编码等高频场景。所有工具在浏览器中直接运行，保护代码和 API 密钥安全。",
    "sections": [
        {
            "title": "一、数据格式化与调试",
            "body": "处理 API 响应和配置文件时，需要快速格式化和校验数据结构。",
            "tools": [
                ("json-formatter", "JSON格式化：美化或压缩 JSON 数据，支持语法高亮"),
                ("json-diff", "JSON对比：对比两个 JSON 文件，快速找出差异"),
                ("json-viewer", "JSON查看器：在线查看和编辑 JSON 文件"),
                ("regex-tester", "正则表达式测试：实时验证正则匹配结果"),
            ]
        },
        {
            "title": "二、编码与转换工具",
            "body": "开发中需要将图片转为 Base64、编码 URL 参数、或转换各种数据格式。",
            "tools": [
                ("image-to-base64", "图片转Base64：将图片编码为 Base64 字符串，嵌入 HTML/CSS"),
                ("url-encode", "URL编码工具：对 URL 参数进行编码和解码"),
                ("time-converter", "时间戳转换：Unix时间戳与可读时间互转"),
            ]
        },
        {
            "title": "三、文本与数据处理",
            "body": "处理日志、数据清洗、批量文本替换等场景。",
            "tools": [
                ("find-replace", "查找替换：批量替换文本中的内容"),
                ("sort-lines", "排序文本：按字母、数字或自定义规则排序"),
                ("case-convert", "大小写转换：批量转换文本大小写格式"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "开发者应将这些工具添加到浏览器收藏夹，形成日常开发工具箱。",
            "tools": [],
            "tips": [
                "处理敏感 JSON 数据（如包含 API Key）时，确保浏览器已关闭其他标签页。",
                "正则表达式测试工具支持 PCRE 和 JS 正则语法，可以切换模式。",
                "图片转 Base64 适合嵌入小图标，大图片建议使用 CDN 加载。",
                "URL 编码工具支持编码和解码两种模式，一键切换。"
            ]
        }
    ],
    "tools_list": [
        ("json-formatter", "JSON格式化"), ("json-diff", "JSON对比"), ("json-viewer", "JSON查看"),
        ("regex-tester", "正则测试"), ("image-to-base64", "图片转Base64"),
        ("url-encode", "URL编码"), ("time-converter", "时间戳转换"),
        ("find-replace", "查找替换"), ("sort-lines", "文本排序")
    ],
    "related_tools": [
        ("dev/", "全部开发工具"), ("tools/dev-tools.html", "开发工具集")
    ]
})

# 4. 自媒体内容创作工具集
scenarios.append({
    "slug": "content-creation-tools",
    "title_zh": "自媒体内容创作者必备的 10 个在线工具",
    "title_en": "10 Essential Tools for Content Creators",
    "desc_zh": "自媒体创作者全套工具：AI写作、AI总结、图片处理、视频剪辑、音频编辑、SEO优化。一站式解决方案。",
    "cat_emoji": "✍️",
    "intro_zh": "运营公众号、小红书、抖音、B站等平台，需要不断产出高质量内容。本指南精选 10 个 ZenTools 工具，覆盖文案创作、图片设计、视频剪辑、音频编辑、SEO 优化等全流程。每个工具都可在浏览器中直接使用，无需下载软件。",
    "sections": [
        {
            "title": "一、文案创作与编辑",
            "body": "优质内容是自媒体成功的核心。以下 AI 工具帮助你快速生成高质量文案。",
            "tools": [
                ("ai-writing", "AI写作助手：生成公众号、小红书、抖音文案"),
                ("ai-summarize", "AI文本总结：提炼长文要点，快速生成摘要",),
                ("ai-social-copy", "AI社交媒体文案：一键生成小红书、微博、朋友圈文案"),
                ("word-count", "字数统计：检查文案长度是否符合平台要求"),
            ]
        },
        {
            "title": "二、图片与视觉素材",
            "body": "好看的封面和配图是吸引流量的关键。以下工具帮你制作和编辑图片。",
            "tools": [
                ("image-compress", "图片压缩：压缩图片大小，加快网页加载速度"),
                ("image-resize", "图片尺寸修改：快速调整封面尺寸，适配不同平台"),
                ("image-watermark", "图片水印：添加品牌水印，保护原创内容"),
                ("image-convert", "图片格式转换：将 PSD、AI 转为 JPG、PNG、WebP"),
            ]
        },
        {
            "title": "三、视频与音频",
            "body": "短视频和播客越来越重要，以下工具帮助你快速剪辑和处理音视频。",
            "tools": [
                ("compress-video", "视频压缩：压缩视频大小，方便上传和分享"),
                ("audio-cutter", "音频裁剪：裁剪音频，提取精彩片段"),
            ]
        },
        {
            "title": "四、SEO与数据分析",
            "body": "优化内容可见度，提高搜索排名和曝光率。",
            "tools": [
                ("seo-meta-generator", "Meta标签生成：生成 SEO 友好的标题和描述"),
                ("seo-keyword-research", "关键词研究：分析热门关键词，优化内容标题"),
            ]
        },
        {
            "title": "五、实用建议",
            "body": "建议按内容类型将工具分组收藏，形成高效的工作流程。",
            "tools": [],
            "tips": [
                "AI 生成的文案建议人工审阅，确保符合平台规范和品牌调性。",
                "图片压缩建议在保持清晰度的前提下尽量压缩，加快网页加载速度。",
                "视频压缩选择 1080p 输出即可，既保证画质又控制文件大小。",
                "SEO 优化是一个持续过程，建议每周用关键词研究工具检查趋势。"
            ]
        }
    ],
    "tools_list": [
        ("ai-writing", "AI写作"), ("ai-summarize", "AI总结"), ("ai-social-copy", "AI文案"),
        ("word-count", "字数统计"), ("image-compress", "图片压缩"), ("image-resize", "图片尺寸"),
        ("image-watermark", "图片水印"), ("image-convert", "图片转换"),
        ("compress-video", "视频压缩"), ("audio-cutter", "音频裁剪"),
        ("seo-meta-generator", "Meta生成"), ("seo-keyword-research", "关键词研究")
    ],
    "related_tools": [
        ("ai/", "AI工具"), ("image/", "图片工具"), ("seo/", "SEO工具")
    ]
})

# 5. 图片编辑与工作流
scenarios.append({
    "slug": "image-editing-workflow",
    "title_zh": "图片编辑完整工作流：从拍摄到发布",
    "title_en": "Complete Image Editing Workflow: From Capture to Publish",
    "desc_zh": "从拍照到发布的完整图片编辑流程：裁剪、调色、压缩、添加水印、转换格式。10 个工具覆盖全部环节。",
    "cat_emoji": "🖼️",
    "intro_zh": "一张高质量图片从拍摄到发布，需要经过裁剪、调色、压缩、水印、格式转换等多个环节。本指南将这 10 个步骤拆解为清晰的工作流，每一步都有对应的 ZenTools 工具，全部在浏览器中完成，无需安装专业软件。",
    "sections": [
        {
            "title": "一、基础调整",
            "body": "拍摄后的图片通常需要先进行尺寸裁剪和旋转调整。",
            "tools": [
                ("image-resize", "图片尺寸修改：调整图片宽高，适配不同平台要求"),
                ("image-rotate", "图片旋转：顺时针/逆时针旋转图片"),
                ("grid-split", "网格分割：将大图分割为多张小图，适合瀑布流展示"),
            ]
        },
        {
            "title": "二、美化与增强",
            "body": "通过滤镜和锐化让图片更加清晰好看。",
            "tools": [
                ("image-filters", "图片滤镜：应用黑白、复古、高饱和等多种滤镜效果"),
                ("image-sharpen", "图片锐化：增强图片边缘清晰度"),
                ("image-annotate", "图片标注：在图片上添加文字、箭头、标注框"),
            ]
        },
        {
            "title": "三、品牌化处理",
            "body": "添加水印和统一风格，建立品牌视觉识别。",
            "tools": [
                ("image-watermark", "图片水印：添加文字或图片水印，保护版权"),
                ("image-mosaic", "图片马赛克：对敏感区域进行马赛克处理"),
            ]
        },
        {
            "title": "四、输出与发布",
            "body": "压缩和转换格式，适配不同发布渠道。",
            "tools": [
                ("image-compress", "图片压缩：大幅压缩图片体积，保持清晰度"),
                ("image-convert", "图片格式转换：JPG/PNG/WebP 互转，WebP 体积更小"),
                ("image-to-base64", "图片转Base64：将图片编码为字符串，嵌入网页代码"),
            ]
        },
        {
            "title": "五、实用建议",
            "body": "建立标准化的图片处理流程，每次按统一标准处理。",
            "tools": [],
            "tips": [
                "建议先裁剪再压缩，避免对无用区域进行无效压缩。",
                "滤镜和锐化操作建议适度使用，过度处理会降低图片质量。",
                "水印建议放在图片角落，透明度调至 30-50%，不影响主体内容。",
                "发布到社交媒体时优先使用 WebP 格式，体积比 JPG 小 25-35%。"
            ]
        }
    ],
    "tools_list": [
        ("image-resize", "尺寸修改"), ("image-rotate", "旋转"), ("grid-split", "网格分割"),
        ("image-filters", "滤镜"), ("image-sharpen", "锐化"), ("image-annotate", "标注"),
        ("image-watermark", "水印"), ("image-mosaic", "马赛克"),
        ("image-compress", "压缩"), ("image-convert", "格式转换"), ("image-to-base64", "Base64")
    ],
    "related_tools": [
        ("image/", "图片工具"), ("tutorials/image-compress.html", "图片压缩教程")
    ]
})

# 6. 视频剪辑入门工具
scenarios.append({
    "slug": "video-editing-beginners",
    "title_zh": "视频剪辑入门：5 个浏览器工具快速上手",
    "title_en": "Beginner Video Editing: 5 Browser-Based Tools to Get Started",
    "desc_zh": "无需下载 Premiere 或剪映，浏览器即可剪辑视频：裁剪、压缩、提取音频、转换格式。适合新手快速入门。",
    "cat_emoji": "🎬",
    "intro_zh": "对于初学者，安装和配置专业视频剪辑软件门槛较高。本指南推荐的 5 个 ZenTools 视频工具全部在浏览器中运行，无需安装，打开即用。适合快速剪辑短视频、提取背景音乐、压缩视频大小等日常需求。",
    "sections": [
        {
            "title": "一、视频基础处理",
            "body": "裁剪和压缩是最常用的视频处理操作，以下工具帮你快速完成。",
            "tools": [
                ("video-trimmer", "视频裁剪：裁剪视频片段，去除不需要的部分"),
                ("compress-video", "视频压缩：大幅压缩视频体积，方便分享和存储"),
            ]
        },
        {
            "title": "二、音视频提取与转换",
            "body": "从视频中提取音频，或将视频转为不同格式，以下工具轻松完成。",
            "tools": [
                ("video-to-audio", "视频转音频：提取视频中的音频轨道，保存为 MP3 等格式"),
                ("video-converter", "视频格式转换：MP4、MOV、AVI、MKV 等格式互转"),
            ]
        },
        {
            "title": "三、音频辅助处理",
            "body": "对提取的音频进行进一步编辑和处理。",
            "tools": [
                ("audio-speed", "音频变速：调整音频播放速度，适用于短视频配音"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "浏览器工具适合轻量级视频处理，大项目建议还是使用专业软件。",
            "tools": [],
            "tips": [
                "视频裁剪时建议先预览确认裁剪位置，避免反复操作浪费时间。",
                "压缩视频时注意平衡画质和文件大小，1080p 是大多数场景的最佳选择。",
                "提取音频时选择高质量输出格式，避免多次转码造成音质损失。",
                "所有处理均在浏览器本地完成，大文件处理可能需要较长时间，请耐心等待。"
            ]
        }
    ],
    "tools_list": [
        ("video-trimmer", "视频裁剪"), ("compress-video", "视频压缩"),
        ("video-to-audio", "视频转音频"), ("video-converter", "视频转换"),
        ("audio-speed", "音频变速")
    ],
    "related_tools": [
        ("video/", "视频工具"), ("audio/", "音频工具")
    ]
})

# 7. 音频内容创作工具
scenarios.append({
    "slug": "audio-content-creation",
    "title_zh": "音频内容创作工具集：录制、编辑、转换全搞定",
    "title_en": "Audio Content Creation Toolkit: Record, Edit & Convert",
    "desc_zh": "从录制到发布的音频创作全套工具：录音、裁剪、变速、反转、音量调节、淡入淡出。打造你的播客或有声内容。",
    "cat_emoji": "🎙️",
    "intro_zh": "播客、有声读物、短视频配音——音频内容创作越来越受欢迎。本指南精选 8 个 ZenTools 音频工具，覆盖从录音到发布的全流程。所有操作在浏览器本地完成，保护录音隐私，无需上传到任何服务器。",
    "sections": [
        {
            "title": "一、录音与采集",
            "body": "开始创作前，你需要录制原始音频。以下工具帮你完成录制。",
            "tools": [
                ("voice-recorder", "在线录音：浏览器直接录音，支持暂停和重录"),
                ("speech-to-text", "语音转文字：将录音内容转为文字稿，方便整理和编辑"),
            ]
        },
        {
            "title": "二、音频编辑",
            "body": "录制完成后，需要对音频进行裁剪、变速、音量调节等编辑操作。",
            "tools": [
                ("audio-cutter", "音频裁剪：裁剪音频片段，去除多余部分"),
                ("audio-speed", "音频变速：调整播放速度，加快或放慢节奏"),
                ("audio-reverse", "音频反转：将音频倒放，适用于创意音效制作"),
                ("volume-booster", "音量增强：提高音量，让声音更清晰"),
            ]
        },
        {
            "title": "三、效果与输出",
            "body": "添加淡入淡出效果，转换音频格式，完成最终输出。",
            "tools": [
                ("audio-fade", "音频淡入淡出：为音频开头和结尾添加平滑过渡效果"),
                ("audio-converter", "音频格式转换：MP3、WAV、AAC、M4A 等格式互转"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "音频创作的质量很大程度上取决于原始录音的质量。",
            "tools": [],
            "tips": [
                "录音时选择安静的环境，使用外接麦克风能获得更好的音质。",
                "裁剪音频时建议保留少量边缘空白，避免切到有效内容。",
                "变速操作建议控制在 0.8x 到 1.2x 之间，超出范围会明显影响听感。",
                "最终发布建议使用 MP3 格式，兼容性最好，文件大小适中。"
            ]
        }
    ],
    "tools_list": [
        ("voice-recorder", "录音"), ("speech-to-text", "语音转文字"),
        ("audio-cutter", "音频裁剪"), ("audio-speed", "音频变速"),
        ("audio-reverse", "音频反转"), ("volume-booster", "音量增强"),
        ("audio-fade", "淡入淡出"), ("audio-converter", "格式转换")
    ],
    "related_tools": [
        ("audio/", "音频工具"), ("tutorials/audio-merge.html", "音频合并教程")
    ]
})

# 8. 财务计算与生活工具
scenarios.append({
    "slug": "finance-life-tools",
    "title_zh": "财务计算与生活工具：房贷、理财、日常计算一站搞定",
    "title_en": "Finance & Life Tools: Mortgage, Investment & Daily Calculations",
    "desc_zh": "房贷计算器、存款利息、股票手续费、单位换算、密码生成器……常用生活计算工具合集，无需下载APP。",
    "cat_emoji": "💰",
    "intro_zh": "生活中涉及大量计算——房贷月供、存款利息、股票手续费、水电费、密码生成。本指南精选 8 个 ZenTools 计算工具，覆盖财务规划和日常生活的各种计算场景。所有计算在浏览器本地完成，结果即时显示，无需联网。",
    "sections": [
        {
            "title": "一、房贷与贷款",
            "body": "买房是人生大事，准确计算月供和利息至关重要。",
            "tools": [
                ("loan-calculator", "贷款计算器：计算等额本息和等额本金的月供与总利息"),
                ("deposit-interest", "存款利息计算：计算定期存款、活期存款的利息收益"),
            ]
        },
        {
            "title": "二、投资理财",
            "body": "投资前需要计算预期收益和交易成本，以下工具提供准确参考。",
            "tools": [
                ("stock-fee", "股票手续费计算：计算买入和卖出股票的综合费用"),
                ("vat-calculator", "增值税计算器：计算含税价和不含税价"),
            ]
        },
        {
            "title": "三、生活实用计算",
            "body": "日常生活中的各种换算和计算需求。",
            "tools": [
                ("currency", "汇率换算：实时查询主流货币汇率，快速换算"),
                ("unit-converter", "单位换算：长度、重量、温度、面积等常见单位互转"),
                ("password-generator", "密码生成器：生成安全随机密码，保护账户安全"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "财务计算工具提供准确的公式计算结果，实际产品以银行和券商官方数据为准。",
            "tools": [],
            "tips": [
                "房贷计算器建议使用等额本息和等额本金两种模式分别计算，对比差异后选择。",
                "股票手续费计算仅包含佣金、印花税和过户费，实际可能还有印花税等隐性费用。",
                "密码生成器建议生成 12 位以上密码，包含大小写字母、数字和符号。",
                "汇率换算建议使用当天的实时汇率，工具数据可能存在短暂延迟。"
            ]
        }
    ],
    "tools_list": [
        ("loan-calculator", "贷款计算"), ("deposit-interest", "存款利息"),
        ("stock-fee", "股票手续费"), ("vat-calculator", "增值税"),
        ("currency", "汇率换算"), ("unit-converter", "单位换算"),
        ("password-generator", "密码生成")
    ],
    "related_tools": [
        ("finance/", "金融工具"), ("life/", "生活工具")
    ]
})

# 9. 网站 SEO 优化完整指南
scenarios.append({
    "slug": "seo-optimization-guide",
    "title_zh": "网站 SEO 优化完整指南：Meta、关键词、结构化数据",
    "title_en": "Complete Website SEO Guide: Meta, Keywords & Structured Data",
    "desc_zh": "SEO 优化全套工具：Meta 标签生成、关键词研究、Robots.txt 生成、网站分析。提升网站搜索排名。",
    "cat_emoji": "🔍",
    "intro_zh": "SEO 优化是一个系统工程，涉及 Meta 标签、关键词布局、结构化数据、robots.txt 等多个环节。本指南精选 5 个 ZenTools SEO 工具，按照优化优先级排列，帮你一步步提升网站的搜索可见度。所有工具均提供详细的操作说明和 SEO 最佳实践建议。",
    "sections": [
        {
            "title": "一、Meta 标签优化",
            "body": "Meta 标签是搜索引擎爬虫了解页面内容的第一入口，必须正确配置。",
            "tools": [
                ("seo-meta-generator", "Meta标签生成：生成 SEO 友好的 title、description、keywords 标签"),
                ("seo-title-checker", "标题检查工具：检查 Meta 标题长度和关键词密度，优化点击率"),
            ]
        },
        {
            "title": "二、关键词研究与布局",
            "body": "找到正确的关键词是 SEO 成功的前提，以下工具帮助你进行关键词研究和布局优化。",
            "tools": [
                ("seo-keyword-research", "关键词研究：分析搜索量、竞争度和关键词趋势"),
                ("ai-keyword-generator", "AI关键词生成：基于主题自动生成相关关键词列表"),
            ]
        },
        {
            "title": "三、网站技术 SEO",
            "body": "结构化数据和 robots.txt 是技术 SEO 的重要组成部分。",
            "tools": [
                ("seo-robots-generator", "Robots.txt生成：生成正确的 robots.txt 文件，控制爬虫行为"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "SEO 优化是一个长期过程，需要持续监控和调整。",
            "tools": [],
            "tips": [
                "Meta 标题建议控制在 50-60 个字符，description 控制在 150-160 个字符。",
                "关键词布局建议遵循 1-3-5 原则：1 个主关键词，3-5 个次要关键词。",
                "结构化数据（JSON-LD）可以显著提升搜索结果展示效果，建议每个重要页面都配置。",
                "SEO 效果通常需要 2-6 个月才能显现，建议按月跟踪数据，持续优化。"
            ]
        }
    ],
    "tools_list": [
        ("seo-meta-generator", "Meta生成"), ("seo-title-checker", "标题检查"),
        ("seo-keyword-research", "关键词研究"), ("ai-keyword-generator", "AI关键词"),
        ("seo-robots-generator", "Robots.txt生成")
    ],
    "related_tools": [
        ("seo/", "SEO工具"), ("ai/", "AI工具")
    ]
})

# 10. 在线教学与演示工具
scenarios.append({
    "slug": "online-teaching-tools",
    "title_zh": "在线教学与演示工具集：课件、录课、直播必备",
    "title_en": "Online Teaching Toolkit: Lesson Plans, Recording & Live Streaming",
    "desc_zh": "在线教师必备工具：图片编辑制作课件、视频录制与剪辑、音频处理、文档转换。打造专业在线课程。",
    "cat_emoji": "👨‍🏫",
    "intro_zh": "无论是制作课件、录制课程视频，还是准备教学文档，在线教师都需要一套高效的工具链。本指南精选 9 个 ZenTools 工具，覆盖从课件设计到课程发布的完整教学流程。所有工具在浏览器中直接运行，无需安装专业软件。",
    "sections": [
        {
            "title": "一、课件制作",
            "body": "制作课件需要大量的图片处理和文档编辑，以下工具帮助你快速完成。",
            "tools": [
                ("image-annotate", "图片标注：在课件图片上添加标注和说明"),
                ("image-resize", "图片尺寸修改：统一课件图片尺寸，保持版面整洁"),
                ("image-convert", "图片格式转换：将课件素材转为统一的图片格式"),
                ("pdf-merge", "PDF合并：将多份教学材料合并为一个课件"),
            ]
        },
        {
            "title": "二、课程录制",
            "body": "录制在线课程需要高质量的音视频，以下工具帮助你完成录制和编辑。",
            "tools": [
                ("voice-recorder", "在线录音：录制课程音频，支持暂停和重录"),
                ("video-trimmer", "视频裁剪：剪辑录制的课程视频，去除错误片段"),
                ("audio-fade", "音频淡入淡出：为课程开头和结尾添加平滑过渡"),
            ]
        },
        {
            "title": "三、文档与资料",
            "body": "教学过程中需要处理和分享大量文档，以下工具简化文档管理工作。",
            "tools": [
                ("pdf-compress", "PDF压缩：压缩教学文档体积，方便学生下载"),
                ("word-count", "字数统计：检查作业和试卷字数要求"),
            ]
        },
        {
            "title": "四、实用建议",
            "body": "在线教学质量很大程度上取决于课件和录制的专业性。",
            "tools": [],
            "tips": [
                "课件图片建议统一分辨率（如 1920x1080），确保在不同设备上显示效果一致。",
                "录制课程时使用外接麦克风和摄像头，音质和画质的提升非常明显。",
                "视频裁剪建议分多次小段裁剪，避免一次裁剪过大的文件。",
                "课程文档建议提供 PDF 和 Word 两种格式，方便不同需求的老师。"
            ]
        }
    ],
    "tools_list": [
        ("image-annotate", "图片标注"), ("image-resize", "图片尺寸"), ("image-convert", "图片转换"),
        ("pdf-merge", "PDF合并"), ("voice-recorder", "录音"), ("video-trimmer", "视频裁剪"),
        ("audio-fade", "淡入淡出"), ("pdf-compress", "PDF压缩"), ("word-count", "字数统计")
    ],
    "related_tools": [
        ("image/", "图片工具"), ("video/", "视频工具"), ("pdf/", "PDF工具")
    ]
})


# ===== Generate scenario HTML files =====
created = 0
for s in scenarios:
    html = make_scenario_html(**s)
    filepath = os.path.join(BASE, f"{s['slug']}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {filepath} ({len(html)} chars)")
    created += 1

print(f"\n=== Done! Created {created} scenario collection guides. ===")
