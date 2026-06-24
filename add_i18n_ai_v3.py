#!/usr/bin/env python3
"""Add i18n infrastructure to AI tool pages — lambda-based re.sub to avoid backref issues."""

import os, re, html as html_mod

AI_DIR = '/workspace/ai'
EXISTING_I18N = {
    'ai-title.html','ai-email.html','ai-resume.html','ai-summary.html',
    'ai-interview.html','ai-japanese-essay.html','ai-code-explain.html',
    'index.html'
}

def has_i18n(c):
    return 'data-i18n' in c or 'pageTranslations' in c or 'ZT_PAGE' in c

def find_meta(c, name):
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', c)
    return html_mod.unescape(m.group(1)) if m else ''

def find_title(c):
    m = re.search(r'<title>([^<]*)</title>', c)
    return html_mod.unescape(m.group(1)) if m else 'AI Tool'

def extract_ui(c):
    texts = {}
    for tag in ['h1','h2','h3','h4']:
        for m in re.finditer(rf'<{tag}[^>]*>([^<]+)</{tag}>', c):
            t = m.group(1).strip()
            if len(t) >= 2: texts.setdefault(t, 'heading_' + re.sub(r'\W+','_',t[:12]).lower().strip('_'))
    for m in re.finditer(r'<button[^>]*>([^<]+)</button>', c):
        t = m.group(1).strip()
        if len(t) >= 2: texts.setdefault(t, re.sub(r'\W+','_',t[:12]).lower().strip('_'))
    for m in re.finditer(r'<label[^>]*>([^<]+)</label>', c):
        t = m.group(1).strip()
        if len(t) >= 2: texts.setdefault(t, 'label_' + re.sub(r'\W+','_',t[:10]).lower().strip('_'))
    for m in re.finditer(r'placeholder="([^"]+)"', c):
        t = html_mod.unescape(m.group(1))
        if len(t) >= 2: texts.setdefault(t, 'ph_' + re.sub(r'\W+','_',t[:8]).lower().strip('_'))
    for m in re.finditer(r'alt="([^"]+)"', c):
        t = html_mod.unescape(m.group(1))
        if len(t) >= 2: texts.setdefault(t, 'alt_' + re.sub(r'\W+','_',t[:8]).lower().strip('_'))
    return texts

def inj(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if has_i18n(c):
        return False

    pt = find_title(c)
    md = find_meta(c, 'description')
    ui = extract_ui(c)
    
    tn = re.sub(r'\s*[-–—|].*$', '', pt).strip() or 'AI Tool'
    
    en_d = {k: v for k, v in [
        ('pageTitle', tn + ' - Free Online Tool | ZenTools'),
        ('metaDesc', 'Free online tool. Process locally in your browser.'),
    ]}
    ja_d = {k: v for k, v in [
        ('pageTitle', tn + ' - 無料オンラインツール | ZenTools'),
        ('metaDesc', 'ブラウザで動作する無料オンラインツール。'),
    ]}
    vi_d = {k: v for k, v in [
        ('pageTitle', tn + ' - Công cụ Trực tuyến Miễn phí | ZenTools'),
        ('metaDesc', 'Công cụ trực tuyến miễn phí. Xử lý trong trình duyệt.'),
    ]}
    
    zh_d = {'pageTitle': pt, 'metaDesc': md}
    
    for zt, k in ui.items():
        zh_d[k] = zt
        en_d[k] = zt
        ja_d[k] = zt
        vi_d[k] = zt
    
    def esc(v):
        return v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')
    def fmt(d):
        return '{' + ', '.join(k + ": '" + esc(v) + "'" for k,v in d.items()) + '}'
    
    trans_js = f'var pageTranslations={{"zh":{fmt(zh_d)},"en":{fmt(en_d)},"ja":{fmt(ja_d)},"vi":{fmt(vi_d)}}};'
    
    # Inject lang-select CSS
    lcss = '.lang-select{background:rgba(255,255,255,0.08);color:#fff;border:1px solid var(--border,rgba(255,255,255,0.12));border-radius:8px;padding:8px 10px;font-size:13px;cursor:pointer}.lang-select:focus{outline:none;border-color:var(--accent,#3b82f6)}'
    sm = re.search(r'</style>', c)
    if sm: c = c[:sm.start()] + lcss + '\n' + c[sm.start():]
    else: c = c.replace('</head>', f'<style>{lcss}</style>\n</head>', 1)
    
    c = c.replace('</head>', f'<script>{trans_js}</script>\n</head>', 1)
    
    # data-i18n on title
    c = re.sub(r'<title>', '<title data-i18n="pageTitle">', c, 1)
    
    # lang select HTML
    lhtml = '<select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="ja">日本語</option><option value="en">English</option><option value="vi">Tiếng Việt</option></select>'
    
    # Insert into header
    inserted = False
    for pat in [r'(</div>\s*(?:<div class="main|<main))', r'(</header>\s*)', r'(class="(?:actions|header-right|header-actions)[^>]*>)']:
        m = re.search(pat, c)
        if m:
            if pat.startswith('(class='):
                c = c[:m.end(1)] + '\n' + lhtml + c[m.end(1):]
            else:
                c = c[:m.start(1)] + lhtml + '\n' + c[m.start(1):]
            inserted = True
            break
    if not inserted:
        m = re.search(r'(class="logo"[^<]*</div>\s*)', c)
        if m:
            c = c[:m.end(1)] + '\n' + lhtml + '\n' + c[m.end(1):]
            inserted = True
    if not inserted:
        m = re.search(r'(<header[^>]*>)', c)
        if m:
            c = c[:m.end(1)] + '\n' + lhtml + '\n' + c[m.end(1):]
    
    # data-i18n on elements using lambda repl
    for zt, k in ui.items():
        esc = re.escape(zt)
        for tag in ['h1','h2','h3','h4']:
            c = re.sub(rf'(<{tag}[^>]*?)>{esc}</{tag}>', lambda m, k=k: f'{m.group(1)} data-i18n="{k}">{m.group(1).partition(">")[2] if ">" in m.group(1) else zt}</{tag}>', c, 1)
        c = re.sub(rf'(<button[^>]*?)>{esc}</button>', lambda m, k=k: f'{m.group(1)} data-i18n="{k}">{zt}</button>', c, 1)
        c = re.sub(rf'(<label[^>]*?)>{esc}</label>', lambda m, k=k: f'{m.group(1)} data-i18n="{k}">{zt}</label>', c, 1)
        c = re.sub(rf'(placeholder="){esc}(")', lambda m, k=k: f'{m.group(1)}{zt}{m.group(2)} data-i18n-placeholder="{k}"', c, 1)
        for tag in ['p','span','div','a']:
            c = re.sub(rf'(<{tag}[^>]*?)>{esc}</{tag}>', lambda m, k=k, t=tag: f'{m.group(1)} data-i18n="{k}">{zt}</{t}>', c, 1)
    
    # setLanguage JS before </body>
    ijs = '<script>(function(){var t=window.pageTranslations||{};function a(l){var d=t[l]||t.zh||{};document.documentElement.lang=l;var ti=document.querySelector(\'title[data-i18n]\');if(ti){var pk=ti.getAttribute(\'data-i18n\');if(d[pk])document.title=d[pk];}document.querySelectorAll(\'[data-i18n]\').forEach(function(e){var k=e.getAttribute(\'data-i18n\');if(d[k]&&k!==\'pageTitle\')e.textContent=d[k];});document.querySelectorAll(\'[data-i18n-placeholder]\').forEach(function(e){var k=e.getAttribute(\'data-i18n-placeholder\');if(d[k])e.placeholder=d[k];});var mc=document.querySelector(\'meta[name="description"]\');if(mc&&d.metaDesc)mc.content=d.metaDesc;}var s=document.getElementById(\'langSelect\');if(s){s.addEventListener(\'change\',function(){a(this.value);localStorage.setItem(\'zentools_lang\',this.value);});var sv=localStorage.getItem(\'zentools_lang\')||\'zh\';s.value=sv;a(sv);}})();</script>'
    c = c.replace('</body>', ijs + '\n</body>', 1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

p, s = [], []
for fn in sorted(os.listdir(AI_DIR)):
    if not fn.endswith('.html'): continue
    if fn in EXISTING_I18N:
        s.append(fn)
        continue
    if inj(os.path.join(AI_DIR, fn)):
        p.append(fn)
    else:
        s.append(fn + ' (has i18n)')

print(f"Processed: {len(p)}")
for f in p: print(f"  + {f}")
print(f"\nSkipped: {len(s)}")
for f in s: print(f"  - {f}")