#!/usr/bin/env python3
"""
Universal i18n injection for all directories.
Handles Pattern A (old card), Pattern B (nav-bar + tool-box), Pattern C (site-header), Pattern D (index pages).
"""

import os, re, html as html_mod

EXCLUDE_DIRS = {'assets', 'css', 'js', 'data', 'guides', 'tutorials', 'node_modules', '__pycache__', '.git'}
ROOT = '/workspace'

def has_i18n(c):
    return bool(re.search(r'data-i18n\s*=|pageTranslations|ZTPAGE|ZT_PAGE', c))

def find_title(c):
    m = re.search(r'<title>([^<]*)</title>', c)
    return html_mod.unescape(m.group(1).strip()) if m else 'Tool'

def find_desc(c):
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', c)
    return html_mod.unescape(m.group(1)) if m else ''

def extract_ui(c):
    """Extract Chinese UI text nodes."""
    texts = {}
    for t in ['h1','h2','h3','h4']:
        for m in re.finditer(rf'<{t}[^>]*>([^<]+)</{t}>', c):
            tx = m.group(1).strip()
            if len(tx) >= 2 and not tx.startswith('<'): texts.setdefault(tx, 'h_' + re.sub(r'\W+','_',tx[:10]).lower().strip('_'))
    for m in re.finditer(r'<button[^>]*>([^<]+)</button>', c):
        tx = m.group(1).strip()
        if len(tx) >= 2: texts.setdefault(tx, 'btn_' + re.sub(r'\W+','_',tx[:8]).lower().strip('_'))
    for m in re.finditer(r'<label[^>]*>([^<]+)</label>', c):
        tx = m.group(1).strip()
        if len(tx) >= 2: texts.setdefault(tx, 'lbl_' + re.sub(r'\W+','_',tx[:8]).lower().strip('_'))
    for m in re.finditer(r'placeholder="([^"]+)"', c):
        tx = html_mod.unescape(m.group(1))
        if len(tx) >= 2: texts.setdefault(tx, 'ph_' + re.sub(r'\W+','_',tx[:8]).lower().strip('_'))
    for m in re.finditer(r'alt="([^"]+)"', c):
        tx = html_mod.unescape(m.group(1))
        if len(tx) >= 2 and tx not in ('logo','banner'): texts.setdefault(tx, 'alt_' + re.sub(r'\W+','_',tx[:8]).lower().strip('_'))
    return texts

CN_EN = {
    '清空': 'Clear', '复制结果': 'Copy Result', '开始生成': 'Generate', '开始处理': 'Process',
    '开始压缩': 'Compress', '开始裁剪': 'Crop', '开始转换': 'Convert', '开始分析': 'Analyze',
    '计算年龄': 'Calculate', '下载': 'Download', '下载图片': 'Download Image', '发送': 'Send',
    '复制': 'Copy', '已复制': 'Copied', '上传图片': 'Upload Image', '选择图片': 'Select Image',
    '预览': 'Preview', '结果': 'Result', '搜索': 'Search',
    '使用说明': 'How to Use', '隐私说明': 'Privacy Notice',
    '广告位（Google AdSense）': 'Ad Space', '广告位': 'Ad Space',
    '← 返回首页': '← Back Home', '返回首页': 'Back Home', '返回': 'Back',
    '开始': 'Start', '停止': 'Stop', '重置': 'Reset',
    '原始大小：': 'Original:', '压缩后：': 'Compressed:',
    '压缩完成': 'Compression Done', '请选择图片': 'Please select an image',
    '输入内容...': 'Enter content...',
    '请输入内容': 'Please enter content',
    '请输入内容...': 'Enter content...',
    '请输入关键词': 'Enter keywords',
    '结果会显示在这里...': 'Result will appear here...',
    '在此粘贴要分析的文本内容...': 'Paste text content to analyze...',
    '请在此输入文本': 'Enter your text here',
}

def process(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if has_i18n(c):
        # Already has i18n - add window alias & fix localStorage key
        mod = False
        if 'window.pageTranslations' not in c and 'pageTranslations' in c:
            c = c.replace('var pageTranslations=', 'window.pageTranslations=', 1)
            c = c.replace('const pageTranslations=', 'window.pageTranslations=', 1)
            mod = True
        if 'window.pageTranslations' not in c and re.search(r'const\s+translations\s*=', c):
            c = re.sub(r'(const\s+translations\s*=\s*\{)', r'\1\nwindow.pageTranslations = translations;\n', c, 1)
            mod = True
        if '"siteLanguage"' in c:
            c = c.replace('"siteLanguage"', '"zentools_lang"')
            mod = True
        if "'siteLanguage'" in c:
            c = c.replace("'siteLanguage'", "'zentools_lang'")
            mod = True
        # Fix languageSelect -> langSelect in JS
        if 'getElementById("languageSelect")' in c:
            c = c.replace('getElementById("languageSelect")', 'getElementById("langSelect")')
            c = c.replace('id="languageSelect"', 'id="langSelect"')
            mod = True
        if mod:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(c)
            return 'unified'
        return 'skipped'
    
    pt = find_title(c)
    md = find_desc(c)
    ui = extract_ui(c)
    tn = re.sub(r'\s*[-–—|].*$', '', pt).strip() or 'Tool'
    
    def esc(v):
        return v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')
    
    def mk_lang(d):
        parts = []
        for k, v in d.items():
            parts.append(f"{k}: '{esc(v)}'")
        return '{' + ', '.join(parts) + '}'
    
    zh_d = {'pageTitle': pt, 'metaDesc': md}
    en_d = {'pageTitle': tn + ' - Free Online Tool | ZenTools', 'metaDesc': 'Free online tool. Process in browser.'}
    ja_d = {'pageTitle': tn + ' - 無料オンラインツール | ZenTools', 'metaDesc': 'ブラウザで動作する無料ツール。'}
    vi_d = {'pageTitle': tn + ' - Công cụ Trực tuyến | ZenTools', 'metaDesc': 'Công cụ trực tuyến miễn phí.'}
    
    for zt, k in ui.items():
        zh_d[k] = zt
        en_d[k] = CN_EN.get(zt, zt)
        ja_d[k] = zt
        vi_d[k] = zt
    
    trans_js = f'<script>window.pageTranslations={{"zh":{mk_lang(zh_d)},"en":{mk_lang(en_d)},"ja":{mk_lang(ja_d)},"vi":{mk_lang(vi_d)}}};</script>'
    
    # lang-select CSS
    lcss = '.lang-select{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.12);border-radius:8px;padding:8px 10px;font-size:13px;cursor:pointer}.lang-select:focus{outline:none;border-color:#3b82f6}'
    
    # Inject CSS
    sm = re.search(r'</style>', c)
    if sm:
        c = c[:sm.start()] + lcss + '\n' + c[sm.start():]
    else:
        c = c.replace('</head>', f'<style>{lcss}</style>\n</head>', 1)
    
    # Inject translations
    c = c.replace('</head>', trans_js + '\n</head>', 1)
    
    # data-i18n on title
    c = re.sub(r'<title>', '<title data-i18n="pageTitle">', c, 1)
    
    # Add lang select
    lhtml = '<select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="ja">日本語</option><option value="en">English</option><option value="vi">Tiếng Việt</option></select>'
    
    inserted = False
    for pat in [r'(</div>\s*<div class="main)', r'(</header>\s*<main)', r'(</header>\s*)', r'(class="(?:actions|header-right|header-actions)[^>]*>)']:
        m = re.search(pat, c)
        if m:
            c = c[:m.start(1)] + lhtml + '\n' + c[m.start(1):]
            inserted = True
            break
    if not inserted:
        m = re.search(r'(class="nav-bar[^"]*"[^>]*>)', c)
        if m:
            c = c[:m.end(1)] + '\n' + lhtml + c[m.end(1):]
            inserted = True
    if not inserted:
        m = re.search(r'(class="logo"[^<]*</div>\s*)', c)
        if m:
            c = c[:m.end(1)] + '\n' + lhtml + '\n' + c[m.end(1):]
            inserted = True
    if not inserted:
        m = re.search(r'(<header[^>]*>)', c)
        if m:
            c = c[:m.end(1)] + '\n' + lhtml + '\n' + c[m.end(1):]
            inserted = True
    if not inserted:
        # For Pattern A: before h1 in .card or .container
        m = re.search(r'(<h1[^>]*>)', c)
        if m:
            c = c[:m.start(1)] + '<div class="top-bar" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:15px;margin-bottom:20px">' + lhtml + '</div>\n' + c[m.start(1):]
    
    # data-i18n on elements
    for zt, k in ui.items():
        esc_zt = re.escape(zt)
        for tag in ['h1','h2','h3','h4']:
            c = re.sub(rf'(<{tag})([^>]*?)>{esc_zt}</{tag}>', lambda m, k=k, zt=zt, t=tag: f'{m.group(1)}{m.group(2)} data-i18n="{k}">{zt}</{t}>' if 'data-i18n' not in m.group(2) else m.group(0), c, 1)
        c = re.sub(rf'(<button)([^>]*?)>{esc_zt}</button>', lambda m, k=k, zt=zt: f'{m.group(1)}{m.group(2)} data-i18n="{k}">{zt}</button>' if 'data-i18n' not in m.group(2) else m.group(0), c, 1)
        c = re.sub(rf'(<label)([^>]*?)>{esc_zt}</label>', lambda m, k=k, zt=zt: f'{m.group(1)}{m.group(2)} data-i18n="{k}">{zt}</label>' if 'data-i18n' not in m.group(2) else m.group(0), c, 1)
        c = re.sub(rf'placeholder="{esc_zt}"', lambda m, k=k, zt=zt: f'placeholder="{zt}" data-i18n-placeholder="{k}"', c, 1)
        for tag in ['p','span','div','a']:
            c = re.sub(rf'(<{tag})([^>]*?)>{esc_zt}</{tag}>', lambda m, k=k, zt=zt, t=tag: f'{m.group(1)}{m.group(2)} data-i18n="{k}">{zt}</{t}>' if 'data-i18n' not in m.group(2) else m.group(0), c, 1)
    
    # setLanguage JS before </body>
    ijs = '<script>(function(){var t=window.pageTranslations||{};function a(l){var d=t[l]||t.zh||{};document.documentElement.lang=l;var ti=document.querySelector(\'title[data-i18n]\');if(ti){var pk=ti.getAttribute(\'data-i18n\');if(d[pk])document.title=d[pk];}document.querySelectorAll(\'[data-i18n]\').forEach(function(e){var k=e.getAttribute(\'data-i18n\');if(d[k]&&k!==\'pageTitle\')e.textContent=d[k];});document.querySelectorAll(\'[data-i18n-placeholder]\').forEach(function(e){var k=e.getAttribute(\'data-i18n-placeholder\');if(d[k])e.placeholder=d[k];});var mc=document.querySelector(\'meta[name="description"]\');if(mc&&d.metaDesc)mc.content=d.metaDesc;}var s=document.getElementById(\'langSelect\');if(s){s.addEventListener(\'change\',function(){a(this.value);localStorage.setItem(\'zentools_lang\',this.value);});var sv=localStorage.getItem(\'zentools_lang\')||\'zh\';s.value=sv;a(sv);}})();</script>'
    c = c.replace('</body>', ijs + '\n</body>', 1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    return 'injected'

# Process all directories
results = {}
for item in sorted(os.listdir(ROOT)):
    dpath = os.path.join(ROOT, item)
    if not os.path.isdir(dpath) or item in EXCLUDE_DIRS:
        continue
    htmld = [f for f in os.listdir(dpath) if f.endswith('.html')]
    if not htmld:
        continue
    injected, unified, skipped = 0, 0, 0
    for fn in sorted(htmld):
        fpath = os.path.join(dpath, fn)
        try:
            r = process(fpath)
            if r == 'injected': injected += 1
            elif r == 'unified': unified += 1
            else: skipped += 1
        except Exception as e:
            print(f"ERROR {fn}: {e}")
    results[item] = (injected, unified, skipped)

print("Results (injected | unified | skipped):")
total_i, total_u, total_s = 0, 0, 0
for d, (i, u, s) in sorted(results.items()):
    print(f"  {d:12s}  +{i:3d} injected  ~{u:3d} unified  -{s:3d} skipped")
    total_i += i; total_u += u; total_s += s
print(f"{'TOTAL':12s}  +{total_i:3d} injected  ~{total_u:3d} unified  -{total_s:3d} skipped")