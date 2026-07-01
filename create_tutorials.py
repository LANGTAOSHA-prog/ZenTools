#!/usr/bin/env python3
"""批量生成AI工具教程HTML页面"""

import os

# 工具配置
tools = [
    {
        "name": "ai-paraphrase",
        "title": "AI改写教程：智能改写和润色文本",
        "description": "使用AI改写和润色文本内容，保持原意的同时提升表达质量",
        "svg": "/guides/img/ai-paraphrase-step1.svg",
        "related": [
            ("/tutorials/ai-polish.html", "AI润色教程"),
            ("/tutorials/ai-translate.html", "AI翻译教程"),
            ("/tutorials/ai-writing.html", "AI写作教程")
        ],
        "reading_time": "3 分钟阅读",
        "intro": "学会使用 ZenTools AI 改写工具，智能改写和润色文本内容，保持原意的同时提升表达质量，支持同义改写、扩写、缩写和风格转换。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-paraphrase.html\" target=\"blank\">AI 改写工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件，文件不会上传到服务器。",
        "step2_title": "输入文本",
        "step2_body": "在输入框中粘贴或输入需要改写的原始文本，工具会自动分析文本内容。",
        "step3_title": "选择改写模式",
        "step3_body": "根据需求选择改写模式：同义改写、扩写、缩写或风格转换，工具会实时显示预览效果。",
        "step4_title": "获取结果",
        "step4_body": "改写完成后，可以复制改写结果或下载保存，所有处理在浏览器本地完成。",
        "tip1": "改写前可以先尝试不同的改写模式，找到最适合的效果。",
        "tip2": "保持原文的核心意思不变，改写主要优化表达方式。",
        "tip3": "所有操作在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持多大的文本？",
        "faq1_a": "取决于浏览器内存，通常 10000 字以内都可以处理。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "文本会上传吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成。"
    },
    {
        "name": "ai-poem",
        "title": "AI诗歌生成教程：用AI创作诗歌",
        "description": "使用AI生成各类风格的诗歌，支持古典诗词、现代诗和外语诗歌",
        "svg": "/guides/img/ai-poem-step1.svg",
        "related": [
            ("/tutorials/ai-story.html", "AI故事生成教程"),
            ("/tutorials/ai-writing.html", "AI写作教程"),
            ("/tutorials/ai-novel-generator.html", "AI小说生成教程")
        ],
        "reading_time": "2 分钟阅读",
        "intro": "学会使用 ZenTools AI 诗歌生成工具，用AI创作各类风格的诗歌，支持古典诗词、现代诗和外语诗歌，让创意无限延伸。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-poem.html\" target=\"blank\">AI 诗歌生成工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。",
        "step2_title": "选择风格",
        "step2_body": "选择诗歌风格：古典诗词、现代诗、外语诗歌或自由创作，输入诗歌主题。",
        "step3_title": "生成诗歌",
        "step3_body": "点击「生成诗歌」按钮，AI会根据选择的风格和主题自动生成诗歌内容。",
        "step4_title": "获取结果",
        "step4_body": "生成完成后，可以复制诗歌内容或下载保存，支持多种导出格式。",
        "tip1": "可以尝试不同的风格组合，发现更多创意可能。",
        "tip2": "主题描述越具体，生成的诗歌越符合预期。",
        "tip3": "所有处理在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持哪些诗歌风格？",
        "faq1_a": "支持古典诗词（五言、七言、词）、现代诗、外语诗歌和自由创作。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "生成内容会保存吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成，刷新页面后内容会消失。"
    },
    {
        "name": "ai-polish",
        "title": "AI润色教程：优化文本表达和语法",
        "description": "使用AI优化文本的语法、用词和表达方式，提升文章的可读性和专业性",
        "svg": "/guides/img/ai-polish-step1.svg",
        "related": [
            ("/tutorials/ai-paraphrase.html", "AI改写教程"),
            ("/tutorials/ai-writing.html", "AI写作教程"),
            ("/tutorials/ai-japanese-essay.html", "AI日语作文教程")
        ],
        "reading_time": "3 分钟阅读",
        "intro": "学会使用 ZenTools AI 润色工具，优化文本的语法、用词和表达方式，提升文章的可读性和专业性，让文字更加流畅优美。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-polish.html\" target=\"blank\">AI 润色工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。",
        "step2_title": "输入文本",
        "step2_body": "在输入框中粘贴或输入需要润色的文本内容，工具会自动分析文本质量。",
        "step3_title": "选择润色模式",
        "step3_body": "选择润色模式：语法优化、用词润色、表达提升或专业性增强，工具会实时显示预览效果。",
        "step4_title": "获取结果",
        "step4_body": "润色完成后，可以对比原文和润色结果，复制或下载保存。",
        "tip1": "可以先尝试语法优化，再进行用词润色，分步提升文本质量。",
        "tip2": "保留原文的核心意思，润色主要优化表达方式。",
        "tip3": "所有操作在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持多大的文本？",
        "faq1_a": "取决于浏览器内存，通常 10000 字以内都可以处理。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "文本会上传吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成。"
    },
    {
        "name": "ai-product-desc",
        "title": "AI产品描述教程：生成吸引人的产品描述",
        "description": "使用AI生成电商产品描述、商品文案和卖点提炼",
        "svg": "/guides/img/ai-product-desc-step1.svg",
        "related": [
            ("/tutorials/ai-ad-copy.html", "AI广告文案教程"),
            ("/tutorials/ai-copywriting.html", "AI文案写作教程"),
            ("/tutorials/ai-social.html", "AI社交媒体教程")
        ],
        "reading_time": "2 分钟阅读",
        "intro": "学会使用 ZenTools AI 产品描述工具，生成电商产品描述、商品文案和卖点提炼，提升产品吸引力和转化率。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-product-desc.html\" target=\"blank\">AI 产品描述工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。",
        "step2_title": "输入产品信息",
        "step2_body": "输入产品名称、类别和主要特点，工具会自动分析产品特性。",
        "step3_title": "选择描述风格",
        "step3_body": "选择描述风格：电商描述、商品文案、卖点提炼或营销文案，工具会实时生成预览。",
        "step4_title": "获取结果",
        "step4_body": "生成完成后，可以复制产品描述或下载保存，支持多种导出格式。",
        "tip1": "输入的产品特点越详细，生成的描述越精准。",
        "tip2": "可以尝试不同风格，找到最适合产品的描述方式。",
        "tip3": "所有处理在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持哪些产品类型？",
        "faq1_a": "支持各类电商产品，包括电子产品、服装、食品、家居用品等。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "生成内容会保存吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成，刷新页面后内容会消失。"
    },
    {
        "name": "ai-prompt-generator",
        "title": "AI提示词生成教程：创建高效AI提示词",
        "description": "使用AI生成高质量的提示词模板，优化AI工具的输出效果",
        "svg": "/guides/img/ai-prompt-generator-step1.svg",
        "related": [
            ("/tutorials/ai-image-prompt.html", "AI图像提示词教程"),
            ("/tutorials/ai-qa.html", "AI问答教程"),
            ("/tutorials/ai-seo-article.html", "AI SEO文章教程")
        ],
        "reading_time": "2 分钟阅读",
        "intro": "学会使用 ZenTools AI 提示词生成工具，创建高质量的提示词模板，优化AI工具的输出效果，提升工作效率。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-prompt-generator.html\" target=\"blank\">AI 提示词生成工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。",
        "step2_title": "选择任务类型",
        "step2_body": "选择任务类型：文本生成、图像生成、代码生成或数据分析，输入任务描述。",
        "step3_title": "生成提示词",
        "step3_body": "点击「生成提示词」按钮，AI会根据任务类型和描述自动生成优化后的提示词模板。",
        "step4_title": "获取结果",
        "step4_body": "生成完成后，可以复制提示词或下载保存，直接用于其他AI工具。",
        "tip1": "任务描述越具体，生成的提示词效果越好。",
        "tip2": "可以尝试不同的任务类型，发现更多应用场景。",
        "tip3": "所有处理在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持哪些任务类型？",
        "faq1_a": "支持文本生成、图像生成、代码生成、数据分析等多种任务类型。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "生成内容会保存吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成，刷新页面后内容会消失。"
    },
    {
        "name": "ai-qa",
        "title": "AI问答教程：智能问答和知识检索",
        "description": "使用AI进行智能问答，回答各类知识问题，支持多轮对话和上下文理解",
        "svg": "/guides/img/ai-qa-step1.svg",
        "related": [
            ("/tutorials/ai-chat.html", "AI聊天教程"),
            ("/tutorials/ai-knowledge-base.html", "AI知识库教程"),
            ("/tutorials/ai-summarize.html", "AI总结教程")
        ],
        "reading_time": "3 分钟阅读",
        "intro": "学会使用 ZenTools AI 问答工具，进行智能问答和知识检索，回答各类知识问题，支持多轮对话和上下文理解。",
        "step1_title": "打开工具",
        "step1_body": "访问 <a href=\"/ai/ai-qa.html\" target=\"blank\">AI 问答工具</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需安装任何软件。",
        "step2_title": "输入问题",
        "step2_body": "在输入框中输入需要回答的问题，工具会自动分析问题内容。",
        "step3_title": "获取答案",
        "step3_body": "AI会根据问题内容生成详细准确的答案，支持多轮对话和上下文理解。",
        "step4_title": "继续对话",
        "step4_body": "可以根据答案继续提问，进行深入的对话和知识探索。",
        "tip1": "问题描述越具体，获得的答案越准确。",
        "tip2": "支持多轮对话，可以深入探讨感兴趣的话题。",
        "tip3": "所有处理在浏览器本地完成，文件不会上传到服务器。",
        "faq1_q": "支持哪些类型的问题？",
        "faq1_a": "支持知识问答、技术问题、生活常识、学术研究等多种类型。",
        "faq2_q": "需要注册吗？",
        "faq2_a": "不需要。完全免费，无需注册。",
        "faq3_q": "对话记录会保存吗？",
        "faq3_a": "不会。所有处理在浏览器本地完成，刷新页面后对话会消失。"
    }
]

def generate_html(tool):
    # 生成相关工具链接
    related_links = " · ".join([f'<a href="{url}">{name}</a>' for url, name in tool["related"]])
    
    # 构建HTML内容
    html = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title data-i18n="pageTitle">%s - ZenTools</title>
<meta name="description" content="%s"/>
<link rel="canonical" href="https://zentools.xyz/tutorials/%s.html"/>
<link rel="manifest" href="/manifest.json" />
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
.article-body { max-width:860px; margin:0 auto; padding:20px 28px; background:rgba(255,255,255,0.02); border:1px solid var(--border); border-radius:16px; }
.article-body h2 { font-size:20px; font-weight:700; color:var(--text); margin:32px 0 12px; }
.article-body h3 { font-size:16px; font-weight:600; color:var(--cyan); margin:24px 0 8px; }
.article-body p, .article-body li { font-size:14px; color:var(--muted); line-height:1.8; margin-bottom:10px; }
.article-body .tip { background:rgba(0,229,255,0.06); border-left:3px solid var(--cyan); padding:14px 18px; border-radius:0 10px 10px 0; margin:16px 0; font-size:14px; color:var(--text); }
.article-body .rel-tools { font-size:13px; color:var(--muted); margin-top:12px; }
.article-body .rel-tools a { color:var(--cyan); text-decoration:none; }
.article-body .rel-tools a:hover { text-decoration:underline; }
.page-tutorial { max-width:920px; margin:0 auto; padding:20px 16px 60px; }
.page-tutorial .back-link { display:inline-flex; align-items:center; gap:6px; font-size:14px; color:var(--muted); margin-bottom:20px; transition:color 0.2s; }
.page-tutorial .back-link:hover { color:var(--cyan); }
.page-tutorial .page-eyebrow { font-size:12px; font-weight:700; color:var(--cyan); letter-spacing:1px; text-transform:uppercase; margin-bottom:8px; display:block; }
.page-tutorial h1 { font-size:28px; font-weight:800; margin-bottom:8px; }
.page-tutorial .meta { font-size:13px; color:var(--muted); display:flex; gap:16px; margin-bottom:24px; }
.screenshot-wrap img { max-width:100%%; border-radius:12px; border:1px solid rgba(255,255,255,0.08); margin:12px 0; box-shadow:0 8px 24px rgba(0,0,0,0.3); }
</style>
<meta name="google-adsense-account" content="ca-pub-1955887568822472">
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-1955887568822472" crossorigin="anonymous"></script>
<script type="application/ld+json">{"@context":"https://schema.org","@type":"TechArticle","headline":"%s","description":"%s","datePublished":"2026-06-23","author":{"@type":"Organization","name":"ZenTools"},"publisher":{"@type":"Organization","name":"ZenTools"},"mainEntityOfPage":{"@type":"WebPage","@id":"https://zentools.xyz/tutorials/%s.html"}}</script>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/tools.html" data-i18n="navAll">全部工具</a><select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">← <span data-i18n="backToIndex">返回教程中心</span></a>
<span class="page-eyebrow" data-i18n="catAI">🤖 AI 工具</span>
<h1 data-i18n="a1Title">%s</h1>
<div class="meta"><span data-i18n="a1">📅 2026-06-23</span><span data-i18n="a1">⏱ %s</span></div>

<div class="article-body">
<h2 data-i18n="introTitle">功能介绍</h2>
<p data-i18n="a1Intro">%s</p>

<h2 data-i18n="openTitle">打开工具</h2>
<p data-i18n="a1OpenBody">%s</p>

<h2 data-i18n="stepTitle">操作步骤</h2>
<h3 data-i18n="a1Step1T">1. %s</h3>
<p data-i18n="a1Step1B">%s</p>
<div class="screenshot-wrap"><img src="%s" alt="%s - %s" style="max-width:100%%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);"></div>
<h3 data-i18n="a1Step2T">2. %s</h3>
<p data-i18n="a1Step2B">%s</p>
<h3 data-i18n="a1Step3T">3. %s</h3>
<p data-i18n="a1Step3B">%s</p>
<h3 data-i18n="a1Step4T">4. %s</h3>
<p data-i18n="a1Step4B">%s</p>

<h2 data-i18n="tipTitle">实用技巧</h2>
<div class="tip"><strong data-i18n="tipLabel">提示 1：</strong><span data-i18n="a1Tip1">%s</span></div>
<div class="tip"><strong data-i18n="tipLabel">提示 2：</strong><span data-i18n="a1Tip2">%s</span></div>
<div class="tip"><strong data-i18n="tipLabel">提示 3：</strong><span data-i18n="a1Tip3">%s</span></div>

<h2 data-i18n="faqTitle">常见问题</h2>
<p><strong data-i18n="a1Faq1Q">%s</strong><br/><span data-i18n="a1Faq1A">%s</span></p>
<p><strong data-i18n="a1Faq2Q">%s</strong><br/><span data-i18n="a1Faq2A">%s</span></p>
<p><strong data-i18n="a1Faq3Q">%s</strong><br/><span data-i18n="a1Faq3A">%s</span></p>

<div class="rel-tools"><strong data-i18n="relTitle">相关工具：</strong>
%s
</div>
</div>
</div>

<footer><div class="footer-inner"><div class="footer-logo">ZenTools</div><div class="footer-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/privacy.html" data-i18n="navPrivacy">隐私政策</a></div><p class="footer-copy" data-i18n="footerCopy">© 2026 ZenTools. 免费在线工具箱。</p></div></footer>
</div>

<script>
window.ZT_PAGE={zh:{a1Intro:'%s',a1OpenBody:'%s',a1Step1T:'%s',a1Step1B:'%s',a1Step2T:'%s',a1Step2B:'%s',a1Step3T:'%s',a1Step3B:'%s',a1Step4T:'%s',a1Step4B:'%s',a1Tip1:'%s',a1Tip2:'%s',a1Tip3:'%s',a1Faq1Q:'%s',a1Faq1A:'%s',a1Faq2Q:'%s',a1Faq2A:'%s',a1Faq3Q:'%s',a1Faq3A:'%s',introTitle:'功能介绍',openTitle:'打开工具',stepTitle:'操作步骤',tipTitle:'实用技巧',faqTitle:'常见问题',relTitle:'相关工具：',backToIndex:'返回教程中心',tipLabel:'提示',pageTitle:'%s - ZenTools',catAI:'🤖 AI 工具',a1Title:'%s',a1:'📅 2026-06-23 ⏱ %s'},en:{a1Intro:'%s',a1OpenBody:'%s',a1Step1T:'%s',a1Step1B:'%s',a1Step2T:'%s',a1Step2B:'%s',a1Step3T:'%s',a1Step3B:'%s',a1Step4T:'%s',a1Step4B:'%s',a1Tip1:'%s',a1Tip2:'%s',a1Tip3:'%s',a1Faq1Q:'%s',a1Faq1A:'%s',a1Faq2Q:'%s',a1Faq2A:'%s',a1Faq3Q:'%s',a1Faq3A:'%s',introTitle:'Feature Introduction',openTitle:'Open Tool',stepTitle:'Operation Steps',tipTitle:'Tips',faqTitle:'FAQ',relTitle:'Related Tools:',backToIndex:'Back to Tutorial Center',tipLabel:'Tip',pageTitle:'%s - ZenTools',catAI:'🤖 AI Tools',a1Title:'%s',a1:'📅 2026-06-23 ⏱ %s'},ja:{a1Intro:'%s',a1OpenBody:'%s',a1Step1T:'%s',a1Step1B:'%s',a1Step2T:'%s',a1Step2B:'%s',a1Step3T:'%s',a1Step3B:'%s',a1Step4T:'%s',a1Step4B:'%s',a1Tip1:'%s',a1Tip2:'%s',a1Tip3:'%s',a1Faq1Q:'%s',a1Faq1A:'%s',a1Faq2Q:'%s',a1Faq2A:'%s',a1Faq3Q:'%s',a1Faq3A:'%s',introTitle:'機能紹介',openTitle:'ツールを開く',stepTitle:'操作手順',tipTitle:'ヒント',faqTitle:'よくある質問',relTitle:'関連ツール：',backToIndex:'チュートリアルセンターに戻る',tipLabel:'ヒント',pageTitle:'%s - ZenTools',catAI:'🤖 AI ツール',a1Title:'%s',a1:'📅 2026-06-23 ⏱ %s'},vi:{a1Intro:'%s',a1OpenBody:'%s',a1Step1T:'%s',a1Step1B:'%s',a1Step2T:'%s',a1Step2B:'%s',a1Step3T:'%s',a1Step3B:'%s',a1Step4T:'%s',a1Step4B:'%s',a1Tip1:'%s',a1Tip2:'%s',a1Tip3:'%s',a1Faq1Q:'%s',a1Faq1A:'%s',a1Faq2Q:'%s',a1Faq2A:'%s',a1Faq3Q:'%s',a1Faq3A:'%s',introTitle:'Giới thiệu tính năng',openTitle:'Mở công cụ',stepTitle:'Các bước thực hiện',tipTitle:'Mẹo',faqTitle:'Câu hỏi thường gặp',relTitle:'Công cụ liên quan:',backToIndex:'Trở lại trung tâm hướng dẫn',tipLabel:'Mẹo',pageTitle:'%s - ZenTools',catAI:'🤖 AI 工具',a1Title:'%s',a1:'📅 2026-06-23 ⏱ %s'}}}
</script>
<script src="../assets/js/tool-ui.min.js"></script>
<button class="bookmark-float" onclick="prompt('复制链接收藏本站','https://zentools.xyz')">⭐ 收藏本站，下次办公快人一步</button>
<script>
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/service-worker.js').catch(() => {});
  });
}
</script>
</body>
</html>''' % (
        tool["title"], tool["description"], tool["name"],
        tool["title"], tool["description"], tool["name"],
        tool["title"], tool["reading_time"],
        tool["intro"],
        tool["step1_body"],
        tool["step1_title"], tool["step1_body"], tool["svg"], tool["title"], tool["step1_title"],
        tool["step2_title"], tool["step2_body"],
        tool["step3_title"], tool["step3_body"],
        tool["step4_title"], tool["step4_body"],
        tool["tip1"], tool["tip2"], tool["tip3"],
        tool["faq1_q"], tool["faq1_a"],
        tool["faq2_q"], tool["faq2_a"],
        tool["faq3_q"], tool["faq3_a"],
        related_links,
        # 中文翻译
        tool["intro"], tool["step1_body"], tool["step1_title"], tool["step1_body"],
        tool["step2_title"], tool["step2_body"],
        tool["step3_title"], tool["step3_body"],
        tool["step4_title"], tool["step4_body"],
        tool["tip1"], tool["tip2"], tool["tip3"],
        tool["faq1_q"], tool["faq1_a"],
        tool["faq2_q"], tool["faq2_a"],
        tool["faq3_q"], tool["faq3_a"],
        tool["title"], tool["title"], tool["reading_time"],
        # 英文翻译
        tool["intro"], tool["step1_body"], tool["step1_title"], tool["step1_body"],
        tool["step2_title"], tool["step2_body"],
        tool["step3_title"], tool["step3_body"],
        tool["step4_title"], tool["step4_body"],
        tool["tip1"], tool["tip2"], tool["tip3"],
        tool["faq1_q"], tool["faq1_a"],
        tool["faq2_q"], tool["faq2_a"],
        tool["faq3_q"], tool["faq3_a"],
        tool["title"], tool["title"], tool["reading_time"],
        # 日文翻译
        tool["intro"], tool["step1_body"], tool["step1_title"], tool["step1_body"],
        tool["step2_title"], tool["step2_body"],
        tool["step3_title"], tool["step3_body"],
        tool["step4_title"], tool["step4_body"],
        tool["tip1"], tool["tip2"], tool["tip3"],
        tool["faq1_q"], tool["faq1_a"],
        tool["faq2_q"], tool["faq2_a"],
        tool["faq3_q"], tool["faq3_a"],
        tool["title"], tool["title"], tool["reading_time"],
        # 越南文翻译
        tool["intro"], tool["step1_body"], tool["step1_title"], tool["step1_body"],
        tool["step2_title"], tool["step2_body"],
        tool["step3_title"], tool["step3_body"],
        tool["step4_title"], tool["step4_body"],
        tool["tip1"], tool["tip2"], tool["tip3"],
        tool["faq1_q"], tool["faq1_a"],
        tool["faq2_q"], tool["faq2_a"],
        tool["faq3_q"], tool["faq3_a"],
        tool["title"], tool["title"], tool["reading_time"]
    )
    return html

# 为每个工具生成HTML文件
for tool in tools:
    html_content = generate_html(tool)
    file_path = f"/workspace/tutorials/{tool['name']}.html"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Created: {file_path}")

print("All tutorial HTML files created successfully!")