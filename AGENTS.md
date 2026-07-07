# ZenTools AGENTS.md

## Project Overview

Pure static HTML5/CSS3/Vanilla JS site. ~410 HTML pages, 279 tools across 13 categories. Deployed via GitHub Pages from main branch root. No package.json, no build tools, no frameworks.

## Quick Commands

```bash
# Start local dev server (HTTP server only - no build step)
python3 -m http.server 8000

# Generate new tool page (creates HTML + updates tools-data.json + regenerates sitemap)
python3 _add_tool.py --slug pdf-ocr --category "PDF工具" \
  --name-zh "PDF OCR" --name-en "PDF OCR" --name-ja "PDF OCR" --name-vi "PDF OCR" \
  --desc-zh "描述" --desc-en "Description" --desc-ja "説明" --desc-vi "Mô tả" \
  --keywords "keyword1 keyword2"

# Generate new tutorial (result in /tutorials/)
python3 _add_tutorial.py --slug my-tutorial --category "PDF工具" \
  --title-zh "教程标题" --desc-zh "描述" --tool-url "/pdf/some-tool.html"

# Generate new guide/review (result in /guides/)
python3 _add_guide.py --slug my-review --type review \
  --title-zh "评测标题" --desc-zh "描述" --word-count 2500 --read-minutes 20

# Post-edit verification pipeline (run in this order after any data change)
python3 _check_json.py                  # validate JSON integrity
python3 _sync_tools_data_js.py          # JSON -> JS data sync
python3 _gen_sitemap.py                 # regenerate sitemap.xml
python3 _minify_assets.py               # re-minify JS/CSS

# Validate JSON files only
python3 _check_json.py
```

## Architecture

- **Data layer**: `data/tools-data.json` (~666KB) drives all tool rendering. Single source of truth. Categories map to directories.
- **i18n system**: `assets/js/common-i18n.js` (public, `window.ZT_COMMON`) + inline `window.ZT_PAGE` per page. Engine: `ZT.applyLanguage()` in `assets/js/tool-ui.js`. Merge priority: `ZT_PAGE` overrides `ZT_COMMON`. Supports zh/en/ja/vi.
- **PWA**: `sw.js` (cache-first with 5 cache tiers: core, assets, data, html/LRU-200, pages), `manifest.json`.
- **Anti-crash**: `assets/js/anti-crash.js` must load FIRST in `<head>`. Catches global errors, JSON corruption, switches to fallback mode after 5 errors/5s.
- **SEO per tool page**: FAQPage + WebApplication + HowTo schema.org JSON-LD, Og tags, Twitter Card, canonical URL.

## Script load order (critical)

Every page `<head>` must follow this exact order:
1. `anti-crash.min.js` (first, before anything else)
2. Meta/SEO tags, canonical, manifest link
3. `tool-ui.min.css`
4. Tool-specific `<style>` block (use CSS variables only: `var(--cyan)`, `var(--purple)`, `var(--pink)`, `var(--border)`, `var(--text)`, `var(--muted)`, `var(--glass)`)
5. AdSense script (`ca-pub-1955887568822472`)
6. FAQPage + WebApplication + (optional) HowTo schema JSON-LD
7. Inline `window.ZT_PAGE` with zh/en/ja/vi keys

At end of `<body>`:
8. `common-i18n.min.js`
9. `tool-ui.min.js`
10. Tool-specific logic

## Key Directories

| Path | Content |
|------|---------|
| `pdf/`, `image/`, `text/`, `dev/`, `audio/`, `video/`, `ai/`, `seo/`, `life/`, `finance/`, `qr/`, `json/`, `tools/` | Tool HTML pages (each dir has its own `index.html` category page) |
| `tutorials/` | Tutorial pages (360). No articles/, blog/, posts/ allowed. |
| `guides/` | Deep guides and reviews (28 pages) |
| `compare/` | Tool comparison landing page |
| `assets/js/` | `main.js` (homepage), `tool-ui.js` (global engine), `common-i18n.js` (shared translations), `anti-crash.js` (error resilience) |
| `assets/css/` | `tool-ui.css` (global), `style.css` (auxiliary) |
| `data/` | `tools-data.json` (source of truth), `categories.json` |
| `pdf_tools/` | Standalone Python PDF scripts (not part of web app) |

## Tool page skeleton

Every tool HTML page must contain these structural elements in order:
```
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="z-wrap">
    <nav><div class="nav-inner">...</div></nav>
    <div class="page-header reveal">
      <div class="breadcrumb">...</div>
      <h1 data-i18n="pageTitle">...</h1>
      <p data-i18n="pageDesc">...</p>
    </div>
    <div class="tool-box reveal">...</div>         <!-- core tool UI -->
    <div class="section">
      <div class="section-head"><h2>...</h2></div>
      <div class="info-grid">...</div>             <!-- usage instructions, 3-col cards -->
    </div>
    <footer>...</footer>
  </div>
</body>
```

## Conventions

- **No frameworks**: Pure vanilla JS. No React/Vue/jQuery.
- **No build step**: All pages run directly in browser. `.min.js`/`.min.css` are the compressed versions (run `_minify_assets.py` after editing sources).
- **CSS variables only**: Never hardcode color values. Use `var(--bg)`, `var(--text)`, `var(--muted)`, `var(--cyan)`, `var(--purple)`, `var(--pink)`, `var(--border)`, `var(--glass)`.
- **i18n every page**: Every page must define `window.ZT_PAGE` with zh/en/ja/vi keys. Text in HTML uses `data-i18n="key"` and `data-i18n-placeholder="key"`.
- **Fallback text must match**: The HTML text content must match the zh value in `ZT_PAGE` for the same key.
- **Dynamic content pages**: Pages that render content via JS (compare/, guides/, tutorials/) must listen to `zt-langchange` event to re-render when language switches.
- **Schema.org required**: Each tool page needs `FAQPage` + `WebApplication` JSON-LD. Tutorial/guide pages use `Article` schema.
- **AdSense**: Publisher ID is `ca-pub-1955887568822472`. Already wired into tool page template.
- **Adding a tool**: Create HTML page + add entry to `data/tools-data.json`. Then run check → sync → sitemap → minify pipeline.
- **`.atomcode/settings.json`**: Contains a Windows-path hook for JSON validation (`D:\\Users\\taojiang\\...`). This only works on the author's machine; ignore on Linux.

## Constraints from PROJECT_RULES.md

- Search existing code before adding: check `components/`, `tools/`, `tutorials/`, `assets/js/`.
- Prefer extending existing implementations over rewriting.
- No duplicate pages or features.
- No temporary test files.
- Tutorials only in `/tutorials/` (not `/articles/`, `/blog/`, `/posts/`).

## CI

`backup.yml` backs up data/config/core scripts on push to main and daily at 00:00 UTC.
