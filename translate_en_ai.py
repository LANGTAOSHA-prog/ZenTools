#!/usr/bin/env python3
"""Replace placeholder en/ja/vi translations with real English translations for 16 ai/ files."""

import re, os

AI_DIR = '/workspace/ai'

FILES = [
    'ai-paraphrase.html', 'ai-poem.html', 'ai-polish.html', 'ai-product-desc.html',
    'ai-prompt-generator.html', 'ai-qa.html', 'ai-regex-generator.html',
    'ai-script-generator.html', 'ai-seo-article.html', 'ai-social.html',
    'ai-story.html', 'ai-study-plan.html', 'ai-summarize.html',
    'ai-translate.html', 'ai-video-script.html', 'ai-writing.html',
    'ai-ad-copy.html', 'ai-chat.html', 'ai-code-comment.html',
    'ai-code-fix.html', 'ai-code-generator.html', 'ai-copywriting.html',
    'ai-image-generator.html', 'ai-image-prompt.html', 'ai-keyword-extractor.html',
    'ai-knowledge-base.html', 'ai-meeting-minutes.html', 'ai-mind-map.html',
    'ai-novel-generator.html', 'ai-ocr.html', 'ai-paper-assistant.html'
]

# Common Chinese → English dictionary
CN_EN = {
    '清空': 'Clear',
    '复制结果': 'Copy Result',
    '开始生成': 'Generate',
    '复制': 'Copy',
    '使用说明': 'How to Use',
    '隐私说明': 'Privacy Notice',
    '隐私说明': 'Privacy Notice',
    '收藏本站': '⭐ Bookmark Us',
    'H1 标题': 'Heading 1',
    'H2 标题': 'Heading 2',
    'H3 标题': 'Heading 3',
    '列表': 'List',
    '引用': 'Quote',
    '代码': 'Code',
    'AI 写作': 'AI Writing',
    'AI 问答助手': 'AI Q&A Assistant',
    '✍️ 写作设置': '✍️ Writing Settings',
    '📝 生成内容': '📝 Generated Content',
    '📝 原文': '📝 Original Text',
    '📝 原文输入': '📝 Original Text',
    '✨ 总结结果': '✨ Summary',
    '🔍 结果': '🔍 Result',
    '🔍 搜索结果': '🔍 Search Results',
    '🔄 改写结果': '🔄 Rewritten',
    '📄 文本总结': '📄 Text Summary',
    '🎨 润色结果': '🎨 Polished Result',
    '🌐 翻译结果': '🌐 Translation',
    '📊 主要修改': '📊 Key Changes',
    '📜 脚本': '📜 Script',
    '📜 脚本信息': '📜 Script Info',
    '📜 视频脚本': '📜 Video Script',
    '🎬 视频信息': '🎬 Video Info',
    '🧪 在线测试': '🧪 Live Test',
    '⚙️ API 设置': '⚙️ API Settings',
    '📝 描述你需要的正则表达': '📝 Describe Your Regex',
    '写作类型': 'Writing Type',
    '主题/标题': 'Topic / Title',
    '风格': 'Style',
    '语言': 'Language',
    '长度': 'Length',
    '额外要求': 'Extra Requirements',
    '额外要求（可选）': 'Extra (Optional)',
    '主题': 'Topic',
    '场景': 'Scenario',
    '类别': 'Category',
    '类型': 'Type',
    '角色': 'Role',
    '模型': 'Model',
    '平台': 'Platform',
    '篇幅': 'Length',
    '输出语言': 'Output Language',
    '源语言': 'Source Language',
    '目标语言': 'Target Language',
    '目标平台': 'Target Platform',
    '目标读者': 'Target Audience',
    '任务描述': 'Task Description',
    '原文': 'Source Text',
    '待总结文本': 'Text to Summarize',
    '改写模式': 'Rewrite Mode',
    '润色类型': 'Polish Type',
    '总结类型': 'Summary Type',
    '学习目标': 'Learning Goal',
    '学习周期': 'Learning Period',
    '当前基础': 'Current Level',
    '每周可投入时间': 'Hours per Week',
    '产品名称': 'Product Name',
    '产品特点（每行一个）': 'Features (one per line)',
    '核心关键词': 'Key Keywords',
    '核心内容（可选）': 'Core Content (Optional)',
    '补充信息（可选）': 'Extra Info (Optional)',
    '风格/语气': 'Style / Tone',
    'API Endpoint': 'API Endpoint',
    'API Key': 'API Key',
    '藏头字（藏头诗时填写）': 'Acrostic (for acrostic poems)',
    '1. 首先': '1. First',
    '2. 其次': '2. Second', 
    '3. 最后': '3. Last',
    # Placeholder examples
    '例如：人工智能的未来发展': 'e.g., The future of AI',
    '例如：需要包含案例、数据支持、引用来源等': 'e.g., Include case studies, data, references',
    '例如：一只小猫': 'e.g., A little cat',
    '例如：写一篇关于环保的博客文章': 'e.g., Write a blog post about environment',
    '例如：列出要点、给出例子': 'e.g., List key points with examples',
    '例如：办公白领': 'e.g., Office worker',
    '例如：友情、冒险': 'e.g., Friendship, adventure',
    '例如：学会 Python 编程': 'e.g., Learn Python',
    '例如：家居用品': 'e.g., Home products',
    '例如：我爱你': 'e.g., I love you',
    '例如：推荐5个免费在线工具': 'e.g., Recommend 5 free online tools',
    '例如：春天、离别': 'e.g., Spring, farewell',
    '例如：智能保温杯': 'e.g., Smart insulated cup',
    '例如：免费PDF工具': 'e.g., Free PDF tools',
    '例如：魔法森林': 'e.g., Magic forest',
    '例如：匹配中国大陆11位手机号，以1开头，第二位是3-9': 'e.g., Match Chinese phone: 11 digits, starts with 1, second digit 3-9',
    '304不锈钢\n12小时保温\n500ml容量': '304 stainless steel\n12h heat retention\n500ml capacity',
    'sk-...': 'sk-...',
    '在此输入需要改写的文本...': 'Enter text to rewrite...',
    '用自然语言描述你需要的正则，例如：匹配中国大陆11位手机号，以1开头，第二位是3-9': 'Describe regex in natural language, e.g., match Chinese mobile numbers',
    '粘贴或输入需要总结的长文本...': 'Paste or enter long text to summarize...',
    '脚本主题 / 标题': 'Script Topic / Title',
    '补充信息：目标受众、核心卖点、参考风格、需要包含的关键词等': 'Extra: target audience, USP, style reference, keywords',
    '补充要求：目标受众、核心信息、风格偏好等': 'Extra: target audience, key message, style preferences',
    '视频主题 / 标题': 'Video Topic / Title',
    '输入你的问题...': 'Enter your question...',
    '输入测试文本，匹配部分会高亮显示': 'Enter test text - matches will be highlighted',
    '输入要分享的核心内容...': 'Enter the main content to share...',
    '输入需要润色的文本...': 'Enter text to polish...',
    '输入需要翻译的文本...': 'Enter text to translate...',
    '需要包含的内容点...': 'Points to include...',
    '开始处理': 'Start Processing',
    '搜索结果': 'Search Results',
    '搜索': 'Search',
    '搜索工具': 'Search Tools',
    '结果会显示在这里...': 'Result will appear here...',
    '请输入内容...': 'Enter content...',
    '请输入内容': 'Please enter content',
    '已复制': 'Copied',
    '广告位（Google AdSense）': 'Ad Space (Google AdSense)',
    '广告位': 'Ad Space',
    '← 返回首页': '← Back to Home',
    'AI 聊天': 'AI Chat',
    'AI 改写': 'AI Rewriter',
    'AI 润色': 'AI Polisher',
    'AI 总结': 'AI Summarizer',
    'AI 翻译': 'AI Translator',
    'AI 写作': 'AI Writer',
    'AI 问答': 'AI Q&A',
    'AI 诗歌生成': 'AI Poem Generator',
    'AI 正则生成': 'AI Regex Generator',
    'AI 脚本生成': 'AI Script Generator',
    'AI 产品描述生成': 'AI Product Desc Generator',
    'AI 提示词生成器': 'AI Prompt Generator',
    'AI 社交媒体文案': 'AI Social Media Copy',
    'AI 故事创作': 'AI Story Creator',
    'AI 学习计划生成': 'AI Study Plan Generator',
    'AI 视频脚本': 'AI Video Script',
    'AI SEO 文章生成': 'AI SEO Article Generator',
    '提取图片文字': 'Extract Text from Image',
    '选择图片': 'Select Image',
    '识别文字': 'Recognize Text',
    '识别结果': 'Result',
    '上传图片': 'Upload Image',
    '支持 jpg、png、webp 格式': 'Supports jpg, png, webp',
    '点击选择或拖拽图片到此处': 'Click or drag image here',
    'OCR 文字识别，免费准确': 'OCR - Free & Accurate',
    # tool-specific buttons/etc
    '发送': 'Send',
    '开始对话': 'Start Chat',
    '输入消息...': 'Enter a message...',
    'AI 回复': 'AI Response',
    '请输入或粘贴代码': 'Enter or paste code',
    '解释代码': 'Explain Code',
    '修复代码': 'Fix Code',
    '生成代码': 'Generate Code',
    '添加注释': 'Add Comments',
    '代码注释': 'Code Comments',
    '代码修复': 'Code Fix',
    '代码生成': 'Code Generator',
    '搜索关键词...': 'Search keywords...',
    '关键词提取': 'Keyword Extractor',
    '提取关键词': 'Extract Keywords',
    '导入文本': 'Import Text',
    '导出结果': 'Export Result',
    '知识库问答': 'Knowledge Base QA',
    '添加知识': 'Add Knowledge',
    '会议纪要': 'Meeting Minutes',
    '会议记录': 'Meeting Notes',
    '思维导图': 'Mind Map',
    '生成思维导图': 'Generate Mind Map',
    '小说生成': 'Novel Generator',
    'AI 小说': 'AI Novel',
    '论文助手': 'Paper Assistant',
    'AI 论文': 'AI Paper',
    '创意文案': 'Creative Copy',
    '广告文案': 'Ad Copy',
    'AI 广告文案': 'AI Ad Copy',
    'AI 图片生成': 'AI Image Generator',
    '生成图片': 'Generate Image',
    '图片描述': 'Image Description',
    'AI 图片提示词': 'AI Image Prompt',
}

def translate_en(zh_text):
    if zh_text in CN_EN:
        return CN_EN[zh_text]
    return zh_text

def process_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Check if any en values differ from zh values
    m = re.search(r'"en":\s*\{([^}]+)\}', c)
    if not m:
        m = re.search(r"en:\s*\{([^}]+)\}", c)
    if not m:
        print(f"  SKIP: no en translations found")
        return False
    
    # Extract zh values for comparison
    zm = re.search(r'"zh":\s*\{([^}]+)\}', c)
    if not zm:
        zm = re.search(r"zh:\s*\{([^}]+)\}", c)
    
    zh_pairs = {}
    if zm:
        for k, v in re.findall(r"([a-zA-Z_]\w*):\s*'([^']*)'", zm.group(1)):
            zh_pairs[k] = v
    
    en_block = m.group(1)
    changed = False
    new_pairs = []
    for k, v in re.findall(r"([a-zA-Z_]\w*):\s*'([^']*)'", en_block):
        if k in zh_pairs and v == zh_pairs[k]:
            # Same as zh - translate
            new_v = translate_en(v)
            if new_v != v:
                # Check if it wasn't already manually translated
                changed = True
                new_pairs.append((k, new_v))
                continue
        new_pairs.append((k, v))
    
    if not changed:
        print(f"  NO CHANGE: already translated")
        return False
    
    # Rebuild the en block
    def esc(v):
        return v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')
    new_en = '{' + ', '.join(k + ": '" + esc(v) + "'" for k,v in new_pairs) + '}'
    
    # Replace old en block with new one
    old_en = m.group(1)
    c = c[:m.start(1)] + new_en + c[m.end(1):]
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    
    print(f"  OK: translated {len(new_pairs)} keys")
    return True

processed = []
for fn in sorted(os.listdir(AI_DIR)):
    if not fn.endswith('.html'):
        continue
    fpath = os.path.join(AI_DIR, fn)
    print(fn)
    if process_file(fpath):
        processed.append(fn)

print(f"\nTotal updated: {len(processed)} files")