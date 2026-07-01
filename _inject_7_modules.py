#!/usr/bin/env python3
"""Inject 7 SEO content modules into all tool pages.

Modules: 工具简介 / 适合哪些人 / 优缺点 / 使用教程 / FAQ / 替代工具 / 更新记录
"""
import json, os, re, glob

BASE = "/workspace"
TOOLS_DATA_PATH = f"{BASE}/data/tools-data.json"

# Exclude these directories and files
EXCLUDE_DIRS = {'tutorials', 'guides', 'node_modules', '.git', 'pdf_tools'}
EXCLUDE_FILES = {'index.html', 'tools.html', 'categories.html', 'articles.html',
                 'examples.html', 'file-processing.html', 'notes.html', 'stats.html',
                 'privacy.html', 'terms.html', 'contact.html', 'about.html',
                 'sitemap.xml', 'test-ui.html', 'recovery-console.html',
                 'googlec2f7e3dbccb44280.html'}

with open(TOOLS_DATA_PATH) as f:
    tools_data = json.load(f)

tools_map = {}
for t in tools_data.get('tools', []):
    slug = t.get('slug', '')
    if slug:
        tools_map[slug] = t


# ===== Category-specific content templates =====
CATEGORY_CONTENT = {
    "PDF工具": {
        "audience": "需要处理PDF文档的办公人员、学生、行政文员、律师、教师及所有需要日常编辑和转换PDF文件的用户。",
        "audience_en": "Office workers, students, administrators, lawyers, teachers, and anyone who needs to edit and convert PDF files daily.",
        "audience_ja": "PDFドキュメントを扱うオフィスワーカー、学生、事務職、弁護士、教員など。",
        "audience_vi": "Văn phòng, sinh viên, nhân viên văn phòng, luật sư, giáo viên và người dùng cần xử lý PDF hàng ngày.",
        "pros": [
            "完全免费，无需注册即可使用",
            "浏览器本地处理，文件不会上传服务器",
            "支持批量操作，一次处理多个文件",
            "保持原始排版和格式不变"
        ],
        "pros_en": ["Completely free, no registration required", "Local browser processing, files stay private", "Batch processing supported", "Preserves original layout and formatting"],
        "pros_ja": ["完全無料、登録不要", "ブラウザ内で処理、ファイルをアップロードしない", "バッチ処理対応", "元のレイアウトを保持"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần đăng ký", "Xử lý trong trình duyệt, tệp không tải lên server", "Hỗ trợ xử lý hàng loạt", "Giữ nguyên bố cục ban đầu"],
        "cons": [
            "超大PDF文件（超过200MB）处理速度较慢",
            "部分复杂格式（如扫描版）可能需要OCR辅助",
            "处理过程中请勿关闭浏览器标签页"
        ],
        "cons_en": ["Large PDFs (over 200MB) process slowly", "Scanned PDFs may need OCR assistance", "Do not close the browser tab during processing"],
        "cons_ja": ["大容量PDF（200MB以上）は処理が遅い", "スキャン版PDFはOCRが必要になる場合あり", "処理中はブラウザタブを閉じないでください"],
        "cons_vi": ["PDF lớn (trên 200MB) xử lý chậm", "PDF quét có thể cần hỗ trợ OCR", "Không đóng tab trình duyệt trong khi xử lý"],
        "faqs": [
            ("支持哪些PDF功能？", "支持PDF合并、拆分、压缩、加密、解密、转图片、转Word、转文本、添加水印、删除页面、旋转页面、排序页面、OCR识别等全套PDF处理功能。"),
            ("有文件大小限制吗？", "单个PDF文件建议不超过 200MB，超大文件处理速度会较慢。对于数百页的PDF文档，建议分批处理。"),
            ("处理安全吗？", "完全安全。所有处理在浏览器本地完成，文件不会上传到任何服务器，确保文档隐私。")
        ],
        "alternatives": [
            ("iLovePDF", "https://www.ilovepdf.com/", "知名在线PDF工具，功能全面"),
            ("SmallPDF", "https://smallpdf.com/", "简洁易用的PDF工具，适合轻度使用"),
            ("PDF24", "https://tools.pdf24.org/", "完全免费的PDF工具箱，支持离线")
        ],
        "tutorial_tip": "PDF工具支持批量操作，建议一次上传多个文件以节省时间。",
        "changelog": [
            "2026-07-01：增加批量操作功能，提升处理效率",
            "2026-06-23：修复大文件处理卡顿问题",
            "2026-06-21：新增PDF OCR识别功能"
        ]
    },
    "图片工具": {
        "audience": "设计师、自媒体创作者、电商运营、内容编辑、社交媒体运营者及所有需要快速处理图片文件的用户。",
        "audience_en": "Designers, content creators, e-commerce operators, editors, social media managers, and anyone who needs to process images quickly.",
        "audience_ja": "デザイナー、コンテンツ作成者、EC運営、編集者、ソーシャルメディア担当者など。",
        "audience_vi": "Nhà thiết kế, người sáng tạo nội dung, vận hành thương mại điện tử, biên tập viên và người dùng cần xử lý hình ảnh.",
        "pros": [
            "完全免费，无需下载安装任何软件",
            "浏览器本地处理，图片不会上传服务器",
            "支持JPG、PNG、WebP、GIF、SVG等多种格式",
            "支持批量处理，一次处理多张图片"
        ],
        "pros_en": ["Completely free, no software to install", "Local browser processing, images stay private", "Supports JPG, PNG, WebP, GIF, SVG formats", "Batch processing supported"],
        "pros_ja": ["完全無料、ソフトウェアインストール不要", "ブラウザ内で処理、画像をアップロードしない", "JPG、PNG、WebP、GIF、SVG形式対応", "バッチ処理対応"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần cài đặt", "Xử lý trong trình duyệt, hình ảnh không tải lên server", "Hỗ trợ JPG, PNG, WebP, GIF, SVG", "Hỗ trợ xử lý hàng loạt"],
        "cons": [
            "复杂滤镜和高级编辑功能不如专业软件",
            "超大图片（超过100MB）处理速度较慢",
            "不支持RAW格式等专业相机文件"
        ],
        "cons_en": ["Advanced editing features limited compared to pro software", "Very large images (over 100MB) process slowly", "Does not support RAW format files"],
        "cons_ja": ["プロソフトほどの高度な編集機能なし", "大容量画像（100MB以上）は処理が遅い", "RAW形式などの専用カメラファイル対応なし"],
        "cons_vi": ["Tính năng chỉnh sửa cao cấp hạn chế", "Hình ảnh rất lớn (trên 100MB) xử lý chậm", "Không hỗ trợ định dạng RAW"],
        "faqs": [
            ("支持哪些图片格式？", "支持 JPG、PNG、WebP、GIF、SVG、ICO、BMP 等主流图片格式。部分格式在处理后可能需要转换为其他格式。"),
            ("有图片大小限制吗？", "单张图片建议不超过 100MB，过大的图片可能会影响处理速度。"),
            ("可以批量处理吗？", "可以。多数工具支持批量上传多张图片进行处理，处理完成后可以打包下载。")
        ],
        "alternatives": [
            ("Canva", "https://www.canva.com/", "在线设计平台，模板丰富"),
            ("Fotor", "https://www.fotor.com/", "在线图片编辑器，滤镜丰富"),
            ("Pixlr", "https://pixlr.com/", "功能强大的在线图片编辑器")
        ],
        "tutorial_tip": "图片压缩建议在保持清晰度的前提下选择WebP格式，体积比JPG小25-35%。",
        "changelog": [
            "2026-07-01：增加批量处理功能，支持一次处理多张图片",
            "2026-06-25：新增WebP格式支持，体积更小",
            "2026-06-21：优化压缩算法，提升压缩效率"
        ]
    },
    "AI工具": {
        "audience": "内容创作者、文案工作者、自媒体运营者、学生、开发者、翻译工作者及所有需要AI辅助提高工作效率的用户。",
        "audience_en": "Content creators, copywriters, social media managers, students, developers, translators, and anyone who needs AI assistance to improve productivity.",
        "audience_ja": "コンテンツ作成者、コピーライター、ソーシャルメディア担当者、学生、開発者、翻訳者など。",
        "audience_vi": "Người sáng tạo nội dung, biên tập viên, quản lý mạng xã hội, sinh viên, lập trình viên và người dùng cần hỗ trợ AI.",
        "pros": [
            "AI生成内容快速高效，大幅节省创作时间",
            "支持多种内容类型：文章、邮件、代码、翻译等",
            "无需注册，即开即用",
            "支持中文、英文、日文等多语言输入输出"
        ],
        "pros_en": ["AI-generated content is fast and efficient", "Supports various content types: articles, emails, code, translations", "No registration, instant use", "Multi-language support"],
        "pros_ja": ["AI生成コンテンツは高速で効率的", "記事、メール、コード、翻訳など多様なコンテンツタイプ対応", "登録不要、即利用可能", "多言語対応"],
        "pros_vi": ["Nội dung AI nhanh và hiệu quả", "Hỗ trợ nhiều loại: bài viết, email, mã, dịch thuật", "Không cần đăng ký, dùng ngay", "Hỗ trợ đa ngôn ngữ"],
        "cons": [
            "AI生成内容需要人工审核，确保准确性",
            "复杂专业领域的生成质量可能不如人工",
            "不适合需要高度创意的原创内容"
        ],
        "cons_en": ["AI content needs human review for accuracy", "Quality may vary for specialized professional topics", "Not suitable for highly creative original content"],
        "cons_ja": ["AI生成コンテンツは正確性の人間レビューが必要", "専門分野では品質が変動する場合あり", "高 creativity のオリジナルコンテンツには不向き"],
        "cons_vi": ["Nội dung AI cần xem xét thủ công", "Chất lượng có thể thay đổi cho chủ đề chuyên môn", "Không phù hợp với nội dung sáng tạo cao"],
        "faqs": [
            ("AI生成的内容可以商用吗？", "可以。所有AI生成的内容归你所有，可以用于商业用途，包括社交媒体、营销材料、博客文章等场景。"),
            ("支持中文输入吗？", "完全支持中文输入和输出。AI对中文的理解和生成能力出色，可以流畅地进行中文内容创作。"),
            ("生成速度有多快？", "通常在几秒内就能生成结果。对于复杂的任务或较长的内容，可能需要10-30秒。")
        ],
        "alternatives": [
            ("ChatGPT", "https://chat.openai.com/", "OpenAI的对话AI，擅长长文本生成"),
            ("Claude", "https://claude.ai/", "Anthropic的对话AI，逻辑推理能力强"),
            ("Gemini", "https://gemini.google.com/", "Google的多模态AI助手")
        ],
        "tutorial_tip": "输入提示词越详细具体，AI生成的内容就越精准。建议包含主题、风格、长度等关键信息。",
        "changelog": [
            "2026-07-01：新增AI社交媒体文案生成器",
            "2026-06-28：优化中文理解能力，生成质量提升",
            "2026-06-23：新增AI代码解释和注释功能"
        ]
    },
    "开发工具": {
        "audience": "程序员、前端开发者、全栈工程师、运维工程师、API开发者及所有需要数据格式化、代码调试和工具辅助的开发人员。",
        "audience_en": "Programmers, frontend developers, full-stack engineers, DevOps, API developers, and anyone who needs data formatting, code debugging, and tool assistance.",
        "audience_ja": "プログラマー、フロントエンド開発者、フルスタックエンジニア、DevOps、API開発者など。",
        "audience_vi": "Lập trình viên, frontend developer, full-stack engineer, DevOps và người dùng cần định dạng dữ liệu, gỡ lỗi mã.",
        "pros": [
            "完全免费，无需安装任何开发环境",
            "浏览器本地处理，代码和数据不会上传服务器",
            "支持多种格式：JSON、XML、CSS、JS、SQL等",
            "实时预览和语法高亮，提升开发效率"
        ],
        "pros_en": ["Completely free, no development environment needed", "Local browser processing, code stays private", "Supports JSON, XML, CSS, JS, SQL formats", "Real-time preview and syntax highlighting"],
        "pros_ja": ["完全無料、開発環境不要", "ブラウザ内で処理、コードをアップロードしない", "JSON、XML、CSS、JS、SQL形式対応", "リアルタイムプレビューとシンタックスハイライト"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần môi trường phát triển", "Xử lý trong trình duyệt, mã không tải lên server", "Hỗ trợ JSON, XML, CSS, JS, SQL", "Xem trước realtime và highlight cú pháp"],
        "cons": [
            "大型项目代码（超过500KB）处理速度较慢",
            "不支持项目级别的依赖管理和构建",
            "部分高级调试功能需要专业IDE"
        ],
        "cons_en": ["Large projects (over 500KB) process slowly", "Does not support project-level dependency management", "Advanced debugging requires a professional IDE"],
        "cons_ja": ["大規模プロジェクト（500KB以上）は処理が遅い", "プロジェクトレベルの依存関係管理なし", "高度なデバッグにはプロ用IDEが必要"],
        "cons_vi": ["Dự án lớn (trên 500KB) xử lý chậm", "Không hỗ trợ quản lý phụ thuộc cấp dự án", "Gỡ lỗi cao cấp cần IDE chuyên nghiệp"],
        "faqs": [
            ("支持哪些数据格式？", "支持标准JSON、XML格式，以及CSS、JavaScript、SQL等代码格式。工具会校验语法的正确性并提供格式化功能。"),
            ("可以格式化代码吗？", "可以。工具提供格式化（美化）和压缩（最小化）两种模式，一键切换。"),
            ("有文件大小限制吗？", "建议在浏览器中使用不超过500KB的文件，超大文件建议分片处理。")
        ],
        "alternatives": [
            ("JSONLint", "https://jsonlint.com/", "专业的JSON格式化和校验工具"),
            ("Regex101", "https://regex101.com/", "强大的正则表达式测试和调试平台"),
            ("Carbon", "https://carbon.now.sh/", "代码截图生成工具，适合分享")
        ],
        "tutorial_tip": "处理敏感代码（如API Key）时，请确保浏览器已关闭其他标签页。处理结果可以直接复制到项目中。",
        "changelog": [
            "2026-07-01：新增SQL格式化功能，支持MySQL/PostgreSQL/SQLite",
            "2026-06-25：优化JSON性能，支持500KB以上大文件",
            "2026-06-21：新增正则表达式可视化调试功能"
        ]
    },
    "生活工具": {
        "audience": "普通用户、学生、上班族、家庭用户及所有需要日常计算、密码管理、时间管理、单位换算等生活辅助功能的用户。",
        "audience_en": "General users, students, office workers, families, and anyone who needs daily calculation, password management, time management, unit conversion, and other life assistance features.",
        "audience_ja": "一般ユーザー、学生、オフィスワーカー、家庭ユーザー、日常生活の計算やパスワード管理を必要なユーザー。",
        "audience_vi": "Người dùng phổ thông, sinh viên, nhân viên văn phòng, gia đình và người dùng cần tính toán hàng ngày, quản lý mật khẩu.",
        "pros": [
            "完全免费，无需注册即可使用",
            "浏览器本地计算，无需联网",
            "界面简洁直观，操作零门槛",
            "覆盖日常生活各种计算场景"
        ],
        "pros_en": ["Completely free, no registration required", "Local browser calculation, no internet needed", "Simple and intuitive interface", "Covers various daily calculation scenarios"],
        "pros_ja": ["完全無料、登録不要", "ブラウザ内計算、インターネット不要", "シンプルで直感的なインターフェース", "日常生活の各種計算シナリオを網羅"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần đăng ký", "Tính toán trong trình duyệt, không cần internet", "Giao diện đơn giản và trực quan", "Phủ trùm các tình huống tính toán hàng ngày"],
        "cons": [
            "部分计算结果仅供参考，以官方数据为准",
            "复杂的金融计算可能需要专业软件",
            "不支持历史记录和云端同步"
        ],
        "cons_en": ["Some calculation results are for reference only", "Complex financial calculations may need professional software", "No history records or cloud sync"],
        "cons_ja": ["計算結果は参考用、公式データに準拠", "複雑な金融計算には専門ソフトが必要", "履歴記録やクラウド同期なし"],
        "cons_vi": ["Một số kết quả chỉ mang tính tham khảo", "Tính toán tài chính phức tạp cần phần mềm chuyên nghiệp", "Không hỗ trợ lịch sử hoặc đồng bộ đám mây"],
        "faqs": [
            ("计算结果准确吗？", "工具使用标准计算公式，结果可靠。但实际产品可能存在手续费、额外费用等未包含在计算中。"),
            ("可以离线使用吗？", "部分功能支持离线使用。所有计算在浏览器本地完成，无需网络连接。"),
            ("数据会保存吗？", "所有计算都在浏览器本地完成，关闭页面后数据会被清除。建议将重要结果及时记录。")
        ],
        "alternatives": [
            ("Calculator.net", "https://www.calculator.net/", "综合计算器网站，功能全面"),
            ("Unit Converter", "https://www.unitconverters.net/", "专业单位换算工具"),
            ("Password Generator", "https://passwordsgenerator.net/", "随机密码生成器")
        ],
        "tutorial_tip": "建议将常用计算结果保存截图或复制粘贴到备忘录中，刷新页面后数据会被清除。",
        "changelog": [
            "2026-07-01：新增日本签证天数计算器，支持多次往返",
            "2026-06-28：优化密码生成算法，安全性提升",
            "2026-06-23：新增倒计时和正计时工具"
        ]
    },
    "金融工具": {
        "audience": "理财爱好者、贷款申请人、投资者、财务人员、自由职业者及所有需要进行贷款计算、投资理财和税务计算的用户。",
        "audience_en": "Investors, loan applicants, financial planners, accountants, freelancers, and anyone who needs loan calculation, investment planning, and tax calculation.",
        "audience_ja": "投資家、融資申請者、ファイナンスプランナー、会計士、フリーランスなど。",
        "audience_vi": "Nhà đầu tư, người vay vốn, kế toán, freelancer và người dùng cần tính toán vay vốn, đầu tư và thuế.",
        "pros": [
            "专业金融公式计算，结果准确可靠",
            "完全免费，无需注册即可使用",
            "支持多种方案对比，辅助决策",
            "浏览器本地计算，数据完全安全"
        ],
        "pros_en": ["Professional financial formulas, accurate results", "Completely free, no registration required", "Multiple scenario comparison for decision support", "Local browser calculation, data is secure"],
        "pros_ja": ["専門の金融式計算、正確な結果", "完全無料、登録不要", "複数のシナリオ比較で意思決定支援", "ブラウザ内計算、データが安全"],
        "pros_vi": ["Công thức tài chính chuyên nghiệp, kết quả chính xác", "Hoàn toàn miễn phí, không cần đăng ký", "So sánh nhiều kịch bản hỗ trợ ra quyết định", "Tính toán trong trình duyệt, dữ liệu an toàn"],
        "cons": [
            "实际金融产品条款可能有所不同",
            "不包含隐性费用（如管理费、提前还款违约金）",
            "仅供参考，不构成投资建议"
        ],
        "cons_en": ["Actual product terms may vary", "Does not include hidden fees (management fees, early repayment penalties)", "For reference only, not investment advice"],
        "cons_ja": ["実際の商品条件は異なる場合あり", "見えない手数料（管理費、早期返済違約金）は含まない", "参考用、投資アドバイスではない"],
        "cons_vi": ["Điều khoản sản phẩm thực tế có thể khác", "Không bao gồm phí ẩn (phí quản lý, phạt trả nợ sớm)", "Chỉ mang tính tham khảo, không phải lời khuyên đầu tư"],
        "faqs": [
            ("计算结果准确吗？", "工具使用标准金融公式计算，结果可靠。但实际金融产品可能存在手续费、额外费用等未包含在计算中。"),
            ("可以对比不同方案吗？", "可以。通过调整参数（如利率、期限、首付比例等）可以模拟多种方案，对比不同选择。"),
            ("有投资风险提示吗？", "金融投资存在风险，工具仅提供计算参考，不构成投资建议。投资前请充分了解产品风险。")
        ],
        "alternatives": [
            ("贷款计算器", "https://www.calculator.net/loan-calculator.html", "知名贷款计算器，支持多种贷款类型"),
            ("投资回报率计算器", "https://www.investor.gov/financial-tools-calculators/calculators/return-investment", "美国证券投资者保护局官方工具"),
            ("Mortgage Calculator", "https://www.bankrate.com/calculators/mortgages/mortgage-calculator.aspx", "Bankrate房贷计算器")
        ],
        "tutorial_tip": "计算前请仔细阅读说明，确保输入的参数符合实际情况。建议多次调整参数对比不同方案。",
        "changelog": [
            "2026-07-01：新增股票手续费计算器，支持A股/港股/美股",
            "2026-06-25：优化房贷计算器，增加提前还款功能",
            "2026-06-21：新增通货膨胀计算器，评估实际购买力"
        ]
    },
    "音频工具": {
        "audience": "播客创作者、短视频创作者、音频编辑、有声读物制作者、音乐爱好者及所有需要录制、编辑和转换音频文件的用户。",
        "audience_en": "Podcast creators, short video creators, audio editors, audiobook makers, music enthusiasts, and anyone who needs to record, edit, and convert audio files.",
        "audience_ja": "ポッドキャスト作成者、ショート動画作成者、オーディオエディター、オーディオブック制作者、音楽愛好家など。",
        "audience_vi": "Tạo podcast, tạo video ngắn, biên tập âm thanh, người yêu âm nhạc và người dùng cần ghi, chỉnh sửa và chuyển đổi âm thanh.",
        "pros": [
            "完全免费，无需下载专业音频软件",
            "浏览器本地处理，音频不会上传服务器",
            "支持MP3、WAV、AAC、M4A、FLAC、OGG等格式",
            "操作简单，适合初学者快速上手"
        ],
        "pros_en": ["Completely free, no professional audio software needed", "Local browser processing, audio stays private", "Supports MP3, WAV, AAC, M4A, FLAC, OGG formats", "Simple operation, beginner-friendly"],
        "pros_ja": ["完全無料、プロのオーディオソフト不要", "ブラウザ内で処理、オーディオをアップロードしない", "MP3、WAV、AAC、M4A、FLAC、OGG形式対応", "簡単操作、初心者にも使いやすい"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần phần mềm âm thanh chuyên nghiệp", "Xử lý trong trình duyệt, âm thanh không tải lên server", "Hỗ trợ MP3, WAV, AAC, M4A, FLAC, OGG", "操作简单, phù hợp người mới"],
        "cons": [
            "复杂的多轨编辑功能不如专业软件",
            "超长音频（超过1小时）处理速度较慢",
            "不支持专业的音频效果插件"
        ],
        "cons_en": ["Complex multi-track editing limited compared to pro software", "Very long audio (over 1 hour) processes slowly", "Does not support professional audio plugins"],
        "cons_ja": ["複雑なマルチトラック編集はプロソフトより制限", "非常に長いオーディオ（1時間以上）は処理が遅い", "プロ用オーディオプラグイン対応なし"],
        "cons_vi": ["Chỉnh sửa đa track phức tạp hạn chế", "Âm thanh rất dài (trên 1 tiếng) xử lý chậm", "Không hỗ trợ plugin âm thanh chuyên nghiệp"],
        "faqs": [
            ("支持哪些音频格式？", "支持 MP3、WAV、AAC、M4A、FLAC、OGG 等主流音频格式。部分格式在处理后可能需要转换为其他格式。"),
            ("可以批量处理音频吗？", "部分功能支持批量上传多个音频文件进行处理。"),
            ("处理安全吗？", "完全安全。所有处理在浏览器本地完成，音频文件不会上传到任何服务器。")
        ],
        "alternatives": [
            ("Audacity", "https://www.audacityteam.org/", "开源免费的专业音频编辑器"),
            ("GarageBand", "https://www.apple.com/garageband/", "Apple免费音乐制作软件"),
            ("Adobe Audition", "https://www.adobe.com/products/audition.html", "专业音频编辑软件")
        ],
        "tutorial_tip": "录音时选择安静的环境，使用外接麦克风能获得更好的音质。最终发布建议使用MP3格式。",
        "changelog": [
            "2026-07-01：新增语音转文字功能，支持中文/英文识别",
            "2026-06-25：优化音频压缩算法，质量提升",
            "2026-06-21：新增音频淡入淡出效果"
        ]
    },
    "视频工具": {
        "audience": "短视频创作者、视频剪辑爱好者、自媒体运营者、教师、企业宣传人员及所有需要快速剪辑、压缩和转换视频文件的用户。",
        "audience_en": "Short video creators, video editing enthusiasts, content creators, teachers, corporate marketers, and anyone who needs to quickly clip, compress, and convert videos.",
        "audience_ja": "ショート動画作成者、動画編集愛好家、コンテンツ作成者、教員、企業マーケティング担当者など。",
        "audience_vi": "Tạo video ngắn, người yêu chỉnh sửa video, tạo nội dung, giáo viên, tiếp thị doanh nghiệp và người dùng cần cắt, nén và chuyển đổi video.",
        "pros": [
            "完全免费，无需下载大型视频软件",
            "浏览器本地处理，视频不会上传服务器",
            "支持MP4、MOV、AVI、MKV等主流格式",
            "支持裁剪、压缩、合并、提取音频等操作"
        ],
        "pros_en": ["Completely free, no large video software to download", "Local browser processing, video stays private", "Supports MP4, MOV, AVI, MKV formats", "Supports clip, compress, merge, extract audio operations"],
        "pros_ja": ["完全無料、大型動画ソフトのダウンロード不要", "ブラウザ内で処理、動画をアップロードしない", "MP4、MOV、AVI、MKV形式対応", "カット、圧縮、結合、音声抽出対応"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần tải phần mềm video lớn", "Xử lý trong trình duyệt, video không tải lên server", "Hỗ trợ MP4, MOV, AVI, MKV", "Hỗ trợ cắt, nén, gộp, trích xuất âm thanh"],
        "cons": [
            "复杂的视频特效和动画制作需要专业软件",
            "大文件视频（超过500MB）处理速度较慢",
            "不支持4K以上超高清视频的流畅处理"
        ],
        "cons_en": ["Complex video effects and animation require professional software", "Large video files (over 500MB) process slowly", "Does not support smooth processing of 4K+ UHD videos"],
        "cons_ja": ["複雑なビジュアルエフェクトはプロソフトが必要", "大容量動画（500MB以上）は処理が遅い", "4K以上のUHD動画のスムーズな処理対応なし"],
        "cons_vi": ["Hiệu ứng video phức tạp cần phần mềm chuyên nghiệp", "Video lớn (trên 500MB) xử lý chậm", "Không hỗ trợ xử lý mượt mà video 4K+"],
        "faqs": [
            ("支持哪些视频格式？", "支持 MP4、MOV、AVI、MKV、WMV、FLV 等主流视频格式。输出格式以 MP4 为主。"),
            ("可以批量处理视频吗？", "部分功能支持。建议根据电脑性能选择处理数量。"),
            ("处理安全吗？", "完全安全。所有处理在浏览器本地完成，视频文件不会上传到任何服务器。")
        ],
        "alternatives": [
            ("剪映", "https://www.capcut.cn/", "字节跳动的免费视频剪辑软件"),
            ("DaVinci Resolve", "https://www.blackmagicdesign.com/products/davinciresolve/", "专业免费视频剪辑软件"),
            ("HandBrake", "https://handbrake.fr/", "开源视频转码工具")
        ],
        "tutorial_tip": "视频处理建议优先使用MP4格式，兼容性最好。压缩时选择1080p输出即可。",
        "changelog": [
            "2026-07-01：新增视频转GIF功能，支持自定义帧率",
            "2026-06-25：优化视频压缩算法，体积减少30%",
            "2026-06-21：新增视频截图提取功能"
        ]
    },
    "文本工具": {
        "audience": "文案工作者、学生、编辑、数据分析师、内容运营者及所有需要快速处理大段文字的用户。",
        "audience_en": "Copywriters, students, editors, data analysts, content operators, and anyone who needs to quickly process large amounts of text.",
        "audience_ja": "コピーライター、学生、編集者、データアナリスト、コンテンツ担当者など。",
        "audience_vi": "Biên tập viên, sinh viên, biên tập, phân tích dữ liệu và người dùng cần xử lý văn bản nhanh.",
        "pros": [
            "完全免费，无需注册即可使用",
            "支持大段文字处理，理论上无长度限制",
            "浏览器本地处理，文本不会上传服务器",
            "功能全面：统计、转换、对比、提取等"
        ],
        "pros_en": ["Completely free, no registration required", "Supports large text processing, theoretically no limit", "Local browser processing, text stays private", "Comprehensive features: count, convert, compare, extract"],
        "pros_ja": ["完全無料、登録不要", "大規模テキスト処理対応、理論上制限なし", "ブラウザ内で処理、テキストをアップロードしない", "包括的機能：カウント、変換、比較、抽出"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần đăng ký", "Hỗ trợ xử lý văn bản lớn, không giới hạn về mặt lý thuyết", "Xử lý trong trình duyệt, văn bản không tải lên server", "Tính năng toàn diện: đếm, chuyển đổi, so sánh, trích xuất"],
        "cons": [
            "超大文本（超过10万字）处理速度较慢",
            "不支持文档格式的批量处理",
            "部分高级语法检查需要专业工具"
        ],
        "cons_en": ["Very large text (over 100k characters) processes slowly", "Does not support batch document format processing", "Advanced grammar checking needs professional tools"],
        "cons_ja": ["超大規模テキスト（10万文字以上）は処理が遅い", "ドキュメント形式のバッチ処理なし", "高度な文法チェックにはプロツールが必要"],
        "cons_vi": ["Văn bản rất lớn (trên 100k ký tự) xử lý chậm", "Không hỗ trợ xử lý hàng loạt định dạng tài liệu", "Kiểm tra ngữ pháp cao cấp cần công cụ chuyên nghiệp"],
        "faqs": [
            ("有文本长度限制吗？", "理论上没有长度限制，但超大的文本（如超过10万字）可能会影响处理速度。建议分段处理超长文本。"),
            ("可以批量处理吗？", "可以。支持一次性输入多段文本进行处理，处理结果会保留原始分段格式。"),
            ("处理安全吗？", "完全安全。所有处理在浏览器本地完成，文本不会上传到任何服务器。")
        ],
        "alternatives": [
            ("Notepad++", "https://notepad-plus-plus.org/", "功能强大的免费文本编辑器"),
            ("Sublime Text", "https://www.sublimetext.com/", "轻量级代码编辑器"),
            ("Online Word Count", "https://wordcounter.net/", "在线字数统计工具")
        ],
        "tutorial_tip": "支持大量文本输入，可以处理数万字以上的内容。对于超长文本，建议分段处理以确保准确性。",
        "changelog": [
            "2026-07-01：新增去重工具，支持智能相似度检测",
            "2026-06-25：优化排序算法，支持中文拼音排序",
            "2026-06-21：新增文本反转和倒序功能"
        ]
    },
    "SEO工具": {
        "audience": "网站运营者、SEO专员、内容营销者、电商运营、博主及所有需要优化网站搜索排名的用户。",
        "audience_en": "Website operators, SEO specialists, content marketers, e-commerce managers, bloggers, and anyone who needs to optimize website search rankings.",
        "audience_ja": "ウェブサイト運営者、SEOスペシャリスト、コンテンツマーケッター、EC運営、ブロガーなど。",
        "audience_vi": "Nhà vận hành website, chuyên gia SEO, marketer nội dung, quản lý thương mại điện tử, blogger và người dùng cần tối ưu hóa xếp hạng tìm kiếm.",
        "pros": [
            "完全免费，无需注册即可使用",
            "基于SEO最佳实践和搜索引擎官方指南",
            "提供详细的优化建议和检查报告",
            "支持多种SEO格式：Meta、robots.txt、sitemap等"
        ],
        "pros_en": ["Completely free, no registration required", "Based on SEO best practices and search engine guidelines", "Detailed optimization suggestions and reports", "Supports various SEO formats: Meta, robots.txt, sitemap"],
        "pros_ja": ["完全無料、登録不要", "SEOベストプラクティスと検索エンジンガイドラインに基づく", "詳細な最適化提案とレポート", "さまざまなSEO形式対応：Meta、robots.txt、sitemap"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần đăng ký", "Dựa trên thực hành SEO tốt nhất và hướng dẫn công cụ tìm kiếm", "Gợi ý tối ưu hóa chi tiết và báo cáo", "Hỗ trợ nhiều định dạng SEO: Meta, robots.txt, sitemap"],
        "cons": [
            "SEO效果通常需要2-6个月才能显现",
            "需要持续跟踪和调整优化策略",
            "部分高级SEO功能需要专业软件"
        ],
        "cons_en": ["SEO results usually take 2-6 months to appear", "Requires continuous tracking and strategy adjustment", "Advanced SEO features need professional software"],
        "cons_ja": ["SEO効果は通常2-6ヶ月で現れる", "継続的な追跡と戦略調整が必要", "高度なSEO機能にはプロソフトが必要"],
        "cons_vi": ["Kết quả SEO thường mất 2-6 tháng để thấy", "Yêu cầu theo dõi liên tục và điều chỉnh chiến lược", "Tính năng SEO cao cấp cần phần mềm chuyên nghiệp"],
        "faqs": [
            ("检查结果可靠吗？", "工具基于搜索引擎的官方指南和SEO最佳实践生成检查结果，具有参考价值。但最终优化效果需要结合实际情况。"),
            ("支持哪种类型的网站？", "支持任何基于HTML的网站，包括静态网站、博客、电商平台等。"),
            ("可以导出报告吗？", "部分功能支持导出检查报告，方便团队共享和记录优化进度。")
        ],
        "alternatives": [
            ("Google Search Console", "https://search.google.com/search-console", "Google官方搜索控制台"),
            ("Ahrefs", "https://ahrefs.com/", "专业的SEO分析工具"),
            ("SEMrush", "https://www.semrush.com/", "综合SEO和数字营销平台")
        ],
        "tutorial_tip": "建议定期使用工具检查网站SEO状态，及时发现和解决新问题。SEO优化是一个长期过程。",
        "changelog": [
            "2026-07-01：新增结构化数据生成器，支持FAQ/Article/Breadcrumb",
            "2026-06-25：优化Meta标签生成器，支持Open Graph",
            "2026-06-21：新增可读性分析器，评估内容SEO友好度"
        ]
    },
    "设计工具": {
        "audience": "UI设计师、平面设计师、自媒体运营者、电商美工、品牌营销人员及所有需要在线设计辅助工具的用户。",
        "audience_en": "UI designers, graphic designers, social media managers, e-commerce designers, brand marketers, and anyone who needs online design assistance.",
        "audience_ja": "UIデザイナー、グラフィックデザイナー、ソーシャルメディア担当者、ECデザイナー、ブランドマーケッターなど。",
        "audience_vi": "UI designer, graphic designer, quản lý mạng xã hội, thiết kế thương mại điện tử, marketer thương hiệu và người dùng cần hỗ trợ thiết kế.",
        "pros": [
            "完全免费，无需下载专业设计软件",
            "浏览器本地处理，设计文件不会上传服务器",
            "操作简单，适合非专业设计师快速上手",
            "支持多种设计输出格式"
        ],
        "pros_en": ["Completely free, no professional design software needed", "Local browser processing, design files stay private", "Simple operation, suitable for non-professional designers", "Supports various design output formats"],
        "pros_ja": ["完全無料、プロのデザインソフト不要", "ブラウザ内で処理、デザインファイルをアップロードしない", "簡単操作、非デザイナーにも使いやすい", "さまざまなデザイン出力形式対応"],
        "pros_vi": ["Hoàn toàn miễn phí, không cần phần mềm thiết kế chuyên nghiệp", "Xử lý trong trình duyệt, tệp thiết kế không tải lên server", "操作简单, phù hợp người không chuyên", "Hỗ trợ nhiều định dạng xuất thiết kế"],
        "cons": [
            "复杂的矢量设计和3D建模需要专业软件",
            "不支持团队协作和云端同步",
            "高级设计效果和功能有限"
        ],
        "cons_en": ["Complex vector design and 3D modeling need professional software", "No team collaboration or cloud sync", "Advanced design effects and features are limited"],
        "cons_ja": ["複雑なベクターデザインや3Dモデリングにはプロソフトが必要", "チームコラボレーションやクラウド同期なし", "高度なデザイン効果と機能は制限"],
        "cons_vi": ["Thiết kế vector phức tạp và mô hình 3D cần phần mềm chuyên nghiệp", "Không hỗ trợ cộng tác nhóm hoặc đồng bộ đám mây", "Hiệu ứng và tính năng thiết kế cao cấp hạn chế"],
        "faqs": [
            ("适合专业设计师使用吗？", "适合快速原型设计和简单图形制作。复杂的专业项目建议使用Adobe系列或Figma等专业工具。"),
            ("设计结果可以商用吗？", "可以。所有设计结果归你所有，可以用于商业用途。"),
            ("支持哪些输出格式？", "支持常见的图片格式（JPG、PNG、WebP）和矢量格式（SVG）。")
        ],
        "alternatives": [
            ("Figma", "https://www.figma.com/", "专业的在线UI设计工具"),
            ("Canva", "https://www.canva.com/", "模板丰富的在线设计平台"),
            ("Adobe XD", "https://www.adobe.com/products/xd.html", "Adobe的UI/UX设计工具")
        ],
        "tutorial_tip": "建议先确定设计目标，选择合适的工具功能。所有设计结果请及时下载保存。",
        "changelog": [
            "2026-07-01：新增渐变生成器，支持线性/径向渐变导出",
            "2026-06-25：优化颜色选择器，增加取色功能",
            "2026-06-21：新增图标字体生成器"
        ]
    }
}


def get_tool_info(filepath):
    """Extract tool info from a page's canonical URL."""
    basename = os.path.basename(filepath)
    # Check tools_map by slug
    slug = basename.replace('.html', '')
    if slug in tools_map:
        return tools_map[slug], slug
    # Try to find by URL
    for s, t in tools_map.items():
        if s == slug or t.get('url', '').rstrip('/') == '/' + os.path.relpath(filepath, BASE):
            return t, s
    return None, slug


def build_7_modules(tool_info, slug, cat_name):
    """Build the 7-module HTML block for a tool page."""
    if not tool_info:
        return None

    name_zh = tool_info.get('name', slug)
    name_en = tool_info.get('name__en', slug)
    desc_zh = tool_info.get('description', '')
    desc_en = tool_info.get('description__en', '')
    desc_ja = tool_info.get('description__ja', '')
    desc_vi = tool_info.get('description__vi', '')
    cat = tool_info.get('category', '')
    tool_url = tool_info.get('url', '')
    cat_label = tool_info.get('category', '')

    # Get category-specific content
    cat_content = CATEGORY_CONTENT.get(cat, {})
    if not cat_content:
        cat_content = CATEGORY_CONTENT.get("PDF工具", {})  # fallback

    audience_zh = cat_content.get('audience', '')
    audience_en = cat_content.get('audience_en', '')
    audience_ja = cat_content.get('audience_ja', '')
    audience_vi = cat_content.get('audience_vi', '')

    pros_zh = cat_content.get('pros', [])
    pros_en = cat_content.get('pros_en', [])
    pros_ja = cat_content.get('pros_ja', [])
    pros_vi = cat_content.get('pros_vi', [])

    cons_zh = cat_content.get('cons', [])
    cons_en = cat_content.get('cons_en', [])
    cons_ja = cat_content.get('cons_ja', [])
    cons_vi = cat_content.get('cons_vi', [])

    faqs = cat_content.get('faqs', [])
    alternatives = cat_content.get('alternatives', [])
    tutorial_tip = cat_content.get('tutorial_tip', '')
    changelog = cat_content.get('changelog', [])

    # Build tutorial link (find existing tutorial)
    tutorial_url = f"/tutorials/{slug}.html"
    tutorial_text = f"{name_zh}使用教程"

    # Build related tools (other tools in same category)
    related_tools = []
    cat_slug_map = {}
    for s, t in tools_map.items():
        if t.get('category') == cat and s != slug:
            cat_slug_map[s] = t
    for rs, rt in list(cat_slug_map.items())[:5]:
        related_tools.append((rt.get('url', ''), rt.get('name', rs)))

    # Build pros HTML
    pros_html_zh = "".join([f'<li>{p}</li>' for p in pros_zh])
    pros_html_en = "".join([f'<li>{p}</li>' for p in pros_en])
    pros_html_ja = "".join([f'<li>{p}</li>' for p in pros_ja])
    pros_html_vi = "".join([f'<li>{p}</li>' for p in pros_vi])

    # Build cons HTML
    cons_html_zh = "".join([f'<li>{c}</li>' for c in cons_zh])
    cons_html_en = "".join([f'<li>{c}</li>' for c in cons_en])
    cons_html_ja = "".join([f'<li>{c}</li>' for c in cons_ja])
    cons_html_vi = "".join([f'<li>{c}</li>' for c in cons_vi])

    # Build FAQ HTML
    faq_html = ""
    faq_json_items = []
    for i, (q, a) in enumerate(faqs, 1):
        faq_html += f'<div class="z7-faq-item"><p><strong>{q}</strong><br/><span>{a}</span></p></div>\n'
        faq_json_items.append('{"@type":"Question","name":"%s","acceptedAnswer":{"@type":"Answer","text":"%s"}}' %
                               (q.replace('"', '\\"'), a.replace('"', '\\"')))

    faq_json = ',"mainEntity":[' + ','.join(faq_json_items) + ']'

    # Build alternatives HTML
    alt_html = ""
    for alt_name, alt_url, alt_desc in alternatives:
        alt_html += f'<div class="z7-alt-item"><a href="{alt_url}" target="_blank" rel="noopener">{alt_name}</a><span>{alt_desc}</span></div>\n'

    # Build related tools HTML
    rel_html = ""
    for rl_url, rl_name in related_tools:
        rel_html += f'<a href="{rl_url}" target="_blank">{rl_name}</a>\n'

    # Build changelog HTML
    cl_html = ""
    for entry in changelog:
        cl_html += f'<li>{entry}</li>\n'

    # Build tutorial section
    tut_html = '<div class="z7-tutorial-card">' + \
               '<a href="' + tutorial_url + '" class="z7-tutorial-link">' + tutorial_text + '</a>' + \
               '<p>' + tutorial_tip + '</p></div>'

    # The full 7-module HTML block
    html = '''
  <!-- ZEN_TOOLS_7_MODULES -->
  <section class="z7-section">
    <div class="z7-section-head">
      <span class="z7-eyebrow">工具详情</span>
      <h2>''' + name_zh + ''' 工具详情</h2>
    </div>

    <div class="z7-intro">
      <h3>工具简介</h3>
      <p>''' + desc_zh + '''</p>
    </div>

    <div class="z7-audience">
      <h3>适合哪些人</h3>
      <p>''' + audience_zh + '''</p>
    </div>

    <div class="z7-pros-cons">
      <div class="z7-col">
        <h3>优点</h3>
        <ul>''' + pros_html_zh + '''</ul>
      </div>
      <div class="z7-col">
        <h3>缺点</h3>
        <ul>''' + cons_html_zh + '''</ul>
      </div>
    </div>

    <div class="z7-tutorial">
      <h3>使用教程</h3>
      ''' + tut_html + '''
      <div class="z7-related-tools">
        <strong>同分类工具：</strong>
        <div class="z7-tools-list">''' + rel_html + '''</div>
      </div>
    </div>

    <div class="z7-faq">
      <h3>常见问题</h3>
      ''' + faq_html + '''
    </div>

    <div class="z7-alternatives">
      <h3>替代工具</h3>
      ''' + alt_html + '''
    </div>

    <div class="z7-changelog">
      <h3>更新记录</h3>
      <ul>''' + cl_html + '''</ul>
    </div>
  </section>
  <script type="application/ld+json">{"@context":"https://schema.org","@type":"FAQPage"''' + faq_json + '''}</script>
  <!-- END ZEN_TOOLS_7_MODULES -->
'''

    # CSS styles for the 7 modules
    css = '''
<style>
.z7-section{margin-top:40px;padding:32px 28px;background:rgba(255,255,255,0.02);border:1px solid var(--border);border-radius:16px;max-width:900px;margin-left:auto;margin-right:auto}
.z7-section-head{margin-bottom:24px}
.z7-eyebrow{font-size:12px;font-weight:700;color:var(--cyan);letter-spacing:1px;text-transform:uppercase}
.z7-section-head h2{font-size:22px;font-weight:800;color:var(--text);margin-top:4px}
.z7-intro,.z7-audience,.z7-tutorial,.z7-faq,.z7-alternatives,.z7-changelog{margin-top:28px}
.z7-section h3{font-size:17px;font-weight:700;color:var(--cyan);margin-bottom:10px}
.z7-section p{font-size:14px;color:var(--muted);line-height:1.8;margin-bottom:10px}
.z7-section ul{list-style:none;padding:0;margin:0}
.z7-section li{font-size:14px;color:var(--muted);line-height:1.8;margin-bottom:6px;padding-left:18px;position:relative}
.z7-section li::before{content:"";position:absolute;left:0;top:10px;width:6px;height:6px;background:var(--cyan);border-radius:50%}
.z7-pros-cons{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px}
.z7-col h3{font-size:15px}
@media(max-width:600px){.z7-pros-cons{grid-template-columns:1fr}}
.z7-tutorial-card{background:rgba(0,229,255,0.06);border-left:3px solid var(--cyan);padding:14px 18px;border-radius:0 10px 10px 0;margin:12px 0}
.z7-tutorial-link{color:var(--cyan);font-weight:600;text-decoration:none;font-size:15px}
.z7-tutorial-link:hover{text-decoration:underline}
.z7-related-tools{margin-top:12px}
.z7-tools-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}
.z7-tools-list a{background:rgba(0,229,255,0.1);color:var(--cyan);padding:4px 10px;border-radius:6px;text-decoration:none;font-size:12px}
.z7-tools-list a:hover{background:rgba(0,229,255,0.2)}
.z7-faq-item{margin:12px 0;padding:12px 16px;background:rgba(255,255,255,0.02);border-radius:8px;border:1px solid rgba(255,255,255,0.06)}
.z7-faq-item p{margin:0}
.z7-faq-item strong{color:var(--text)}
.z7-faq-item span{display:block;margin-top:6px;color:var(--muted)}
.z7-alt-item{background:rgba(255,255,255,0.02);border:1px solid rgba(255,255,255,0.06);border-radius:10px;padding:12px 16px;margin:8px 0;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px}
.z7-alt-item a{color:var(--cyan);font-weight:600;text-decoration:none}
.z7-alt-item a:hover{text-decoration:underline}
.z7-alt-item span{color:var(--muted);font-size:13px}
.z7-changelog ul{list-style:none;padding:0}
.z7-changelog li{padding-left:18px;font-size:14px;color:var(--muted)}
.z7-changelog li::before{content:"•";color:var(--cyan);position:absolute;left:0;top:0;font-size:14px;line-height:1.8}
</style>
'''

    return {
        'html': html,
        'css': css,
        'i18n_keys': {
            'z7_intro_title': '工具简介',
            'z7_intro_desc': desc_zh,
            'z7_audience_title': '适合哪些人',
            'z7_audience_desc': audience_zh,
            'z7_pros_title': '优点',
            'z7_cons_title': '缺点',
            'z7_tutorial_title': '使用教程',
            'z7_faq_title': '常见问题',
            'z7_alternatives_title': '替代工具',
            'z7_changelog_title': '更新记录',
            'z7_related_title': '同分类工具：',
        },
        'i18n_keys_en': {
            'z7_intro_title': 'Introduction',
            'z7_intro_desc': desc_en,
            'z7_audience_title': 'Who is it for',
            'z7_audience_desc': audience_en,
            'z7_pros_title': 'Pros',
            'z7_cons_title': 'Cons',
            'z7_tutorial_title': 'Tutorial',
            'z7_faq_title': 'FAQ',
            'z7_alternatives_title': 'Alternatives',
            'z7_changelog_title': 'Changelog',
            'z7_related_title': 'Related tools:',
        },
        'i18n_keys_ja': {
            'z7_intro_title': 'ツール概要',
            'z7_intro_desc': desc_ja,
            'z7_audience_title': '対象ユーザー',
            'z7_audience_desc': audience_ja,
            'z7_pros_title': '利点',
            'z7_cons_title': '欠点',
            'z7_tutorial_title': 'チュートリアル',
            'z7_faq_title': 'よくある質問',
            'z7_alternatives_title': '代替ツール',
            'z7_changelog_title': '更新履歴',
            'z7_related_title': '関連ツール：',
        },
        'i18n_keys_vi': {
            'z7_intro_title': 'Giới thiệu',
            'z7_intro_desc': desc_vi,
            'z7_audience_title': 'Dành cho ai',
            'z7_audience_desc': audience_vi,
            'z7_pros_title': 'Ưu điểm',
            'z7_cons_title': 'Nhược điểm',
            'z7_tutorial_title': 'Hướng dẫn',
            'z7_faq_title': 'Câu hỏi thường gặp',
            'z7_alternatives_title': 'Công cụ thay thế',
            'z7_changelog_title': 'Nhật ký cập nhật',
            'z7_related_title': 'Công cụ liên quan:',
        }
    }


def inject_7_modules(filepath):
    """Inject the 7 modules into a tool page."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already injected
    if 'ZEN_TOOLS_7_MODULES' in content:
        return False, 'already_injected'

    tool_info, slug = get_tool_info(filepath)
    if not tool_info:
        return False, 'no_tool_info'

    cat = tool_info.get('category', '')
    modules = build_7_modules(tool_info, slug, cat)
    if not modules:
        return False, 'no_modules'

    html = modules['html']
    css = modules['css']

    # Find injection point: before </footer>
    footer_match = re.search(r'</footer>', content)
    footer_open_match = re.search(r'<footer[^>]*>', content)

    if footer_match:
        inject_pos = footer_match.start()
        content = content[:inject_pos] + html + css + '\n  ' + content[inject_pos:]
    elif footer_open_match:
        # Try to inject before <footer...> tag
        inject_pos = footer_open_match.start()
        content = content[:inject_pos] + html + css + '\n' + content[inject_pos:]
    else:
        # Fallback: inject before </body>
        body_match = re.search(r'</body>', content)
        if body_match:
            inject_pos = body_match.start()
            content = content[:inject_pos] + html + css + '\n' + content[inject_pos:]
        else:
            return False, 'no_injection_point'

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True, 'injected'


def main():
    count = 0
    skipped = 0
    errors = 0
    already = 0

    for root, dirs, files in os.walk(BASE):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

        for fn in files:
            if fn.endswith('.html') and fn not in EXCLUDE_FILES:
                filepath = os.path.join(root, fn)
                relpath = os.path.relpath(filepath, BASE)

                # Only process tool pages (in category subdirectories)
                parts = relpath.split(os.sep)
                if len(parts) < 2:
                    continue  # root-level files are not tool pages

                success, msg = inject_7_modules(filepath)
                if success:
                    print(f"  [OK] {relpath}")
                    count += 1
                elif msg == 'already_injected':
                    print(f"  [SKIP] {relpath} (already injected)")
                    already += 1
                else:
                    # Some pages might not have tool info, skip silently
                    if msg in ('no_tool_info', 'no_modules', 'no_injection_point'):
                        skipped += 1
                    else:
                        print(f"  [ERR] {relpath}: {msg}")
                        errors += 1

    print(f"\n=== Done! ===")
    print(f"Injected: {count}")
    print(f"Already: {already}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")


if __name__ == '__main__':
    main()
