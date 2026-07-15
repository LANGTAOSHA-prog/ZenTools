#!/usr/bin/env python3
"""Batch-update all tool pages and category indexes to new --zen-* design system."""
import os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DIRS = ['pdf','image','text','dev','audio','video','ai','seo','life','finance','qr','json','tools']

# ── CSS variable mapping ──
VAR_MAP = [
    ('var(--cyan)',   'var(--zen-primary)'),
    ('var(--purple)', 'var(--zen-secondary)'),
    ('var(--pink)',   'var(--zen-danger)'),
    ('var(--text)',   'var(--zen-text-main)'),
    ('var(--muted)',  'var(--zen-text-sub)'),
    ('var(--glass)',  'var(--zen-bg-card)'),
    ('var(--border)', 'var(--zen-border)'),
    ('var(--bg)',     'var(--zen-bg-base)'),
    ('var(--border-h)', 'var(--zen-border)'),
    ('var(--glow-c)', 'var(--zen-border)'),
]

ZEN_ROOT = """        --zen-primary: #0066FF;
        --zen-secondary: #00C2B8;
        --zen-gradient: linear-gradient(135deg, #0066FF, #00C2B8);
        --zen-success: #22C55E;
        --zen-warning: #F97316;
        --zen-danger: #EF4444;
        --zen-text-main: #111827;
        --zen-text-sub: #4B5563;
        --zen-text-placeholder: #9CA3AF;
        --zen-bg-base: #F9FAFB;
        --zen-bg-card: #FFFFFF;
        --zen-border: #E5E7EB;
        --zen-radius-base: 12px;
        --zen-radius-card: 16px;
        --zen-radius-btn: 8px;
        --zen-radius-tag: 6px;
      }
      .dark {
        --zen-text-main: #F9FAFB;
        --zen-text-sub: #D1D5DB;
        --zen-text-placeholder: #64748B;
        --zen-bg-base: #0F172A;
        --zen-bg-card: #1E293B;
        --zen-border: #334155;
      }"""

BODY_OPEN = """<body>
<div class="z-wrap">
  <nav class="site-nav">
    <div class="container nav-inner">
      <div class="brand-logo">
        <a href="/" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:inherit">
          <div class="logo-icon" style="width:36px;height:36px;border-radius:50%;background:var(--zen-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:700">Z</div>
          <div><span class="logo-text-blue">Zen</span><span class="logo-text-teal">Tools</span><span class="logo-ver" style="font-size:11px;color:var(--zen-text-placeholder);font-weight:400;margin-left:2px">3.2</span></div>
        </a>
      </div>""".strip() + '\n'


def get_nav_links(content):
    """Extract existing nav links (a href / text) and language select from old nav."""
    # Find existing nav links
    nav_match = re.search(r'<nav>(.*?)</nav>', content, re.DOTALL)
    if not nav_match:
        nav_match = re.search(r'<nav.*?>(.*?)</nav>', content, re.DOTALL)
    
    links = []
    has_guides = False
    has_compare = False
    has_professions = False
    has_my = False
    
    if nav_match:
        nav_html = nav_match.group(1)
        # Extract <a> tags
        for a in re.finditer(r'<a\s+(.*?)>(.*?)</a>', nav_html, re.DOTALL):
            attrs = a.group(1)
            text = re.sub(r'<.*?>', '', a.group(2)).strip()
            href = ''
            cls = ''
            data_i18n = ''
            href_m = re.search(r'href="([^"]*)"', attrs)
            if href_m: href = href_m.group(1)
            cls_m = re.search(r'class="([^"]*)"', attrs)
            if cls_m: cls = cls_m.group(1)
            i18n_m = re.search(r'data-i18n="([^"]*)"', attrs)
            if i18n_m: data_i18n = i18n_m.group(1)
            links.append((href, text, data_i18n, cls))
            
            # Detect which nav items exist
            if href and 'guides' in href: has_guides = True
            if href and 'compare' in href: has_compare = True
            if href and 'professions' in href: has_professions = True
            if href and 'my.html' in href: has_my = True
    
    return links, has_guides, has_compare, has_professions, has_my


def extract_breadcrumb(content):
    """Extract breadcrumb crumbs from old page-header."""
    bc_match = re.search(r'<div class="breadcrumb">(.*?)</div>', content, re.DOTALL)
    crumbs = []
    if bc_match:
        bc_html = bc_match.group(1)
        for span in re.finditer(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', bc_html, re.DOTALL):
            crumbs.append((span.group(1), span.group(2).strip()))
        # Also get the current page crumb
        cur_m = re.search(r'<span class="cur"[^>]*>(.*?)</span>', bc_html)
        if cur_m:
            crumbs.append(('', cur_m.group(1).strip()))
    return crumbs


def extract_page_header(content):
    """Extract data from old .page-header: eyebrow, h1/sub, description."""
    header = {}
    ph_match = re.search(r'<div class="page-header.*?">(.*?)</div>\s*(?:<div class="tool-box|<div class="section|<div class="cat-grid)', content, re.DOTALL)
    if not ph_match:
        # Try shorter match (category pages)
        ph_match = re.search(r'<div class="page-header[^"]*">(.*?)(?:<div id="toolGrid"|<div class="cat-grid"|<div class="tool-list"|<div class="section"|</div>\s*</div>\s*<script)', content, re.DOTALL)
    
    if ph_match:
        ph = ph_match.group(1)
        # H1 with grad
        h1_m = re.search(r'data-i18n="h1Grad">(.*?)</span>', ph)
        if h1_m: header['h1Grad'] = h1_m.group(1)
        
        h1sub_m = re.search(r'data-i18n="h1Sub">(.*?)</span>', ph)
        if h1sub_m: header['h1Sub'] = h1sub_m.group(1)
        
        desc_m = re.search(r'data-i18n="pageDesc">(.*?)</p>', ph)
        if desc_m: header['pageDesc'] = desc_m.group(1)
        
        eyebrow_m = re.search(r'data-i18n="eyebrow">(.*?)</span>', ph)
        if eyebrow_m: header['eyebrow'] = eyebrow_m.group(1)
        
        h1_plain = re.search(r'<span\s+data-i18n="h1Grad">(.*?)</span>', ph)
        if h1_plain: header['h1Text'] = h1_plain.group(1)
        
        # Category pages may have different patterns
        h1_cat = re.search(r'<h1>(.*?)</h1>', ph, re.DOTALL)
        if h1_cat: header['h1Cat'] = h1_cat.group(1).strip()
    
    return header


def get_asset_prefix(filepath):
    """Determine the correct path prefix for assets."""
    rel = os.path.relpath(ROOT, os.path.dirname(filepath)).replace('\\', '/')
    if rel == '.': return ''
    depth = len(rel.split('/'))
    if depth == 1 and rel != '': return '../'
    return '../' * depth if rel != '.' else ''


def get_body_styles(content):
    """Extract existing <style> block content and merge with zen variables."""
    style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
    if style_match:
        original_style = style_match.group(1)
        # Remove old blob styles if any
        original_style = re.sub(r'\.blob\s*\{[^}]*\}', '', original_style)
        original_style = re.sub(r'\.blob-\d\s*\{[^}]*\}', '', original_style)
    else:
        original_style = ''
    return original_style


def extract_footer(content):
    """Extract footer links and copyright from old footer."""
    footer = {'links': []}
    ft_match = re.search(r'<footer>(.*?)</footer>', content, re.DOTALL)
    if ft_match:
        ft = ft_match.group(1)
        for a in re.finditer(r'<a\s+href="([^"]*)"[^>]*>(.*?)</a>', ft, re.DOTALL):
            footer['links'].append((a.group(1), a.group(2).strip()))
        copy_m = re.search(r'<p[^>]*data-i18n="footerCopy"[^>]*>(.*?)</p>', ft)
        if copy_m: footer['copy'] = copy_m.group(1)
    return footer


def transform_file(filepath):
    """Transform a single HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    asset_prefix = get_asset_prefix(filepath)
    
    # 1. Remove blob divs
    content = re.sub(r'\s*<div class="blob blob-1"></div>\s*', '', content)
    content = re.sub(r'\s*<div class="blob blob-2"></div>\s*', '', content)
    
    # 2. Remove old nav and z-wrap open
    content = re.sub(r'<nav\s*>\s*<div class="nav-inner">.*?</div>\s*</nav>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="z-wrap">\s*', '', content, count=1)
    
    # 3. Transform .page-header to hero section
    crumbs = extract_breadcrumb(original)
    header = extract_page_header(original)
    
    hero_html = build_hero(crumbs, header)
    
    # Replace page-header
    content = re.sub(
        r'<div class="page-header[^"]*">.*?</div>\s*(?=<div class="tool-box|<div class="section|<div class="cat-grid|<div id="toolGrid"|<div class="tool-list"|<div class="subcat-section"|</div>\s*</div>\s*<script)',
        hero_html,
        content, flags=re.DOTALL
    )
    
    # 4. Replace footer
    footer = extract_footer(original)
    new_footer = build_footer(footer)
    content = re.sub(r'<footer>.*?</footer>', new_footer, content, flags=re.DOTALL)
    
    # 5. Update CSS variables in style block
    for old, new in VAR_MAP:
        content = content.replace(old, new)
    
    # 6. Add :root/.dark variables
    content = re.sub(
        r'(<style>)',
        r'\1\n    :root {\n' + ZEN_ROOT + '\n    }\n',
        content, count=1
    )
    
    # 7. Add common base styles for nav/hero/footer
    base_styles = get_base_styles()
    content = re.sub(
        r'(</style>)',
        base_styles + r'\n\1',
        content, count=1
    )
    
    # 8. Replace body opening with nav
    content = re.sub(
        r'<body>',
        BODY_OPEN + build_nav_content(asset_prefix) + '\n  </nav>\n' + build_mobile_drawer(),
        content, count=1
    )
    
    # 9. Fix asset paths
    if asset_prefix:
        content = content.replace('../assets/', '/assets/')
        for pattern_old, pattern_new in [
            ('src="../assets/', 'src="/assets/'),
            ('href="../assets/', 'href="/assets/'),
        ]:
            content = content.replace(pattern_old, pattern_new)
    
    # 10. Add theme toggle + mobile drawer + SW scripts before </body>
    scripts = build_scripts()
    content = re.sub(r'(</body>)', scripts + r'\n\1', content, count=1)
    
    # 11. Fix double z-wrap closing if any
    content = content.replace('</div>\n</div>\n<script', '</script')
    
    # 12. Add closing z-wrap div before scripts area (but after main content)
    # Find the last </footer> or the </body> close and insert </div> before it
    content = content.replace('\n<script', '\n</div>\n<script', 1)
    
    # 13. Add anti-crash.js if missing
    if 'anti-crash.min.js' not in content:
        content = content.replace('</title>', '</title>\n  <script src="' + asset_prefix + 'assets/js/anti-crash.min.js" defer></script>')
    
    # 14. Update theme-color
    content = content.replace('<meta name="theme-color" content="#0a0a1a">', '<meta name="theme-color" content="#0066FF">')
    content = content.replace('<meta name="theme-color" content="#000000">', '<meta name="theme-color" content="#0066FF">')
    
    # Only write if changes were made
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def build_nav_content(prefix):
    """Build the nav-links section."""
    return """      <div class="nav-links">
        <a href=""" + ('"/"' if prefix == '' else '"/"') + """ data-i18n="navHome">首页</a>
        <a href=""" + ('"/tools.html"' if prefix == '' else '"/tools.html"') + """ data-i18n="navAll">全部工具</a>
        <a href=""" + ('"/tutorials/"' if prefix == '' else '"/tutorials/"') + """ data-i18n="navArticles">教程中心</a>
        <a href=""" + ('"/guides/"' if prefix == '' else '"/guides/"') + """ data-i18n="navGuides">深度指南</a>
        <a href=""" + ('"/compare/"' if prefix == '' else '"/compare/"') + """ data-i18n="navCompare">工具对比</a>
        <a href=""" + ('"/professions.html"' if prefix == '' else '"/professions.html"') + """ data-i18n="navProfessions">职业工具</a>
        <a href=""" + ('"/my.html"' if prefix == '' else '"/my.html"') + """ data-i18n="navMy">用户中心</a>
        <button class="theme-toggle" id="themeToggle" title="切换主题" style="all:unset;display:inline-flex;align-items:center;justify-content:center;padding:8px 12px;border-radius:8px;font-size:14px;color:var(--zen-text-sub);cursor:pointer">🌙</button>
        <select class="lang-select" id="langSelect" style="all:unset;display:inline-flex;align-items:center;padding:8px 12px;border-radius:8px;font-size:13px;color:var(--zen-text-sub);cursor:pointer;font-family:inherit">
          <option value="zh">中文</option>
          <option value="en">English</option>
          <option value="ja">日本語</option>
          <option value="vi">Tiếng Việt</option>
        </select>
        <button class="hamburger" id="hamburgerBtn" style="all:unset;display:none;align-items:center;justify-content:center;padding:8px 12px;border-radius:8px;font-size:16px;color:var(--zen-text-sub);cursor:pointer">☰</button>
      </div>
    </div>
  </nav>"""


def build_mobile_drawer():
    return """\n  <div class="mobile-overlay" id="mobileOverlay">
    <div class="mobile-drawer" id="mobileDrawer">
      <button class="close-btn" id="mobileClose" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;border:1px solid var(--zen-border);background:transparent;color:var(--zen-text-sub);cursor:pointer;font-size:18px;margin:0 0 20px auto">✕</button>
      <a href="/" data-i18n="navHome" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">首页</a>
      <a href="/tools.html" data-i18n="navAll" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">全部工具</a>
      <a href="/tutorials/" data-i18n="navArticles" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">教程中心</a>
      <a href="/guides/" data-i18n="navGuides" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">深度指南</a>
      <a href="/compare/" data-i18n="navCompare" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">工具对比</a>
      <a href="/professions.html" data-i18n="navProfessions" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">职业工具</a>
      <a href="/my.html" data-i18n="navMy" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">用户中心</a>
      <a href="/about.html" data-i18n="navAbout" style="display:block;padding:12px 16px;border-radius:8px;font-size:16px;font-weight:500;color:var(--zen-text-sub);text-decoration:none">关于</a>
    </div>
  </div>\n"""


def build_hero(crumbs, header):
    """Build hero section from old page-header data."""
    tag_text = header.get('eyebrow', 'Tool')
    h1_text = header.get('h1Grad', header.get('h1Text', header.get('h1Cat', '工具')))
    sub_text = header.get('h1Sub', '')
    desc_text = header.get('pageDesc', '')
    
    breadcrumb_html = ''
    if crumbs:
        bc_parts = []
        for href, text in crumbs:
            if href:
                bc_parts.append(f'<a href="{href}">{text}</a>')
            else:
                bc_parts.append(f'<span style="color:var(--zen-primary)">{text}</span>')
        breadcrumb_html = '<div class="breadcrumb" style="display:flex;align-items:center;gap:8px;font-size:13px;color:var(--zen-text-placeholder);margin-bottom:28px">' + ' <span style="opacity:0.3">/</span> '.join(bc_parts) + '</div>\n'
    
    sub_line = ''
    if sub_text:
        sub_line = f'\n      <p class="hero-sub" data-i18n="h1Sub" style="font-size:17px;color:var(--zen-text-sub);max-width:560px;margin:8px auto 24px">{sub_text}</p>'
    
    desc_line = ''
    if desc_text and desc_text != sub_text:
        desc_line = f'\n      <p data-i18n="pageDesc" style="font-size:15px;color:var(--zen-text-sub);max-width:560px;margin:0 auto">{desc_text}</p>'
    
    return f"""<section class="page-hero" style="padding-top:150px;padding-bottom:30px;text-align:center;position:relative;overflow:hidden">
    <div class="hero-bg" style="position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse 60% 50% at 30% 20%,rgba(0,102,255,.05) 0%,transparent 50%),radial-gradient(ellipse 50% 40% at 70% 70%,rgba(0,194,184,.04) 0%,transparent 50%)"></div>
    <div class="container" style="max-width:1200px;margin:0 auto;padding:0 24px">
      <div class="hero-tag" style="display:inline-flex;align-items:center;gap:8px;font-size:12px;font-weight:600;color:var(--zen-text-placeholder);letter-spacing:2px;margin-bottom:24px"><span style="width:6px;height:6px;background:var(--zen-primary);border-radius:50%"></span>{tag_text}</div>
      {breadcrumb_html}
      <h1 style="font-size:clamp(32px,5vw,48px);font-weight:800;letter-spacing:-1.5px;line-height:1.1;margin-bottom:8px"><span class="hero-gradient-text" data-i18n="h1Grad" style="background:var(--zen-gradient);-webkit-background-clip:text;background-clip:text;color:transparent">{h1_text}</span></h1>{sub_line}{desc_line}
    </div>
  </section>\n"""


def build_footer(footer_data):
    """Build new footer."""
    links_html = ''
    for href, text in footer_data.get('links', []):
        links_html += f'\n        <a href="{href}">{text}</a>'
    
    copy_text = footer_data.get('copy', '© 2026 ZenTools · https://zentools.xyz · All rights reserved')
    
    return f"""<footer style="border-top:1px solid var(--zen-border);padding:36px 0;text-align:center">
    <div class="footer-inner" style="max-width:1200px;margin:0 auto;padding:0 24px">
      <div class="footer-logo" style="font-size:18px;font-weight:700;margin-bottom:12px;background:var(--zen-gradient);-webkit-background-clip:text;background-clip:text;color:transparent">ZenTools</div>
      <div class="footer-links" style="display:flex;justify-content:center;gap:20px;flex-wrap:wrap;margin-bottom:14px;font-size:13px">{links_html}
      </div>
      <p class="footer-copy" data-i18n="footerCopy" style="font-size:13px;color:var(--zen-text-placeholder)">{copy_text}</p>
    </div>
  </footer>"""


def get_base_styles():
    return """
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: Inter, "Source Han Sans SC", PingFang SC, Microsoft YaHei, system-ui, sans-serif; background: var(--zen-bg-base); color: var(--zen-text-main); line-height: 1.5; transition: background 0.35s, color 0.35s; -webkit-font-smoothing: antialiased; }
    a { color: inherit; text-decoration: none; }
    .site-nav { position: fixed; top: 0; left: 0; width: 100%; z-index: 999; backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); background: rgba(255,255,255,0.75); border-bottom: 1px solid var(--zen-border); transition: background 0.3s; }
    .dark .site-nav { background: rgba(15,23,42,0.75); }
    .nav-inner { height: 70px; display: flex; align-items: center; justify-content: space-between; gap: 16px; }
    .logo-text-blue { color: var(--zen-primary); }
    .logo-text-teal { color: var(--zen-secondary); }
    .nav-links a { padding: 8px 14px; border-radius: 8px; font-size: 14px; font-weight: 500; color: var(--zen-text-sub); cursor: pointer; transition: color 0.2s, background 0.2s; text-decoration: none; }
    .nav-links a:hover { color: var(--zen-text-main); background: rgba(0,0,0,0.04); }
    .dark .nav-links a:hover { background: rgba(255,255,255,0.06); }
    .nav-links a.active { color: var(--zen-primary); font-weight: 600; }
    .hamburger:hover, .theme-toggle:hover { background: rgba(0,0,0,0.04); }
    .dark .hamburger:hover, .dark .theme-toggle:hover { background: rgba(255,255,255,0.06); }
    .mobile-overlay { position: fixed; inset: 0; z-index: 300; background: rgba(0,0,0,0.7); backdrop-filter: blur(8px); opacity: 0; visibility: hidden; transition: opacity 0.3s, visibility 0.3s; }
    .mobile-overlay.open { opacity: 1; visibility: visible; }
    .mobile-drawer { position: fixed; top: 0; right: 0; bottom: 0; width: 300px; max-width: 85vw; background: rgba(249,250,251,0.97); border-left: 1px solid var(--zen-border); padding: 24px 20px; z-index: 310; overflow-y: auto; transform: translateX(100%); transition: transform 0.3s; backdrop-filter: blur(24px); }
    .dark .mobile-drawer { background: rgba(15,23,42,0.97); }
    .mobile-overlay.open .mobile-drawer { transform: translateX(0); }
    .close-btn:hover { background: rgba(0,0,0,0.04); }
    .dark .close-btn:hover { background: rgba(255,255,255,0.06); }
    .mobile-drawer a:hover { background: rgba(0,0,0,0.04); }
    .dark .mobile-drawer a:hover { background: rgba(255,255,255,0.06); }
    .tool-box { max-width: 900px; margin: 0 auto 48px; background: var(--zen-bg-card); border: 1px solid var(--zen-border); border-radius: 16px; padding: 36px; }
    .tool-box h2 { font-size: 24px; font-weight: 700; margin-bottom: 12px; }
    .tool-box .note { color: var(--zen-text-sub); font-size: 15px; margin-bottom: 24px; }
    .file-input-row { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
    .file-input-row input[type="file"] { flex: 1; min-width: 280px; padding: 14px 18px; border: 1px dashed var(--zen-border); border-radius: 12px; background: var(--zen-bg-base); color: var(--zen-text-sub); font-size: 14px; cursor: pointer; }
    .file-input-row input[type="file"]::file-selector-button { border: none; background: rgba(0,102,255,0.08); color: var(--zen-primary); padding: 8px 16px; border-radius: 8px; margin-right: 12px; cursor: pointer; transition: background 0.2s; }
    .btn-primary { display: inline-flex; align-items: center; justify-content: center; padding: 14px 32px; border-radius: 12px; border: none; background: var(--zen-gradient); color: #fff; font-size: 16px; font-weight: 700; cursor: pointer; transition: opacity 0.2s, transform 0.2s; }
    .btn-primary:hover { opacity: 0.9; transform: translateY(-2px); }
    .btn-primary:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
    .status { margin-top: 16px; color: var(--zen-text-sub); font-size: 14px; min-height: 22px; }
    .section { max-width: 1200px; margin: 0 auto; padding: 40px 24px; }
    .section-head { text-align: center; margin-bottom: 36px; }
    .section-head h2 { font-size: 26px; font-weight: 700; }
    .info-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
    .info-card { background: var(--zen-bg-card); border: 1px solid var(--zen-border); border-radius: 16px; padding: 24px; }
    .info-card h4 { font-size: 16px; font-weight: 700; margin-bottom: 10px; color: var(--zen-primary); }
    .info-card p { font-size: 14px; color: var(--zen-text-sub); line-height: 1.65; }
    .cat-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 14px; }
    .cat-card { background: var(--zen-bg-card); border: 1px solid var(--zen-border); border-radius: 16px; padding: 20px; text-align: center; text-decoration: none; color: var(--zen-text-main); display: block; transition: border-color 0.2s, transform 0.2s; }
    .cat-card:hover { border-color: var(--zen-primary); transform: translateY(-4px); }
    .cat-card .name { font-size: 14px; font-weight: 600; margin-bottom: 4px; color: var(--zen-text-main); }
    .cat-card .desc { font-size: 12px; color: var(--zen-text-sub); }
    .lang-select { background: transparent; border: 1px solid var(--zen-border); border-radius: 8px; padding: 6px 10px; color: var(--zen-text-sub); font-size: 13px; cursor: pointer; }
    @media (max-width: 768px) {
      .nav-links a:not(.hamburger):not(.theme-toggle):not(.lang-select) { display: none; }
      .hamburger { display: inline-flex !important; }
      .page-hero { padding-top: 120px !important; }
      .info-grid { grid-template-columns: 1fr; }
      .tool-box { padding: 24px; }
    }
    @media (max-width: 480px) {
      .nav-inner { height: 60px; gap: 8px; }
      .page-hero { padding-top: 100px !important; }
    }"""


def build_scripts():
    return """
<script>
// 暗黑模式切换
(function() {
  var savedTheme = localStorage.getItem('zentools_theme');
  if (savedTheme === 'dark') document.documentElement.classList.add('dark');
  var btn = document.getElementById('themeToggle');
  if (btn) {
    btn.textContent = document.documentElement.classList.contains('dark') ? '☀️' : '🌙';
    btn.addEventListener('click', function() {
      document.documentElement.classList.toggle('dark');
      var isDark = document.documentElement.classList.contains('dark');
      this.textContent = isDark ? '☀️' : '🌙';
      localStorage.setItem('zentools_theme', isDark ? 'dark' : 'light');
    });
  }
})();

// 移动端侧滑
(function() {
  var overlay = document.getElementById('mobileOverlay');
  var hamBtn = document.getElementById('hamburgerBtn');
  var closeBtn = document.getElementById('mobileClose');
  if (!hamBtn || !overlay) return;
  function closeMenu() { overlay.classList.remove('open'); hamBtn.textContent = '☰'; document.body.style.overflow = ''; }
  hamBtn.addEventListener('click', function(e) {
    e.stopPropagation();
    if (overlay.classList.contains('open')) { closeMenu(); } else {
      overlay.classList.add('open'); hamBtn.textContent = '✕'; document.body.style.overflow = 'hidden';
    }
  });
  if (closeBtn) closeBtn.addEventListener('click', closeMenu);
  overlay.addEventListener('click', function(e) {
    var drawer = document.getElementById('mobileDrawer');
    if (drawer && !drawer.contains(e.target)) closeMenu();
  });
  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape' && overlay.classList.contains('open')) closeMenu();
  });
})();

if ('serviceWorker' in navigator) {
  window.addEventListener('load', function() {
    navigator.serviceWorker.register('/sw.js').catch(function() {});
  });
}
</script>
"""


def main():
    files = []
    for d in DIRS:
        dpath = ROOT / d
        if not dpath.exists(): continue
        for f in dpath.rglob('*.html'):
            files.append(str(f))
    
    total = len(files)
    updated = 0
    errors = []
    
    print(f"Processing {total} files across {len(DIRS)} directories...")
    
    for i, f in enumerate(files):
        try:
            if transform_file(f):
                updated += 1
            if (i + 1) % 50 == 0:
                print(f"  {i+1}/{total} ... {updated} updated")
        except Exception as e:
            errors.append((f, str(e)))
    
    print(f"\nDone! {updated}/{total} files updated.")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for f, e in errors[:10]:
            print(f"  {f}: {e}")


if __name__ == '__main__':
    main()
