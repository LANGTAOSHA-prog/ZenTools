#!/usr/bin/env python3
"""Batch-unify tutorial pages (tutorials/*.html) to --zen-* design system."""
import glob, re, os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSET_PREFIX = '../'  # tutorials/ is one level deep

ZEN_VARS = """    :root {
      --zen-primary: #0066FF;
      --zen-secondary: #00C2B8;
      --zen-gradient: linear-gradient(135deg, #0066FF, #00C2B8);
      --zen-text-main: #111827;
      --zen-text-sub: #4B5563;
      --zen-text-placeholder: #9CA3AF;
      --zen-bg-base: #F9FAFB;
      --zen-bg-card: #FFFFFF;
      --zen-border: #E5E7EB;
      --zen-radius-base: 12px;
      --zen-radius-card: 16px;
      --zen-radius-btn: 8px;
    }
    .dark {
      --zen-text-main: #F9FAFB;
      --zen-text-sub: #D1D5DB;
      --zen-text-placeholder: #64748B;
      --zen-bg-base: #0F172A;
      --zen-bg-card: #1E293B;
      --zen-border: #334155;
    }"""

BASE_STYLES = """
    * { margin:0; padding:0; box-sizing:border-box; }
    body { font-family:Inter,"Source Han Sans SC",PingFang SC,Microsoft YaHei,system-ui,sans-serif; background:var(--zen-bg-base); color:var(--zen-text-main); line-height:1.5; transition:background .35s,color .35s; -webkit-font-smoothing:antialiased; }
    a { color:inherit; text-decoration:none; }
    .site-nav { position:fixed; top:0; left:0; width:100%; z-index:999; backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px); background:rgba(255,255,255,0.75); border-bottom:1px solid var(--zen-border); transition:background .3s; }
    .dark .site-nav { background:rgba(15,23,42,0.75); }
    .nav-inner { height:70px; display:flex; align-items:center; justify-content:space-between; gap:16px; max-width:1200px; margin:0 auto; padding:0 24px; }
    .logo-text-blue { color:var(--zen-primary); }
    .logo-text-teal { color:var(--zen-secondary); }
    .nav-links a { padding:8px 14px; border-radius:8px; font-size:14px; font-weight:500; color:var(--zen-text-sub); transition:color .2s,background .2s; text-decoration:none; }
    .nav-links a:hover { color:var(--zen-text-main); background:rgba(0,0,0,0.04); }
    .dark .nav-links a:hover { background:rgba(255,255,255,0.06); }
    .nav-links a.active { color:var(--zen-primary); font-weight:600; }
    .mobile-overlay { position:fixed; inset:0; z-index:300; background:rgba(0,0,0,0.7); backdrop-filter:blur(8px); opacity:0; visibility:hidden; transition:opacity .3s,visibility .3s; }
    .mobile-overlay.open { opacity:1; visibility:visible; }
    .mobile-drawer { position:fixed; top:0; right:0; bottom:0; width:300px; max-width:85vw; background:rgba(249,250,251,0.97); border-left:1px solid var(--zen-border); padding:24px 20px; z-index:310; overflow-y:auto; transform:translateX(100%); transition:transform .3s; backdrop-filter:blur(24px); }
    .dark .mobile-drawer { background:rgba(15,23,42,0.97); }
    .mobile-overlay.open .mobile-drawer { transform:translateX(0); }
    .mobile-drawer a { display:block; padding:12px 16px; border-radius:8px; font-size:16px; font-weight:500; color:var(--zen-text-sub); transition:color .2s,background .2s; }
    .mobile-drawer a:hover { background:rgba(0,0,0,0.04); }
    .dark .mobile-drawer a:hover { background:rgba(255,255,255,0.06); }
    .page-tutorial { max-width:900px; margin:120px auto 40px; padding:0 24px; }
    .page-tutorial .meta { color:var(--zen-text-sub); font-size:14px; margin-bottom:24px; }
    .page-tutorial .meta h1 { font-size:clamp(28px,4vw,40px); font-weight:800; letter-spacing:-1px; line-height:1.2; margin-bottom:12px; background:var(--zen-gradient); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .article-body { color:var(--zen-text-main); font-size:16px; line-height:1.85; }
    .article-body h2 { font-size:24px; font-weight:700; margin:36px 0 16px; color:var(--zen-text-main); }
    .article-body h3 { font-size:20px; font-weight:600; margin:28px 0 12px; }
    .article-body p { margin-bottom:16px; }
    .article-body ul,.article-body ol { margin:12px 0 20px 24px; }
    .article-body li { margin-bottom:8px; }
    .tip { background:var(--zen-bg-card); border:1px solid var(--zen-border); border-radius:var(--zen-radius-base); padding:16px 20px; margin:20px 0; }
    .tip::before { content:attr(data-label); display:block; font-size:12px; font-weight:700; color:var(--zen-primary); margin-bottom:8px; text-transform:uppercase; letter-spacing:1px; }
    .screenshot-wrap { margin:24px 0; text-align:center; }
    .screenshot-wrap img { max-width:100%; border-radius:var(--zen-radius-base); border:1px solid var(--zen-border); }
    .rel-tools { max-width:900px; margin:40px auto; padding:0 24px; }
    .rel-tools h3 { font-size:16px; font-weight:700; color:var(--zen-text-sub); margin-bottom:16px; }
    .back-link { text-align:center; margin:20px 0 40px; }
    .back-link a { display:inline-flex; align-items:center; gap:6px; padding:10px 20px; border-radius:8px; border:1px solid var(--zen-border); color:var(--zen-text-sub); font-size:14px; transition:color .2s,border-color .2s; }
    .back-link a:hover { color:var(--zen-primary); border-color:var(--zen-primary); }
    footer { border-top:1px solid var(--zen-border); padding:36px 0; text-align:center; }
    .footer-inner { max-width:1200px; margin:0 auto; padding:0 24px; }
    .footer-logo { font-size:18px; font-weight:700; margin-bottom:12px; background:var(--zen-gradient); -webkit-background-clip:text; background-clip:text; color:transparent; }
    .footer-links { display:flex; justify-content:center; gap:20px; flex-wrap:wrap; margin-bottom:14px; font-size:13px; }
    .footer-links a { color:var(--zen-text-sub); transition:color .2s; }
    .footer-links a:hover { color:var(--zen-primary); }
    .footer-copy { font-size:13px; color:var(--zen-text-placeholder); }
    .lang-select { background:transparent; border:1px solid var(--zen-border); border-radius:8px; padding:6px 10px; color:var(--zen-text-sub); font-size:13px; cursor:pointer; }
    @media(max-width:768px) {
      .nav-links a:not(#hamburgerBtn):not(#themeToggle):not(#langSelect) { display:none; }
      #hamburgerBtn { display:inline-flex !important; }
      .page-tutorial { margin-top:100px; }
      .nav-inner { height:60px; gap:8px; }
    }"""

NAV_HTML = """  <nav class="site-nav">
    <div class="nav-inner">
      <div class="brand-logo">
        <a href="/" style="display:flex;align-items:center;gap:8px;text-decoration:none;color:inherit">
          <div class="logo-icon" style="width:36px;height:36px;border-radius:50%;background:var(--zen-gradient);display:flex;align-items:center;justify-content:center;color:#fff;font-size:20px;font-weight:700">Z</div>
          <div><span class="logo-text-blue">Zen</span><span class="logo-text-teal">Tools</span><span class="logo-ver" style="font-size:11px;color:var(--zen-text-placeholder);font-weight:400;margin-left:2px">3.2</span></div>
        </a>
      </div>
      <div class="nav-links">
        <a href="/">首页</a>
        <a href="/tools.html">全部工具</a>
        <a href="/tutorials/" class="active">教程中心</a>
        <a href="/guides/">深度指南</a>
        <a href="/compare/">工具对比</a>
        <a href="/professions.html">职业工具</a>
        <a href="/my.html">用户中心</a>
        <a href="/about.html">关于</a>
        <button id="themeToggle" title="切换主题" style="all:unset;display:inline-flex;align-items:center;justify-content:center;padding:8px 12px;border-radius:8px;font-size:14px;color:var(--zen-text-sub);cursor:pointer">🌙</button>
        <select id="langSelect" class="lang-select">
          <option value="zh">中文</option>
          <option value="en">English</option>
          <option value="ja">日本語</option>
          <option value="vi">Tiếng Việt</option>
        </select>
        <button id="hamburgerBtn" style="all:unset;display:none;align-items:center;justify-content:center;padding:8px 12px;border-radius:8px;font-size:16px;color:var(--zen-text-sub);cursor:pointer">☰</button>
      </div>
    </div>
  </nav>
"""

MOBILE_DRAWER = """  <div class="mobile-overlay" id="mobileOverlay">
    <div class="mobile-drawer" id="mobileDrawer">
      <button id="mobileClose" style="display:flex;align-items:center;justify-content:center;width:36px;height:36px;border-radius:8px;border:1px solid var(--zen-border);background:transparent;color:var(--zen-text-sub);cursor:pointer;font-size:18px;margin:0 0 20px auto">✕</button>
      <a href="/">首页</a>
      <a href="/tools.html">全部工具</a>
      <a href="/tutorials/">教程中心</a>
      <a href="/guides/">深度指南</a>
      <a href="/compare/">工具对比</a>
      <a href="/professions.html">职业工具</a>
      <a href="/my.html">用户中心</a>
      <a href="/about.html">关于</a>
    </div>
  </div>
"""

SCRIPTS = """<script>
(function(){
var t=localStorage.getItem('zentools_theme');
if(t==='dark')document.documentElement.classList.add('dark');
var b=document.getElementById('themeToggle');
if(b){b.textContent=document.documentElement.classList.contains('dark')?'☀️':'🌙';
b.addEventListener('click',function(){document.documentElement.classList.toggle('dark');
var d=document.documentElement.classList.contains('dark');
this.textContent=d?'☀️':'🌙';localStorage.setItem('zentools_theme',d?'dark':'light');});}
})();
(function(){
var o=document.getElementById('mobileOverlay'),h=document.getElementById('hamburgerBtn'),c=document.getElementById('mobileClose');
function cl(){o.classList.remove('open');h.textContent='☰';document.body.style.overflow='';}
if(!h||!o)return;
h.addEventListener('click',function(e){e.stopPropagation();
if(o.classList.contains('open'))cl();else{o.classList.add('open');h.textContent='✕';document.body.style.overflow='hidden';}});
if(c)c.addEventListener('click',cl);
o.addEventListener('click',function(e){var d=document.getElementById('mobileDrawer');if(d&&!d.contains(e.target))cl();});
document.addEventListener('keydown',function(e){if(e.key==='Escape'&&o.classList.contains('open'))cl();});
})();
if('serviceWorker'in navigator){window.addEventListener('load',function(){navigator.serviceWorker.register('/sw.js').catch(function(){});});}
</script>"""


def fix_tutorial(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # 1. Remove blob divs
    content = re.sub(r'\s*<div class="blob blob-1"></div>\s*', '', content)
    content = re.sub(r'\s*<div class="blob blob-2"></div>\s*', '', content)

    # 2. Remove old <nav>...</nav>
    content = re.sub(r'<nav>.*?</nav>', '', content, flags=re.DOTALL)

    # 3. Remove <div class="z-wrap">
    content = re.sub(r'<div class="z-wrap">\s*', '', content, count=1)

    # 4. Insert new nav + mobile drawer after <body>
    content = content.replace('<body>', '<body>\n' + NAV_HTML + '\n' + MOBILE_DRAWER + '\n')

    # 5. Add CSS variables and base styles
    if '<style>' in content:
        content = content.replace('<style>', '<style>\n' + ZEN_VARS + '\n' + BASE_STYLES, 1)

    # 6. Add theme-color meta if missing
    if 'theme-color' not in content:
        content = content.replace('<meta charset', '<meta name="theme-color" content="#0066FF">\n<meta charset', 1)

    # 7. Replace old CSS var references
    for old, new in [
        ('var(--cyan)', 'var(--zen-primary)'),
        ('var(--purple)', 'var(--zen-secondary)'),
        ('var(--pink)', 'var(--zen-danger)'),
        ('var(--text)', 'var(--zen-text-main)'),
        ('var(--muted)', 'var(--zen-text-sub)'),
        ('var(--glass)', 'var(--zen-bg-card)'),
        ('var(--border)', 'var(--zen-border)'),
        ('var(--bg)', 'var(--zen-bg-base)'),
        ('var(--border-h)', 'var(--zen-border)'),
        ('var(--glow-c)', '0 0 40px rgba(0,102,255,0.12)'),
    ]:
        content = content.replace(old, new)

    # 8. Fix hardcoded dark colors in tutorial-specific styles
    content = content.replace('background: #06070d;', 'background: var(--zen-bg-base);')
    content = content.replace('background:#06070d;', 'background:var(--zen-bg-base);')
    content = content.replace('color: #f0f4ff;', 'color: var(--zen-text-main);')
    content = content.replace('color:#f0f4ff;', 'color:var(--zen-text-main);')
    content = content.replace('color: #6b7a9f;', 'color: var(--zen-text-sub);')
    content = content.replace('color:#6b7a9f;', 'color:var(--zen-text-sub);')

    # 9. Fix old logo class references in CSS
    content = content.replace('.logo {', '/* .logo deprecated */ .brand-logo {')

    # 10. Fix lang-select styling in tutorial pages that hardcode it
    content = re.sub(r'\.lang-select\s*\{[^}]*\}', '', content)

    # 11. Add scripts before </body>
    content = content.replace('</body>', SCRIPTS + '\n</body>')

    # 12. Fix any remaining .logo class on <a> tags (should be gone after nav removal)
    # but some tutorials might have logo in footer

    # 13. Add manifest link if missing
    if 'link rel="manifest"' not in content:
        content = content.replace('<link rel="canonical"', '<link rel="manifest" href="/manifest.json">\n<link rel="canonical"', 1)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    files = glob.glob(str(ROOT / 'tutorials' / '*.html'))
    
    updated = 0
    errors = []
    
    print(f"Processing {len(files)} tutorial pages...")
    
    for i, f in enumerate(files):
        try:
            if fix_tutorial(f):
                updated += 1
            if (i + 1) % 50 == 0:
                print(f"  {i+1}/{len(files)} ... {updated} updated")
        except Exception as e:
            errors.append((f, str(e)))
    
    print(f"\nDone! {updated}/{len(files)} tutorials updated.")
    if errors:
        print(f"Errors: {len(errors)}")
        for f, e in errors[:5]:
            print(f"  {f}: {e}")


if __name__ == '__main__':
    main()
