#!/usr/bin/env python3
"""Extract full ZT_PAGE from git, supplement missing entries, and fix i18n."""
import re, json, subprocess, os

# ── Step 1: Extract ZT_PAGE from git ──
result = subprocess.run(
    ['git', 'show', '56e7a38:tutorials/index.html'],
    capture_output=True, text=True
)
orig = result.stdout

# Find the ZT_PAGE block
start = orig.find('window.ZT_PAGE={')
end = orig.find('\n<script src="../assets/js/tool-ui.min.js"></script>', start)
zt_raw = orig[start:end]

# Parse ZT_PAGE into structured data
# Format: zh:{key:'val',key2:'val2',...}\nen:{...}\nja:{...}\nvi:{...}
def parse_zt(zt_text):
    data = {}
    # Split by language blocks
    pattern = r'(zh|en|ja|vi):\{([^}]+)\}'
    for m in re.finditer(pattern, zt_text):
        lang = m.group(1)
        body = m.group(2)
        kv = {}
        # Parse key:value pairs
        for pair in re.findall(r"(\w+):'((?:[^'\\]|\\.)*)'", body):
            kv[pair[0]] = pair[1]
        data[lang] = kv
    return data

zt_data = parse_zt(zt_raw)
print(f"Parsed ZT_PAGE: {[f'{k}:{len(v)} keys' for k,v in zt_data.items()]}")

# ── Step 2: Read current index.html for supplement data ──
with open('/workspace/tutorials/index.html', 'r') as f:
    current = f.read()

# Extract card text from current HTML (Chinese only, for missing entries)
card_data = {}
for m in re.finditer(r'<!-- (Article \d+: .+?) -->\n<a class="article-card"[^>]*>.*?<div class="cat"[^>]*>([^<]+)</div>\s*<h3[^>]*>([^<]+)</h3>\s*<div class="meta"><span[^>]*>([^<]+)</span><span[^>]*>([^<]+)</span></div>\s*<div class="summary"[^>]*>([^<]*)</div>', current, re.DOTALL):
    cat_text = m.group(2)
    title = m.group(3)
    date_text = m.group(4)
    read_text = m.group(5)
    summary = m.group(6)
    
    # Extract key from href
    href_m = re.search(r'href="/tutorials/([^"]+)"', current[:m.start()])
    if not href_m:
        href_m = re.search(r'href="([^"]+)"', current[m.start()-200:m.start()])
    if not href_m:
        continue
    
    # Find the a_key from surrounding context
    a_key = None
    context = current[max(0,m.start()-500):m.start()]
    ak = re.search(r'data-i18n="(a\d+)Title"', context)
    if ak:
        a_key = ak.group(1)
    
    # Find cat_key
    cat_key = None
    ck = re.search(r'data-i18n="(cat\w+)"', context[-200:])
    if ck:
        cat_key = ck.group(1)
    
    if a_key:
        card_data[a_key] = dict(cat=cat_text, title=title, date=date_text, read=read_text, summary=summary, cat_key=cat_key)

print(f"Extracted {len(card_data)} cards from current HTML")

# ── Step 3: Find missing entries and supplement ──
zh = zt_data.get('zh', {})
missing_zh = {}
for a_key, cd in card_data.items():
    if a_key not in zh:
        missing_zh[a_key] = cd
        print(f"MISSING in zh: {a_key} - {cd['title']}")
    # Also check if catKey exists
    if cd.get('cat_key') and cd['cat_key'] not in zh:
        print(f"MISSING cat in zh: {cd['cat_key']}")

print(f"\nMissing zh entries: {len(missing_zh)}")

# ── Step 4: Generate complete ZT_PAGE JS for index.html ──
def build_zt_js(zt_data, card_data, lang):
    """Build a complete ZT_PAGE language block with all required keys."""
    existing = zt_data.get(lang, {}).copy()
    
    if lang == 'zh':
        # For zh, add missing card data
        for a_key, cd in card_data.items():
            if a_key not in existing:
                existing[a_key + 'Title'] = cd['title']
                existing[a_key + 'Date'] = cd['date']
                existing[a_key + 'Read'] = cd['read']
                existing[a_key + 'Sum'] = cd['summary']
                if cd.get('cat_key') and cd['cat_key'] not in existing:
                    existing[cd['cat_key']] = cd['cat']
    
    # Build the JS string
    parts = []
    for key in existing:
        val = existing[key]
        # Escape single quotes
        val = val.replace("'", "\\'")
        parts.append(f"{key}:'{val}'")
    
    return ','.join(parts)

# Build complete ZT_PAGE
langs = {}
for lang in ['zh', 'en', 'ja', 'vi']:
    existing = zt_data.get(lang, {}).copy()
    if lang == 'zh':
        for a_key, cd in card_data.items():
            if a_key + 'Title' not in existing:
                existing[a_key + 'Title'] = cd['title']
                existing[a_key + 'Date'] = cd['date']
                existing[a_key + 'Read'] = cd['read']
                existing[a_key + 'Sum'] = cd['summary']
                if cd.get('cat_key') and cd['cat_key'] not in existing:
                    existing[cd['cat_key']] = cd['cat']
    langs[lang] = existing

# Generate the JS
zt_js_lines = ['window.ZT_PAGE={']
for lang in ['zh', 'en', 'ja', 'vi']:
    parts = []
    for key in langs[lang]:
        val = langs[lang][key].replace("'", "\\'")
        parts.append(f"{key}:'{val}'")
    zt_js_lines.append(f"{lang}:{{{','.join(parts)}}},")
zt_js_lines.append('};')

zt_js = '\n'.join(zt_js_lines)

# ── Step 5: Update index.html ──
# Replace everything from window.ZT_PAGE to </script>
new_index = re.sub(
    r'window\.ZT_PAGE=\{.*?</script>',
    zt_js + '\n</script>',
    current,
    flags=re.DOTALL
)

with open('/workspace/tutorials/index.html', 'w') as f:
    f.write(new_index)

print(f"\nUpdated index.html ZT_PAGE")
print(f"zh: {len(langs['zh'])} keys")
print(f"en: {len(langs['en'])} keys")
print(f"ja: {len(langs['ja'])} keys")
print(f"vi: {len(langs['vi'])} keys")

# Save for tutorial generator
import json as j
with open('/tmp/zt_data.json', 'w') as f:
    j.dump(langs, f, ensure_ascii=False)
print("Saved ZT data to /tmp/zt_data.json")
