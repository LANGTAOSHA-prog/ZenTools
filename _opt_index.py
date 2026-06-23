import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', encoding='utf-8') as f:
    html = f.read()

# 1. Add resource hints after baidu meta tag
old1 = '''  <meta name="baidu-site-verification" content="codeva-Al7SOJ5bzC" />

  <link rel="manifest" href="/manifest.json" />
  <link rel="stylesheet" href="assets/css/tool-ui.css" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="apple-touch-icon" href="favicon.svg" />

  <!-- ===== 防崩 1.0 — 最先加载，兜住所有错误 ===== -->
  <script src="assets/js/anti-crash.js"></script>'''

new1 = '''  <meta name="baidu-site-verification" content="codeva-Al7SOJ5bzC" />

  <!-- ===== 资源预加载 ===== -->
  <link rel="dns-prefetch" href="https://www.googletagmanager.com" />
  <link rel="preconnect" href="https://www.googletagmanager.com" />
  <link rel="preconnect" href="https://pagead2.googlesyndication.com" />

  <link rel="manifest" href="/manifest.json" />
  <link rel="stylesheet" href="assets/css/tool-ui.min.css" />
  <link rel="icon" type="image/svg+xml" href="favicon.svg" />
  <link rel="apple-touch-icon" href="favicon.svg" />

  <!-- ===== 防崩 1.0 — 最先加载 ===== -->
  <script src="assets/js/anti-crash.min.js" defer></script>'''

if old1 in html:
    html = html.replace(old1, new1, 1)
    print("OK: Updated head section")
else:
    print("FAIL: head pattern not found")
    # Debug
    idx = html.find('baidu-site-verification')
    if idx >= 0:
        snippet = html[idx:idx+400]
        print(repr(snippet))

# 2. Update other CSS/JS references to minified versions
html = html.replace('assets/css/tool-ui.css', 'assets/css/tool-ui.min.css')
html = html.replace('assets/css/style.css', 'assets/css/style.min.css')
html = html.replace('assets/js/tool-ui.js', 'assets/js/tool-ui.min.js')
html = html.replace('assets/js/common-i18n.js', 'assets/js/common-i18n.min.js')

# 3. Add loading="lazy" to images
html = html.replace('<img src=', '<img loading="lazy" src=')

# 4. Add preload for favicon
if 'rel="preload"' not in html:
    html = html.replace(
        '<link rel="icon"',
        '<link rel="preload" href="/favicon.svg" as="image" />\n  <link rel="icon"',
        1
    )

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("OK: All optimizations applied to index.html")
