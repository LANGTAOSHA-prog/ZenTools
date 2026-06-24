#!/usr/bin/env python3
"""Auto-add i18n infrastructure to AI tool pages without existing i18n."""
import os, re, html as html_mod

AI_DIR = '/workspace/ai'

def has_i18n(content):
    return 'data-i18n' in content or 'pageTranslations' in content or 'ZT_PAGE' in content

def extract_text_nodes(html_content):
    """Extract meaningful Chinese text from the body."""
    texts = []
    # Remove script/style tags and their content
    cleaned = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', html_content, flags=re.DOTALL)
    # Remove HTML tags
    cleaned = re.sub(r'<[^>]+>', '\n', cleaned)
    # Split into lines and find non-empty text
    for line in cleaned.split('\n'):
        line = line.strip()
        if len(line) >= 2 and not line.startswith('//') and not line.startswith('/*'):
            texts.append(line)
    return texts

def find_page_title(html_content):
    m = re.search(r'<title>([^<]+)</title>', html_content)
    return html_mod.unescape(m.group(1)) if m else 'AI Tool - ZenTools'

def find_h1(html_content):
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html_content)
    return html_mod.unescape(m.group(1)) if m else ''

def find_desc(html_content):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]+)"', html_content)
    return html_mod.unescape(m.group(1)) if m else ''

def inject_i18n(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_i18n(content):
        return False
    
    page_title = find_page_title(content)
    h1_text = find_h1(content)
    desc_text = find_desc(content)
    
    slug = os.path.splitext(os.path.basename(filepath))[0]
    tool_name = h1_text or page_title.split('-')[0].strip() or slug
    
    # Build the translations script to inject before </head>
    trans_script = f'''
<script>
var pageTranslations = {{
  zh: {{ pageTitle: "{html_mod.escape(page_title)}", back: "← 返回首页", title: "{html_mod.escape(tool_name)}", desc: "{html_mod.escape(desc_text or '')}", ad: "广告位（Google AdSense）", run: "开始生成", copy: "复制结果", clear: "清空", copied: "已复制", guideTitle: "使用说明", privacyTitle: "隐私说明", privacyText: "本工具为浏览器本地处理，不会上传内容到服务器。", inputPlaceholder: "请输入内容...", outputPlaceholder: "结果会显示在这里..." }},
  en: {{ pageTitle: "{html_mod.escape(tool_name)} - Free Online Tool | ZenTools", back: "← Back to Home", title: "{html_mod.escape(tool_name)}", desc: "Free online tool. Process locally in your browser.", ad: "Ad Space", run: "Generate", copy: "Copy", clear: "Clear", copied: "Copied", guideTitle: "How to Use", privacyTitle: "Privacy Notice", privacyText: "This tool runs locally in your browser. No data is uploaded to any server.", inputPlaceholder: "Enter content...", outputPlaceholder: "Result will appear here..." }},
  ja: {{ pageTitle: "{html_mod.escape(tool_name)} - 無料オンラインツール | ZenTools", back: "← ホームに戻る", title: "{html_mod.escape(tool_name)}", desc: "ブラウザで動作する無料オンラインツール。", ad: "広告スペース", run: "生成", copy: "コピー", clear: "クリア", copied: "コピーしました", guideTitle: "使い方", privacyTitle: "プライバシー", privacyText: "このツールはブラウザ内で処理され、サーバーへ送信されません。", inputPlaceholder: "内容を入力...", outputPlaceholder: "結果が表示されます..." }},
  vi: {{ pageTitle: "{html_mod.escape(tool_name)} - Công cụ Trực tuyến Miễn phí | ZenTools", back: "← Quay lại trang chủ", title: "{html_mod.escape(tool_name)}", desc: "Công cụ trực tuyến miễn phí. Xử lý trong trình duyệt.", ad: "Vị trí quảng cáo", run: "Tạo", copy: "Sao chép", clear: "Xóa", copied: "Đã sao chép", guideTitle: "Hướng dẫn", privacyTitle: "Quyền riêng tư", privacyText: "Công cụ này xử lý trong trình duyệt. Không tải dữ liệu lên máy chủ.", inputPlaceholder: "Nhập nội dung...", outputPlaceholder: "Kết quả sẽ hiển thị ở đây..." }}
}};
window.ZT_PAGE = pageTranslations;
</script>
<style>
.lang-select{{background:#111827;color:white;border:1px solid #334155;border-radius:10px;padding:10px 12px;font-size:14px;cursor:pointer}}
.lang-select:focus{{outline:none;border-color:#3b82f6}}
</style>
'''
    
    # Inject before </head>
    content = content.replace('</head>', trans_script + '</head>')
    
    # Add data-i18n to title
    content = re.sub(r'<title>', '<title data-i18n="pageTitle">', content, 1)
    
    # Add data-i18n to h1
    content = re.sub(r'<h1>', '<h1 data-i18n="title">', content, 1)
    
    # Add lang select to top-bar
    lang_select = '<select id="languageSelect" class="lang-select"><option value="zh">中文</option><option value="ja">日本語</option><option value="en">English</option><option value="vi">Tiếng Việt</option></select>'
    
    # Find top-bar or header area and add lang select
    top_bar_patterns = [
        r'(<a[^>]*返回首页[^<]*</a>)',
        r'(<button[^>]*>.*?返回.*?</button>)',
    ]
    for pat in top_bar_patterns:
        m = re.search(pat, content)
        if m:
            anchor = m.group(1)
            # Add data-i18n to the back link
            new_anchor = re.sub(r'<a', '<a data-i18n="back"', anchor, 1)
            content = content.replace(anchor, new_anchor + lang_select, 1)
            break
    
    # Add data-i18n to description paragraph
    content = re.sub(r'<p\s+class="desc">(?!data-i18n)', '<p class="desc" data-i18n="desc">', content, 1)
    
    # Add data-i18n to ad div
    content = re.sub(r'class="ad-box"', 'class="ad-box" data-i18n="ad"', content, 1)
    
    # Add data-i18n to buttons
    btn_labels = {
        '开始生成': 'run', '生成': 'run', '开始处理': 'run',
        '复制结果': 'copy', '复制': 'copy',
        '清空': 'clear',
    }
    for label, key in btn_labels.items():
        content = re.sub(f'({re.escape(label)})</button>', f' data-i18n="{key}">{label}</button>', content, 1)
    
    # Add the i18n script before </body>
    i18n_js = '''
<script>
var translations = window.ZT_PAGE || {};
function setLanguage(lang) {
  var data = translations[lang] || translations.zh || {};
  document.title = data.pageTitle || document.title;
  document.querySelectorAll("[data-i18n]").forEach(function(el) {
    var k = el.getAttribute("data-i18n");
    if (data[k]) el.textContent = data[k];
  });
  document.querySelectorAll("[data-i18n-placeholder]").forEach(function(el) {
    var k = el.getAttribute("data-i18n-placeholder");
    if (data[k]) el.placeholder = data[k];
  });
  localStorage.setItem("zentools_lang", lang);
}
var sel = document.getElementById("languageSelect");
if (sel) {
  sel.addEventListener("change", function() { setLanguage(this.value); });
  var saved = localStorage.getItem("zentools_lang") || "zh";
  sel.value = saved;
  setLanguage(saved);
}
</script>
'''
    content = content.replace('</body>', i18n_js + '</body>')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True

# Process all ai/ files
processed = []
skipped = []
for fname in sorted(os.listdir(AI_DIR)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(AI_DIR, fname)
    if inject_i18n(fpath):
        processed.append(fname)
    else:
        skipped.append(fname)

print(f"Processed ({len(processed)}): {', '.join(processed)}")
print(f"Skipped (already has i18n) ({len(skipped)}): {', '.join(skipped)}")
