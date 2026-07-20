# -*- coding: utf-8 -*-
"""
统一内容扩写生成器（AdSense 整改核心）
======================================
处理全站工具页（模板 C=hero / D=其他 / 孤儿占位页），基于每工具真实
description 生成专属长文 + 差异化 FAQ，替换全站重复的通用 FAQ，消除
「低价值内容」信号。

要点：
- 内容由 tools-data.json 的真实 description 驱动 → 每页天然差异化、不套话。
- 通用 FAQ（"免费吗/上传吗/安装吗/浏览器" 中英文版）检测后整段替换。
- 中英双语：按页面 <html lang> 选 zh / en 内容。
- 模板 C 注入 <footer 前（回退 </body 前）；模板 D 注入 <footer 前。
- 全程 CRLF；修复页内非法 JSON-LD；不覆盖页面已有工具专属可见 FAQ。
- 孤儿占位页（currency-converter / pdf-converter 等）用页内 title/desc 生成。

用法：
  python _p1_expand_unified.py --dry-run --category=图片工具 --limit=2
  python _p1_expand_unified.py --category=图片工具
  python _p1_expand_unified.py --orphans          # 处理已知孤儿占位页
  python _p1_expand_unified.py --all               # 全量（谨慎）
"""
import json, os, re, sys, html as htmlmod

BASE = os.path.dirname(os.path.abspath(__file__))
INSERT_MARK = "<!-- P1-EXPAND SEO CONTENT -->"
CRLF = "\r\n"

# 通用 FAQ 问题集合（用于检测并替换）
GEN_ZH = {
    "这个工具免费吗？", "我的文件会上传到服务器吗？", "需要安装软件吗？",
    "支持哪些浏览器？", "我的文件会上传吗？", "文件会上传到服务器吗？",
}
GEN_EN = {
    "Is this tool free?", "Are my files uploaded to a server?",
    "Which browsers are supported?", "How to use this tool?",
}

CJK = re.compile(r"[一-鿿]")

# ------------------------- 分类模块（适合谁 / 进阶技巧） -------------------------
CAT_MODULE_ZH = {
    "图片工具": {
        "audiences": "设计师、自媒体运营、电商卖家，以及任何经常需要处理截图、头像、商品图的普通用户。",
        "tips": ["批量处理前先用统一规则命名，结果更容易区分", "对画质要求高时避免过度压缩，保留细节",
                 "处理前后留意尺寸与比例，避免变形", "多张图可先拼合或统一格式再一次性导出"],
    },
    "AI工具": {
        "audiences": "内容创作者、学生、程序员、运营和职场人士，想把重复脑力活交给 AI 提效的人。",
        "tips": ["把需求说清楚、给足上下文，生成质量更高", "长任务拆成几步，逐步迭代比一次成型更稳",
                 "关键内容务必人工核对，AI 结果仅供参考", "把常用提示词存成模板，复用更省时"],
    },
    "生活工具": {
        "audiences": "需要快速换算、记账、安排日程的普通用户，以及经常跨境购物或出差旅行的人。",
        "tips": ["涉及金额或日期的结果，核对一遍再使用", "把常用单位或币种设为默认，减少重复操作",
                 "倒计时、日历类工具可提前设好提醒", "随机类工具适合做决策或抽奖，结果仅供娱乐"],
    },
    "文本工具": {
        "audiences": "编辑、文案、程序员和学生，经常要整理、清洗或比对大段文字的人。",
        "tips": ["大文件先小样验证再全量处理", "去重/排序前确认是否要保留原顺序",
                 "正则操作前备份原始文本", "处理完用字数统计快速验收"],
    },
    "SEO工具": {
        "audiences": "站长、独立博主、内容运营和增长团队，关注搜索可见度与流量的人。",
        "tips": ["先看清页面当前指标，再针对性优化", "标题与描述保持简洁且含核心词",
                 "外链与内链搭配，提升整体权重", "改动后隔几天回看排名变化"],
    },
    "开发工具": {
        "audiences": "前端、后端、脚本开发者，以及需要临时格式化、编码或调试的工程师。",
        "tips": ["格式化前保留原始副本", "正则/Base64 处理注意字符编码",
                 "大 JSON 先折叠再定位字段", "结果可直接复制进编辑器继续改"],
    },
    "视频工具": {
        "audiences": "短视频创作者、教程作者、运营，以及需要裁剪、合并或提取素材的用户。",
        "tips": ["导出前确认分辨率与帧率", "大视频分段处理更稳妥",
                 "提取音频时注意格式兼容", "GIF 适合做动图预览，时长别太长"],
    },
    "音频工具": {
        "audiences": "播客主、视频配音、音乐爱好者和需要剪辑或转换语音的用户。",
        "tips": ["降噪强度适中，避免过度损伤原音", "剪辑前标记好入出点",
                 "导出格式选播放器兼容的", "语音转文字后务必校对专有名词"],
    },
    "金融工具": {
        "audiences": "个人理财、房贷车贷规划、投资和记账的用户，以及需要快速估算的人。",
        "tips": ["利率/汇率会变动，结果以当下为准", "长期规划用复利视角看",
                 "贷款类结果仅作参考，以机构为准", "重要决策前多换几个参数对比"],
    },
    "设计工具": {
        "audiences": "设计师、产品经理、运营，以及需要快速生成或排版视觉素材的人。",
        "tips": ["导出前确认尺寸与用途匹配", "二维码类注意留足静区便于扫描",
                 "AI 工具生成结果可二次编辑", "统一风格有助于品牌一致"],
    },
    "办公工具": {
        "audiences": "职场人士、教师、学生，经常做 PPT、汇报和文档整理的人。",
        "tips": ["模板统一字体与配色更专业", "长文档先列大纲再填充",
                 "导出前检查页码与目录", "多人协作时约定好命名规范"],
    },
    "PDF工具": {
        "audiences": "办公行政、法务财务、师生，以及经常处理合同、论文与扫描件的人。",
        "tips": ["批量前规范命名，结果易区分", "大文件分批处理避免卡顿",
                 "导出后核对页码与书签", "多步任务可串接使用（先压再合）"],
    },
}
CAT_MODULE_EN = {
    "图片工具": {"audiences": "Designers, social media managers, e-commerce sellers, and anyone who often handles screenshots or product images.",
                 "tips": ["Name files consistently before batch processing", "Avoid over-compression when quality matters",
                          "Keep aspect ratio to prevent distortion", "Merge or unify format before exporting"]},
    "AI工具": {"audiences": "Creators, students, developers, and professionals who want AI to handle repetitive mental work.",
               "tips": ["Give clear context for better output", "Break big tasks into steps",
                        "Always proofread key content", "Save reusable prompt templates"]},
    "生活工具": {"audiences": "Everyday users who need quick conversion, budgeting, or scheduling, plus travelers and cross-border shoppers.",
                 "tips": ["Double-check amounts and dates", "Set common units as default",
                          "Set reminders for countdowns", "Random tools are for fun decisions"]},
    "文本工具": {"audiences": "Editors, writers, developers, and students who clean or compare text.",
                 "tips": ["Validate on a sample first", "Decide whether order matters", "Back up before regex", "Verify with word count"]},
    "SEO工具": {"audiences": "Site owners, bloggers, and growth teams focused on search visibility.",
                "tips": ["Read current metrics first", "Keep titles concise with core keywords", "Combine internal and external links", "Recheck rankings after changes"]},
    "开发工具": {"audiences": "Front-end, back-end, and script developers who need quick formatting or debugging.",
                 "tips": ["Keep an original copy", "Watch character encoding", "Collapse big JSON to locate fields", "Paste results straight into editor"]},
    "视频工具": {"audiences": "Short-video creators, tutorial authors, and users who trim or merge clips.",
                 "tips": ["Confirm resolution and fps", "Process large video in segments", "Watch audio format compatibility", "Keep GIF previews short"]},
    "音频工具": {"audiences": "Podcasters, voice-over artists, and users who edit or convert audio.",
                 "tips": ["Use moderate noise reduction", "Mark in/out points first", "Pick a compatible export format", "Proofread transcribed terms"]},
    "金融工具": {"audiences": "Individuals planning loans, investments, or budgeting.",
                 "tips": ["Rates change; treat results as current", "Think in compound terms long-term", "Loan figures are indicative", "Compare several parameters"]},
    "设计工具": {"audiences": "Designers, PMs, and anyone generating visual assets quickly.",
                 "tips": ["Match export size to use", "Leave quiet zone for QR codes", "Edit AI output further", "Keep a consistent style"]},
    "办公工具": {"audiences": "Professionals, teachers, and students making slides and documents.",
                 "tips": ["Unify fonts and colors", "Outline before filling", "Check page numbers", "Agree on naming for collaboration"]},
    "PDF工具": {"audiences": "Office, legal, finance, and students handling contracts and scans.",
                "tips": ["Name files consistently", "Process large files in batches", "Verify page numbers", "Chain steps (compress then merge)"]},
}

# ------------------------- 功能 → FAQ 库（中文） -------------------------
FUNC_FAQ_ZH = {
    "crop": [("裁剪后画质会下降吗？", "一般不会。裁剪只是截取画面局部，不改变剩余区域的清晰度，导出后依旧清晰。"),
             ("能只裁剪一部分区域吗？", "可以。在画面上框选需要保留的范围即可，其余部分会被裁掉。"),
             ("支持哪些图片格式？", "常见 JPG、PNG、WEBP 等均支持，具体以页面可选列表为准。"),
             ("裁剪结果能直接下载吗？", "能。处理完成后页面会提供下载按钮，结果保存在你自己的设备。")],
    "compress": [("压缩后还清晰吗？", "工具会在体积和清晰度之间取平衡，普通内容依旧清晰可读；对画质要求高可适当调低压缩强度。"),
                 ("压缩对文件大小有限制吗？", "没有固定上限，但文件越大处理越久，必要时可分批压缩。"),
                 ("压缩后还能打印吗？", "可以。压缩只减小体积，排版与内容不变，打印效果一致。"),
                 ("支持批量压缩吗？", "支持。可一次加入多张图，处理完通常能打包下载。")],
    "convert": [("转换后排版会乱吗？", "工具尽量保留原始排版、字体与图片，极少数复杂版式建议导出后核对一遍。"),
                ("转换需要联网吗？", "不需要。转换在浏览器本地完成，文件不上传。"),
                ("能转成哪些格式？", "常见格式互转均支持，具体以页面可选目标格式为准。"),
                ("转换对大小有限制吗？", "无固定限制，但文件越大越久，超大文件建议先拆分。")],
    "resize": [("改尺寸会变形吗？", "按指定宽高或比例调整；锁定比例可避免变形，自由拉伸则可能失真。"),
               ("最大能放大到多少？", "可设目标像素或百分比，过大可能变模糊，建议配合放大增强。"),
               ("改尺寸后画质如何？", "普通缩放保持可用画质，显著放大建议用超分辨率功能。"),
               ("能批量改尺寸吗？", "支持。统一设定后一次处理多张，结果分别保存。")],
    "rotate": [("旋转后清晰度变吗？", "不会。旋转只改方向，不改变分辨率。"),
               ("能只旋转几页/几张吗？", "可以。选择需要调整的页面或图片范围即可。"),
               ("支持 90/180 度吗？", "支持。可按 90 度步进或 180 度翻转。"),
               ("能批量旋转吗？", "可以。对多页/多图指定统一角度一次性处理。")],
    "watermark": [("水印能被去掉吗？", "作为所有者你可随时重新生成不带水印版本；对外分发的水印用于标识归属。"),
                  ("能只在部分页加水印吗？", "可以。设置覆盖范围即可灵活控制。"),
                  ("支持图片水印吗？", "支持。可上传 PNG 等透明图片作 logo 水印，调大小与透明度。"),
                  ("水印位置能自定义吗？", "能。四角、居中、平铺等位置均可选。")],
    "removebg": [("去背景后边缘干净吗？", "自动识别主体并去除背景，复杂边缘建议放大预览后微调。"),
                 ("去背后能换底色吗？", "可以。去背景后通常可填纯色或透明，便于二次合成。"),
                 ("支持哪些图片？", "常见 JPG/PNG 均支持，主体清晰的图效果更好。"),
                 ("结果能直接下载吗？", "能。导出为透明 PNG 最常用，也可转其他格式。")],
    "upscale": [("放大后真的更清晰吗？", "超分辨率会在放大同时补充细节，比普通拉伸更锐利，但极模糊原图提升有限。"),
                ("最大放大几倍？", "常见 2x/4x 可选，倍数越大对原图要求越高。"),
                ("放大需要联网吗？", "不需要。处理在浏览器本地完成。"),
                ("适合哪些图？", "老照片、截图、电商图等低分辨率素材最适合。")],
    "merge": [("合并后还能搜索文字吗？", "可以。合并只是按顺序拼接，原有文字保留，仍可被搜索与复制。"),
              ("怎么调整顺序？", "在工具里拖拽文件即可调整先后，确认后再生成。"),
              ("一次能合并多少？", "数量无硬上限，但取决于设备性能，文件多时建议分批。"),
              ("合并后体积会变大吗？", "会随页数累加，若过大可先压缩再合并。")],
    "split": [("能只提取几页吗？", "可以。按页码范围提取，未选中的不会被导出。"),
              ("拆分后会丢书签吗？", "单页文件不含原大纲；需保留结构建议先在原文件整理。"),
              ("拆分大文件慢吗？", "在本地完成，速度取决于体积与设备。"),
              ("能分别保存成独立文件吗？", "可以。每页或每范围生成独立文件，方便发送。")],
    "translate": [("翻译准确吗？", "对常见语种与日常表达效果很好；专业术语建议人工核对。"),
                 ("支持哪些语言？", "常见中英日越等互译均支持，以页面可选列表为准。"),
                 ("需要联网吗？", "翻译需调用模型，请在联网环境下使用，文本不长期留存。"),
                 ("能整段翻译吗？", "可以。粘贴或输入整段文本，一次性得到译文。")],
    "summary": [("总结会遗漏重点吗？", "工具按关键信息提炼，长文建议通读原文，重要处可让它在总结中保留。"),
                ("支持多长文本？", "适合文章、报告等长文本，超长可分段处理。"),
                ("能调总结长度吗？", "通常可设简短/标准，按需要选择。"),
                ("结果能直接复制吗？", "能。总结生成后可直接复制或导出。")],
    "write": [("生成的内容能直接用吗？", "可以。结果直接显示，可复制、续写或导出；关键内容建议人工核对。"),
              ("写不出来怎么办？", "补充主题、受众、语气等要求，约束越清晰产出越贴合。"),
              ("支持哪些文体？", "文案、邮件、大纲、社媒帖等常见文体均支持。"),
              ("能改语气吗？", "能。说明正式/口语/活泼等风格即可调整。")],
    "paraphrase": [("改写会改意思吗？", "改写重在换表达不改原意，关键句建议复核。"),
                  ("能调风格吗？", "可要求更正式、更简洁或更口语。"),
                  ("适合哪些场景？", "降重、润色、本地化表述都适用。"),
                  ("结果能直接复制吗？ " , "能。改写后直接复制使用。")],
    "chat": [("它能连续对话吗？", "支持多轮对话，可基于上下文继续追问。"),
             ("回答可靠吗？", "对事实类内容建议交叉核实，它也可能出错。"),
             ("能处理文件吗？", "部分版本支持上传文本/文档，以页面功能为准。"),
             ("记录会被保存吗？", "对话按页面规则处理，敏感信息请勿输入。")],
    "code": [("生成的代码能直接用吗？", "可直接复制进项目，复杂逻辑建议先本地测试。"),
             ("支持哪些语言？", "常见前后端语言均支持，以页面说明为准。"),
             ("能解释现有代码吗？", "可以。粘贴代码让它逐段说明作用。"),
             ("错误能帮忙修吗？", "能。贴上报错信息，它可给出修改建议。")],
    "format": [("格式化会改变内容吗？", "不会。只调整缩进与换行，数据原样保留。"),
               ("支持哪些格式？", "JSON、SQL、HTML 等常见结构均支持。"),
               ("处理大文件慢吗？", "在本地完成，超大文件可分次处理。"),
               ("结果能直接复制吗？", "能。格式化后直接复制进编辑器。")],
    "calc": [("计算准确吗？", "按页面公式精确计算，输入正确则结果可靠。"),
             ("支持哪些计算？", "取决于具体工具，如汇率、贷款、BMI 等。"),
             ("结果能导出吗？", "可复制或截图保存，部分支持导出。"),
             ("参数能改吗？", "能。随时调整输入，结果实时更新。")],
    "encrypt": [("忘记密码能打开吗？", "密码由你设定，工具不保存也不传输，请务必牢记。"),
                ("能设不同权限吗？", "可以。常见禁止打印、复制、编辑等权限可勾选。"),
                ("加密后还能打开吗？", "知道密码的设备均可正常打开。"),
                ("加密安全吗？", "处理在本地完成，文件不上传。")],
    "decrypt": [("解密需要原密码吗？", "是的。合法解密需你已知的正确密码，仅用于你有权限的文件。"),
                ("解密后内容保留吗？", "会。解密只移除打开限制，内容原样保留。"),
                ("解密后能重加密吗？ " , "可以。随时可再次设密码。"),
                ("对大小有限制吗？", "无硬性限制，大文件建议分批。")],
    "ocr": [("识别后文字能复制吗？", "可以。识别后文本变可选中真实文字，方便搜索复制。"),
            ("扫描件识别准吗？", "清晰正向扫描识别率高；倾斜水印建议先校正。"),
            ("支持哪些语言？", "常见中英文均可，多语混排勾选对应语种。"),
            ("识别后排版保留吗？", "文字层叠加原图，复杂表格建议人工核对。")],
    "cut": [("剪辑后画质变吗？", "剪裁区间不改变编码质量，导出清晰。"),
            ("能精确掐头去尾吗？", "可以。设定起止时间，只保留需要的片段。"),
            ("支持哪些格式？", "常见视频格式均支持，以页面为准。"),
            ("结果能直接下载吗？", "能。处理完提供下载。")],
    "gif": [("GIF 时长怎么定？", "按设定时长截取视频片段生成动图，时长别太长更易传播。"),
            ("能调分辨率吗？", "可以。在体积与清晰度间取舍。"),
            ("支持哪些来源？", "视频或图片序列均可转 GIF。"),
            ("结果能直接下载吗？", "能。生成后直接下载。")],
    "extractaudio": [("提取的音频清晰吗？", "直接抽取音轨，质量与原视频一致。"),
                     ("支持哪些格式？", "MP3 等常见格式，以页面可选为准。"),
                     ("会损失画质吗？", "只抽声音，画面被丢弃，音频本身不失真。"),
                     ("结果能直接下载吗？", "能。导出后保存在本地。")],
    "tts": [("发音自然吗？", "合成语音较自然，可试听后选择满意的声音。"),
            ("支持哪些语言？", "常见中英等语种均支持。"),
            ("能调语速吗？ " , "可以。按需要加快或放慢。"),
            ("结果能下载吗？", "能。生成音频可直接下载使用。")],
    "stt": [("识别准确吗？", "清晰人声识别率高；杂音环境建议先降噪。"),
            ("支持哪些语言？", "常见语种均支持，以页面为准。"),
            ("能导出文字吗？", "能。识别结果可复制或导出文本。"),
            ("专业名词准吗？", "建议对专有名词人工校对。")],
    "dedupe": [("去重会改顺序吗？", "默认可保留首次出现顺序，具体以选项为准。"),
               ("按行还是按块？", "通常按行去重，适合列表类文本。"),
               ("大小写算重复吗？", "可设是否忽略大小写，按需选择。"),
               ("结果能直接复制吗？", "能。去重后直接复制使用。")],
    "wordcount": [("统计包含标点吗？", "可按字符或词统计，是否含标点以选项为准。"),
                  ("能分中英文吗？", "通常分别统计中文字与英文词，更直观。"),
                  ("大文件慢吗？", "在本地完成，普通文档瞬时出结果。"),
                  ("结果能复制吗？", "能。统计数字直接显示。")],
    "regex": [("正则怎么写？", "页面通常提供示例，照着改即可上手。"),
              ("能测试吗？", "可以。输入文本实时看匹配高亮。"),
              ("不懂正则能用吗？", "可用预设模式，如邮箱、网址提取。"),
              ("结果能导出吗？", "能。匹配内容可复制。")],
    "timestamp": [("时间戳怎么转？", "输入 Unix 时间戳或日期，双向转换。"),
                  ("支持时区吗？", "通常按 UTC 或本地时区，以页面为准。"),
                  ("毫秒级支持吗？", "多数支持秒/毫秒，注意单位。"),
                  ("结果能复制吗？", "能。转换结果直接显示。")],
    "hash": [("哈希能反推原文吗？", "不能。哈希单向，只能校验一致性。"),
             ("支持哪些算法？", "MD5、SHA 等常见算法均支持。"),
             ("用来做什么？", "校验文件完整性、比对内容是否一致。"),
             ("结果能复制吗？", "能。哈希值直接显示。")],
    "qr": [("生成的二维码能扫吗？", "能。生成后可用手机相机直接扫描。"),
           ("能存网址吗？", "可以。网址、文本、WiFi 等均可编码。"),
           ("能调大小吗？", "能。导出时选合适尺寸，注意留静区。"),
           ("结果能下载吗？", "能。通常导出为 PNG 或 SVG。")],
    "unit": [("支持哪些单位？", "长度、面积、体积、重量、温度等常见单位均支持。"),
             ("换算准确吗？", "按标准换算系数计算，输入正确即准确。"),
             ("能反向换算吗？", "能。任意两单位互相转换。"),
             ("结果能复制吗？", "能。结果直接显示。")],
    "currency": [("汇率是实时的吗？", "汇率定期更新，具体以页面标注的时效为准。"),
                 ("支持哪些货币？", "覆盖全球主要货币，以页面可选列表为准。"),
                 ("换算准确吗？", "按当前汇率估算，实际以银行成交价为准。"),
                 ("能复制结果吗？", "能。换算金额直接显示可复制。")],
    "date": [("能算间隔多少天吗？", "可以。选两个日期即得相差天数。"),
             ("支持倒计时吗？", "支持。设目标日期实时显示剩余时间。"),
             ("时区怎么算？", "按页面设定时区计算，跨境以当地为准。"),
             ("结果能复制吗？", "能。日期差直接显示。")],
}

# 功能关键词 → FUNC_FAQ_ZH 键（slug 用英文词，name/desc 用中文词）
FUNC_MAP = [
    (("crop", "裁剪"), "crop"),
    (("compress", "压缩"), "compress"),
    (("convert", "转换", "格式"), "convert"),
    (("resize", "尺寸", "调整大小"), "resize"),
    (("rotate", "旋转"), "rotate"),
    (("watermark", "水印"), "watermark"),
    (("remove-bg", "去背景", "抠图", "bg"), "removebg"),
    (("upscale", "super-resolution", "放大", "超分", "enhance"), "upscale"),
    (("sharpen", "锐化"), "upscale"),
    (("merge", "合并"), "merge"),
    (("split", "拆分", "分割", "提取页"), "split"),
    (("translate", "翻译"), "translate"),
    (("summary", "summar", "总结", "摘要"), "summary"),
    (("write", "写作", "文案", "copy"), "write"),
    (("paraphrase", "改写", "润色", "polish"), "paraphrase"),
    (("chat", "对话", "问答", "qa"), "chat"),
    (("code", "代码", "code"), "code"),
    (("format", "格式化", "format"), "format"),
    (("calculator", "calc", "计算", "计算器"), "calc"),
    (("converter", "换算", "汇率", "货币"), "currency"),
    (("encrypt", "加密", "encrypt", "protect"), "encrypt"),
    (("decrypt", "解密", "unlock", "decrypt"), "decrypt"),
    (("ocr", "识别", "ocr"), "ocr"),
    (("cut", "剪辑", "cutter", "trim"), "cut"),
    (("gif",), "gif"),
    (("to-mp3", "to-audio", "提取音频"), "extractaudio"),
    (("tts", "text-to-speech", "语音合成", "配音"), "tts"),
    (("stt", "speech-to-text", "语音转", "听写"), "stt"),
    (("dedupe", "去重"), "dedupe"),
    (("wordcount", "字数", "word count"), "wordcount"),
    (("regex", "正则"), "regex"),
    (("timestamp", "时间戳"), "timestamp"),
    (("hash", "哈希", "hash"), "hash"),
    (("qr", "二维码"), "qr"),
    (("unit", "单位换算"), "unit"),
    (("currency", "汇率", "货币"), "currency"),
    (("date", "日期", "倒计时", "日历"), "date"),
]

# 孤儿占位页元数据（不在 tools-data.json，用页内 title/desc 兜底）
ORPHAN_PAGES = [
    "/tools/currency-converter.html",
    "/tools/pdf-converter.html",
]


def load_tools():
    with open(os.path.join(BASE, "data", "tools-data.json"), encoding="utf-8") as f:
        return json.load(f)


def detect_lang(doc):
    m = re.search(r'<html[^>]*lang="([^"]+)"', doc)
    if m and m.group(1).lower().startswith("en"):
        return "en"
    return "zh"


def pick_func(tool):
    blob = " ".join([tool.get("slug", ""), tool.get("name", ""), tool.get("description", "")]).lower()
    for keys, fk in FUNC_MAP:
        for k in keys:
            if k.lower() in blob:
                return fk
    return None


def extract_existing_faq(doc):
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        raw = m.group(1)
        if '"@type": "FAQPage"' not in raw and '"@type":"FAQPage"' not in raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue
        ents = [(e.get("name", ""), e.get("acceptedAnswer", {}).get("text", ""))
                for e in obj.get("mainEntity", []) if isinstance(e, dict)]
        return ents if ents else None
    return None


def is_generic(faq, lang):
    if not faq:
        return False
    qs = {q for q, _ in faq}
    return bool(qs) and qs.issubset(GEN_ZH if lang == "zh" else GEN_EN)


def gen_faq(tool, lang):
    """返回 [(q,a)...] 工具专属 FAQ（4 条）。"""
    if lang == "en":
        return gen_faq_en(tool)
    name = tool.get("name") or os.path.splitext(os.path.basename(tool.get("url", "")))[0]
    desc = (tool.get("description") or "").rstrip("。")
    fk = pick_func(tool)
    if fk and fk in FUNC_FAQ_ZH:
        # 把工具名嵌入每题，保证每页 FAQ 唯一（绝不退回通用四问）
        return [(f"用{name}时，{q}", a) for q, a in FUNC_FAQ_ZH[fk][:4]]
    # 兜底：由 description 驱动，天然差异化
    scene = desc or f"{name} 把繁琐操作变成浏览器里的一步工具"
    q1 = f"{name}主要能做什么？"
    a1 = f"{name}：{scene}。它把原本需要专门软件或手动完成的任务，变成浏览器里一步到位的小工具，省去下载安装与注册的麻烦。"
    q2 = f"第一次使用{name}要注意什么？"
    a2 = "打开网页后按界面提示操作：选择或拖入文件、设置参数，本地处理完成后直接下载结果。整个过程在浏览器本地完成，文件不会离开你的设备。"
    q3 = f"{name}处理我的文件安全吗？"
    a3 = f"安全。{name}所有计算都在你的浏览器本地运行，文件不会上传到任何服务器，处理完关闭页面即可，不留痕迹。"
    # 第 4 条按功能/分类给针对性问题
    cat = tool.get("category", "")
    if any(k in (name + desc) for k in ("换算", "计算", "汇率", "转换", "单位")):
        q4 = f"{name}支持哪些{cat or '项目'}？"
        a4 = "覆盖常见项目，具体以页面可选列表为准；结果可直接复制或下载。"
    elif any(k in (name + desc) for k in ("写作", "翻译", "总结", "生成", "对话", "AI")):
        q4 = f"用{name}生成的内容可以直接用吗？"
        a4 = "可以。生成结果会直接显示在页面，你可复制、续写或导出；建议对关键内容做人工核对，确保符合你的场景。"
    else:
        q4 = f"{name}的结果怎么保存？"
        a4 = "处理完成后页面会提供下载或复制按钮，结果保存在你自己的设备，随时可用。"
    return [(q1, a1), (q2, a2), (q3, a3), (q4, a4)]


def gen_faq_en(tool):
    name = tool.get("name__en") or tool.get("name") or os.path.splitext(os.path.basename(tool.get("url", "")))[0]
    desc = (tool.get("description__en") or tool.get("description") or "a handy browser tool").rstrip(".")
    q1 = f"What does {name} do?"
    a1 = f"{name} {desc.lower() if desc[0].islower() else desc}. It turns tedious tasks into a one-step browser tool—no install, no sign-up."
    q2 = f"Is {name} safe to use?"
    a2 = f"Yes. {name} runs entirely in your browser; your files are not uploaded to any server and nothing is kept after you close the tab."
    q3 = f"Do I need to install software for {name}?"
    a3 = "No. It is a web tool—just open the page and use it; all processing happens locally."
    q4 = f"How do I save results from {name}?"
    a4 = "After processing, use the on-page download or copy button; results stay on your own device."
    return [(q1, a1), (q2, a2), (q3, a3), (q4, a4)]


def gen_body(tool, lang, faq_pairs):
    name = (tool.get("name__en") if lang == "en" else None) or tool.get("name") or os.path.splitext(os.path.basename(tool.get("url", "")))[0]
    desc = (tool.get("description__en") if lang == "en" else None) or tool.get("description") or ""
    desc = desc.rstrip("。").rstrip(".") + ("。" if lang == "zh" else ".")
    cat = tool.get("category", "")
    mod = (CAT_MODULE_EN if lang == "en" else CAT_MODULE_ZH).get(cat) or {
        "audiences": ("普通用户与各类职场人群。" if lang == "zh" else "General users and professionals."),
        "tips": ["按需使用，结果以实际为准" if lang == "zh" else "Use as needed; verify results",
                 "关键内容建议人工核对" if lang == "zh" else "Proofread key content"],
    }
    if lang == "en":
        scene = f"{name} {desc} It turns a tedious task into a one-step browser tool—no install, no sign-up, everything runs locally."
        who = mod["audiences"]
        tips_ul = "<ul>" + CRLF + CRLF.join(f"<li>{htmlmod.escape(t)}</li>" for t in mod["tips"][:4]) + CRLF + "</ul>"
        sections = [f'<h2>Use cases</h2>{CRLF}  <p>{htmlmod.escape(scene)}</p>',
                    f'<h2>Who it is for</h2>{CRLF}  <p>{htmlmod.escape(who)}</p>',
                    f'<h2>Tips</h2>{CRLF}  {tips_ul}']
    else:
        scene = f"{name}：{desc}它把繁琐的操作变成浏览器里的一步工具，无需安装软件、无需注册，打开网页即可使用，所有计算都在本地完成，文件不会离开你的设备。"
        who = mod["audiences"]
        tips_ul = "<ul>" + CRLF + CRLF.join(f"<li>{htmlmod.escape(t)}</li>" for t in mod["tips"][:4]) + CRLF + "</ul>"
        sections = [f'<h2>适用场景</h2>{CRLF}  <p>{htmlmod.escape(scene)}</p>',
                    f'<h2>适合谁使用</h2>{CRLF}  <p>{htmlmod.escape(who)}</p>',
                    f'<h2>进阶技巧</h2>{CRLF}  {tips_ul}']
    if faq_pairs:
        faq_html = CRLF.join(
            f'<details open><summary>{htmlmod.escape(q)}</summary><p>{htmlmod.escape(a)}</p></details>'
            for q, a in faq_pairs)
        h = "常见问题" if lang == "zh" else "FAQ"
        sections.append(f'<h2>{h}</h2>{CRLF}  <div class="faq">{CRLF}    {faq_html}{CRLF}  </div>')
    inner = CRLF + CRLF.join(sections) + CRLF
    return f"{INSERT_MARK}{CRLF}<section class=\"section\">{inner}</section>"


def repair_jsonld(doc):
    def fix_one(raw):
        cjk = lambda ch: ("\u4e00" <= ch <= "\u9fff") or ch.isalnum()
        chars = list(raw)
        flip = False
        for i, ch in enumerate(chars):
            if ch == '"' and 0 < i < len(chars) - 1 and cjk(chars[i - 1]) and cjk(chars[i + 1]):
                chars[i] = "\u201c" if not flip else "\u201d"
                flip = not flip
        fixed = "".join(chars)
        try:
            return json.dumps(json.loads(fixed), ensure_ascii=False, separators=(",", ": ")), True
        except Exception:
            return None, False

    out = doc
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        raw = m.group(1).strip()
        try:
            json.loads(raw)
            continue
        except Exception:
            new_raw, ok = fix_one(raw)
            if ok:
                out = out[:m.start()] + '<script type="application/ld+json">' + new_raw + '</script>' + out[m.end():]
                return repair_jsonld(out)
            out = out[:m.start()] + "<!-- P1: removed invalid JSON-LD -->" + out[m.end():]
            return repair_jsonld(out)
    return out


def remove_faq_jsonld(doc):
    out = doc
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', doc, re.S):
        raw = m.group(1)
        if '"@type": "FAQPage"' in raw or '"@type":"FAQPage"' in raw:
            out = out[:m.start()] + "<!-- P1: replaced generic FAQ JSON-LD -->" + out[m.end():]
    return out


def remove_visible_faq(doc):
    """删除页面内已有的可见 <div class="faq">…</div> 块，避免新旧 FAQ 并存。"""
    return re.sub(r'<div class="faq">.*?</div>', '', doc, flags=re.S)


def remove_inline_generic_faq(doc):
    """删除工具页正文里硬编码的通用 FAQ 块（两种形态：<div class="box"> 与 <div class="seo-card">）。"""
    pat = re.compile(
        r'<h2[^>]*>.*?常见问题.*?</h2>\s*<div class="box">.*?这个工具免费吗.*?</div>\s*'
        r'|<div class="seo-card">.*?这个工具免费吗.*?</div>\s*',
        re.S)
    return pat.sub('', doc)


def extract_orphan_meta(path, d):
    name = os.path.splitext(os.path.basename(path))[0]
    desc = ""
    mt = re.search(r"<title[^>]*>(.*?)</title>", d, re.S)
    if mt:
        name = re.sub(r"\s*[-|]\s*.*$", "", mt.group(1)).strip() or name
    md = re.search(r'<meta name="description" content="([^"]*)"', d)
    if md:
        desc = md.group(1)
    # 去掉站点级样板句，避免孤儿页互相重复
    BOILER = "免费在线使用，浏览器本地运行，无需安装、无需上传文件，保护隐私安全。ZenTools 提供数百款实用在线工具。"
    desc = desc.replace(BOILER, "").strip("。").strip()
    slug = os.path.splitext(os.path.basename(path))[0]
    return {"url": "/" + path, "name": name, "description": desc,
            "category": "工具", "slug": slug}


def strip_p1(doc):
    """移除已注入的 P1-EXPAND 整段（repair 用）。"""
    idx = doc.find(INSERT_MARK)
    if idx == -1:
        return doc
    end = doc.find("</section>", idx)
    if end == -1:
        return doc
    return doc[:idx] + doc[end + len("</section>"):]


def build_faq_jsonld(faq_pairs, lang):
    obj = {"@context": "https://schema.org", "@type": "FAQPage",
           "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
                          for q, a in faq_pairs]}
    return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ": ")) + '</script>'


def expand_page(path, tool, repair=False):
    full = os.path.join(BASE, path)
    if not os.path.exists(full):
        return None, "FILE_MISSING"
    with open(full, encoding="utf-8", newline="") as f:
        doc = f.read()
    if INSERT_MARK in doc:
        if not repair:
            return None, "ALREADY_DONE"
        # repair：清空旧 P1 块与旧 FAQ，准备重生成
        doc = strip_p1(doc)
        doc = remove_visible_faq(doc)
        doc = remove_faq_jsonld(doc)
    if "hero-gradient-text" not in doc and "<footer" not in doc and "</body" not in doc:
        return None, "NO_ANCHOR"
    anchor = "<footer" if "<footer" in doc else "</body"
    doc = repair_jsonld(doc)
    lang = detect_lang(doc)
    has_visible = "<details" in doc
    existing = extract_existing_faq(doc)
    generic = is_generic(existing, lang)

    if has_visible and not generic:
        # 页面已有工具专属可见 FAQ → 保留，只补长文，不动 JSON-LD
        faq_pairs = None
        add_jsonld = False
    else:
        # REPLACE：先删旧可见 FAQ（含通用可见 FAQ 与目录页内联通用块），再注入专属 FAQ，杜绝重复
        doc = remove_visible_faq(doc)
        doc = remove_inline_generic_faq(doc)
        faq_pairs = gen_faq(tool, lang)
        add_jsonld = True

    body = gen_body(tool, lang, faq_pairs)
    new_doc = doc.replace(anchor, body + CRLF + anchor, 1)

    if add_jsonld and faq_pairs:
        new_doc = remove_faq_jsonld(new_doc)
        new_doc = new_doc.replace("</body>", build_faq_jsonld(faq_pairs, lang) + CRLF + "</body>", 1)

    if new_doc == doc:
        return None, "NO_CHANGE"
    return new_doc, "OK"


def main():
    dry = "--dry-run" in sys.argv
    orphans = "--orphans" in sys.argv
    do_all = "--all" in sys.argv
    repair = "--repair" in sys.argv
    category = None
    limit = None
    for a in sys.argv[1:]:
        if a.startswith("--category="):
            category = a.split("=", 1)[1]
        elif a.startswith("--limit="):
            limit = int(a.split("=", 1)[1])

    targets = []
    if orphans:
        # 自动发现所有「不在 tools-data.json + 含通用 FAQ」的孤儿页（tools/*.html 等目录页）
        data_tool_urls = {t.get("url", "").lstrip("/") for t in load_tools().get("tools", [])}
        BLOCK_DIRS = {"articles", "tutorials", "guides", "compare", "professions",
                      "docs", "assets", "data", ".git", "node_modules",
                      "coverage_analysis", "_site", "templates"}
        for root, dirs, files in os.walk(BASE):
            dirs[:] = [d for d in dirs if d not in BLOCK_DIRS]
            for fn in files:
                if not fn.endswith(".html"):
                    continue
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, BASE).replace(os.sep, "/")
                if "/" not in rel:
                    continue
                if rel in data_tool_urls:
                    continue
                with open(full, encoding="utf-8", newline="") as f:
                    d = f.read()
                if not ("这个工具免费吗" in d or "Are my files" in d or "Is this tool free" in d):
                    continue
                targets.append((rel, extract_orphan_meta(rel, d)))
    else:
        data = load_tools()
        for t in data.get("tools", []):
            if category and t.get("category") != category:
                continue
            if not do_all and category is None:
                # 默认不跑全量，需显式 --category 或 --all
                continue
            targets.append((t.get("url", "").lstrip("/"), t))

    if limit:
        targets = targets[:limit]
    done = skip = 0
    for path, tool in targets:
        new_doc, status = expand_page(path, tool, repair=repair)
        if status != "OK":
            if status not in ("ALREADY_DONE", "NO_ANCHOR"):
                print(f"[{status}] {path} ({tool.get('name')})")
            skip += 1
            continue
        if dry:
            m = re.search(r"P1-EXPAND SEO CONTENT -->(.*?)</section>", new_doc, re.S)
            txt = re.sub(r"<[^>]+>", " ", m.group(1)) if m else ""
            txt = re.sub(r"\s+", " ", txt).strip()
            has_d = "<details" in new_doc
            print(f"\n===== {path} | chars={len(CJK.findall(txt))} | visibleFAQ={has_d} =====\n{txt[:1100]}\n")
            done += 1
            continue
        with open(os.path.join(BASE, path), "w", encoding="utf-8", newline="") as f:
            f.write(new_doc)
        done += 1
    print(f"\n[SUMMARY] category={category} orphans={orphans} repair={repair} processed={done} skipped={skip} dry={dry}")


if __name__ == "__main__":
    main()
