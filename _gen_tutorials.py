#!/usr/bin/env python3
"""Generate 11 life tools tutorial HTML pages for ZenTools."""

import json, os

BASE = os.path.join(os.path.dirname(__file__), "tutorials")
IMG = os.path.join(os.path.dirname(__file__), "guides", "img")

def build_html(tool_id, title_zh, desc_zh, func_zh, duration, tool_url, svg_file, step_keys, tips, faqs, related, cat_label="🏠 生活工具"):
    """Build a complete tutorial HTML with 4-language i18n."""
    
    zh = {
        "a1Intro": func_zh,
        "a1OpenBody": f'访问 <a href="{tool_url}" target="_blank">{title_zh.split("：")[0] if "：" in title_zh else title_zh.split(":")[0]}</a>，在浏览器中直接使用。所有操作在浏览器本地完成，无需注册账号，完全免费。',
    }
    zh[f"{step_keys}Step1T"] = "打开工具"
    zh[f"{step_keys}Step1B"] = f'访问<a href="{tool_url}" target="_blank">{title_zh.split("：")[0] if "：" in title_zh else title_zh.split(":")[0]}</a>，在浏览器中打开工具页面。页面简洁直观，无需安装任何软件。'
    zh[f"{step_keys}Step2T"] = "输入数据"
    zh[f"{step_keys}Step2B"] = "在对应的输入框中输入需要计算的数据，工具会实时进行运算并显示结果。"
    zh[f"{step_keys}Step3T"] = "调整参数"
    zh[f"{step_keys}Step3B"] = "根据需要调整相关参数和选项，确保计算条件符合你的实际情况。工具提供了多种参数组合供选择。"
    zh[f"{step_keys}Step4T"] = "查看结果"
    zh[f"{step_keys}Step4B"] = "计算结果会清晰展示在页面上，你可以直接复制结果或截图保存。所有计算均可重复进行。"
    for i, tip in enumerate(tips, 1):
        zh[f"{step_keys}Tip{i}"] = tip
    for i, (q, a) in enumerate(faqs, 1):
        zh[f"{step_keys}Faq{i}Q"] = q
        zh[f"{step_keys}Faq{i}A"] = a
    zh.update({
        "introTitle": "功能介绍", "openTitle": "打开工具", "stepTitle": "操作步骤",
        "tipTitle": "实用技巧", "faqTitle": "常见问题", "relTitle": "相关工具：",
        "backToIndex": "返回教程中心", "tipLabel": "提示",
        "pageTitle": f"{title_zh} - ZenTools", "catLife": cat_label,
        "a1Title": title_zh, "a1Date": "📅 2026-06-23", "a1Read": f"⏱ {duration} 分钟阅读",
        "navHome": "首页", "navDev": "开发工具", "navAll": "全部工具",
        "navPrivacy": "隐私政策", "footerCopy": "© 2026 ZenTools. 免费在线工具箱。"
    })

    # English translations - use same structure
    en = dict(zh)
    en.update({
        "introTitle": "Introduction", "openTitle": "Open the Tool", "stepTitle": "Steps",
        "tipTitle": "Tips", "faqTitle": "FAQ", "relTitle": "Related Tools:",
        "backToIndex": "Back to Tutorials", "tipLabel": "Tip",
        "catLife": "🏠 Life Tools", "a1Read": f"⏱ {duration} min read",
        "navHome": "Home", "navDev": "Dev Tools", "navAll": "All Tools",
        "navPrivacy": "Privacy", "footerCopy": "© 2026 ZenTools. Free Online Toolbox."
    })
    for k in list(en.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                en[k] = zh[k].replace("打开工具", "Open the Tool").replace("输入数据", "Enter Data").replace("调整参数", "Adjust Parameters").replace("查看结果", "View Results")
            elif k.endswith("B"):
                en[k] = zh[k]

    ja = dict(zh)
    ja.update({
        "introTitle": "機能紹介", "openTitle": "ツールを開く", "stepTitle": "操作手順",
        "tipTitle": "ヒント", "faqTitle": "よくある質問", "relTitle": "関連ツール：",
        "backToIndex": "チュートリアルに戻る", "tipLabel": "ヒント",
        "catLife": "🏠 生活ツール", "a1Read": f"⏱ {duration}分",
        "navHome": "ホーム", "navDev": "開発ツール", "navAll": "すべてのツール",
        "navPrivacy": "プライバシー", "footerCopy": "© 2026 ZenTools. 無料オンラインツールボックス。"
    })
    for k in list(ja.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                ja[k] = zh[k].replace("打开工具", "ツールを開く").replace("输入数据", "データを入力").replace("调整参数", "パラメータを調整").replace("查看结果", "結果を確認")
            elif k.endswith("B"):
                ja[k] = zh[k]

    vi = dict(zh)
    vi.update({
        "introTitle": "Giới thiệu", "openTitle": "Mở Công cụ", "stepTitle": "Các bước",
        "tipTitle": "Mẹo", "faqTitle": "Câu hỏi thường gặp", "relTitle": "Công cụ liên quan:",
        "backToIndex": "Quay lại Hướng dẫn", "tipLabel": "Mẹo",
        "catLife": "🏠 Công cụ Đời sống", "a1Read": f"⏱ {duration} phút đọc",
        "navHome": "Trang chủ", "navDev": "Công cụ Dev", "navAll": "Tất cả",
        "navPrivacy": "Quyền riêng tư", "footerCopy": "© 2026 ZenTools. Hộp công cụ trực tuyến miễn phí."
    })
    for k in list(vi.keys()):
        if k.startswith(f"{step_keys}Step"):
            if k.endswith("T"):
                vi[k] = zh[k].replace("打开工具", "Mở Công cụ").replace("输入数据", "Nhập Dữ liệu").replace("调整参数", "Điều chỉnh Tham số").replace("查看结果", "Xem Kết quả")
            elif k.endswith("B"):
                vi[k] = zh[k]

    # Related tools HTML
    rel_html = " · ".join([f'<a href="{r[0]}">{r[1]}</a>' for r in related])

    # SVG steps HTML
    svg_steps = ""
    step_labels = [("打开工具", f"{title_zh} - 打开工具"),
                   ("输入数据", f"{title_zh} - 输入数据"),
                   ("调整参数", f"{title_zh} - 调整参数"),
                   ("查看结果", f"{title_zh} - 查看结果")]
    for i, (label, alt) in enumerate(step_labels, 1):
        svg_steps += f'''<h3 data-i18n="{step_keys}Step{i}T">{i}. {label}</h3>
<p data-i18n="{step_keys}Step{i}B">{zh[f"{step_keys}Step{i}B"]}</p>
<div class="screenshot-wrap"><img src="/guides/img/{svg_file}" alt="{alt}" style="max-width:100%;border-radius:12px;border:1px solid rgba(255,255,255,0.08);margin:12px 0;box-shadow:0 8px 24px rgba(0,0,0,0.3);"></div>
'''

    # Tips HTML
    tips_html = ""
    for i, tip in enumerate(tips, 1):
        tips_html += f'''<div class="tip"><strong data-i18n="tipLabel">提示 {i}：</strong><span data-i18n="{step_keys}Tip{i}">{tip}</span></div>
'''

    # FAQ HTML
    faq_html = ""
    for i, (q, a) in enumerate(faqs, 1):
        faq_html += f'''<p><strong data-i18n="{step_keys}Faq{i}Q">{q}</strong><br/><span data-i18n="{step_keys}Faq{i}A">{a}</span></p>
'''

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
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"TechArticle","headline":"{title_zh}","description":"{desc_zh}","datePublished":"2026-06-23","author":{{"@type":"Organization","name":"ZenTools"}},"publisher":{{"@type":"Organization","name":"ZenTools"}},"mainEntityOfPage":{{"@type":"WebPage","@id":"https://zentools.xyz/tutorials/{tool_id}.html"}}}}</script>
</head>
<body>
<div class="blob blob-1"></div><div class="blob blob-2"></div>
<div class="z-wrap">
<nav><div class="nav-inner"><a class="logo" href="/">ZenTools<span>2.0</span></a><div class="nav-links"><a href="/" data-i18n="navHome">首页</a><a href="/dev/" data-i18n="navDev">开发工具</a><a href="/tools.html" data-i18n="navAll">全部工具</a><select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="en">English</option><option value="ja">日本語</option><option value="vi">Tiếng Việt</option></select></div></div></nav>

<div class="page-tutorial">
<a class="back-link" href="/tutorials/">← <span data-i18n="backToIndex">返回教程中心</span></a>
<span class="page-eyebrow" data-i18n="catLife">{cat_label}</span>
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


# Define all 11 tutorials
tutorials = [
    {
        "tool_id": "volume-converter",
        "title_zh": "体积转换教程：升、加仑、立方米互转",
        "desc_zh": "学会使用 ZenTools 在线体积转换工具，在升、毫升、加仑、立方米等体积单位间快速转换，支持烹饪、工程和学术场景。",
        "func_zh": "体积转换工具是一个实用的在线换算器，帮助你在升(L)、毫升(mL)、立方米(m³)、加仑(gal)、品脱(pt)、夸脱(qt)和液体盎司(fl oz)等常用体积单位之间快速转换。无论你是在厨房做菜需要换算食谱中的容量单位，还是工程师计算水箱容积，抑或学生在做物理化学实验，这个工具都能节省大量手动计算时间。你只需输入数值并选择来源和目标单位，结果实时显示。",
        "duration": "2",
        "tool_url": "/life/volume-converter.html",
        "svg_file": "volume-converter-step1.svg",
        "step_keys": "vc",
        "tips": [
            "记住常用换算关系：1升 = 1000毫升 = 0.001立方米，1加仑 ≈ 3.785升（美制）≈ 4.546升（英制），这些基础换算在日常生活和工作中非常实用。",
            "该工具同时支持美制加仑和英制加仑，注意区分。美制加仑在美国和部分拉丁美洲国家使用，英制加仑则在英国和英联邦国家使用，两者相差约20%。",
            "如果你需要批量转换多个数值，可以记录每次转换结果或配合电子表格使用。同时建议将常用换算结果收藏备用，提高日常工作效率。"
        ],
        "faqs": [
            ("支持哪些体积单位？", "目前支持升(L)、毫升(mL)、立方米(m³)、美制加仑(gal)、英制加仑(gal UK)、品脱(pt)、夸脱(qt)和液体盎司(fl oz)等常用体积单位，涵盖公制和英制两大体系。"),
            ("美制加仑和英制加仑有什么区别？", "1美制加仑约等于3.785升，1英制加仑约等于4.546升。美制加仑主要用于美国，英制加仑用于英国及英联邦国家。工具中分别标注了gal和gal UK以便区分。"),
            ("精度如何？", "工具使用JavaScript高精度浮点运算，结果精确到小数点后6位。对于高精度需求的场景（如科学实验），建议参考原始换算比例进行校验。")
        ],
        "related": [
            ("/tutorials/area-converter.html", "面积转换"),
            ("/tutorials/length-converter.html", "长度转换"),
            ("/tutorials/weight-converter.html", "重量转换")
        ]
    },
    {
        "tool_id": "weight-converter",
        "title_zh": "重量转换教程：千克、磅、盎司互转",
        "desc_zh": "学会使用 ZenTools 在线重量转换工具，在千克、克、磅、盎司等重量单位间快速转换，支持物流、健身和烹饪场景。",
        "func_zh": "重量转换工具是一个高效的在线换算器，支持在千克(kg)、克(g)、毫克(mg)、吨(t)、磅(lb)、盎司(oz)、斤、两等常见重量单位之间快速切换换算。无论你是需要计算国际物流包裹重量，还是健身时转换磅和千克来跟踪训练数据，抑或是在厨房做菜时换算不同国家的食材重量单位，这个工具都能帮你秒速完成。输入数值后，所有已选目标单位的结果同时显示，一目了然。",
        "duration": "2",
        "tool_url": "/life/weight-converter.html",
        "svg_file": "weight-converter-step1.svg",
        "step_keys": "wtc",
        "tips": [
            "常用换算口诀：1千克 ≈ 2.2磅，1磅 ≈ 0.454千克，1盎司 ≈ 28.35克，1斤 = 500克。记住这几个关键换算比例可以快速心算大致结果。",
            "国际物流中常用的重量进制是千克和磅，建议发货前使用工具确认包裹重量换算是否准确，避免因重量误差导致运费超支或清关问题。",
            "健身追踪中，如果你使用的是以磅为单位的国外训练计划，可以快速用工具将所有磅值转换为千克，方便对照国内的杠铃片和哑铃重量。"
        ],
        "faqs": [
            ("支持哪些重量单位？", "目前支持千克(kg)、克(g)、毫克(mg)、吨(t)、磅(lb)、盎司(oz)、斤、两、钱等常用重量单位，覆盖公制、英制和市制三大体系。"),
            ("斤和千克怎么换算？", "1斤 = 500克 = 0.5千克。这是中国市制单位，在日常生活中广泛使用。在工具中选择斤作为源单位即可快速查看所有对应值。"),
            ("结果可以复制吗？", "可以。所有显示的结果都是纯文本格式，你可以直接选中复制。在结果区域通常会有复制按钮，点击即可一键复制当前换算结果。")
        ],
        "related": [
            ("/tutorials/length-converter.html", "长度转换"),
            ("/tutorials/volume-converter.html", "体积转换"),
            ("/tutorials/area-converter.html", "面积转换")
        ]
    },
    {
        "tool_id": "visa-days",
        "title_zh": "签证天数计算教程：停留天数计算",
        "desc_zh": "学会使用 ZenTools 在线签证天数计算工具，输入出入境日期自动计算停留天数，辅助签证申请和行程规划。",
        "func_zh": "签证天数计算工具帮助你精确计算出入境日期之间的停留天数，是申请签证和规划行程的必备工具。无论是申请申根签证需要确认在180天内的累计停留天数，还是填写签证申请表时需要填写精确的停留时长，抑或在规划跨国旅行时需要核对各国免签停留期限，这个工具都能帮你轻松计算出准确的天数。工具支持多次出入境记录计算，可自由选择是否包含入境当日和出境当日。",
        "duration": "2",
        "tool_url": "/life/visa-days.html",
        "svg_file": "visa-days-step1.svg",
        "step_keys": "vd",
        "tips": [
            '申请申根签证时需要注意"任意180天内累计不超过90天"的规定，建议使用工具的多次出入境记录功能，将近期所有行程的出入境日期输入，工具会自动计算累计停留天数。',
            "不同国家对停留天数的计算方式可能不同（有些含头不含尾，有些含头含尾），请根据签证申请表的具体要求选择是否包含出入境当日。工具提供了两种计数方式的灵活切换。",
            "规划多国旅行行程时，建议先用工具逐国计算停留天数，确保每个国家的停留时间都不超过免签期限，再确定最终的航班和住宿安排。"
        ],
        "faqs": [
            ("停留天数从哪天开始算？", '通常情况下，入境当天算作停留的第一天。例如1月1日入境、1月5日出境，停留天数为5天。但不同国家的计算规则可能不同，工具提供了"含入境日"和"不含入境日"的切换选项。'),
            ("可以计算多次出境的累计天数吗？", '可以。工具支持添加多组出入境记录，每一组分别计算天数后，底部会显示所有记录的累计总天数。这对需要满足"任意180天内累计不超过X天"要求的申根签证申请非常有用。'),
            ("计算结果准确吗？", "工具基于JavaScript日期函数进行精确计算，自动处理闰年、跨月和跨年等各种情况。但由于各国移民局的计算标准可能略有差异，建议以官方计算结果为准。")
        ],
        "related": [
            ("/tutorials/date-calculator.html", "日期计算器"),
            ("/tutorials/countdown.html", "倒计时"),
            ("/tutorials/holiday-checker.html", "节假日查询")
        ]
    },
    {
        "tool_id": "moneyuppercase",
        "title_zh": "金额大写转换教程：人民币金额大写",
        "desc_zh": "学会使用 ZenTools 在线金额大写转换工具，将数字金额转换为中文大写金额，用于支票、合同和发票等正式文书。",
        "func_zh": '金额大写转换工具帮助你将阿拉伯数字金额快速准确地转换为中文大写金额，适用于填写支票、合同、发票、财务凭证等正式文书中对金额大写的要求。工具严格按照中国人民银行《支付结算办法》规定的大写金额书写规范进行转换，正确处理元、角、分以及"零"的用法，支持人民币整数金额和小数金额的转换。无论是财务人员制作凭证，还是法务人员起草合同，这个工具都能帮你一键完成金额大写的正确填写，避免手写错误带来的法律风险。',
        "duration": "2",
        "tool_url": "/life/moneyuppercase.html",
        "svg_file": "moneyuppercase-step1.svg",
        "step_keys": "muc",
        "tips": [
            '大写金额中"零"的用法有严格规范：当金额中间有连续多个0时，只写一个"零"字。例如10004元写作"壹万零肆元整"，而不是"壹万零零肆元整"。工具会自动遵循此规则。',
            '整数金额后面必须加"整"字，有角分的金额后面不加"整"。例如100元写作"壹佰元整"，100.50元写作"壹佰元伍角"。工具会根据金额是否有小数部分自动决定是否加"整"字。',
            "在合同中填写金额时，建议同时标注大写金额和小写金额。如果两者不一致，根据《票据法》规定，以大写金额为准。因此大写金额的准确性至关重要。"
        ],
        "faqs": [
            ("大写金额有哪些规范要求？", "根据中国人民银行规定：大写金额数字应用正楷或行书填写，如壹、贰、叁、肆、伍、陆、柒、捌、玖、拾、佰、仟、万、亿、元、角、分、零、整。不得用一、二、三、四等简化字代替，不得自造简化字。"),
            ("支持的最大金额是多少？", "工具支持最大到千亿级别（12位整数）的金额转换，可以满足绝大多数商业和财务场景的需求。对于超出此范围的金额，请分笔处理。"),
            ("转换结果可以直接用于银行票据吗？", "可以。转换结果严格遵循中国人民银行《支付结算办法》规范，可以用于填写支票、银行汇票、本票等银行票据的大写金额栏。")
        ],
        "related": [
            ("/tutorials/currency.html", "货币汇率"),
            ("/tutorials/cny-jpy.html", "日元人民币换算"),
            ("/tutorials/percentage-calculator.html", "百分比计算器")
        ]
    },
    {
        "tool_id": "cny-jpy",
        "title_zh": "日元人民币换算教程：实时中日汇率",
        "desc_zh": "学会使用 ZenTools 在线日元人民币换算工具，查询日元与人民币的实时汇率和历史走势，支持多种金额的快速换算。",
        "func_zh": "日元人民币换算工具为你提供实时的日元(JPY)与人民币(CNY)汇率查询和换算服务。无论是准备赴日旅行需要预估开销、在日本购物时快速换算价格、还是进行跨境电商贸易需要核算成本，这个工具都能让你快速获取最新的汇率信息。工具展示实时汇率和历史走势图，支持7天、30天、90天和1年的汇率变化趋势，帮助你掌握汇率波动规律，选择最优的兑换时机。",
        "duration": "2",
        "tool_url": "/life/cny-jpy.html",
        "svg_file": "cny-jpy-step1.svg",
        "step_keys": "cj",
        "tips": [
            "赴日旅行时，建议在汇率好的时候提前兑换一部分日元现金。可以利用工具的历史走势图观察汇率波动规律，在人民币相对强势时多兑换一些，可以节省不少旅游开销。",
            "在日本购物时，可以打开这个工具快速将日元标价换算为人民币，直观了解实际支付金额。同时建议注意信用卡的跨境手续费，有时直接刷银联卡的汇率比现金兑换更划算。",
            "跨境电商卖家可以关注汇率长期走势，在日元低位时从日本进货可以降低成本。建议将工具的走势图设置为90天或1年视图，从宏观角度把握汇率趋势。"
        ],
        "faqs": [
            ("汇率数据多久更新一次？", "汇率数据从公开金融市场数据源获取，通常每5-10分钟更新一次。实际更新频率取决于数据源的推送频率和网络状况。对于高精度实时交易需求，建议使用银行或专业外汇平台的报价。"),
            ("换算结果与银行实际兑换汇率有差异吗？", "会有一定差异。工具使用的是中间市场汇率，而银行和兑换点会在中间汇率基础上加收一定的手续费或买卖差价（汇差通常在0.5%-3%之间）。实际兑换时请以银行当日报价为准。"),
            ("支持其他货币吗？", "本工具专注于日元与人民币的双向换算。如果你需要查询其他货币汇率，可以使用本站的通用货币汇率转换工具，支持美元、欧元、英镑等全球主流货币。")
        ],
        "related": [
            ("/tutorials/currency.html", "货币汇率"),
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-tax.html", "日本个税计算")
        ]
    },
    {
        "tool_id": "japan-electricity",
        "title_zh": "日本电费计算教程：估算月度电费支出",
        "desc_zh": "学会使用 ZenTools 在线日本电费计算工具，根据日本电力公司费率计算月度电费，支持东京、关西、中部等各地域。",
        "func_zh": "日本电费计算工具帮助你根据日本各地区电力公司的实际费率体系，精确估算月度电费支出。工具覆盖东京电力、关西电力、中部电力、九州电力、东北电力和北海道电力等日本主要的电力公司，内置各公司的基本料金、电力量料金和燃料费调整额等三级费率结构。无论你是在日本租房生活需要预估生活成本，还是计划移居日本想提前了解水电开销，这个工具都能为你提供准确的月度电费估算，帮助你做好预算规划。",
        "duration": "3",
        "tool_url": "/life/japan-electricity.html",
        "svg_file": "japan-electricity-step1.svg",
        "step_keys": "je",
        "tips": [
            "日本电费由三部分组成：基本料金（按契约电流固定收取）、电力量料金（按实际用电量阶梯计费）和燃料费调整额（根据燃料市场价格浮动）。了解这三个组成部分有助于你选择合适的契约方案。",
            "不同电力公司的费率标准差异较大，例如东京电力和冲绳电力的单价可能相差30%以上。如果你有搬迁计划，可以先用工具比较不同地区的电费成本。",
            "日本推行电力自由化后，你可以选择不同的电力公司和套餐方案。建议在签约前使用工具模拟不同契约方案的电费，选择最适合自己用电习惯的方案。"
        ],
        "faqs": [
            ("电费计算包含哪些费用？", "日本电费包含基本料金（按契约安培数固定收取）、电力量料金（按用电量分三阶段递增费率）和燃料费调整额（每月根据燃料价格变动）。工具已内置各地域电力公司的最新费率数据。"),
            ("为什么夏季和冬季电费更高？", "夏季空调制冷和冬季暖房用电量大增，电力量料金按阶梯递增，用电量越高单价越高。同时燃料费调整额也会随季节变化波动，导致夏季和冬季电费明显高于春秋季。"),
            ("如何选择最省钱的电力方案？", "建议先用工具输入你家的月均用电量，然后切换不同电力公司进行对比。一般来说，用电量少的家庭适合安培数低的契约（如30A），用电量大的家庭选择安培数高的契约（如60A）会比较划算。")
        ],
        "related": [
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-tax.html", "日本个税计算"),
            ("/tutorials/japan-mortgage.html", "日本房贷计算")
        ]
    },
    {
        "tool_id": "japan-mortgage",
        "title_zh": "日本房贷计算教程：住房贷款月供计算",
        "desc_zh": "学会使用 ZenTools 在线日本房贷计算工具，计算日本住房贷款利率、月供和还款计划，支持固定利率和浮动利率。",
        "func_zh": "日本房贷计算工具帮助你全面模拟日本住房贷款的还款方案，支持固定利率和浮动利率两种主流贷款方式。工具内置Flat35长期固定利率住宅贷款和变动金利型贷款的利率体系，可以根据贷款金额、年利率和还款年限计算出每月还款额（元利均等返済方式），同时生成总还款额和累计支付利息的详细明细。无论你是准备在日购房需要评估还款能力，还是比较不同银行贷款方案的月供差异，这个工具都能提供清晰可靠的还款计划参考。",
        "duration": "3",
        "tool_url": "/life/japan-mortgage.html",
        "svg_file": "japan-mortgage-step1.svg",
        "step_keys": "jmort",
        "tips": [
            "日本房贷主要有两种利率类型：Flat35长期固定利率（35年固定）和変動金利（浮动利率，每半年调整一次）。固定利率适合追求还款稳定的家庭，浮动利率初期较低但存在上升风险。",
            "日本贷款审查中，银行主要考察年收入对还款额的比例（返済負担率），通常要求不超过年收入的25%-35%。建议先用工具计算月供，再对照自己的年收确认是否符合贷款条件。",
            "除了月供外，购房还需要准备约房价6%-8%的诸费用（包括登录免许税、不动产取得税、中介费等）。建议在总预算中预留这部分费用，不要全部用于首付。"
        ],
        "faqs": [
            ("Flat35和变动金利哪个更划算？", "Flat35提供35年固定利率（目前约1.5%-2.0%），月供稳定可预测；变动金利初期利率较低（约0.3%-0.5%），但可能随市场利率上升而增加。对于长期自住，Flat35更安心；对于短期持有（5-10年），变动金利可能更省钱。"),
            ("元利均等返済和元金均等返済有什么区别？", "元利均等返済每月还款额固定（本金+利息总额不变），适合收入稳定的工薪族；元金均等返済每月还款额递减（每月还本金固定、利息递减），初期还款压力大但总利息少。本工具采用最为普遍的元利均等返済方式计算。"),
            ("ボーナス併用返済是什么意思？", "ボーナス併用返済是指在奖金月份（通常为6月和12月）增加还款金额的方案，可以加速还款进度。工具支持设置奖金月增加还款金额，帮助你规划更灵活的还款策略。")
        ],
        "related": [
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-tax.html", "日本个税计算"),
            ("/tutorials/japan-pension.html", "日本年金计算")
        ]
    },
    {
        "tool_id": "japan-overtime",
        "title_zh": "日本加班费计算教程：加班工资计算",
        "desc_zh": "学会使用 ZenTools 在线日本加班费计算工具，根据日本劳动基准法计算加班费、深夜津贴和假日工资。",
        "func_zh": "日本加班费计算工具严格依据日本劳动基准法，帮助你精确计算各类加班工资。工具支持法定内残業（加班费率1.25倍）、法定外残業（1.25倍）、深夜割増（22:00-5:00，加算0.25倍至1.50倍）和休日手当（1.35倍）等多种加班类型的独立计算。你只需输入月基本给与额和各类加班时间，工具会自动计算时给单价和各类割増工资的详细明细，帮助你和雇主核对加班费的准确性，维护劳动者的合法权益。",
        "duration": "3",
        "tool_url": "/life/japan-overtime.html",
        "svg_file": "japan-overtime-step1.svg",
        "step_keys": "jo",
        "tips": [
            "日本劳动基准法规定，法定劳动时间为每日8小时、每周40小时。超过法定时间的加班按1.25倍计算（中小企业的法定外残業暫定措置可能不同）。超过每月60小时的加班，超出部分按1.50倍计算。",
            "深夜劳动（22:00至次日5:00）在基础加班费率上再加0.25倍。如果深夜时段同时是法定外加班，则费率为1.50倍（1.25 + 0.25）。休日劳动（法定休息日）的费率为1.35倍。",
            "时给单价的计算方式是：月基本给 ÷ 月平均所定劳动时间。月平均所定劳动时间通常为173.8小时（365天÷7天×40小时÷12个月）。使用正确的时给单价是计算加班费的基础。"
        ],
        "faqs": [
            ("36協定是什么？", "36協定（劳使協定）是雇主和员工代表之间签订的关于加班和休日劳动的协议。签订36協定后，法定加班时间上限为每月45小时、每年360小时（特别情况下720小时）。无36協定则不得安排法定外加班。"),
            ("管理職有加班费吗？", '管理監督者（具有经营决策权和劳动时间自主权的管理职位）通常不适用劳动基准法的劳动时间规定，因此没有加班费。但"名ばかり管理職"（名义上的管理者）如果实际上没有管理权限，仍有权获得加班费。'),
            ("加班费什么时候支付？", "加班费通常与当月工资一起在次月支付（例如1月加班费在2月25日发放）。根据劳动基准法第24条，工资必须每月一次以上、在固定日期以货币直接支付给劳动者。")
        ],
        "related": [
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-tax.html", "日本个税计算"),
            ("/tutorials/japan-pension.html", "日本年金计算")
        ]
    },
    {
        "tool_id": "japan-pension",
        "title_zh": "日本年金计算教程：国民年金和厚生年金",
        "desc_zh": "学会使用 ZenTools 在线日本年金计算工具，计算日本国民年金和厚生年金的缴纳金额和未来领取额。",
        "func_zh": "日本年金计算工具帮助你了解日本公的年金制度的两大支柱：国民年金（基礎年金）和厚生年金。工具可以根据你的月收和加入期间，精确计算每月的保险料缴纳金额（包括个人负担和会社负担部分），并基于现行制度估算未来的年金受给额。无论你是在日工作的会社员需要了解厚生年金的扣款明细，还是自营业者需要计算国民年金的缴纳计划，这个工具都能为你提供清晰的年金试算结果。",
        "duration": "3",
        "tool_url": "/life/japan-pension.html",
        "svg_file": "japan-pension-step1.svg",
        "step_keys": "jp",
        "tips": [
            "国民年金是日本的基础年金，所有20-60岁的在日居民都必须加入。2024年度国民年金保险料为每月16,980日元。缴纳满40年（480个月）可领取满额老齢基礎年金，2024年度满额为816,000日元/年。",
            "厚生年金的保险料率为18.3%（2024年度），由会社和个人各负担一半（9.15%）。保险料直接从工资中扣除，会社負担部分不计入个人课税所得，这部分是会社提供的福利。",
            "在日外国人如果回国，可以申请脱退一时金（一次性提取）。缴纳满6个月以上即可申请，但最多只能提取最近5年的部分。如果缴纳满10年，则可以在达到领取年龄后领取年金（即使已回国）。"
        ],
        "faqs": [
            ("国民年金和厚生年金有什么区别？", "国民年金是面向所有居民的基础年金，缴纳固定金额，领取额也相对固定；厚生年金是面向会社员和公务员的附加年金，按收入比例缴纳，退休后领取的金额也更高。会社员同时加入两种年金，自营业者只加入国民年金。"),
            ("如果中途回国可以退还年金吗？", "可以申请脱退一时金（一次性退还）。条件是：非日本国籍、已缴纳6个月以上、已回国且在日本无住所。退还金额根据缴纳月数计算，但最多只退还最近5年缴纳的部分，且需要扣除约20%的所得税。"),
            ("厚生年金的领取年龄是多少？", "老齢厚生年金的支給開始年龄原则上是65岁。可以选择60-64岁提前领取（减额），或66-75岁延迟领取（增额）。每提前一个月减0.4%，每延迟一个月增0.7%，延迟到75岁可增额84%。")
        ],
        "related": [
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-tax.html", "日本个税计算"),
            ("/tutorials/japan-mortgage.html", "日本房贷计算")
        ]
    },
    {
        "tool_id": "japan-salary",
        "title_zh": "日本工资计算教程：税后到手工资计算",
        "desc_zh": "学会使用 ZenTools 在线日本工资计算工具，计算日本工资的税前税后、社保和年金扣除后的实际到手金额。",
        "func_zh": "日本工资计算工具帮助你全面了解日本会社员的工资结构和到手金额（手取り）。工具依据日本现行的社会保険制度和税制，精确计算月额支给额在扣除健康保险、厚生年金、雇用保险、所得税和住民税之后的实际到手金额。支持选择不同都道府县（住民税率略有差异）、不同扶養人数和不同年龄段的保险费率，让你对每月的工资扣除有清晰的认知。无论你是在考虑日本就职的求职者，还是已经在日工作的会社员，这个工具都是计算实际收入的必备利器。",
        "duration": "3",
        "tool_url": "/life/japan-salary.html",
        "svg_file": "japan-salary-step1.svg",
        "step_keys": "js",
        "tips": [
            "日本工资扣除主要包括：健康保险料（约5%）、厚生年金保险料（9.15%）、雇用保险料（约0.6%）、所得税（累进税率5%-45%）和住民税（约10%，前一年收入基准）。总共约占月收的20%-25%。",
            "住民税的计算基于前一年的收入，因此来日第一年通常没有住民税扣除（或金额很低），第二年才开始按前一年收入计算。这一点在规划首年生活预算时需要注意。",
            "年末调整（年末調整）是会社在12月对全年所得税进行精算的制度。如果你有住宅贷款控除、医疗费控除等，可以在年末调整中申请退还多缴的所得税。也可以在次年2-3月自行进行确定申告。"
        ],
        "faqs": [
            ("手取り是什么意思？", "手取り（到手金额）是指扣除所有社会保険料和税金后实际打入银行账户的金额。例如月收35万日元，手取り约27.4万日元，扣除率约21.6%。这是你实际可以自由支配的收入。"),
            ("扶養家族对工资有什么影响？", "扶養家族人数会影响所得税和住民税的控除额。配偶者和子女均可作为扶養对象，每增加一名扶養家族，所得税和住民税都会减少。如果配偶年收入低于103万日元，还可享受配偶者控除。"),
            ("ボーナス（奖金）需要缴税吗？", '需要。奖金同样需要缴纳健康保险、厚生年金、雇用保险和所得税。但保险费率与月工资相同，所得税则按"赏与に対する源泉徴収税額表"另行计算。奖金的住民税按年度总收入统一计算。')
        ],
        "related": [
            ("/tutorials/japan-tax.html", "日本个税计算"),
            ("/tutorials/japan-pension.html", "日本年金计算"),
            ("/tutorials/japan-overtime.html", "日本加班费计算")
        ]
    },
    {
        "tool_id": "japan-tax",
        "title_zh": "日本个税计算教程：个人所得税计算",
        "desc_zh": "学会使用 ZenTools 在线日本个税计算工具，计算日本个人所得税、住民税和复兴特别税，含各类收入扣除项。",
        "func_zh": "日本个税计算工具帮助你全面计算在日本工作的个人所得税负担。工具基于日本国税厅公布的所得税率表（累进课税5%-45%），综合计算所得税、住民税（都道府县民税+市町村民税）和复兴特别所得税（所得税额×2.1%）。工具内置给与所得控除、基础控除、社会保险料控除和扶養控除等主要扣除项目，可以根据你的年收入、家庭结构和社保缴纳情况，精确估算年度纳税总额和实际税率，帮助你进行税务规划和节税决策。",
        "duration": "3",
        "tool_url": "/life/japan-tax.html",
        "svg_file": "japan-tax-step1.svg",
        "step_keys": "jt",
        "tips": [
            "日本所得税采用7级累进税率：5%（195万以下）、10%（195-330万）、20%（330-695万）、23%（695-900万）、33%（900-1800万）、40%（1800-4000万）、45%（4000万以上）。这是适用税率，实际负担率（纳税额÷总收入）远低于此。",
            "给与所得控除是工资收入者最大的扣除项。最低55万日元，随着收入增加而递增。例如年收500万日元，给与所得控除约为154万日元，课税所得降为346万日元，大幅降低了纳税基数。",
            "ふるさと納税（故乡纳税）是日本特色的节税制度。向地方自治体捐款后，捐款额减去2000日元的部分可从住民税和所得税中扣除。实质上用2000日元的负担换取各地特产礼品，是非常划算的节税方式。"
        ],
        "faqs": [
            ("所得税和住民税有什么区别？", "所得税是向国家缴纳的国税，基于当年收入采用累进税率（5%-45%）；住民税是向都道府县和市町村缴纳的地方税，基于前一年收入，税率固定约10%（所得割+均等割）。两者合计为个人的总税负。"),
            ("复兴特别所得税是什么？", "复兴特别所得税是东日本大震灾后设立的临时附加税，税额为基准所得税额的2.1%。例如基准所得税为10万日元，复兴特别税为2,100日元，合计缴纳102,100日元。该税种计划持续到2037年。"),
            ("有哪些常见的节税方法？", "常见的节税方法包括：iDeCo（个人型确定拠出年金，最高月额68,000日元全额控除）、生命保险料控除（最高12万日元）、医疗费控除（超过10万日元部分）、住宅贷款控除（年末贷款余额的0.7%）、ふるさと納税等。合理利用这些制度可显著降低税负。")
        ],
        "related": [
            ("/tutorials/japan-salary.html", "日本工资计算"),
            ("/tutorials/japan-pension.html", "日本年金计算"),
            ("/tutorials/japan-overtime.html", "日本加班费计算")
        ]
    }
]

# Generate HTML files
for t in tutorials:
    html = build_html(**t)
    filepath = os.path.join(BASE, f"{t['tool_id']}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Created: {filepath} ({len(html)} chars)")

print(f"\nDone! Created {len(tutorials)} tutorial files.")
