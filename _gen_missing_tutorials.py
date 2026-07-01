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

# ===== build_html function with full i18n support =====
# [多语言完整] 每个文本字段都有 zh/en/ja/vi 四种语言翻译
def build_html(tool_id, title_zh, desc_zh, func_zh, duration, tool_url, svg_file, step_keys,
               tips, faqs, related, cat_label="🏠 生活工具",
               title_en="", desc_en="", func_en="",
               title_ja="", desc_ja="", func_ja="",
               title_vi="", desc_vi="", func_vi="",
               cat_label_en="🔧 Life Tools", cat_label_ja="🏠 生活ツール", cat_label_vi="🏠 Công cụ cuộc sống",
               tips_en=None, tips_ja=None, tips_vi=None,
               faqs_en=None, faqs_ja=None, faqs_vi=None):
    tool_name = title_zh.split("：")[0] if "：" in title_zh else title_zh.split(":")[0]
    tool_name_en = title_en.split(":")[0] if ":" in title_en else title_en.split("：")[0] if "：" in title_en else title_en
    tool_name_ja = title_ja.split("：")[0] if "：" in title_ja else title_ja.split(":")[0] if ":" in title_ja else title_ja
    tool_name_vi = title_vi.split("：")[0] if "：" in title_vi else title_vi.split(":")[0] if ":" in title_vi else title_vi

    if not tool_name_en:
        tool_name_en = tool_name
    if not tool_name_ja:
        tool_name_ja = tool_name
    if not tool_name_vi:
        tool_name_vi = tool_name
    if not func_en:
        func_en = func_zh
    if not func_ja:
        func_ja = func_zh
    if not func_vi:
        func_vi = func_zh
    if not desc_en:
        desc_en = desc_zh
    if not desc_ja:
        desc_ja = desc_zh
    if not desc_vi:
        desc_vi = desc_zh
    if tips_en is None:
        tips_en = tips
    if tips_ja is None:
        tips_ja = tips
    if tips_vi is None:
        tips_vi = tips

    # ---- ZH (中文) ----
    zh = {
        "a1Intro": func_zh,
        "a1OpenBody": f'访问 <a href="{tool_url}" target="_blank">{tool_name}</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需注册账号，完全免费。',
        f"{step_keys}Step1T": "打开工具",
        f"{step_keys}Step1B": f'访问<a href="{tool_url}" target="_blank">{tool_name}</a>，在浏览器中打开工具页面。页面简洁直观，无需安装任何软件。',
        f"{step_keys}Step2T": "选择操作",
        f"{step_keys}Step2B": "根据需要选择操作模式或输入处理参数。工具提供多种操作选项，可以根据不同的使用场景灵活配置。",
        f"{step_keys}Step3T": "上传文件",
        f"{step_keys}Step3B": "点击上传区域或拖拽文件到指定区域。支持多种常见格式，单文件最大100MB。上传的文件在浏览器本地处理，不会上传到服务器。",
        f"{step_keys}Step4T": "查看结果",
        f"{step_keys}Step4B": "处理完成后结果会实时显示，你可以预览、复制或下载处理结果。所有操作均可重复进行。",
        "introTitle": "功能介绍", "openTitle": "打开工具", "stepTitle": "操作步骤",
        "tipTitle": "实用技巧", "faqTitle": "常见问题", "relTitle": "相关工具：",
        "backToIndex": "返回教程中心", "tipLabel": "提示",
        "pageTitle": f"{title_zh} - ZenTools", "catLabel": cat_label,
        "a1Title": title_zh, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration} 分钟阅读",
        "navHome": "首页", "navDev": "开发工具", "navAll": "全部工具",
        "navPrivacy": "隐私政策", "footerCopy": "© 2026 ZenTools. 免费在线工具箱。",
    }
    for i, tip in enumerate(tips, 1):
        zh[f"{step_keys}Tip{i}"] = tip

    # ---- EN (English) ----
    en = {
        "a1Intro": func_en,
        "a1OpenBody": f'Visit <a href="{tool_url}" target="_blank">{tool_name_en}</a> directly in your browser. All operations run locally, no registration required, completely free.',
        f"{step_keys}Step1T": "Open the Tool",
        f"{step_keys}Step1B": f'Visit <a href="{tool_url}" target="_blank">{tool_name_en}</a> in your browser. The interface is clean and intuitive, no software installation needed.',
        f"{step_keys}Step2T": "Select Action",
        f"{step_keys}Step2B": "Choose the operation mode or enter processing parameters as needed. The tool provides multiple options for different use scenarios.",
        f"{step_keys}Step3T": "Upload Files",
        f"{step_keys}Step3B": "Click the upload area or drag & drop files. Supports multiple formats, max 100MB per file. Files are processed locally in your browser, never uploaded to any server.",
        f"{step_keys}Step4T": "View Results",
        f"{step_keys}Step4B": "Results are displayed in real-time. You can preview, copy, or download. All operations can be repeated.",
        "introTitle": "Introduction", "openTitle": "Open the Tool", "stepTitle": "Steps",
        "tipTitle": "Tips", "faqTitle": "FAQ", "relTitle": "Related Tools:",
        "backToIndex": "Back to Tutorials", "tipLabel": "Tip",
        "pageTitle": f"{title_en} - ZenTools", "catLabel": cat_label_en,
        "a1Title": title_en, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration} min read",
        "navHome": "Home", "navDev": "Dev Tools", "navAll": "All Tools",
        "navPrivacy": "Privacy", "footerCopy": "© 2026 ZenTools. Free Online Toolbox.",
    }
    for i, tip in enumerate(tips_en, 1):
        en[f"{step_keys}Tip{i}"] = tip

    # ---- JA (日本語) ----
    ja = {
        "a1Intro": func_ja,
        "a1OpenBody": f'ブラウザで <a href="{tool_url}" target="_blank">{tool_name_ja}</a> にアクセスしてすぐに使用できます。すべての操作はブラウザ内で完結し、登録不要、完全無料です。',
        f"{step_keys}Step1T": "ツールを開く",
        f"{step_keys}Step1B": f'ブラウザで <a href="{tool_url}" target="_blank">{tool_name_ja}</a> にアクセスしてください。シンプルで直感的なインターフェースで、ソフトウェアのインストールは不要です。',
        f"{step_keys}Step2T": "操作を選択",
        f"{step_keys}Step2B": "必要に応じて操作モードを選択するか、処理パラメータを入力します。さまざまな使用シーンに対応する複数のオプションを提供しています。",
        f"{step_keys}Step3T": "ファイルをアップロード",
        f"{step_keys}Step3B": "アップロードエリアをクリックするか、ファイルをドラッグ＆ドロップしてください。複数の形式に対応、1ファイル最大100MB。ファイルはブラウザ内でローカル処理され、サーバーにアップロードされることはありません。",
        f"{step_keys}Step4T": "結果を確認",
        f"{step_keys}Step4B": "処理が完了すると結果がリアルタイムに表示されます。プレビュー、コピー、ダウンロードが可能です。操作は繰り返し実行できます。",
        "introTitle": "機能紹介", "openTitle": "ツールを開く", "stepTitle": "操作手順",
        "tipTitle": "ヒント", "faqTitle": "よくある質問", "relTitle": "関連ツール：",
        "backToIndex": "チュートリアルに戻る", "tipLabel": "ヒント",
        "pageTitle": f"{title_ja} - ZenTools", "catLabel": cat_label_ja,
        "a1Title": title_ja, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration}分",
        "navHome": "ホーム", "navDev": "開発ツール", "navAll": "すべてのツール",
        "navPrivacy": "プライバシー", "footerCopy": "© 2026 ZenTools. 無料オンラインツールボックス。",
    }
    for i, tip in enumerate(tips_ja, 1):
        ja[f"{step_keys}Tip{i}"] = tip

    # ---- VI (Tiếng Việt) ----
    vi = {
        "a1Intro": func_vi,
        "a1OpenBody": f'Truy cập <a href="{tool_url}" target="_blank">{tool_name_vi}</a> trực tiếp trong trình duyệt. Tất cả thao tác xử lý tại máy cục bộ, không cần đăng ký, hoàn toàn miễn phí.',
        f"{step_keys}Step1T": "Mở Công cụ",
        f"{step_keys}Step1B": f'Truy cập <a href="{tool_url}" target="_blank">{tool_name_vi}</a> trong trình duyệt. Giao diện đơn giản, trực quan, không cần cài đặt phần mềm.',
        f"{step_keys}Step2T": "Chọn Thao tác",
        f"{step_keys}Step2B": "Chọn chế độ thao tác hoặc nhập tham số xử lý theo nhu cầu. Công cụ cung cấp nhiều tùy chọn cho các tình huống sử dụng khác nhau.",
        f"{step_keys}Step3T": "Tải lên Tệp",
        f"{step_keys}Step3B": "Nhấp vào khu vực tải lên hoặc kéo thả tệp vào khu vực chỉ định. Hỗ trợ nhiều định dạng phổ biến, tối đa 100MB mỗi tệp. Tệp được xử lý cục bộ trong trình duyệt, không tải lên máy chủ.",
        f"{step_keys}Step4T": "Xem Kết quả",
        f"{step_keys}Step4B": "Kết quả được hiển thị theo thời gian thực. Bạn có thể xem trước, sao chép hoặc tải xuống. Tất cả thao tác có thể thực hiện lại.",
        "introTitle": "Giới thiệu", "openTitle": "Mở Công cụ", "stepTitle": "Các bước",
        "tipTitle": "Mẹo", "faqTitle": "Câu hỏi thường gặp", "relTitle": "Công cụ liên quan:",
        "backToIndex": "Quay lại Hướng dẫn", "tipLabel": "Mẹo",
        "pageTitle": f"{title_vi} - ZenTools", "catLabel": cat_label_vi,
        "a1Title": title_vi, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration} phút đọc",
        "navHome": "Trang chủ", "navDev": "Công cụ Dev", "navAll": "Tất cả",
        "navPrivacy": "Quyền riêng tư", "footerCopy": "© 2026 ZenTools. Hộp công cụ trực tuyến miễn phí.",
    }
    for i, tip in enumerate(tips_vi, 1):
        vi[f"{step_keys}Tip{i}"] = tip

    # ---- 通用 FAQ（4语言完整翻译）----
    universal_faqs_zh = [
        ("这个工具适合谁？适合哪些使用场景？",
         f"本教程介绍的{tool_name}适合日常办公用户、学生、自由职业者和小型企业团队。无论你是需要快速处理文档的上班族、整理学习资料的学生，还是需要批量处理素材的内容创作者，都可以免费使用。无需任何专业技能，打开浏览器即可上手。"),
        ("完全免费吗？有什么使用限制？",
         f"{tool_name}完全免费，无隐藏费用、无订阅要求、无水印。主要限制包括：单文件最大 100MB，部分批量操作一次最多处理 20 个文件。所有处理在浏览器本地完成，不消耗你的云端配额或 API 额度。"),
        ("支持中文吗？界面和操作是否友好？",
         "完全支持中文界面（简体中文），同时也提供英文、日文、越南文界面。所有按钮、提示和说明均已本地化为中文，无需担心语言障碍。操作流程符合国内用户习惯，拖拽上传、一键处理，直观易用。"),
    ]
    universal_faqs_en = [
        ("Who is this tool for? What use cases?",
         f"{tool_name_en} is designed for office workers, students, freelancers, and small business teams. Whether you need to process documents, organize study materials, or batch-edit content, you can use it for free with zero learning curve."),
        ("Is it completely free? Any limitations?",
         f"{tool_name_en} is 100% free — no hidden fees, no subscriptions, no watermarks. Main limits: 100MB max per file, batch operations up to 20 files at a time. All processing runs locally in your browser, consuming zero cloud quota."),
        ("Does it support Chinese? Is the UI friendly?",
         "The interface fully supports Simplified Chinese, plus English, Japanese, and Vietnamese. All buttons, tooltips, and instructions are localized. The workflow is intuitive: drag & drop upload, one-click processing."),
    ]
    universal_faqs_ja = [
        ("このツールは誰向けですか？どのような使用シーンがありますか？",
         f"{tool_name_ja}は、一般オフィスワーカー、学生、フリーランサー、中小企業チーム向けです。書類処理、学習資料の整理、コンテンツの一括編集など、専門スキル不要で無料でご利用いただけます。"),
        ("完全無料ですか？制限はありますか？",
         f"{tool_name_ja}は完全無料です。隠れた費用、サブスクリプション、ウォーターマークは一切ありません。主な制限：1ファイル最大100MB、一括操作は最大20ファイルまで。すべてブラウザ内でローカル処理され、クラウドクォータを消費しません。"),
        ("日本語は対応していますか？インターフェースは使いやすいですか？",
         "インターフェースは日本語（簡体字中国語・英語・ベトナム語も対応）を完全サポート。すべてのボタン、ヒント、説明文は日本語にローカライズされています。ドラッグ＆ドロップとワンクリック処理で直感的に操作できます。"),
    ]
    universal_faqs_vi = [
        ("Công cụ này phù hợp với ai? Trường hợp sử dụng nào?",
         f"{tool_name_vi} phù hợp cho nhân viên văn phòng, sinh viên, freelancer và nhóm doanh nghiệp nhỏ. Dù bạn cần xử lý tài liệu, sắp xếp tài liệu học tập hay chỉnh sửa nội dung hàng loạt, đều có thể sử dụng miễn phí."),
        ("Có hoàn toàn miễn phí không? Có giới hạn gì không?",
         f"{tool_name_vi} hoàn toàn miễn phí — không phí ẩn, không đăng ký, không hình mờ. Giới hạn chính: tối đa 100MB mỗi tệp, thao tác hàng loạt tối đa 20 tệp một lần. Xử lý cục bộ trong trình duyệt, không tiêu tốn hạn ngạch đám mây."),
        ("Có hỗ trợ tiếng Trung không? Giao diện có thân thiện không?",
         "Giao diện hỗ trợ đầy đủ tiếng Trung (giản thể), cùng với tiếng Anh, tiếng Nhật và tiếng Việt. Tất cả nút bấm, gợi ý và hướng dẫn đều được bản địa hóa. Thao tác kéo thả, xử lý một cú nhấp chuột, trực quan và dễ sử dụng."),
    ]

    def make_faqs(base, extra):
        """Combine category-specific + universal FAQs for one language."""
        result = list(base) + extra
        return result

    faq_zh_all = make_faqs(faqs, universal_faqs_zh)
    faq_en_all = make_faqs(faqs_en if faqs_en else faqs, universal_faqs_en)
    faq_ja_all = make_faqs(faqs_ja if faqs_ja else faqs, universal_faqs_ja)
    faq_vi_all = make_faqs(faqs_vi if faqs_vi else faqs, universal_faqs_vi)

    for i, (q, a) in enumerate(faq_zh_all, 1):
        zh[f"{step_keys}Faq{i}Q"] = q
        zh[f"{step_keys}Faq{i}A"] = a
    for i, (q, a) in enumerate(faq_en_all, 1):
        en[f"{step_keys}Faq{i}Q"] = q
        en[f"{step_keys}Faq{i}A"] = a
    for i, (q, a) in enumerate(faq_ja_all, 1):
        ja[f"{step_keys}Faq{i}Q"] = q
        ja[f"{step_keys}Faq{i}A"] = a
    for i, (q, a) in enumerate(faq_vi_all, 1):
        vi[f"{step_keys}Faq{i}Q"] = q
        vi[f"{step_keys}Faq{i}A"] = a

    # ---- 结构化数据 JSON-LD 仅用中文（搜索引擎优化）----
    all_faqs_zh_for_jsonld = faq_zh_all
    faq_jsonld_items = []
    for q, a in all_faqs_zh_for_jsonld:
        faq_jsonld_items.append(f'{{"@type":"Question","name":{json.dumps(q)},"acceptedAnswer":{{"@type":"Answer","text":{json.dumps(a)}}}}}')
    faq_jsonld = f'<script type="application/ld+json">{{"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{",".join(faq_jsonld_items)}]}}</script>'

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
    for i, (q, a) in enumerate(faq_zh_all, 1):
        faq_html += f'''<div class="faq-item"><p><strong data-i18n="{step_keys}Faq{i}Q">{q}</strong><br/><span data-i18n="{step_keys}Faq{i}A">{a}</span></p></div>
'''

    # [AI 搜索优化] 构建 FAQPage JSON-LD 结构化数据
    faq_jsonld_items = []
    for q, a in faq_zh_all:
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


# ===== Build generic category-specific content with full i18n =====
def make_image_tutorial(slug, name_zh, name_en, tool_url):
    """Generate image tool tutorial with image-specific steps."""
    cat_label = "🖼 图片工具"
    cat_label_en = "🖼 Image Tools"
    cat_label_ja = "🖼 画像ツール"
    cat_label_vi = "🖼 Công cụ ảnh"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线图片处理"
    title_en = f"{name_en} Tutorial: Online Image Processing"
    title_ja = f"{name_en}チュートリアル：オンライン画像処理"
    title_vi = f"{name_en} Hướng dẫn: Xử lý ảnh trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理图片文件。支持批量操作，所有处理在浏览器本地完成，保护图片隐私。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to quickly process images. Supports batch operations, all processing done locally in your browser, protecting image privacy."
    desc_ja = f"ZenTools のオンライン{name_en}ツールを使って画像を素早く処理する方法を学びます。バッチ操作対応、すべてブラウザ内でローカル処理。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để xử lý ảnh nhanh chóng. Hỗ trợ thao tác hàng loạt, xử lý cục bộ trong trình duyệt."
    func = f"ZenTools {name_zh}工具是一款高效在线图片处理工具，支持对 JPG、PNG、WebP、GIF 等主流图片格式进行处理。"
    func_en = f"ZenTools {name_en} is an efficient online image processing tool supporting JPG, PNG, WebP, GIF and other major image formats."
    func_ja = f"ZenTools {name_en}は、JPG、PNG、WebP、GIFなどの主要画像形式に対応した効率的なオンライン画像処理ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ xử lý ảnh trực tuyến hiệu quả, hỗ trợ các định dạng ảnh chính như JPG, PNG, WebP, GIF."
    tips = [
        f"支持批量处理多张图片，可以同时上传多张图片进行{name_zh}操作，大大提高工作效率。",
        "所有处理在浏览器本地完成，图片不会上传到任何服务器，完全保护你的图片隐私和数据安全。",
        "处理后的图片建议及时保存，刷新页面后本地缓存会被清除。建议将常用操作结果收藏备用。"
    ]
    tips_en = [
        f"Supports batch processing. Upload multiple images at once for {name_en} operations, greatly improving efficiency.",
        "All processing is done locally in your browser. Images are never uploaded to any server, ensuring privacy and security.",
        "Save processed images promptly — local cache is cleared on page refresh. Bookmark frequently used results."
    ]
    tips_ja = [
        f"複数の画像を一括アップロードして{name_en}処理が可能。作業効率が大幅に向上します。",
        "すべてブラウザ内でローカル処理されるため、画像がサーバーにアップロードされることはなく、プライバシーは完全に保護されます。",
        "処理後の画像はすぐに保存してください。ページ更新でキャッシュは消去されます。よく使う結果はブックマークをお勧めします。"
    ]
    tips_vi = [
        f"Hỗ trợ xử lý hàng loạt. Tải lên nhiều ảnh cùng lúc để thực hiện {name_vi if 'name_vi' in dir() else name_en}, tăng hiệu quả đáng kể.",
        "Tất cả xử lý đều tại máy cục bộ trong trình duyệt. Ảnh không bao giờ được tải lên máy chủ, đảm bảo quyền riêng tư.",
        "Lưu ảnh đã xử lý ngay — bộ nhớ đệm sẽ bị xóa khi làm mới trang."
    ]
    faqs = [
        ("支持哪些图片格式？", "支持 JPG、PNG、WebP、GIF、SVG、ICO、BMP 等主流图片格式。部分格式在处理后可能需要转换为其他格式。"),
        ("有图片大小限制吗？", "单张图片建议不超过 100MB，过大的图片可能会影响处理速度。对于超大图片，建议先压缩后再进行处理。"),
        ("可以批量处理吗？", f"可以。支持批量上传多张图片进行{name_zh}操作，处理完成后可以打包下载。")
    ]
    faqs_en = [
        ("What image formats are supported?", "JPG, PNG, WebP, GIF, SVG, ICO, BMP and more. Some formats may need conversion after processing."),
        ("Is there a file size limit?", "Maximum 100MB per image. Very large images may slow processing. Compress first for oversized files."),
        ("Can I batch process?", f"Yes. Upload multiple images for {name_en} and download them all at once.")
    ]
    faqs_ja = [
        ("対応している画像形式は？", "JPG、PNG、WebP、GIF、SVG、ICO、BMPなどの主要形式に対応。処理後に変換が必要な場合があります。"),
        ("ファイルサイズの制限は？", "1枚あたり最大100MB。大きすぎる画像は処理速度に影響する可能性があります。"),
        ("一括処理は可能ですか？", f"はい。複数の画像を一括アップロードして{name_en}処理が可能です。")
    ]
    faqs_vi = [
        ("Hỗ trợ định dạng ảnh nào?", "JPG, PNG, WebP, GIF, SVG, ICO, BMP và nhiều định dạng khác. Một số định dạng có thể cần chuyển đổi sau xử lý."),
        ("Có giới hạn kích thước file không?", "Tối đa 100MB mỗi ảnh. Ảnh quá lớn có thể làm chậm xử lý."),
        ("Có thể xử lý hàng loạt không?", f"Có. Tải lên nhiều ảnh để {name_en} và tải xuống tất cả cùng lúc.")
    ]
    related = [
        ("/tutorials/image-compress.html", "图片压缩"),
        ("/tutorials/image-convert.html", "图片格式转换"),
        ("/tutorials/image-resize.html", "图片尺寸修改")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:8][:4] if slug else "img",
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_pdf_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "📄 PDF工具"
    cat_label_en = "📄 PDF Tools"
    cat_label_ja = "📄 PDFツール"
    cat_label_vi = "📄 Công cụ PDF"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线PDF处理"
    title_en = f"{name_en} Tutorial: Online PDF Processing"
    title_ja = f"{name_en}チュートリアル：オンラインPDF処理"
    title_vi = f"{name_en} Hướng dẫn: Xử lý PDF trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，处理PDF文档。支持批量操作，所有处理在浏览器本地完成。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to process PDF documents. Batch operations supported, all local in browser."
    desc_ja = f"ZenTools のオンライン{name_en}ツールを使ってPDF文書を処理します。バッチ対応、すべてブラウザ内でローカル処理。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để xử lý tài liệu PDF. Hỗ trợ hàng loạt, xử lý cục bộ."
    func = f"ZenTools {name_zh}工具是一款专业的在线PDF处理工具，支持PDF文档的编辑、转换、压缩、加密等多种操作。所有处理均在浏览器本地完成，无需上传文件到服务器，确保文档安全。"
    func_en = f"ZenTools {name_en} is a professional online PDF tool supporting editing, conversion, compression, encryption and more. All processing is local in your browser — files never leave your device."
    func_ja = f"ZenTools {name_en}は、PDF文書の編集、変換、圧縮、暗号化などに対応したプロ仕様のオンラインPDFツールです。すべてブラウザ内でローカル処理。"
    func_vi = f"ZenTools {name_en} là công cụ PDF trực tuyến chuyên nghiệp hỗ trợ chỉnh sửa, chuyển đổi, nén, mã hóa và hơn thế nữa. Xử lý cục bộ trong trình duyệt."
    tips = [
        "支持批量处理多个PDF文件，一次上传多个文件可以同时处理，大大提升工作效率。",
        "PDF处理完成后建议及时下载保存，刷新页面后本地缓存会被清除，确保处理结果不丢失。",
        "对于加密PDF文档，需要先输入密码解密后才能进行后续编辑和转换操作。"
    ]
    tips_en = [
        "Batch process multiple PDFs at once, significantly improving efficiency.",
        "Download processed PDFs promptly — local cache is cleared on page refresh.",
        "Encrypted PDFs require password entry before editing or conversion."
    ]
    tips_ja = [
        "複数のPDFを一括処理可能。作業効率が大幅に向上します。",
        "処理後のPDFはすぐにダウンロードしてください。ページ更新でキャッシュは消去されます。",
        "暗号化されたPDFは、編集や変換の前にパスワードの入力が必要です。"
    ]
    tips_vi = [
        "Xử lý hàng loạt nhiều PDF cùng lúc, tăng hiệu quả đáng kể.",
        "Tải xuống PDF đã xử lý ngay — bộ nhớ đệm bị xóa khi làm mới trang.",
        "PDF đã mã hóa cần nhập mật khẩu trước khi chỉnh sửa hoặc chuyển đổi."
    ]
    faqs = [
        ("支持哪些PDF功能？", "支持PDF合并、拆分、压缩、加密、解密、转图片、转Word、转文本、添加水印、删除页面、旋转页面、排序页面、OCR识别等全套PDF处理功能。"),
        ("有文件大小限制吗？", "单个PDF文件建议不超过 100MB，超大文件处理速度会较慢。对于数百页的PDF文档，建议分批处理。"),
        ("处理后的PDF格式会变化吗？", "处理后的PDF会保持原有的版式和内容，不会出现格式错乱。对于扫描版PDF，可能需要使用OCR功能提取文字。")
    ]
    faqs_en = [
        ("What PDF features are supported?", "Merge, split, compress, encrypt, decrypt, convert to image/Word/text, add watermarks, delete/rotate/reorder pages, OCR and more."),
        ("Is there a file size limit?", "Maximum 100MB per PDF. Very large files may be slower. For hundreds of pages, process in batches."),
        ("Will the PDF format change after processing?", "Original layout and content are preserved. Scanned PDFs may need OCR for text extraction.")
    ]
    faqs_ja = [
        ("対応しているPDF機能は？", "結合、分割、圧縮、暗号化、復号、画像/Word/テキスト変換、透かし追加、ページ削除/回転/並べ替え、OCRなど。"),
        ("ファイルサイズの制限は？", "1ファイル最大100MB。非常に大きなファイルは処理が遅くなる場合があります。"),
        ("処理後にPDFの書式は変わりますか？", "元のレイアウトと内容は保持されます。スキャンPDFはOCR処理が必要な場合があります。")
    ]
    faqs_vi = [
        ("Chức năng PDF nào được hỗ trợ?", "Gộp, tách, nén, mã hóa, giải mã, chuyển đổi sang ảnh/Word/văn bản, thêm watermark, xóa/xoay/sắp xếp trang, OCR và hơn thế nữa."),
        ("Có giới hạn kích thước file không?", "Tối đa 100MB mỗi PDF. Tệp rất lớn có thể chậm hơn. Hàng trăm trang nên xử lý theo lô."),
        ("Định dạng PDF có thay đổi sau xử lý không?", "Bố cục và nội dung gốc được giữ nguyên. PDF scan có thể cần OCR để trích xuất văn bản.")
    ]
    related = [
        ("/tutorials/pdf-merge.html", "PDF合并"),
        ("/tutorials/pdf-split.html", "PDF拆分"),
        ("/tutorials/pdf-compress.html", "PDF压缩")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_ai_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🤖 AI工具"
    cat_label_en = "🤖 AI Tools"
    cat_label_ja = "🤖 AIツール"
    cat_label_vi = "🤖 Công cụ AI"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线AI生成"
    title_en = f"{name_en} Tutorial: Online AI Generation"
    title_ja = f"{name_en}チュートリアル：オンラインAI生成"
    title_vi = f"{name_en} Hướng dẫn: Tạo nội dung AI trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，利用AI快速生成内容。操作简单，即写即用。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to generate content with AI. Simple, write and use instantly."
    desc_ja = f"ZenTools のオンライン{name_en}ツールを使ってAIでコンテンツを素早く生成します。シンプルで即利用可能。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để tạo nội dung bằng AI. Đơn giản, viết và dùng ngay."
    func = f"ZenTools {name_zh}工具是一款智能AI辅助工具，通过先进技术帮助你快速生成高质量的内容。"
    func_en = f"ZenTools {name_en} is a smart AI-powered tool that helps you quickly generate high-quality content."
    func_ja = f"ZenTools {name_en}は、高品質なコンテンツを素早く生成するスマートなAI搭載ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ AI thông minh giúp bạn nhanh chóng tạo nội dung chất lượng cao."
    tips = [
        "输入的关键词或描述越详细具体，AI生成的内容就越精准。",
        "可以尝试多次生成并对比不同版本的结果，选择最符合需求的版本进行微调。",
        "生成的内容建议人工审阅一遍，确保专业术语和特定信息准确无误后再使用。"
    ]
    tips_en = [
        "The more detailed your input, the more accurate the AI-generated content will be.",
        "Try generating multiple times and compare results to pick the best version.",
        "Review generated content for accuracy before use, especially for specialized terminology."
    ]
    tips_ja = [
        "入力が詳細であればあるほど、AI生成の精度が向上します。",
        "複数回生成して結果を比較し、最適なバージョンを選択してください。",
        "専門用語や特定情報の正確性を確認してから使用することをお勧めします。"
    ]
    tips_vi = [
        "Đầu vào càng chi tiết, nội dung AI tạo ra càng chính xác.",
        "Thử tạo nhiều lần và so sánh kết quả để chọn phiên bản tốt nhất.",
        "Xem lại nội dung trước khi sử dụng, đặc biệt là thuật ngữ chuyên ngành."
    ]
    faqs = [
        ("AI生成的内容可以商用吗？", "可以。所有AI生成的内容归你所有，可以用于商业用途。"),
        ("支持中文输入吗？", "完全支持中文输入和输出。AI对中文的理解和生成能力出色。"),
        ("生成速度有多快？", "通常在几秒内就能生成结果。对于复杂的任务可能需要10-30秒。")
    ]
    faqs_en = [
        ("Can I use AI-generated content commercially?", "Yes. All AI-generated content belongs to you and can be used for commercial purposes."),
        ("Does it support Chinese input?", "Fully supports Chinese input and output. The AI has excellent Chinese language capabilities."),
        ("How fast is generation?", "Typically within seconds. Complex tasks may take 10-30 seconds.")
    ]
    faqs_ja = [
        ("AI生成コンテンツは商用利用できますか？", "はい。すべてのAI生成コンテンツはあなたの所有物で、商用利用可能です。"),
        ("中国語の入力に対応していますか？", "中国語の入出力を完全サポート。AIの中国語言語処理能力は優れています。"),
        ("生成速度はどのくらいですか？", "通常数秒以内。複雑なタスクでは10〜30秒かかる場合があります。")
    ]
    faqs_vi = [
        ("Nội dung do AI tạo có thể dùng cho mục đích thương mại không?", "Có. Tất cả nội dung do AI tạo đều thuộc sở hữu của bạn và có thể dùng cho mục đích thương mại."),
        ("Có hỗ trợ nhập tiếng Trung không?", "Hỗ trợ đầy đủ nhập và xuất tiếng Trung. AI có khả năng xử lý tiếng Trung xuất sắc."),
        ("Tốc độ tạo nhanh không?", "Thường trong vài giây. Tác vụ phức tạp có thể mất 10-30 giây.")
    ]
    related = [
        ("/tutorials/ai-writing.html", "AI写作"),
        ("/tutorials/ai-summary.html", "AI总结"),
        ("/tutorials/ai-translate.html", "AI翻译")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_text_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "📝 文本工具"
    cat_label_en = "📝 Text Tools"
    cat_label_ja = "📝 テキストツール"
    cat_label_vi = "📝 Công cụ văn bản"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线文本处理"
    title_en = f"{name_en} Tutorial: Online Text Processing"
    title_ja = f"{name_en}チュートリアル：オンラインテキスト処理"
    title_vi = f"{name_en} Hướng dẫn: Xử lý văn bản trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理文本数据。支持大段文字处理。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to quickly process text. Supports large volumes of text."
    desc_ja = f"ZenTools のオンライン{name_en}ツールを使ってテキストデータを素早く処理します。大量テキスト対応。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để xử lý văn bản nhanh chóng."
    func = f"ZenTools {name_zh}工具是一款实用的在线文本处理工具，帮助你对文本内容进行快速操作和转换。"
    func_en = f"ZenTools {name_en} is a practical online text processing tool for quick text manipulation and conversion."
    func_ja = f"ZenTools {name_en}は、テキストコンテンツの迅速な操作と変換を実現する実用的なオンラインテキスト処理ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ xử lý văn bản trực tuyến thực tế giúp thao tác và chuyển đổi văn bản nhanh chóng."
    tips = [
        "支持大量文本输入，可以处理数万字以上的内容。",
        "处理结果可以直接复制，也可以清空后重新输入。",
        "文本处理不涉及任何网络请求，所有操作在浏览器本地完成。"
    ]
    tips_en = [
        "Supports large text input — process tens of thousands of characters.",
        "Results can be copied directly or cleared and re-entered.",
        "All text processing is done locally in your browser, no network requests."
    ]
    tips_ja = [
        "数万字以上の大量テキスト入力に対応。",
        "処理結果は直接コピー可能。クリアして再入力もできます。",
        "テキスト処理はすべてブラウザ内でローカル実行され、ネットワークリクエストは不要です。"
    ]
    tips_vi = [
        "Hỗ trợ nhập văn bản lớn — xử lý hàng chục nghìn ký tự.",
        "Kết quả có thể sao chép trực tiếp hoặc xóa và nhập lại.",
        "Xử lý văn bản tại máy cục bộ trong trình duyệt, không cần yêu cầu mạng."
    ]
    faqs = [
        ("有文本长度限制吗？", "理论上没有长度限制，但超大的文本（如超过10万字）可能会影响处理速度。"),
        ("可以批量处理多段文本吗？", f"可以。支持一次性输入多段文本进行{name_zh}操作，处理结果会保留原始分段格式。"),
        ("处理结果会保存吗？", "所有处理都在浏览器本地完成，关闭页面后数据会被清除。建议将处理结果及时复制保存。")
    ]
    faqs_en = [
        ("Is there a text length limit?", "No theoretical limit, but very large texts (100K+ characters) may slow processing."),
        ("Can I batch process multiple text segments?", f"Yes. Input multiple text segments at once for {name_en}, preserving original formatting."),
        ("Are results saved?", "All processing is local. Data is cleared when you close the page. Save results promptly.")
    ]
    faqs_ja = [
        ("テキスト長の制限は？", "理論上は制限なし。ただし10万字を超えると処理が遅くなる可能性があります。"),
        ("複数のテキストを一括処理できますか？", f"はい。複数のテキストセグメントを一度に入力して{name_en}処理が可能です。"),
        ("処理結果は保存されますか？", "すべてローカル処理のため、ページを閉じるとデータは消去されます。すぐに保存してください。")
    ]
    faqs_vi = [
        ("Có giới hạn độ dài văn bản không?", "Không có giới hạn lý thuyết, nhưng văn bản rất lớn (100K+ ký tự) có thể làm chậm xử lý."),
        ("Có thể xử lý hàng loạt nhiều đoạn văn bản không?", f"Có. Nhập nhiều đoạn văn bản cùng lúc để {name_en}, giữ nguyên định dạng."),
        ("Kết quả có được lưu không?", "Xử lý cục bộ. Dữ liệu bị xóa khi đóng trang. Lưu kết quả ngay.")
    ]
    related = [
        ("/tutorials/word-count.html", "字数统计"),
        ("/tutorials/case-convert.html", "大小写转换"),
        ("/tutorials/find-replace.html", "查找替换")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_dev_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "💻 开发工具"
    cat_label_en = "💻 Dev Tools"
    cat_label_ja = "💻 開発ツール"
    cat_label_vi = "💻 Công cụ Dev"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线开发工具"
    title_en = f"{name_en} Tutorial: Online Dev Tool"
    title_ja = f"{name_en}チュートリアル：オンライン開発ツール"
    title_vi = f"{name_en} Hướng dẫn: Công cụ Dev trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，提升开发效率。开发者必备。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to boost development efficiency. Essential for developers."
    desc_ja = f"ZenTools のオンライン{name_en}ツールで開発効率を向上。開発者必携。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để tăng hiệu quả phát triển."
    func = f"ZenTools {name_zh}工具是一款专业的在线开发辅助工具，帮助开发者快速完成数据校验、格式化、调试等常见任务。"
    func_en = f"ZenTools {name_en} is a professional online developer tool for validation, formatting, debugging and more."
    func_ja = f"ZenTools {name_en}は、データ検証、フォーマット、デバッグなどを支援するプロ仕様のオンライン開発ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ phát triển trực tuyến chuyên nghiệp hỗ trợ xác thực, định dạng, gỡ lỗi."
    tips = [
        "支持格式化、校验和语法高亮显示，让代码和数据结构一目了然。",
        "处理结果可以直接复制，适合快速集成到项目中。",
        "对于大型JSON文件（超过100KB），建议分段处理或在本地使用专业工具。"
    ]
    tips_en = [
        "Supports formatting, validation and syntax highlighting for clear code/data visualization.",
        "Results can be copied directly for quick project integration.",
        "For large JSON files (100KB+), consider splitting or using a local tool."
    ]
    tips_ja = [
        "整形、検証、シンタックスハイライトに対応し、コードやデータが一目でわかります。",
        "結果は直接コピー可能。プロジェクトへの迅速な統合に最適。",
        "大きなJSONファイル（100KB以上）は分割処理をお勧めします。"
    ]
    tips_vi = [
        "Hỗ trợ định dạng, xác thực và tô sáng cú pháp để trực quan hóa mã/dữ liệu.",
        "Kết quả có thể sao chép trực tiếp để tích hợp nhanh vào dự án.",
        "Với tệp JSON lớn (100KB+), hãy cân nhắc chia nhỏ hoặc dùng công cụ cục bộ."
    ]
    faqs = [
        ("支持哪些开发功能？", "支持JSON格式化、对比、查看、正则测试、哈希生成等常见开发辅助功能。"),
        ("可以格式化JSON吗？", "可以。工具提供格式化（美化）和压缩（最小化）两种模式，一键切换。"),
        ("有文件大小限制吗？", "建议在浏览器中使用不超过500KB的JSON文件，超大文件建议分片处理。")
    ]
    faqs_en = [
        ("What developer features are supported?", "JSON formatting, diff, viewer, regex testing, hash generation and more."),
        ("Can I format JSON?", "Yes. Supports pretty-print (beautify) and minify modes with one-click toggle."),
        ("Is there a file size limit?", "JSON files under 500KB are recommended in browser. Split larger files.")
    ]
    faqs_ja = [
        ("どのような開発機能に対応していますか？", "JSON整形、比較、ビューア、正規表現テスト、ハッシュ生成など。"),
        ("JSONを整形できますか？", "はい。整形（美観）と圧縮（最小化）の2モードをワンクリックで切り替え。"),
        ("ファイルサイズの制限は？", "ブラウザでは500KB以下のJSONファイルを推奨。より大きなファイルは分割処理を。")
    ]
    faqs_vi = [
        ("Chức năng phát triển nào được hỗ trợ?", "Định dạng JSON, so sánh, xem, kiểm tra regex, tạo hash và nhiều hơn nữa."),
        ("Có thể định dạng JSON không?", "Có. Hỗ trợ chế độ làm đẹp và thu nhỏ với chuyển đổi một cú nhấp chuột."),
        ("Có giới hạn kích thước file không?", "Nên dùng tệp JSON dưới 500KB trong trình duyệt. Chia nhỏ tệp lớn hơn.")
    ]
    related = [
        ("/tutorials/json-formatter.html", "JSON格式化"),
        ("/tutorials/json-diff.html", "JSON对比"),
        ("/tutorials/regex-tester.html", "正则测试器")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_life_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🏠 生活工具"
    cat_label_en = "🏠 Life Tools"
    cat_label_ja = "🏠 生活ツール"
    cat_label_vi = "🏠 Công cụ cuộc sống"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线生活计算"
    title_en = f"{name_en} Tutorial: Online Life Calculator"
    title_ja = f"{name_en}チュートリアル：オンライン生活計算"
    title_vi = f"{name_en} Hướng dẫn: Máy tính đời sống trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，轻松完成日常计算。简单实用。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to easily handle daily calculations. Simple and practical."
    desc_ja = f"ZenTools のオンライン{name_en}ツールで日常の計算を簡単に。シンプルで実用的。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để tính toán hàng ngày dễ dàng."
    func = f"ZenTools {name_zh}工具是一款实用的在线生活计算工具，帮助你在日常生活中快速完成各种计算任务。操作简单，结果准确。"
    func_en = f"ZenTools {name_en} is a practical online tool for quick everyday calculations. Simple to use, accurate results."
    func_ja = f"ZenTools {name_en}は、日常のあらゆる計算を素早くこなす実用的なオンラインツールです。"
    func_vi = f"ZenTools {name_en} là công cụ trực tuyến thực tế cho các tính toán hàng ngày nhanh chóng."
    tips = [
        "计算结果可以多次查看和复制，适合在不同场景下使用。",
        "所有计算在浏览器本地完成，无需联网即可使用。",
        "建议收藏常用计算结果，方便下次直接使用。"
    ]
    tips_en = [
        "Results can be viewed and copied multiple times for different scenarios.",
        "All calculations are done locally in your browser, no internet needed.",
        "Bookmark frequently used results for quick access next time."
    ]
    tips_ja = [
        "結果は複数回表示・コピー可能。様々なシーンでご利用いただけます。",
        "すべてブラウザ内でローカル計算。インターネット接続不要。",
        "よく使う計算結果はブックマークして、次回すぐにご利用ください。"
    ]
    tips_vi = [
        "Kết quả có thể xem và sao chép nhiều lần cho các tình huống khác nhau.",
        "Tất cả tính toán tại máy cục bộ trong trình duyệt, không cần internet.",
        "Đánh dấu kết quả thường dùng để truy cập nhanh lần sau."
    ]
    faqs = [
        ("计算结果准确吗？", "工具使用JavaScript高精度运算，计算结果可靠。对于金融相关的计算，建议以银行官方结果为准。"),
        ("支持中文吗？", "完全支持中文界面和中文输入。工具提供中文、英文、日文、越南文四种语言。"),
        ("可以离线使用吗？", "部分功能支持离线使用。所有计算在浏览器本地完成，无需网络连接。")
    ]
    faqs_en = [
        ("Are the results accurate?", "The tool uses high-precision JavaScript arithmetic. For financial calculations, verify with official sources."),
        ("Does it support Chinese?", "Fully supports Chinese UI and input, plus English, Japanese, and Vietnamese."),
        ("Can I use it offline?", "Some features work offline. All calculations are local in your browser, no network needed.")
    ]
    faqs_ja = [
        ("計算結果は正確ですか？", "高精度JavaScript演算を使用。金融計算の場合は公式の情報でご確認ください。"),
        ("中国語に対応していますか？", "中国語UIと入力を完全サポート。英語、日本語、ベトナム語にも対応。"),
        ("オフライン使用できますか？", "一部機能はオフラインで使用可能。すべてブラウザ内でローカル計算。")
    ]
    faqs_vi = [
        ("Kết quả có chính xác không?", "Công cụ sử dụng số học JavaScript độ chính xác cao. Với tính toán tài chính, hãy kiểm tra với nguồn chính thức."),
        ("Có hỗ trợ tiếng Trung không?", "Hỗ trợ đầy đủ giao diện và nhập liệu tiếng Trung, cùng với tiếng Anh, Nhật và Việt."),
        ("Có thể dùng ngoại tuyến không?", "Một số chức năng hoạt động ngoại tuyến. Tính toán cục bộ trong trình duyệt.")
    ]
    related = [
        ("/tutorials/password-generator.html", "密码生成器"),
        ("/tutorials/unit-converter.html", "单位换算"),
        ("/tutorials/bmi-calculator.html", "BMI计算")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_finance_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "💰 金融工具"
    cat_label_en = "💰 Finance Tools"
    cat_label_ja = "💰 金融ツール"
    cat_label_vi = "💰 Công cụ tài chính"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线金融计算"
    title_en = f"{name_en} Tutorial: Online Finance Calculator"
    title_ja = f"{name_en}チュートリアル：オンライン金融計算"
    title_vi = f"{name_en} Hướng dẫn: Máy tính tài chính trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，轻松计算金融数据。财务规划必备。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to calculate financial data. Essential for financial planning."
    desc_ja = f"ZenTools のオンライン{name_en}ツールで金融データを簡単計算。財務計画に必須。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để tính toán dữ liệu tài chính."
    func = f"ZenTools {name_zh}工具是一款专业的在线金融计算工具，帮助你在理财规划、贷款计算、投资收益等场景中快速获取准确的计算结果。"
    func_en = f"ZenTools {name_en} is a professional online financial calculator for investment returns, loan payments, and more."
    func_ja = f"ZenTools {name_en}は、資産設計、ローン計算、投資収益などを素早く計算するプロ仕様のオンライン金融ツールです。"
    func_vi = f"ZenTools {name_en} là máy tính tài chính trực tuyến chuyên nghiệp cho lợi nhuận đầu tư, thanh toán khoản vay."
    tips = [
        "计算结果仅供参考，实际金融产品的条款和利率可能有所不同。",
        "建议在计算前仔细阅读说明，确保输入的参数符合你的实际情况。",
        "可以多次调整参数对比不同方案，选择最适合你的金融方案。"
    ]
    tips_en = [
        "Results are for reference only. Actual terms and rates may differ.",
        "Read instructions carefully before calculating. Ensure parameters match your situation.",
        "Adjust parameters to compare different scenarios and choose the best option."
    ]
    tips_ja = [
        "計算結果は参考値です。実際の金利や条件は異なる場合があります。",
        "計算前に説明をよく読み、入力パラメータが実際の状況と合っていることを確認してください。",
        "パラメータを調整して複数のシナリオを比較し、最適な選択肢を見つけてください。"
    ]
    tips_vi = [
        "Kết quả chỉ để tham khảo. Điều khoản và lãi suất thực tế có thể khác.",
        "Đọc hướng dẫn trước khi tính. Đảm bảo tham số phù hợp với tình huống của bạn.",
        "Điều chỉnh tham số để so sánh các kịch bản khác nhau và chọn phương án tốt nhất."
    ]
    faqs = [
        ("计算结果准确吗？", "工具使用标准金融公式计算，结果可靠。但实际金融产品可能存在手续费、额外费用等未包含在计算中。"),
        ("支持多种方案对比吗？", "可以。通过调整参数（如利率、期限、首付比例等）可以模拟多种方案，对比不同选择。"),
        ("有投资风险提示吗？", "金融投资存在风险，工具仅提供计算参考，不构成投资建议。投资前请充分了解产品风险。")
    ]
    faqs_en = [
        ("Are results accurate?", "Calculated using standard financial formulas. Actual products may have fees not included in calculation."),
        ("Can I compare multiple scenarios?", "Yes. Adjust parameters (rate, term, down payment) to simulate and compare different options."),
        ("Are there investment risk warnings?", "Investing carries risk. This tool provides reference only, not investment advice.")
    ]
    faqs_ja = [
        ("計算結果は正確ですか？", "標準的な金融計算式を使用。実際の商品には手数料などが含まれる場合があります。"),
        ("複数のシナリオを比較できますか？", "はい。パラメータ（金利、期間、頭金）を調整してシミュレーション・比較可能。"),
        ("投資リスクの注意喚起は？", "投資にはリスクが伴います。本ツールは参考値のみ提供し、投資助言ではありません。")
    ]
    faqs_vi = [
        ("Kết quả có chính xác không?", "Tính bằng công thức tài chính chuẩn. Sản phẩm thực tế có thể có phí không được tính."),
        ("Có thể so sánh nhiều kịch bản không?", "Có. Điều chỉnh tham số (lãi suất, thời hạn, trả trước) để mô phỏng và so sánh."),
        ("Có cảnh báo rủi ro đầu tư không?", "Đầu tư có rủi ro. Công cụ chỉ cung cấp tham khảo, không phải lời khuyên đầu tư.")
    ]
    related = [
        ("/tutorials/currency.html", "汇率换算"),
        ("/tutorials/loan-calculator.html", "贷款计算器"),
        ("/tutorials/vat-calculator.html", "增值税计算")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_audio_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🎵 音频工具"
    cat_label_en = "🎵 Audio Tools"
    cat_label_ja = "🎵 音声ツール"
    cat_label_vi = "🎵 Công cụ âm thanh"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线音频处理"
    title_en = f"{name_en} Tutorial: Online Audio Processing"
    title_ja = f"{name_en}チュートリアル：オンライン音声処理"
    title_vi = f"{name_en} Hướng dẫn: Xử lý âm thanh trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，快速处理音频文件。支持多种格式。"
    desc_en = f"Learn to use ZenTools online {name_en} tool to quickly process audio files. Supports multiple formats."
    desc_ja = f"ZenTools のオンライン{name_en}ツールで音声ファイルを素早く処理。複数形式対応。"
    desc_vi = f"Học cách sử dụng công cụ {name_en} trực tuyến của ZenTools để xử lý âm thanh nhanh chóng."
    func = f"ZenTools {name_zh}工具是一款专业的在线音频处理工具，支持 MP3、WAV、AAC、M4A 等主流音频格式。"
    func_en = f"ZenTools {name_en} is a professional online audio processing tool supporting MP3, WAV, AAC, M4A and more."
    func_ja = f"ZenTools {name_en}は、MP3、WAV、AAC、M4Aなどの主要音声形式に対応したオンライン音声処理ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ xử lý âm thanh trực tuyến chuyên nghiệp hỗ trợ MP3, WAV, AAC, M4A."
    tips = [
        "支持多种音频格式输入，处理后可以保存为常见格式。",
        "所有处理在浏览器本地完成，音频文件不会上传到服务器。",
        "处理后的音频建议及时保存，刷新页面后本地缓存会被清除。"
    ]
    tips_en = [
        "Supports various input formats. Output can be saved in common formats.",
        "All processing is local in your browser. Audio files never leave your device.",
        "Save processed audio promptly. Local cache is cleared on page refresh."
    ]
    tips_ja = [
        "多様な入力形式に対応。出力は一般的な形式で保存可能。",
        "すべてブラウザ内でローカル処理。音声ファイルがサーバーに送信されることはありません。",
        "処理後の音声はすぐに保存してください。ページ更新でキャッシュは消去されます。"
    ]
    tips_vi = [
        "Hỗ trợ nhiều định dạng đầu vào. Đầu ra có thể lưu ở định dạng phổ biến.",
        "Xử lý cục bộ trong trình duyệt. Tệp âm thanh không bao giờ rời khỏi thiết bị của bạn.",
        "Lưu âm thanh đã xử lý ngay. Bộ nhớ đệm bị xóa khi làm mới trang."
    ]
    faqs = [
        ("支持哪些音频格式？", "支持 MP3、WAV、AAC、M4A、FLAC、OGG 等主流音频格式。部分格式在处理后可能需要转换为其他格式。"),
        ("有文件大小限制吗？", "单个音频文件建议不超过 100MB。对于超长音频（如超过1小时的录音），建议分段处理。"),
        ("可以批量处理音频吗？", "部分功能支持批量上传多个音频文件进行处理。")
    ]
    faqs_en = [
        ("What audio formats are supported?", "MP3, WAV, AAC, M4A, FLAC, OGG and more. Some formats may need conversion after processing."),
        ("Is there a file size limit?", "Maximum 100MB per file. For very long audio (1hr+), process in segments."),
        ("Can I batch process audio?", "Some features support batch upload and processing of multiple files.")
    ]
    faqs_ja = [
        ("対応している音声形式は？", "MP3、WAV、AAC、M4A、FLAC、OGGなど。処理後に変換が必要な場合があります。"),
        ("ファイルサイズの制限は？", "1ファイル最大100MB。長時間音声（1時間以上）は分割処理をお勧めします。"),
        ("音声を一括処理できますか？", "一部機能は複数ファイルの一括アップロード・処理に対応しています。")
    ]
    faqs_vi = [
        ("Định dạng âm thanh nào được hỗ trợ?", "MP3, WAV, AAC, M4A, FLAC, OGG và nhiều hơn nữa. Một số định dạng có thể cần chuyển đổi sau xử lý."),
        ("Có giới hạn kích thước file không?", "Tối đa 100MB mỗi tệp. Âm thanh rất dài (1 tiếng+) nên xử lý theo đoạn."),
        ("Có thể xử lý hàng loạt âm thanh không?", "Một số chức năng hỗ trợ tải lên và xử lý hàng loạt nhiều tệp.")
    ]
    related = [
        ("/tutorials/audio-merge.html", "音频合并"),
        ("/tutorials/audio-cutter.html", "音频裁剪"),
        ("/tutorials/tts.html", "文字转语音")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
    }

def make_seo_tutorial(slug, name_zh, name_en, tool_url):
    cat_label = "🔍 SEO工具"
    cat_label_en = "🔍 SEO Tools"
    cat_label_ja = "🔍 SEOツール"
    cat_label_vi = "🔍 Công cụ SEO"
    svg_file = f"{slug}-step1.svg"
    title = f"{name_zh}教程：在线SEO分析"
    title_en = f"{name_en} Tutorial: Online SEO Analysis"
    title_ja = f"{name_en}チュートリアル：オンラインSEO分析"
    title_vi = f"{name_en} Hướng dẫn: Phân tích SEO trực tuyến"
    desc = f"学会使用 ZenTools 在线{name_zh}工具，优化网站SEO表现。SEO从业者必备。"
    desc_en = f"Learn ZenTools online {name_en} tool to optimize your website's SEO. Essential for SEO professionals."
    desc_ja = f"ZenTools のオンライン{name_en}ツールでWebサイトのSEOを最適化。SEO担当者必携。"
    desc_vi = f"Học công cụ {name_en} trực tuyến của ZenTools để tối ưu SEO website. Cần thiết cho chuyên gia SEO."
    func = f"ZenTools {name_zh}工具是一款专业的在线SEO分析工具，帮助你全面检查网站的SEO设置和优化机会。"
    func_en = f"ZenTools {name_en} is a professional online SEO analysis tool for comprehensive site audits and optimization."
    func_ja = f"ZenTools {name_en}は、総合的なサイト監査と最適化のためのプロ仕様のオンラインSEO分析ツールです。"
    func_vi = f"ZenTools {name_en} là công cụ phân tích SEO trực tuyến chuyên nghiệp cho kiểm toán và tối ưu hóa trang web."
    tips = [
        "建议定期使用工具检查网站SEO状态，及时发现和解决新问题。",
        "SEO优化是一个长期过程，工具提供的建议需要持续跟踪和调整。",
        "将工具的检查结果与搜索引擎的官方指南结合使用，可以获得最佳优化效果。"
    ]
    tips_en = [
        "Regularly audit your site's SEO health to catch and fix issues early.",
        "SEO is a long-term process. Track and adjust based on the tool's recommendations.",
        "Combine the tool's results with official search engine guidelines for best results."
    ]
    tips_ja = [
        "定期的にサイトのSEO状態をチェックし、問題を早期に発見・修正しましょう。",
        "SEOは長期的なプロセスです。ツールの提案を継続的に追跡・調整しましょう。",
        "ツールの結果と検索エンジンの公式ガイドラインを組み合わせて最適な効果を得ましょう。"
    ]
    tips_vi = [
        "Kiểm tra SEO định kỳ để phát hiện và khắc phục vấn đề sớm.",
        "SEO là quá trình dài hạn. Theo dõi và điều chỉnh dựa trên khuyến nghị của công cụ.",
        "Kết hợp kết quả công cụ với hướng dẫn chính thức của công cụ tìm kiếm để đạt kết quả tốt nhất."
    ]
    faqs = [
        ("检查结果可靠吗？", "工具基于搜索引擎的官方指南和SEO最佳实践生成检查结果，具有参考价值。"),
        ("支持哪种类型的网站？", "支持任何基于HTML的网站，包括静态网站、博客、电商平台等。"),
        ("可以导出报告吗？", "部分功能支持导出检查报告，方便团队共享和记录优化进度。")
    ]
    faqs_en = [
        ("Are the results reliable?", "Based on official search engine guidelines and SEO best practices. Final optimization depends on actual conditions."),
        ("What types of sites are supported?", "Any HTML-based site including static sites, blogs, and e-commerce platforms."),
        ("Can I export reports?", "Some features support report export for team sharing and progress tracking.")
    ]
    faqs_ja = [
        ("結果は信頼できますか？", "検索エンジンの公式ガイドラインとSEOベストプラクティスに基づいています。"),
        ("どのようなサイトに対応していますか？", "静的サイト、ブログ、ECプラットフォームなどHTMLベースのサイトに対応。"),
        ("レポートをエクスポートできますか？", "一部機能はレポートのエクスポートに対応。チーム共有や進捗管理に便利。")
    ]
    faqs_vi = [
        ("Kết quả có đáng tin cậy không?", "Dựa trên hướng dẫn chính thức của công cụ tìm kiếm và thực hành SEO tốt nhất."),
        ("Loại trang web nào được hỗ trợ?", "Bất kỳ trang HTML nào bao gồm trang tĩnh, blog và nền tảng thương mại điện tử."),
        ("Có thể xuất báo cáo không?", "Một số chức năng hỗ trợ xuất báo cáo để chia sẻ nhóm và theo dõi tiến độ.")
    ]
    related = [
        ("/tutorials/seo-keyword-research.html", "关键词研究"),
        ("/tutorials/seo-meta-generator.html", "Meta标签生成"),
        ("/tutorials/seo-robots-generator.html", "Robots.txt生成")
    ]
    return {
        "tool_id": slug, "title_zh": title, "desc_zh": desc, "func_zh": func,
        "title_en": title_en, "desc_en": desc_en, "func_en": func_en,
        "title_ja": title_ja, "desc_ja": desc_ja, "func_ja": func_ja,
        "title_vi": title_vi, "desc_vi": desc_vi, "func_vi": func_vi,
        "cat_label": cat_label, "cat_label_en": cat_label_en, "cat_label_ja": cat_label_ja, "cat_label_vi": cat_label_vi,
        "duration": "2", "tool_url": tool_url, "svg_file": svg_file, "step_keys": slug[:4],
        "tips": tips, "faqs": faqs,
        "tips_en": tips_en, "faqs_en": faqs_en,
        "tips_ja": tips_ja, "faqs_ja": faqs_ja,
        "tips_vi": tips_vi, "faqs_vi": faqs_vi,
        "related": related
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