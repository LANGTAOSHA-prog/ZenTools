#!/usr/bin/env python3
"""生成新工具页面的 HTML 骨架，并可选择添加到 tools-data.json。"""

import argparse
import json
import os
import sys
from datetime import date
from _changelog_utils import build_tool_entry, append_changelog, load_site_info, save_site_info

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(SCRIPT_DIR, 'data', 'tools-data.json')
JS_PATH = os.path.join(SCRIPT_DIR, 'assets', 'js', 'tools-data.js')

CATEGORY_MAP = {
    'AI工具':     ('ai',      'AI Tools',     'AIツール',           'Công cụ AI',        '🤖'),
    '图片工具':   ('image',   'Image Tools',  '画像ツール',         'Công cụ hình ảnh',  '🖼️'),
    'PDF工具':    ('pdf',     'PDF Tools',    'PDFツール',          'Công cụ PDF',       '📄'),
    '文本工具':   ('text',    'Text Tools',   'テキストツール',      'Công cụ văn bản',   '📝'),
    '视频工具':   ('video',   'Video Tools',  '動画ツール',         'Công cụ video',     '🎬'),
    '音频工具':   ('audio',   'Audio Tools',  '音声ツール',         'Công cụ âm thanh',  '🎵'),
    '开发工具':   ('dev',     'Dev Tools',    '開発ツール',         'Công cụ phát triển','💻'),
    'SEO工具':    ('seo',     'SEO Tools',    'SEOツール',          'Công cụ SEO',       '🔍'),
    '办公工具':   ('office',  'Office Tools', 'オフィスツール',      'Công cụ văn phòng', '📎'),
    '生活工具':   ('life',    'Life Tools',   '生活ツール',         'Công cụ đời sống',  '🌍'),
    '金融工具':   ('finance', 'Finance Tools','金融ツール',         'Công cụ tài chính', '💰'),
    '教育工具':   ('education','Education Tools','教育ツール',       'Công cụ giáo dục',  '📚'),
    '设计工具':   ('design',  'Design Tools', 'デザインツール',      'Công cụ thiết kế',  '🎨'),
}

AI_FIELDS_TPL = {
    'free': True,
    'registration': False,
    'chinese': True,
    'languages': ['zh', 'en', 'ja', 'vi'],
    'privacy': '所有处理在浏览器本地完成，文件不会上传到服务器',
    'privacy__en': 'All processing is done locally in your browser. Files are never uploaded.',
    'privacy__ja': 'すべての処理はブラウザでローカルに完了します。ファイルはサーバーにアップロードされません。',
    'privacy__vi': 'Tất cả xử lý được thực hiện cục bộ trong trình duyệt. Tệp không bao giờ được tải lên.',
    'processing': 'browser-local',
    'audience': '普通用户、内容创作者、办公人员',
    'audience__en': 'General users, content creators, office workers',
    'audience__ja': '一般ユーザー、コンテンツクリエイター、オフィスワーカー',
    'audience__vi': 'Người dùng phổ thông, người sáng tạo nội dung, nhân viên văn phòng',
    'useCases': '日常办公、内容处理、效率工具',
    'useCases__en': 'Daily office work, content processing, productivity',
    'useCases__ja': '日常業務、コンテンツ処理、生産性向上',
    'useCases__vi': 'Công việc văn phòng hàng ngày, xử lý nội dung, năng suất',
    'limits': '无严格限制，文件大小取决于浏览器内存',
    'limits__en': 'No strict limits. File size depends on browser memory.',
    'limits__ja': '厳格な制限はありません。ファイルサイズはブラウザメモリに依存します。',
    'limits__vi': 'Không có giới hạn nghiêm ngặt. Kích thước tệp phụ thuộc vào bộ nhớ trình duyệt.'
}


def build_tool_html(slug, category, name_zh, name_en, name_ja, name_vi,
                    desc_zh, desc_en, desc_ja, desc_vi, icon,
                    tool_title_zh='', tool_title_en='', tool_title_ja='', tool_title_vi=''):
    cat_slug = CATEGORY_MAP[category][0]
    cat_en = CATEGORY_MAP[category][1]
    cat_ja = CATEGORY_MAP[category][2]
    cat_vi = CATEGORY_MAP[category][3]
    url = f'/{cat_slug}/{slug}.html'
    if not tool_title_zh:
        tool_title = name_zh
    else:
        tool_title = tool_title_zh
    if not tool_title_en:
        tool_title_en = name_en
    if not tool_title_ja:
        tool_title_ja = name_ja
    if not tool_title_vi:
        tool_title_vi = name_vi

    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1.0"/>
<title>{name_zh} - {name_en} | ZenTools</title>
<meta name="description" content="{desc_zh}"/>
<link rel="manifest" href="/manifest.json"/>
<meta name="theme-color" content="#00e5ff"/>
<link rel="canonical" href="https://zentools.xyz{url}"/>
<meta property="og:title" content="{name_zh} - ZenTools"/>
<meta property="og:description" content="{desc_zh}"/>
<meta property="og:url" content="https://zentools.xyz{url}"/>
<meta property="og:type" content="website"/>
<meta name="twitter:card" content="summary"/>
<meta name="twitter:title" content="{name_zh} - ZenTools"/>
<meta name="twitter:description" content="{desc_zh}"/>
<link rel="stylesheet" href="../assets/css/tool-ui.min.css"/>
<style>
/* TODO: 页面特有样式 */
</style>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{{
    "@type": "Question",
    "name": "如何使用 {name_zh}?",
    "acceptedAnswer": {{
      "@type": "Answer",
      "text": "打开工具 → 上传或输入内容 → 选择参数 → 下载结果。所有处理在浏览器本地完成。"
    }}
  }}]
}}
</script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{name_zh}",
  "url": "https://zentools.xyz{url}",
  "description": "{desc_zh}",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "All",
  "offers": {{ "@type": "Offer", "price": "0", "priceCurrency": "CNY" }}
}}
</script>
</head>
<body>
<div class="blob blob-1"></div>
<div class="blob blob-2"></div>
<div class="z-wrap">

<nav>
<div class="nav-inner">
<a class="logo" href="/">ZenTools<span>2.0</span></a>
<div class="nav-links">
<a href="/" data-i18n="nav_home">首页</a>
<a href="/{cat_slug}/" data-i18n="nav_category">{category}</a>
<a href="/tools.html" data-i18n="nav_all_tools">全部工具</a>
<select id="langSelect" class="lang-select">
<option value="zh">中文</option>
<option value="en">English</option>
<option value="ja">日本語</option>
<option value="vi">Tiếng Việt</option>
</select>
</div>
</div>
</nav>

<div class="page-header reveal">
<div class="breadcrumb">
<a href="/" data-i18n="breadcrumb_home">首页</a><span> › </span>
<a href="/{cat_slug}/">{category}</a><span> › </span>
<span data-i18n="page_title">{name_zh}</span>
</div>
<span class="page-eyebrow" data-i18n="category_label">{category}</span>
<h1>
<span class="grad" data-i18n="heading_grad">{name_zh}</span><br/>
<span data-i18n="heading_sub">{desc_zh[:40]}</span>
</h1>
<p data-i18n="page_desc">{desc_zh}</p>
</div>

<div class="tool-box reveal">
<h2 data-i18n="tool_title">{tool_title}</h2>
<p class="note" data-i18n="tool_desc">上传文件或输入内容开始处理，所有操作在本地完成，文件不上传服务器。</p>

<div class="file-input-row">
<input type="file" id="fileInput" accept="*/*"/>
<button class="btn-primary" id="btnAction" data-i18n="btn_action">开始处理</button>
</div>
<div class="zt-perf-warn"></div>
<div id="status"></div>
<div id="result"></div>
<!-- TODO: 自定义工具 UI -->
</div>

<div class="section">
<div class="section-head">
<h2 data-i18n="info_heading">使用说明</h2>
</div>
<div class="info-grid">
<div class="info-card">
<h4 data-i18n="info_title_1">隐私安全</h4>
<p data-i18n="info_desc_1">所有处理在浏览器本地完成，文件不上传服务器。</p>
</div>
<div class="info-card">
<h4 data-i18n="info_title_2">完全免费</h4>
<p data-i18n="info_desc_2">无使用次数限制，无水印，无需注册。</p>
</div>
<div class="info-card">
<h4 data-i18n="info_title_3">多语言支持</h4>
<p data-i18n="info_desc_3">支持中文、英语、日语、越南语。</p>
</div>
</div>
</div>

<footer>
<div class="footer-inner">
<div class="footer-links">
<a href="/privacy.html" data-i18n="footer_privacy">隐私政策</a>
<a href="/terms.html" data-i18n="footer_terms">服务条款</a>
<a href="/contact">联系我们</a>
</div>
<p class="footer-copy">&copy; 2026 ZenTools</p>
</div>
</footer>

</div>

<script>
window.ZT_PAGE = {{
  zh: {{
    "page_title": "{name_zh}",
    "category_label": "{category}",
    "heading_grad": "{name_zh}",
    "heading_sub": "{desc_zh[:40]}",
    "page_desc": "{desc_zh}",
    "tool_title": "{tool_title}",
    "tool_desc": "上传文件或输入内容开始处理，所有操作在本地完成，文件不上传服务器。",
    "btn_action": "开始处理",
    "perf_warn": "文件较大，处理可能需要一些时间",
    "info_heading": "使用说明",
    "info_title_1": "隐私安全",
    "info_desc_1": "所有处理在浏览器本地完成，文件不上传服务器。",
    "info_title_2": "完全免费",
    "info_desc_2": "无使用次数限制，无水印，无需注册。",
    "info_title_3": "多语言支持",
    "info_desc_3": "支持中文、英语、日语、越南语。"
  }},
  en: {{
    "page_title": "{name_en}",
    "category_label": "{cat_en}",
    "heading_grad": "{name_en}",
    "heading_sub": "{desc_en[:50]}",
    "page_desc": "{desc_en}",
    "tool_title": "{tool_title_en}",
    "tool_desc": "Upload files or enter content to start processing. All operations are local — files never leave your device.",
    "btn_action": "Start",
    "perf_warn": "Large files may take some time",
    "info_heading": "Instructions",
    "info_title_1": "Privacy Safe",
    "info_desc_1": "All processing done locally in your browser. Files are never uploaded.",
    "info_title_2": "100% Free",
    "info_desc_2": "Unlimited usage, no watermark, no registration required.",
    "info_title_3": "Multi-language",
    "info_desc_3": "Supports Chinese, English, Japanese and Vietnamese."
  }},
  ja: {{
    "page_title": "{name_ja}",
    "category_label": "{cat_ja}",
    "heading_grad": "{name_ja}",
    "heading_sub": "{desc_ja[:40]}",
    "page_desc": "{desc_ja}",
    "tool_title": "{tool_title_ja}",
    "tool_desc": "ファイルをアップロードまたは内容を入力して処理を開始。すべての操作はブラウザ内で行われます。",
    "btn_action": "処理開始",
    "perf_warn": "大きなファイルは時間がかかる場合があります",
    "info_heading": "使用方法",
    "info_title_1": "プライバシー安全",
    "info_desc_1": "すべての処理はブラウザでローカルに完了します。ファイルはサーバーにアップロードされません。",
    "info_title_2": "完全無料",
    "info_desc_2": "使用回数無制限、透かしなし、登録不要。",
    "info_title_3": "多言語対応",
    "info_desc_3": "中国語/英語/日本語/ベトナム語に対応。"
  }},
  vi: {{
    "page_title": "{name_vi}",
    "category_label": "{cat_vi}",
    "heading_grad": "{name_vi}",
    "heading_sub": "{desc_vi[:40]}",
    "page_desc": "{desc_vi}",
    "tool_title": "{tool_title_vi}",
    "tool_desc": "Tải tệp lên hoặc nhập nội dung để bắt đầu xử lý. Tất cả thao tác được thực hiện cục bộ.",
    "btn_action": "Bắt đầu",
    "perf_warn": "Tệp lớn có thể mất thời gian xử lý",
    "info_heading": "Hướng dẫn",
    "info_title_1": "An toàn bảo mật",
    "info_desc_1": "Tất cả xử lý được thực hiện cục bộ. Tệp không bao giờ được tải lên.",
    "info_title_2": "Miễn phí 100%",
    "info_desc_2": "Không giới hạn, không watermark, không cần đăng ký.",
    "info_title_3": "Đa ngôn ngữ",
    "info_desc_3": "Hỗ trợ tiếng Trung, Anh, Nhật, Việt."
  }}
}};
</script>
<script src="../assets/js/common-i18n.min.js"></script>
<script src="../assets/js/tool-ui.min.js"></script>
<script>
// TODO: 工具业务逻辑
document.getElementById('btnAction').addEventListener('click', async () => {{
  const file = document.getElementById('fileInput').files[0];
  if (!file) return;
  ZT.showProgress('处理中...', true);
  try {{
    // TODO: 实现工具核心算法
  }} catch (e) {{
    document.getElementById('status').textContent = 'Error: ' + e.message;
  }} finally {{
    ZT.hideProgress();
  }}
}});

if ('serviceWorker' in navigator) {{
  navigator.serviceWorker.register('/sw.js');
}}
</script>
</body>
</html>
'''


def build_tools_json_entry(name_zh, name_en, name_ja, name_vi, slug, category,
                            desc_zh, desc_en, desc_ja, desc_vi, icon, keywords):
    cat_slug = CATEGORY_MAP[category][0]
    url = f'/{cat_slug}/{slug}.html'
    entry = {
        'name': name_zh,
        'name__en': name_en,
        'name__ja': name_ja,
        'name__vi': name_vi,
        'slug': slug,
        'category': category,
        'url': url,
        'description': desc_zh,
        'description__en': desc_en,
        'description__ja': desc_ja,
        'description__vi': desc_vi,
        'icon': icon,
        'featured': False,
        'new': True,
        'keywords': keywords,
        'ai': dict(AI_FIELDS_TPL)
    }
    return entry


def generate_sitemap(base='https://zentools.xyz', out='sitemap.xml'):
    import xml.etree.ElementTree as ET
    root_elem = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    for r, d, f in os.walk(SCRIPT_DIR):
        d[:] = [x for x in d if x[0] != '.' and x not in ('node_modules', 'pdf_tools')]
        for fn in f:
            if fn.endswith('.html'):
                u = ET.SubElement(root_elem, 'url')
                ET.SubElement(u, 'loc').text = base + '/' + os.path.relpath(os.path.join(r, fn), SCRIPT_DIR)
    out_path = os.path.join(SCRIPT_DIR, out)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(ET.tostring(root_elem, encoding='unicode'))
    print(f'✓ sitemap.xml 已更新: {out_path}')


def update_tools_data_json(entry):
    if not os.path.exists(DATA_PATH):
        print(f'✗ 找不到 {DATA_PATH}，跳过 JSON 更新')
        return False
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if any(t.get('slug') == entry['slug'] for t in data['tools']):
        print(f'⚠ slug "{entry["slug"]}" 已存在于 tools-data.json，跳过')
        return False
    data['tools'].append(entry)
    data['lastUpdated'] = date.today().isoformat()
    with open(DATA_PATH, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'✓ tools-data.json 已更新 (共 {len(data["tools"])} 个工具)')
    return True


def sync_tools_data_js():
    if not os.path.exists(DATA_PATH) or not os.path.exists(JS_PATH):
        return
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    js_content = 'const toolsData = ' + json.dumps(data['tools'], ensure_ascii=False, indent=2) + ';\n'
    with open(JS_PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(js_content)
    print(f'✓ tools-data.js 已同步 ({len(data["tools"])} 条)')


def main():
    parser = argparse.ArgumentParser(description='生成 ZenTools 工具页面')
    parser.add_argument('--slug', required=True, help='URL 友好标识, 如 pdf-ocr')
    parser.add_argument('--category', required=True, choices=list(CATEGORY_MAP.keys()),
                        help='工具分类')
    parser.add_argument('--name-zh', required=True, help='中文名称')
    parser.add_argument('--name-en', required=True, help='英文名称')
    parser.add_argument('--name-ja', required=True, help='日文名称')
    parser.add_argument('--name-vi', required=True, help='越南文名称')
    parser.add_argument('--desc-zh', required=True, help='中文描述 (19-52字)')
    parser.add_argument('--desc-en', required=True, help='英文描述')
    parser.add_argument('--desc-ja', required=True, help='日文描述')
    parser.add_argument('--desc-vi', required=True, help='越南文描述')
    parser.add_argument('--icon', default='🔧', help='Emoji 图标 (默认 🔧)')
    parser.add_argument('--keywords', default='', help='SEO 关键词 (空格分隔)')
    parser.add_argument('--tool-title-zh', default='', help='工具标题 (中文，可选)')
    parser.add_argument('--tool-title-en', default='', help='工具标题 (英文，可选)')
    parser.add_argument('--tool-title-ja', default='', help='工具标题 (日文，可选)')
    parser.add_argument('--tool-title-vi', default='', help='工具标题 (越南文，可选)')
    parser.add_argument('--no-json', action='store_true', help='不添加到 tools-data.json')
    parser.add_argument('--no-sitemap', action='store_true', help='不更新 sitemap.xml')
    parser.add_argument('--overwrite', action='store_true', help='覆盖已存在的文件')

    args = parser.parse_args()

    cat_slug = CATEGORY_MAP[args.category][0]
    out_dir = os.path.join(SCRIPT_DIR, cat_slug)
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f'{args.slug}.html')

    if os.path.exists(out_path) and not args.overwrite:
        print(f'✗ 文件已存在: {out_path}')
        print('  使用 --overwrite 强制覆盖')
        sys.exit(1)

    html = build_tool_html(
        args.slug, args.category,
        args.name_zh, args.name_en, args.name_ja, args.name_vi,
        args.desc_zh, args.desc_en, args.desc_ja, args.desc_vi,
        args.icon,
        args.tool_title_zh, args.tool_title_en, args.tool_title_ja, args.tool_title_vi
    )

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html)
    print(f'✓ 工具页面已生成: {out_path}')

    if not args.no_json:
        entry = build_tools_json_entry(
            args.name_zh, args.name_en, args.name_ja, args.name_vi,
            args.slug, args.category,
            args.desc_zh, args.desc_en, args.desc_ja, args.desc_vi,
            args.icon, args.keywords
        )
        if update_tools_data_json(entry):
            sync_tools_data_js()
            try:
                data = load_site_info()
                changelog_entries = [
                    build_tool_entry(args.name_zh, args.name_en, args.name_ja, args.name_vi)
                ]
                data = append_changelog(data, changelog_entries)
                save_site_info(data)
                print(f'✓ site-info.json changelog 已更新')
            except Exception as e:
                print(f'⚠ changelog 更新失败 (非致命): {e}')

    if not args.no_sitemap:
        generate_sitemap()

    print(f'\n📝 下一步：编辑 {out_path} 填写工具业务逻辑')
    print(f'   然后运行: python _check_json.py && python _check_paths.py')


if __name__ == '__main__':
    main()
