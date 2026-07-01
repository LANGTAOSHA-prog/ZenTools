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

update_count = 0
for tool in data['tools']:
    cat = tool.get('category', '')
    
    # Determine if browser-local processing
    local_categories = ['图片工具', 'PDF工具', '文本工具', '音频工具', '视频工具', '生活工具', '开发工具']
    is_local = cat in local_categories
    
    # Add AI-friendly metadata
    tool['ai'] = {
        "free": True,
        "registration": False,
        "chinese": True,
        "languages": ["zh", "en", "ja", "vi"],
        "privacy": "浏览器本地处理，不上传服务器" if is_local else "需要网络连接",
        "processing": "浏览器本地" if is_local else "云端处理",
        "audience": CAT_AUDIENCE.get(cat, "各类用户"),
        "useCases": CAT_USE_CASE.get(cat, ""),
        "limits": CAT_LIMIT.get(cat, "单文件最大100MB"),
    }
    update_count += 1

with open(DATA_PATH, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated {update_count} tools with AI-friendly metadata.")
print("Done!")
