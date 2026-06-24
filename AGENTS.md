# ZenTools AGENTS.md

## Project Overview

Pure static HTML5/CSS3/Vanilla JS site (no build tools, no package.json). 410 HTML pages, 279 tools across 13 categories. Deployed via GitHub Pages from main branch root.

## Quick Commands

```bash
# Validate all JSON data files
python _check_json.py

# Add new tool entry to data/tools-data.json
python _add_tools.py

# Regenerate sitemap.xml (410 URLs)
python -c "
import os,xml.etree.ElementTree as ET
base='https://zentools.xyz'
root_elem=ET.Element('urlset',xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for r,d,f in os.walk('.'):
 d[:]=[x for x in d if x[0]!='.' and x!='node_modules' and x!='pdf_tools']
 for fn in f:
  if fn.endswith('.html'):
   u=ET.SubElement(root_elem,'url')
   ET.SubElement(u,'loc').text=base+'/'+os.path.relpath(os.path.join(r,fn),'.')
with open('sitemap.xml','w') as f: f.write(ET.tostring(root_elem,encoding='unicode'))
"

# Minify JS assets
python _minify_assets.py

# Start local dev server (port 8000)
python -m http.server 8000
```

## Architecture

- **Data layer**: `data/tools-data.json` (205KB) drives all tool rendering. Categories define directory structure.
- **i18n system**: `assets/js/common-i18n.js` (public) + inline `window.ZT_PAGE` (page-specific). Engine: `ZT.applyLanguage()` in `assets/js/tool-ui.js`. Supports zh/en/ja/vi.
- **Page generation**: Tool pages are generated from tools-data.json entries. Category slug = directory name (e.g., `image/`, `pdf/`, `ai/`).
- **PWA**: `sw.js` (cache-first), `manifest.json` (standalone PWA).
- **SEO**: `sitemap.xml`, `robots.txt`, `.htaccess` (CSP/HSTS/Gzip), canonical URLs, Open Graph tags.

## Key Directories

| Path | Content |
|------|---------|
| `image/`, `pdf/`, `audio/`, `video/`, `text/`, `dev/`, `life/`, `finance/`, `ai/`, `seo/`, `qr/`, `tools/` | Tool HTML pages |
| `tutorials/` | Tutorial pages (no articles/, blog/, posts/ allowed) |
| `assets/js/` | Core JS: `main.js` (homepage), `tool-ui.js` (tool pages), `common-i18n.js` (translations), `anti-crash.js` |
| `assets/css/` | `style.css` (global), `tool-ui.css` (tool pages) |
| `data/` | `tools-data.json` (source of truth) |
| `pdf_tools/` | Standalone Python PDF scripts (not part of web app) |

## Conventions

- **No frameworks**: Pure vanilla JS. No React/Vue/jQuery.
- **Page i18n required**: Every new page must include `window.ZT_PAGE` translations + load `common-i18n.min.js` and `tool-ui.min.js`.
- **Prefer .min.js**: Always reference compressed versions (`common-i18n.min.js`, `tool-ui.min.js`, `anti-crash.min.js`).
- **Tool data JSON**: Adding a tool requires updating `data/tools-data.json` AND creating the corresponding HTML page.
- **Google Analytics**: GA4 tracking ID `G-YOUR_MEASUREMENT_ID` is a placeholder. Replace with real ID for production.
- **Search Console**: `YOUR_VERIFICATION_TOKEN_HERE` is a placeholder. Replace with real token for production.

## Automation Hooks (`.atomcode/settings.json`)

- JSON files in `data/` are auto-validated on write via `_check_json.py`.
- Image/font/lockfile/batch-script edits are blocked.

## CI

`backup.yml` backs up data/config/core scripts on push to main and daily at 00:00 UTC.

## Constraints from PROJECT_RULES.md

- Search existing code before adding: check `components/`, `tools/`, `tutorials/`, `assets/js/`.
- Prefer extending existing implementations over rewriting.
- No duplicate pages or features.
- No temporary test files.
- Tutorials only in `/tutorials/` (not `/articles/`, `/blog/`, `/posts/`).
