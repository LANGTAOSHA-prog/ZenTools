#!/usr/bin/env python3
"""
ZenTools 知识库生成器 — 用于持续积累高价值内容。
用法：python _gen_knowledge.py [--rebuild]

6 大分类：
  ai-tutorials  AI 使用教程
  prompts       提示词 / Prompt 工程
  workflows     工作流
  model-compare 模型对比与评测
  api-tutorials API 教程
  deployment    部署指南

每篇文章需要提供：
  slug, cat, title, desc, tags, date, words, url
"""
import json, os, re

BASE = os.path.join(os.path.dirname(__file__), "knowledge")
DATA_FILE = os.path.join(BASE, "kb-data.json")

# ===== 默认知识库数据（可编辑此文件持续添加）=====
KB_DATA = {
  "schemaVersion": "1.0",
  "lastUpdated": "2026-07-01",
  "categories": [
    {"id": "ai-tutorials",   "icon": "🤖", "name": "AI 使用教程", "nameEn": "AI Tutorials",     "desc": "从入门到进阶，涵盖 AI 写作、AI 绘画、AI 编程、AI 翻译等主流场景。"},
    {"id": "prompts",        "icon": "💬", "name": "提示词工程",   "nameEn": "Prompt Engineering", "desc": "提示词模板、设计模式和最佳实践，涵盖写作、绘画、编程等场景。"},
    {"id": "workflows",      "icon": "🔧", "name": "工作流",       "nameEn": "Workflows",          "desc": "将多个工具串联成高效工作流，解决真实场景中的完整问题。"},
    {"id": "model-compare",  "icon": "📊", "name": "模型对比",     "nameEn": "Model Comparisons",  "desc": "独立客观的 AI 模型评测和平台对比，包含性能数据和价格分析。"},
    {"id": "api-tutorials",  "icon": "🔌", "name": "API 教程",     "nameEn": "API Tutorials",      "desc": "从 Key 申请到接口调用，涵盖主流 AI 模型的 API 接入教程。"},
    {"id": "deployment",     "icon": "🚀", "name": "部署指南",     "nameEn": "Deployment Guides",  "desc": "从零部署 AI 模型，包含云服务器、Docker、生产环境优化等内容。"},
  ],
  "articles": [
    # ===== AI 使用教程 =====
    {"slug": "ai-writing",        "cat": "ai-tutorials", "title": "AI 写作教程：如何使用 AI 辅助创作",     "desc": "从灵感到成品的完整 AI 写作流程。涵盖博客、营销文案、技术文档等场景。", "tags": ["入门","写作"], "date": "2026-06", "words": "3200+"},
    {"slug": "ai-image-generator","cat": "ai-tutorials", "title": "AI 图像生成教程：从提示词到成品",         "desc": "主流 AI 绘画工具的使用方法和提示词技巧。", "tags": ["入门","绘画"], "date": "2026-06", "words": "2800+"},
    {"slug": "ai-code-generator", "cat": "ai-tutorials", "title": "AI 编程辅助教程：高效生成代码",           "desc": "使用 AI 辅助编程，提升开发效率的实战指南。", "tags": ["进阶","编程"], "date": "2026-06", "words": "3000+"},
    {"slug": "ai-translate",      "cat": "ai-tutorials", "title": "AI 翻译教程：多语言翻译的最佳实践",       "desc": "利用 AI 进行高质量翻译，支持中英日越等语言。", "tags": ["入门","翻译"], "date": "2026-06", "words": "2000+"},
    {"slug": "ai-summary",        "cat": "ai-tutorials", "title": "AI 总结教程：快速提炼文档要点",           "desc": "用 AI 快速总结长文章、文档、视频字幕等。", "tags": ["入门","总结"], "date": "2026-06", "words": "2000+"},
    {"slug": "ai-paraphrase",     "cat": "ai-tutorials", "title": "AI 改写教程：优化文本表达",               "desc": "使用 AI 改写和润色文本，提升写作质量。", "tags": ["入门","写作"], "date": "2026-06", "words": "2000+"},
    {"slug": "ai-qa",             "cat": "ai-tutorials", "title": "AI 问答教程：构建智能问答系统",           "desc": "利用 AI 构建高效的问答和知识检索系统。", "tags": ["进阶","问答"], "date": "2026-06", "words": "2500+"},
    {"slug": "ai-social-copy",    "cat": "ai-tutorials", "title": "AI 社交媒体文案教程：一键生成爆款文案",   "desc": "使用 AI 生成适合小红书、微博等平台的文案。", "tags": ["入门","文案"], "date": "2026-07", "words": "2000+"},

    # ===== 提示词工程 =====
    {"slug": "ai-writing",        "cat": "prompts", "title": "AI 写作提示词模板：从博客到营销文案",         "desc": "10+ 精选写作提示词模板，覆盖主流场景。", "tags": ["模板","写作"], "date": "2026-06", "words": ""},
    {"slug": "ai-image-prompt",   "cat": "prompts", "title": "AI 绘画提示词技巧：Midjourney & SD",          "desc": "高质量绘画提示词的结构、关键词和风格词库。", "tags": ["模板","绘画"], "date": "2026-06", "words": ""},
    {"slug": "ai-code-generator", "cat": "prompts", "title": "AI 编程提示词：生成高质量代码的秘诀",         "desc": "编程提示词模板和最佳实践。", "tags": ["模板","编程"], "date": "2026-06", "words": ""},
    {"slug": "ai-prompt-generator","cat": "prompts", "title": "AI 提示词生成器：自动优化你的 Prompt",       "desc": "使用工具自动生成和优化提示词。", "tags": ["工具"], "date": "2026-06", "words": ""},
    {"slug": "ai-video-script",   "cat": "prompts", "title": "AI 视频脚本提示词模板",                       "desc": "短视频、口播、教程类视频的脚本模板。", "tags": ["模板","视频"], "date": "2026-06", "words": ""},
    {"slug": "ai-email",          "cat": "prompts", "title": "AI 邮件提示词模板",                           "desc": "商务邮件、营销邮件的提示词模板。", "tags": ["模板","邮件"], "date": "2026-06", "words": ""},

    # ===== 工作流 =====
    {"slug": "ai-writing-workflow",     "cat": "workflows", "title": "AI 写作完整工作流：从灵感到发布",       "desc": "8 步完成从选题到发布的 AI 写作全流程。", "tags": ["推荐","写作"], "date": "2026-06", "words": "3200+"},
    {"slug": "image-editing-workflow",  "cat": "workflows", "title": "图片编辑完整工作流：从拍摄到发布",        "desc": "10 个工具覆盖从裁剪到水印的完整流程。", "tags": ["推荐","图片"], "date": "2026-07", "words": "2500+"},
    {"slug": "pdf-automation-guide",    "cat": "workflows", "title": "PDF 自动化工作流指南",                  "desc": "发票处理、合同整理、报告生成的实战案例。", "tags": ["高效","PDF"], "date": "2026-06", "words": "2600+"},
    {"slug": "video-editing-beginners", "cat": "workflows", "title": "视频剪辑入门工作流",                    "desc": "5 个浏览器工具快速上手视频处理。", "tags": ["入门","视频"], "date": "2026-07", "words": "2000+"},
    {"slug": "audio-content-creation",  "cat": "workflows", "title": "音频内容创作工作流",                    "desc": "从录制到发布的 8 个音频处理步骤。", "tags": ["入门","音频"], "date": "2026-07", "words": "2500+"},
    {"slug": "content-creation-tools",  "cat": "workflows", "title": "自媒体内容创作工作流",                  "desc": "10 个工具覆盖文案+图片+视频全流程。", "tags": ["推荐","自媒体"], "date": "2026-07", "words": "2800+"},
    {"slug": "developer-efficiency-tools","cat": "workflows","title": "开发者效率工作流",                     "desc": "JSON/正则/调试等开发高频操作的工具链。", "tags": ["进阶","开发"], "date": "2026-07", "words": "2000+"},
    {"slug": "image-batch-processing",  "cat": "workflows", "title": "图片批量处理最佳实践",                  "desc": "电商、营销场景下的批量处理完整攻略。", "tags": ["高效","图片"], "date": "2026-06", "words": "2800+"},

    # ===== 模型对比 =====
    {"slug": "longmao-ai-review",       "cat": "model-compare", "title": "龙猫 AI 平台深度评测",              "desc": "免费千万 Token + 华为昇腾/寒武纪等国产算力实测。", "tags": ["深度"], "date": "2026-06", "words": "4200+"},
    {"slug": "workbuddy-free-token-review","cat": "model-compare","title": "Workbuddy 免费无限 Token 实测",    "desc": "AI 编程助手完整评测，含性能数据和竞品对比。", "tags": ["深度"], "date": "2026-06", "words": "4800+"},
    {"slug": "nex-n2-pro-review",       "cat": "model-compare", "title": "Nex-N2-Pro 深度评测",              "desc": "GPT-5.5 级免费 AI Agent 模型实测。", "tags": ["深度"], "date": "2026-06", "words": "3500+"},
    {"slug": "free-api-models-guide",   "cat": "model-compare", "title": "免费 AI 模型 API 大全",            "desc": "30+ 免费 API 接口对比，含 Hugging Face/Gemini/Ollama。", "tags": ["对比"], "date": "2026-06", "words": "3000+"},
    {"slug": "agnes-ai-free-token-tutorial","cat": "model-compare","title": "Agnes AI 免费 Token 接入实测",   "desc": "AI 图像生成平台接入指南，附性能对比数据。", "tags": ["评测"], "date": "2026-06", "words": "3800+"},

    # ===== API 教程 =====
    {"slug": "gemini-25-flash-free-tutorial","cat": "api-tutorials","title": "Gemini 2.5 Flash 免费 API 接入", "desc": "从注册到调用的完整教程，零成本使用 Google 最新模型。", "tags": ["🔥"], "date": "2026-06", "words": "6000+"},
    {"slug": "agnes-desktop-installation","cat": "api-tutorials","title": "Agnes 桌面版安装与 API 配置",      "desc": "Windows/Mac/Linux 全平台安装和 API 配置指南。", "tags": ["教程"], "date": "2026-06", "words": "4500+"},
    {"slug": "qwenpaw-free-deployment","cat": "api-tutorials","title": "QwenPaw 本地部署与 API 调用",        "desc": "从零配置本地 AI 助理的完整教程。", "tags": ["教程"], "date": "2026-06", "words": "5200+"},
    {"slug": "free-api-models",          "cat": "api-tutorials", "title": "免费 AI 模型 API 接口清单",        "desc": "30+ 免费大模型接口的获取方式和调用示例。", "tags": ["清单"], "date": "2026-06", "words": ""},
    {"slug": "agnes-ai-free-token-tutorial","cat": "api-tutorials","title": "Agnes AI API Key 申请与集成",   "desc": "API Key 申请流程和 SDK 集成示例代码。", "tags": ["教程"], "date": "2026-06", "words": "3800+"},

    # ===== 部署指南 =====
    {"slug": "alibaba-cloud-deploy-dify","cat": "deployment","title": "阿里云部署 Dify 完整指南",             "desc": "ECS 选型、Docker 配置、数据库优化、生产调优全流程。", "tags": ["🔥"], "date": "2026-06", "words": "4500+"},
    {"slug": "agnes-desktop-installation","cat": "deployment","title": "Agnes 桌面版安装教程",               "desc": "Windows/Mac/Linux 全平台本地部署指南。", "tags": ["教程"], "date": "2026-06", "words": "4500+"},
    {"slug": "qwenpaw-free-deployment", "cat": "deployment","title": "QwenPaw 免费部署教程：本地 AI 助理",    "desc": "零成本搭建本地 AI 助理的完整部署方案。", "tags": ["🔥"], "date": "2026-06", "words": "5200+"},
    {"slug": "cloud-resources",         "cat": "deployment","title": "免费云环境资源大全",                    "desc": "Oracle Cloud、AWS、GCP 等 30+ 免费云服务清单。", "tags": ["清单"], "date": "2026-06", "words": ""},
    {"slug": "free-ai-aggregator",      "cat": "deployment","title": "免费 AI 模型聚合平台部署",              "desc": "自动轮询 Mistral/Gemma/Phi-3，智能故障切换。", "tags": ["教程"], "date": "2026-06", "words": ""},
  ]
}

def build_article_url(article):
    """Determine the URL for a knowledge base article."""
    slug = article["slug"]
    cat = article["cat"]
    # Map slug to actual file path
    if cat == "deployment":
        if slug == "cloud-resources":
            return f"/yunchuang/{slug}.html"
        if slug == "free-ai-aggregator":
            return "/yunchuang/free-ai-aggregator/"
        return f"/guides/{slug}.html"
    elif cat in ("model-compare", "api-tutorials", "workflows"):
        if slug in ("free-api-models",):
            return f"/yunchuang/{slug}.html"
        if slug == "free-api-models-guide":
            return f"/guides/{slug}.html"
        return f"/guides/{slug}.html"
    elif cat in ("ai-tutorials", "prompts"):
        return f"/tutorials/{slug}.html"
    return f"/tutorials/{slug}.html"

def generate_index():
    """Regenerate the knowledge base index page with updated article list."""
    # Read existing index template
    index_path = os.path.join(BASE, "index.html")
    with open(index_path, encoding='utf-8') as f:
        content = f.read()

    # Build article lists per category
    sections_html = ""
    for cat in KB_DATA["categories"]:
        cid = cat["id"]
        articles = [a for a in KB_DATA["articles"] if a["cat"] == cid]
        rows = ""
        for a in articles:
            url = build_article_url(a)
            tag_str = f'<span class="ar-tag">{a["tags"][0]}</span>' if a.get("tags") else ""
            words_str = f' {a["words"]}' if a.get("words") else ""
            date_str = a.get("date", "")
            rows += f'''<div class="article-row"><span class="ar-icon">{cat["icon"]}</span><span class="ar-title"><a href="{url}">{a["title"]}</a></span><span class="ar-meta">{tag_str}{words_str}{date_str}</span></div>\n'''

        sections_html += f'''<!-- === {cat["name"]} === -->
<div class="kb-section" data-cat="{cid}" id="sec-{cid}">
  <h2 class="section-title">{cat["icon"]} {cat["name"]}</h2>
  <p class="section-desc">{cat["desc"]}</p>
  <div class="article-list">{rows}</div>
</div>\n'''

    # Update the index.html content between markers
    start_marker = '<!-- KB_SECTIONS_START -->'
    end_marker = '<!-- KB_SECTIONS_END -->'
    
    if start_marker in content and end_marker in content:
        parts = content.split(start_marker)
        middle = parts[1].split(end_marker)
        new_content = parts[0] + start_marker + '\n' + sections_html + '\n' + end_marker + middle[1]
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated: {index_path}")
    else:
        print("Warning: KB_SECTIONS markers not found in index.html. Appending to file.")
        # Just save the data
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(KB_DATA, f, ensure_ascii=False, indent=2)
        print(f"Saved data to {DATA_FILE}")

    # Save structured data
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(KB_DATA, f, ensure_ascii=False, indent=2)
    print(f"Saved KB data to {DATA_FILE}")

    total = len(KB_DATA["articles"])
    print(f"\n=== Knowledge Base: {total} articles across {len(KB_DATA['categories'])} categories ===")

if __name__ == "__main__":
    import sys
    if "--init" in sys.argv:
        # Create data file only
        os.makedirs(BASE, exist_ok=True)
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(KB_DATA, f, ensure_ascii=False, indent=2)
        print(f"Initialized: {DATA_FILE}")
    else:
        generate_index()
