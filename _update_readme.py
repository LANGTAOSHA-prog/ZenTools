import json, sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 读取工具数据
with open('D:\\Users\\taojiang\\Documents\\GitHub\\ZenTools\\data\\tools-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

total_tools = len(data['tools'])

# 统计各分类数量
cats = {}
for t in data['tools']:
    c = t.get('category', '其他')
    cats[c] = cats.get(c, 0) + 1

num_cats = len(cats)
print(f'工具总数: {total_tools}, 分类数: {num_cats}')

# 读取 README
with open('D:\\Users\\taojiang\\Documents\\GitHub\\ZenTools\\README.md', 'r', encoding='utf-8') as f:
    readme = f.read()

# 1. 更新第3行：> **XXX 款工具 · 纯本地处理 ...
readme = re.sub(r'> \*\*\d+ 款工具', f'> **{total_tools} 款工具', readme)

# 2. 更新第5行：... **13 大类 279 款工具** ...
readme = re.sub(r'\*\*\d+ 大类 \d+ 款工具\*\*', f'**{num_cats} 大类 {total_tools} 款工具**', readme)

# 3. 更新分类表格
table_start = readme.find('| 分类 | 数量 | 包含工具 |')
table_header_end = readme.find('|:-----|:---:|:---------|')

if table_start != -1 and table_header_end != -1:
    # 找到表格内容结束
    after_header = readme[table_header_end:]
    lines = after_header.split('\n')
    table_end = table_header_end
    for i, line in enumerate(lines):
        table_end += len(line) + 1
        if line.strip() == '' or line.strip().startswith('---'):
            break
    
    # 构建新表格
    desc_map = {
        'PDF工具': '合并、拆分、压缩、转换(Word/Excel/PPT/图片)、加密解密、水印、签名、OCR、扁平化、调整大小、解锁、裁剪、整理、提取图片等',
        '图片工具': '压缩、格式转换、裁剪、去背景、滤镜、拼图、水印、锐化、马赛克等',
        '音频工具': '裁剪、合并、变速、反转、淡入淡出、录音、语音转文字、文字转语音等',
        '视频工具': '压缩、裁剪、合并、变速、旋转、截图、倒放、转 GIF/MP3、GIF 转换（MP4/WEBM/MOV/AVI/APNG/图片 ↔ GIF）等',
        '文本工具': '字数统计、大小写转换、查找替换、排序、去重、文本对比、URL 编码等',
        '开发工具': 'JSON 格式化/对比/树形视图、CSS/JS/SQL 格式化、颜色转换、Markdown 预览、Base64、Hash 生成、正则测试、进制/时间戳转换等',
        'AI工具': 'AI 写作/翻译/润色/简历/摘要、提示词生成、文案写作、故事/诗歌创作、代码注释、学习计划等',
        'SEO工具': '标题检查器、关键词密度分析、Meta 标签生成、SERP 预览、关键词提取等',
        '金融工具': '贷款计算、存款利息、股票手续费、理财计算、通胀计算、增值税计算等',
        '设计工具': 'Midjourney、Canva AI、Figma AI、二维码生成器等 AI 设计导航',
        '生活工具': 'BMI、单位换算、密码生成/强度检测、倒计时器、计时器、年龄/日期计算、渐变色生成、抽奖转盘、随机工具、日本工资/税金/年金/电费等',
        '办公工具': '（待补充）',
    }
    
    icon_map = {
        'PDF工具': '📄', '图片工具': '🖼️', '音频工具': '🎵', '视频工具': '🎬',
        '文本工具': '✏️', '开发工具': '💻', 'AI工具': '🤖', 'SEO工具': '🌐',
        '金融工具': '🏦', '设计工具': '🎨', '生活工具': '☀️', '办公工具': '📋',
    }
    
    new_rows = []
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        name = icon_map.get(cat, '📁') + f' **{cat}**'
        desc = desc_map.get(cat, '（待补充）')
        new_rows.append(f'| {name} | {count} | {desc} |')
    
    new_table = '| 分类 | 数量 | 包含工具 |\n|:-----|:---:|:---------|\n' + '\n'.join(new_rows) + '\n'
    
    readme = readme[:table_start] + new_table + readme[table_end:]

# 写回 README
with open('D:\\Users\\taojiang\\Documents\\GitHub\\ZenTools\\README.md', 'w', encoding='utf-8') as f:
    f.write(readme)

print(f'✅ README.md 已更新：{total_tools} 款工具，{num_cats} 大类')
