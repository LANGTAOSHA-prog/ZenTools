import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

def minify_css(text):
    text = re.sub(r'/\*[\s\S]*?\*/', '', text)  # remove comments
    text = re.sub(r'\s+', ' ', text)              # collapse whitespace
    text = re.sub(r'\s*([{};,:])\s*', r'\1', text) # remove space around operators
    text = re.sub(r';}', '}', text)                # remove last semicolon
    return text.strip()

def minify_js(text):
    text = re.sub(r'//.*', '', text)               # remove single-line comments
    text = re.sub(r'/\*[\s\S]*?\*/', '', text)     # remove multi-line comments
    text = re.sub(r'\s+', ' ', text)               # collapse whitespace
    text = re.sub(r'\s*([{}();,:=+\-*/!<>])\s*', r'\1', text)  # space around operators
    return text.strip()

# Minify CSS files
css_files = ['assets/css/style.css', 'assets/css/tool-ui.css']
for path in css_files:
    with open(path, encoding='utf-8') as f:
        orig = f.read()
    minified = minify_css(orig)
    # Write .min.css version
    base, ext = os.path.splitext(path)
    min_path = base + '.min' + ext
    with open(min_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    savings = (1 - len(minified) / len(orig)) * 100
    print(f"{path}: {len(orig):,} -> {len(minified):,} chars ({savings:.0f}% savings)")
    print(f"  -> {min_path}")

# Minify JS files
js_files = ['assets/js/tool-ui.js', 'assets/js/anti-crash.js', 'assets/js/i18n.js']
for path in js_files:
    if not os.path.exists(path):
        print(f"SKIP: {path} not found")
        continue
    with open(path, encoding='utf-8') as f:
        orig = f.read()
    minified = minify_js(orig)
    base, ext = os.path.splitext(path)
    min_path = base + '.min' + ext
    with open(min_path, 'w', encoding='utf-8') as f:
        f.write(minified)
    savings = (1 - len(minified) / len(orig)) * 100
    print(f"{path}: {len(orig):,} -> {len(minified):,} chars ({savings:.0f}% savings)")
    print(f"  -> {min_path}")

print("\nDone!")
