#!/usr/bin/env python3
"""Add i18n infrastructure to AI tool pages in /workspace/ai/"""

import os, re, html as html_mod

AI_DIR = '/workspace/ai'
EXISTING_I18N_FILES = set(['ai-title','ai-email','ai-resume','ai-summary',
    'ai-interview','ai-japanese-essay','ai-code-explain'])
EXISTING_I18N = {f+'.html' for f in EXISTING_I18N_FILES}

def has_i18n(content):
    return 'data-i18n' in content or 'pageTranslations' in content or 'ZT_PAGE' in content

def find_meta(content, name):
    m = re.search(rf'<meta\s+name="{name}"\s+content="([^"]*)"', content)
    return html_mod.unescape(m.group(1)) if m else ''

def find_title(content):
    m = re.search(r'<title>([^<]*)</title>', content)
    return html_mod.unescape(m.group(1)) if m else 'AI Tool'

def extract_ui_texts(content):
    """Extract Chinese UI text nodes likely needing translation."""
    texts = {}
    
    # h1, h2 text
    for tag in ['h1','h2','h3']:
        for m in re.finditer(rf'<{tag}[^>]*>([^<]+)</{tag}>', content):
            t = m.group(1).strip()
            if len(t) >= 2 and t not in texts:
                texts[t] = '_' + re.sub(r'\s+', '_', t)[:30]
    
    # button text
    for m in re.finditer(r'<button[^>]*>([^<]+)</button>', content):
        t = m.group(1).strip()
        if len(t) >= 2 and t not in texts:
            key = re.sub(r'[^a-zA-Z0-9]+','_',t).lower().strip('_')[:20]
            texts[t] = key or 'btn'
    
    # label text  
    for m in re.finditer(r'<label[^>]*>([^<]+)</label>', content):
        t = m.group(1).strip()
        if len(t) >= 2 and t not in texts:
            texts[t] = re.sub(r'[^a-zA-Z0-9]+','_',t).lower().strip('_')[:20]
    
    # placeholder text in inputs
    for m in re.finditer(r'placeholder="([^"]+)"', content):
        t = html_mod.unescape(m.group(1))
        if len(t) >= 2 and t not in texts:
            texts[t] = 'placeholder_' + re.sub(r'[^a-zA-Z0-9]+','_',t[:10]).lower().strip('_')
    
    # Other notable text spans
    # p with specific class patterns
    for m in re.finditer(r'<(p|span)[^>]*>([^<]{2,40})</\1>', content):
        t = m.group(2).strip()
        if len(t) >= 2 and t not in texts and not t.startswith('<'):
            texts[t] = re.sub(r'[^a-zA-Z0-9]+','_',t[:15]).lower().strip('_')
    
    return texts

def make_translations(page_title, meta_desc, ui_texts):
    """Build translations dict for 4 languages."""
    tool_name = re.sub(r'\s*[-–—|].*$', '', page_title).strip()
    if not tool_name:
        tool_name = page_title
    
    zh = {'pageTitle': page_title, 'metaDesc': meta_desc}
    en = {'pageTitle': tool_name + ' - Free Online Tool | ZenTools', 'metaDesc': 'Free online tool. Process locally in your browser.'}
    ja = {'pageTitle': tool_name + ' - 無料オンラインツール | ZenTools', 'metaDesc': 'ブラウザで動作する無料オンラインツール。'}
    vi = {'pageTitle': tool_name + ' - Công cụ Trực tuyến Miễn phí | ZenTools', 'metaDesc': 'Công cụ trực tuyến miễn phí.'}
    
    for zh_text, key in ui_texts.items():
        zh[key] = zh_text
        en[key] = zh_text  # placeholder - human review needed
        ja[key] = zh_text
        vi[key] = zh_text
    
    return {'zh': zh, 'en': en, 'ja': ja, 'vi': vi}

def format_translations_js(translations):
    """Format translations as compact JS object."""
    langs = {}
    for lang, data in translations.items():
        parts = []
        for k, v in data.items():
            escaped = v.replace('\\', '\\\\').replace("'", "\\'").replace('\n', '\\n').replace('\r', '')
            parts.append(f"{k}: '{escaped}'")
        langs[lang] = '{' + ', '.join(parts) + '}'
    
    entries = ', '.join(f'{lang}: {obj}' for lang, obj in langs.items())
    return 'var pageTranslations={' + entries + '};'

def inject_i18n(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if has_i18n(content):
        return False
    
    page_title = find_title(content)
    meta_desc = find_meta(content, 'description')
    ui_texts = extract_ui_texts(content)
    translations = make_translations(page_title, meta_desc, ui_texts)
    trans_js = format_translations_js(translations)
    
    slug = os.path.splitext(os.path.basename(fpath))[0]
    
    # CSS for lang select
    lang_css = '''
.lang-select{background:rgba(255,255,255,0.08);color:#fff;border:1px solid var(--border,rgba(255,255,255,0.12));border-radius:8px;padding:8px 10px;font-size:13px;cursor:pointer}.lang-select:focus{outline:none;border-color:var(--accent,#3b82f6)}'''
    
    # Inject CSS into existing style tag or create one
    style_match = re.search(r'</style>', content)
    if style_match:
        content = content[:style_match.start()] + lang_css + '\n' + content[style_match.start():]
    else:
        content = content.replace('</head>', f'<style>{lang_css}</style>\n</head>', 1)
    
    # Inject translations script before </head>
    trans_script = f'<script>{trans_js}</script>'
    content = content.replace('</head>', trans_script + '\n</head>', 1)
    
    # Add data-i18n to title tag
    content = re.sub(r'<title>', '<title data-i18n="pageTitle">', content, 1)
    
    # Add lang select to header
    lang_html = '<select id="langSelect" class="lang-select"><option value="zh">中文</option><option value="ja">日本語</option><option value="en">English</option><option value="vi">Tiếng Việt</option></select>'
    
    header_end_patterns = [
        r'(</div>\s*(?:<div class="main|<main))',  # header div close before main
        r'(</header>\s*)',                         # header tag close
    ]
    
    # Try inserting lang select at end of header
    for pat in header_end_patterns:
        m = re.search(pat, content)
        if m:
            content = content[:m.start(1)] + lang_html + '\n' + content[m.start(1):]
            break
    else:
        # Check for .actions or .header-right in header
        m = re.search(r'(<div class="(?:actions|header-right|header-actions)[^>]*>)', content)
        if m:
            content = content[:m.end(1)] + '\n' + lang_html + content[m.end(1):]
        else:
            # Fallback: insert after logo area in header
            m = re.search(r'(.logo[^<]*</div>\s*)', content)
            if m:
                content = content[:m.end(1)] + '\n' + lang_html + '\n' + content[m.end(1):]
    
    # Add data-i18n to elements with known text
    for zh_text, key in ui_texts.items():
        if key in ['pageTitle', 'metaDesc']:
            continue
        
        # Skip if already has data-i18n
        escaped = re.escape(zh_text)
        
        # h1/h2/h3
        for tag in ['h1','h2','h3']:
            content = re.sub(
                rf'(<{tag}[^>]*?)>{escaped}</{tag}>',
                rf'\1 data-i18n="{key}">{zh_text}</{tag}>',
                content, 1
            )
        
        # buttons
        content = re.sub(
            rf'(<button[^>]*?)>{escaped}</button>',
            rf'\1 data-i18n="{key}">{zh_text}</button>',
            content, 1
        )
        
        # labels
        content = re.sub(
            rf'(<label[^>]*?)>{escaped}</label>',
            rf'\1 data-i18n="{key}">{zh_text}</label>',
            content, 1
        )
        
        # placeholder
        content = re.sub(
            rf'(placeholder="){escaped}(")',
            rf'\1{zh_text}\2 data-i18n-placeholder="{key}"',
            content, 1
        )
        
        # p, span, div
        for tag in ['p','span','div']:
            content = re.sub(
                rf'(<{tag}[^>]*?)>{escaped}</{tag}>',
                rf'\1 data-i18n="{key}">{zh_text}</{tag}>',
                content, 1
            )
    
    # Add setLanguage function before </body>
    i18n_js = '''
<script>
(function(){var t=window.pageTranslations||{};function apply(l){var d=t[l]||t.zh||{};document.documentElement.lang=l;var ti=document.querySelector('title[data-i18n]');if(ti){var pk=ti.getAttribute('data-i18n');if(d[pk])document.title=d[pk];}document.querySelectorAll('[data-i18n]').forEach(function(e){var k=e.getAttribute('data-i18n');if(d[k]&&k!=='pageTitle')e.textContent=d[k];});document.querySelectorAll('[data-i18n-placeholder]').forEach(function(e){var k=e.getAttribute('data-i18n-placeholder');if(d[k])e.placeholder=d[k];});var mc=document.querySelector('meta[name="description"]');if(mc&&d.metaDesc)mc.content=d.metaDesc;}var s=document.getElementById('langSelect');if(s){s.addEventListener('change',function(){apply(this.value);localStorage.setItem('zentools_lang',this.value);});var sv=localStorage.getItem('zentools_lang')||'zh';s.value=sv;apply(sv);}})();
</script>'''
    
    content = content.replace('</body>', i18n_js + '\n</body>', 1)
    
    with open(fpath, 'w', encoding='utf-8') as f:
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

print(f"Processed: {len(processed)} files")
for f in processed:
    print(f"  {f}")
print(f"\nSkipped (already has i18n): {len(skipped)} files")
for f in skipped:
    print(f"  {f}")