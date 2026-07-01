#!/usr/bin/env python3
"""Add AI-friendly metadata fields to tools-data.json for AI search optimization."""
import json, os, copy

DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "tools-data.json")

with open(DATA_PATH, encoding='utf-8') as f:
    data = json.load(f)

# Define category -> AI metadata mappings
CAT_AUDIENCE = {
    "AI工具": "内容创作者、文案写手、营销人员",
    "图片工具": "设计师、电商运营、内容创作者、办公用户",
    "PDF工具": "办公用户、学生、律师、财务人员",
    "文本工具": "办公用户、文案写手、开发者",
    "视频工具": "视频创作者、自媒体运营、教育工作者",
    "音频工具": "播客制作者、音频编辑、语言学习者",
    "开发工具": "开发者、运维人员、技术爱好者",
    "SEO工具": "SEO从业者、网站运营、营销人员",
    "办公工具": "上班族、行政人员、团队协作用户",
    "生活工具": "普通用户、家庭用户、旅行者",
    "金融工具": "投资者、理财用户、购房者",
    "教育工具": "学生、教师、自学者",
    "设计工具": "设计师、UI/UX从业者、创意工作者",
}

CAT_USE_CASE = {
    "AI工具": "内容生成、文案创作、翻译、总结提炼、创意辅助",
    "图片工具": "图片编辑、格式转换、批量处理、压缩优化、加水印",
    "PDF工具": "文档管理、格式转换、合并拆分、加密解密、OCR识别",
    "文本工具": "文本处理、格式转换、编码解码、统计分析",
    "视频工具": "视频剪辑、格式转换、压缩、GIF制作、截图",
    "音频工具": "音频编辑、格式转换、录音、语音转文字、剪辑",
    "开发工具": "代码格式化、JSON处理、正则测试、调试辅助、在线测试",
    "SEO工具": "SEO分析、关键词研究、Meta标签优化、站点诊断",
    "办公工具": "文档处理、数据转换、批处理、格式统一",
    "生活工具": "日常计算、单位换算、密码生成、日期计算",
    "金融工具": "贷款计算、投资收益、汇率换算、税务计算",
    "教育工具": "学习辅助、计算工具、测验模拟、知识整理",
    "设计工具": "图形设计、色彩处理、图标生成、UI辅助",
}

CAT_LIMIT = {
    "AI工具": "单次生成最大5000字，部分功能需要联网",
    "图片工具": "单张图片最大100MB，支持批量最多20张",
    "PDF工具": "单个PDF最大100MB，超多页文档建议分批处理",
    "文本工具": "单次输入最大10万字，超长文本建议分段",
    "视频工具": "单个视频最大500MB，处理时间取决于文件大小",
    "音频工具": "单个音频最大100MB，超长音频建议分段",
    "开发工具": "单次输入最大1MB，超大文件建议分段",
    "SEO工具": "单次分析最多100个URL，实时数据依赖网络",
    "办公工具": "单文件最大100MB，支持批量最多20个",
    "生活工具": "无严格限制，计算精度支持小数点后6位",
    "金融工具": "计算结果仅供参考，不构成投资建议",
    "教育工具": "单次输入无限制，计算结果即时显示",
    "设计工具": "单文件最大50MB，支持常见设计格式",
}

CAT_USE_CASE_EN = {
    "AI工具": "Content generation, copywriting, translation, summarization, creative assistance",
    "图片工具": "Image editing, format conversion, batch processing, compression, watermarking",
    "PDF工具": "Document management, format conversion, merge/split, encrypt/decrypt, OCR",
    "文本工具": "Text processing, format conversion, encode/decode, statistical analysis",
    "视频工具": "Video editing, format conversion, compression, GIF creation, screenshots",
    "音频工具": "Audio editing, format conversion, recording, speech-to-text, trimming",
    "开发工具": "Code formatting, JSON processing, regex testing, debugging, online testing",
    "SEO工具": "SEO analysis, keyword research, meta tag optimization, site audit",
    "办公工具": "Document processing, data conversion, batch processing, format unification",
    "生活工具": "Daily calculations, unit conversion, password generation, date calculation",
    "金融工具": "Loan calculation, investment returns, currency conversion, tax calculation",
    "教育工具": "Learning assistance, calculator tools, quiz simulation, knowledge organization",
    "设计工具": "Graphic design, color processing, icon generation, UI assistance",
}
CAT_USE_CASE_JA = {
    "AI工具": "コンテンツ生成、コピーライティング、翻訳、要約、クリエイティブ支援",
    "图片工具": "画像編集、形式変換、一括処理、圧縮、透かし",
    "PDF工具": "文書管理、形式変換、結合/分割、暗号化/復号、OCR",
    "文本工具": "テキスト処理、形式変換、エンコード/デコード、統計分析",
    "视频工具": "動画編集、形式変換、圧縮、GIF作成、スクリーンショット",
    "音频工具": "音声編集、形式変換、録音、音声認識、トリミング",
    "开发工具": "コード整形、JSON処理、正規表現テスト、デバッグ、オンラインテスト",
    "SEO工具": "SEO分析、キーワード調査、メタタグ最適化、サイト診断",
    "办公工具": "文書処理、データ変換、一括処理、形式統一",
    "生活工具": "日常計算、単位変換、パスワード生成、日付計算",
    "金融工具": "ローン計算、投資収益、為替換算、税金計算",
    "教育工具": "学習支援、計算ツール、クイズシミュレーション、知識整理",
    "设计工具": "グラフィックデザイン、色彩処理、アイコン生成、UI支援",
}
CAT_USE_CASE_VI = {
    "AI工具": "Tạo nội dung, viết quảng cáo, dịch thuật, tóm tắt, hỗ trợ sáng tạo",
    "图片工具": "Chỉnh sửa ảnh, chuyển đổi định dạng, xử lý hàng loạt, nén, watermark",
    "PDF工具": "Quản lý tài liệu, chuyển đổi định dạng, gộp/tách, mã hóa/giải mã, OCR",
    "文本工具": "Xử lý văn bản, chuyển đổi định dạng, mã hóa/giải mã, phân tích thống kê",
    "视频工具": "Chỉnh sửa video, chuyển đổi định dạng, nén, tạo GIF, chụp màn hình",
    "音频工具": "Chỉnh sửa âm thanh, chuyển đổi định dạng, ghi âm, chuyển giọng nói thành văn bản",
    "开发工具": "Định dạng mã, xử lý JSON, kiểm tra regex, gỡ lỗi, kiểm tra trực tuyến",
    "SEO工具": "Phân tích SEO, nghiên cứu từ khóa, tối ưu thẻ Meta, kiểm tra trang web",
    "办公工具": "Xử lý tài liệu, chuyển đổi dữ liệu, xử lý hàng loạt, thống nhất định dạng",
    "生活工具": "Tính toán hàng ngày, chuyển đổi đơn vị, tạo mật khẩu, tính ngày",
    "金融工具": "Tính khoản vay, lợi nhuận đầu tư, chuyển đổi tiền tệ, tính thuế",
    "教育工具": "Hỗ trợ học tập, công cụ tính toán, mô phỏng bài kiểm tra, sắp xếp kiến thức",
    "设计工具": "Thiết kế đồ họa, xử lý màu sắc, tạo biểu tượng, hỗ trợ UI",
}

CAT_LIMIT_EN = {
    "AI工具": "Max 5000 chars per generation, some features require internet",
    "图片工具": "Max 100MB per image, batch up to 20 images",
    "PDF工具": "Max 100MB per PDF, very large documents should be split",
    "文本工具": "Max 100K chars per input, very long texts should be segmented",
    "视频工具": "Max 500MB per video, processing time depends on file size",
    "音频工具": "Max 100MB per file, very long audio (1hr+) should be split",
    "开发工具": "Max 1MB per input, very large files should be split",
    "SEO工具": "Max 100 URLs per analysis, live data depends on network",
    "办公工具": "Max 100MB per file, batch up to 20 files",
    "生活工具": "No strict limits, precision up to 6 decimal places",
    "金融工具": "Results for reference only, not investment advice",
    "教育工具": "No input limits, results calculated instantly",
    "设计工具": "Max 50MB per file, supports common design formats",
}
CAT_LIMIT_JA = {
    "AI工具": "1回最大5000文字、一部機能はインターネット接続が必要",
    "图片工具": "1枚最大100MB、一括最大20枚",
    "PDF工具": "1ファイル最大100MB、非常に大きな文書は分割推奨",
    "文本工具": "1回最大10万字、非常に長いテキストは分割推奨",
    "视频工具": "1ファイル最大500MB、処理時間はファイルサイズに依存",
    "音频工具": "1ファイル最大100MB、長時間音声（1時間以上）は分割推奨",
    "开发工具": "1回最大1MB、非常に大きなファイルは分割推奨",
    "SEO工具": "1回最大100URL、リアルタイムデータはネットワークに依存",
    "办公工具": "1ファイル最大100MB、一括最大20ファイル",
    "生活工具": "厳格な制限なし、小数点以下6桁まで対応",
    "金融工具": "結果は参考値です。投資助言ではありません",
    "教育工具": "入力制限なし、結果は即時計算",
    "设计工具": "1ファイル最大50MB、一般的なデザイン形式対応",
}
CAT_LIMIT_VI = {
    "AI工具": "Tối đa 5000 ký tự mỗi lần tạo, một số chức năng cần internet",
    "图片工具": "Tối đa 100MB mỗi ảnh, hàng loạt tối đa 20 ảnh",
    "PDF工具": "Tối đa 100MB mỗi PDF, tài liệu rất lớn nên chia nhỏ",
    "文本工具": "Tối đa 100K ký tự mỗi lần nhập, văn bản rất dài nên chia đoạn",
    "视频工具": "Tối đa 500MB mỗi video, thời gian xử lý phụ thuộc kích thước",
    "音频工具": "Tối đa 100MB mỗi tệp, âm thanh rất dài (1 tiếng+) nên chia đoạn",
    "开发工具": "Tối đa 1MB mỗi lần nhập, tệp rất lớn nên chia nhỏ",
    "SEO工具": "Tối đa 100 URL mỗi lần phân tích, dữ liệu thời gian thực phụ thuộc mạng",
    "办公工具": "Tối đa 100MB mỗi tệp, hàng loạt tối đa 20 tệp",
    "生活工具": "Không có giới hạn nghiêm ngặt, độ chính xác đến 6 chữ số thập phân",
    "金融工具": "Kết quả chỉ để tham khảo, không phải lời khuyên đầu tư",
    "教育工具": "Không có giới hạn đầu vào, kết quả được tính ngay lập tức",
    "设计工具": "Tối đa 50MB mỗi tệp, hỗ trợ định dạng thiết kế phổ biến",
}

CAT_AUDIENCE_EN = {
    "AI工具": "Content creators, copywriters, marketers",
    "图片工具": "Designers, e-commerce operators, content creators, office workers",
    "PDF工具": "Office workers, students, lawyers, financial professionals",
    "文本工具": "Office workers, copywriters, developers",
    "视频工具": "Video creators, social media managers, educators",
    "音频工具": "Podcasters, audio editors, language learners",
    "开发工具": "Developers, DevOps, tech enthusiasts",
    "SEO工具": "SEO professionals, webmasters, marketers",
    "办公工具": "Office staff, administrators, team collaborators",
    "生活工具": "General users, families, travelers",
    "金融工具": "Investors, finance users, home buyers",
    "教育工具": "Students, teachers, self-learners",
    "设计工具": "Designers, UI/UX professionals, creatives",
}
CAT_AUDIENCE_JA = {
    "AI工具": "コンテンツ制作者、コピーライター、マーケター",
    "图片工具": "デザイナー、EC運営者、コンテンツ制作者、オフィスワーカー",
    "PDF工具": "オフィスワーカー、学生、弁護士、財務担当者",
    "文本工具": "オフィスワーカー、コピーライター、開発者",
    "视频工具": "動画制作者、SNS運用者、教育者",
    "音频工具": "ポッドキャスター、音声編集者、語学学習者",
    "开发工具": "開発者、DevOps、技術愛好家",
    "SEO工具": "SEO担当者、ウェブマスター、マーケター",
    "办公工具": "一般職員、管理者、チーム協作者",
    "生活工具": "一般ユーザー、家族、旅行者",
    "金融工具": "投資家、資産運用者、住宅購入者",
    "教育工具": "学生、教師、自習者",
    "设计工具": "デザイナー、UI/UX専門家、クリエイター",
}
CAT_AUDIENCE_VI = {
    "AI工具": "Người sáng tạo nội dung, copywriter, marketer",
    "图片工具": "Nhà thiết kế, người vận hành TMĐT, người sáng tạo nội dung",
    "PDF工具": "Nhân viên văn phòng, sinh viên, luật sư, nhân viên tài chính",
    "文本工具": "Nhân viên văn phòng, copywriter, nhà phát triển",
    "视频工具": "Người sáng tạo video, quản lý MXH, nhà giáo dục",
    "音频工具": "Người làm podcast, biên tập âm thanh, người học ngôn ngữ",
    "开发工具": "Nhà phát triển, DevOps, người đam mê công nghệ",
    "SEO工具": "Chuyên gia SEO, quản trị web, marketer",
    "办公工具": "Nhân viên văn phòng, quản trị viên, người hợp tác nhóm",
    "生活工具": "Người dùng phổ thông, gia đình, du khách",
    "金融工具": "Nhà đầu tư, người dùng tài chính, người mua nhà",
    "教育工具": "Sinh viên, giáo viên, người tự học",
    "设计工具": "Nhà thiết kế, chuyên gia UI/UX, người sáng tạo",
}

CAT_PRIVACY_EN = {
    True: "Processed locally in browser, never uploaded to server",
    False: "Requires network connection",
}
CAT_PRIVACY_JA = {
    True: "ブラウザ内でローカル処理、サーバーにアップロードされません",
    False: "ネットワーク接続が必要です",
}
CAT_PRIVACY_VI = {
    True: "Xử lý cục bộ trong trình duyệt, không tải lên máy chủ",
    False: "Yêu cầu kết nối mạng",
}

update_count = 0
for tool in data['tools']:
    cat = tool.get('category', '')
    
    # Determine if browser-local processing
    local_categories = ['图片工具', 'PDF工具', '文本工具', '音频工具', '视频工具', '生活工具', '开发工具']
    is_local = cat in local_categories
    
    cat_limit_zh = CAT_LIMIT.get(cat, "单文件最大100MB")
    
    # Add multilingual AI-friendly metadata
    tool['ai'] = {
        "free": True,
        "registration": False,
        "chinese": True,
        "languages": ["zh", "en", "ja", "vi"],
        "privacy": CAT_PRIVACY_EN[True if is_local else False],
        "privacy__en": CAT_PRIVACY_EN[True if is_local else False],
        "privacy__ja": CAT_PRIVACY_JA[True if is_local else False],
        "privacy__vi": CAT_PRIVACY_VI[True if is_local else False],
        "processing": "browser-local" if is_local else "cloud",
        "audience": CAT_AUDIENCE.get(cat, "各类用户"),
        "audience__en": CAT_AUDIENCE_EN.get(cat, "All users"),
        "audience__ja": CAT_AUDIENCE_JA.get(cat, "すべてのユーザー"),
        "audience__vi": CAT_AUDIENCE_VI.get(cat, "Tất cả người dùng"),
        "useCases": CAT_USE_CASE.get(cat, ""),
        "useCases__en": CAT_USE_CASE_EN.get(cat, ""),
        "useCases__ja": CAT_USE_CASE_JA.get(cat, ""),
        "useCases__vi": CAT_USE_CASE_VI.get(cat, ""),
        "limits": cat_limit_zh,
        "limits__en": CAT_LIMIT_EN.get(cat, "Max 100MB per file"),
        "limits__ja": CAT_LIMIT_JA.get(cat, "1ファイル最大100MB"),
        "limits__vi": CAT_LIMIT_VI.get(cat, "Tối đa 100MB mỗi tệp"),
    }
    update_count += 1

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {update_count} tools with AI-friendly metadata.")
print("Done!")
