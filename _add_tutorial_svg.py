#!/usr/bin/env python3
"""
Add SVG tutorial graphics to each tool page.
Inserts a 3-step inline SVG illustration showing:
  Step 1: Upload files  ->  Step 2: Process  ->  Step 3: Download
Between the tool-box section and the info-grid section.

Usage:
  python3 _add_tutorial_svg.py             # dry run (show what will change)
  python3 _add_tutorial_svg.py --apply     # actually modify files
"""

import json
import os
import re
import sys

TOOLS_DIR = '/workspace'
DATA_FILE = '/workspace/data/tools-data.json'

# Category-specific SVG icon definitions
# Each icon is a simple inline SVG for the step illustration
CATEGORY_ICONS = {
    'PDF工具': {
        'upload': '<path d="M12 2L20 4V14C20 17.3 17.3 20 14 20H6C3.8 20 2 18.2 2 16V8L12 2Z" fill="none" stroke="{clr}" stroke-width="2"/>',
        'process': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><path d="M9 12L11 14L15 10" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '图片工具': {
        'upload': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><circle cx="8" cy="9" r="1.5" fill="{clr}"/><path d="M3 15L7 11L11 14L14 11L17 15" fill="none" stroke="{clr}" stroke-width="2"/>',
        'process': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><circle cx="8" cy="9" r="1.5" fill="{clr}"/><path d="M3 15L7 11L11 14L14 11L17 15" fill="none" stroke="{clr}" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    'AI工具': {
        'upload': '<circle cx="12" cy="8" r="3" fill="none" stroke="{clr}" stroke-width="2"/><path d="M5 20C5 16 8 14 12 14C16 14 19 16 19 20" fill="none" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><circle cx="9" cy="10" r="1.2" fill="{clr}"/><circle cx="15" cy="10" r="1.2" fill="{clr}"/><circle cx="12" cy="14" r="1.2" fill="{clr}"/><path d="M10 10L14 10M9 14L15 14M12 11V13" stroke="{clr}" stroke-width="0.8"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '开发工具': {
        'upload': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 9L5 12L7 15M13 9L15 12L13 15" fill="none" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 9L5 12L7 15M13 9L15 12L13 15" fill="none" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '文本工具': {
        'upload': '<path d="M4 3H16L18 5V18H6C4.9 18 4 17.1 4 16V3Z" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 9H15M7 12H15M7 15H12" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<path d="M4 3H16L18 5V18H6C4.9 18 4 17.1 4 16V3Z" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 9H15M7 12H15M7 15H12" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '视频工具': {
        'upload': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M12 9V15L8 13V11L12 9Z" fill="{clr}"/>',
        'process': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M12 9V15L8 13V11L12 9Z" fill="{clr}"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '音频工具': {
        'upload': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 14V10M10 14V8M13 14V11M16 14V9" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 14V10M10 14V8M13 14V11M16 14V9" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    'SEO工具': {
        'upload': '<circle cx="11" cy="11" r="6" fill="none" stroke="{clr}" stroke-width="2"/><path d="M16 16L19 19" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/>',
        'process': '<circle cx="11" cy="11" r="6" fill="none" stroke="{clr}" stroke-width="2"/><path d="M16 16L19 19" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '生活工具': {
        'upload': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><path d="M3 12H17M12 3V17" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><path d="M9 6H15M9 10H15M9 14H15M9 18H15" stroke="{clr}" stroke-width="1.5" stroke-linecap="round"/>',
        'process': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><path d="M3 12H17M12 3V17" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><path d="M9 6H15M9 10H15M9 14H15M9 18H15" stroke="{clr}" stroke-width="1.5" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '金融工具': {
        'upload': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><path d="M12 6V18M8 9H14C15.1 9 16 9.9 16 11C16 12.1 15.1 13 14 13H10C8.9 13 8 12.1 8 11C8 9.9 8.9 9 10 9H16M8 15H14C15.1 15 16 15.9 16 17C16 18.1 15.1 19 14 19H10C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15H16" fill="none" stroke="{clr}" stroke-width="1.5"/>',
        'process': '<circle cx="12" cy="12" r="9" fill="none" stroke="{clr}" stroke-width="2"/><path d="M12 6V18M8 9H14C15.1 9 16 9.9 16 11C16 12.1 15.1 13 14 13H10C8.9 13 8 12.1 8 11C8 9.9 8.9 9 10 9H16M8 15H14C15.1 15 16 15.9 16 17C16 18.1 15.1 19 14 19H10C8.9 19 8 18.1 8 17C8 15.9 8.9 15 10 15H16" fill="none" stroke="{clr}" stroke-width="1.5"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '设计工具': {
        'upload': '<path d="M4 12C4 8 7 5 12 5C14 5 15.5 5.5 17 6.5C18.5 5.5 20 5 22 5C27 5 30 8 30 12C30 18 22 22 16 22C10 22 4 18 4 12Z" fill="none" stroke="{clr}" stroke-width="2"/>',
        'process': '<path d="M4 12C4 8 7 5 12 5C14 5 15.5 5.5 17 6.5C18.5 5.5 20 5 22 5C27 5 30 8 30 12C30 18 22 22 16 22C10 22 4 18 4 12Z" fill="none" stroke="{clr}" stroke-width="2"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    'JSON工具': {
        'upload': '<path d="M4 4H18C19.1 4 20 4.9 20 6V18C20 19.1 19.1 20 18 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 8L5 12L7 16M13 8L15 12L13 16" fill="none" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<path d="M4 4H18C19.1 4 20 4.9 20 6V18C20 19.1 19.1 20 18 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 8L5 12L7 16M13 8L15 12L13 16" fill="none" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '二维码工具': {
        'upload': '<rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><rect x="7" y="7" width="3" height="3" fill="{clr}"/><rect x="14" y="7" width="3" height="3" fill="{clr}"/><rect x="7" y="14" width="3" height="3" fill="{clr}"/><rect x="12" y="12" width="2" height="2" fill="{clr}"/>',
        'process': '<rect x="4" y="4" width="16" height="16" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><rect x="7" y="7" width="3" height="3" fill="{clr}"/><rect x="14" y="7" width="3" height="3" fill="{clr}"/><rect x="7" y="14" width="3" height="3" fill="{clr}"/><rect x="12" y="12" width="2" height="2" fill="{clr}"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
    '综合工具': {
        'upload': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 11H15M7 15H13" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
        'process': '<rect x="3" y="5" width="14" height="14" rx="2" fill="none" stroke="{clr}" stroke-width="2"/><path d="M7 11H15M7 15H13" stroke="{clr}" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="16" r="3" fill="{clr}" opacity="0.3"/>',
        'download': '<path d="M12 2V14M12 14L7 9M12 14L17 9" fill="none" stroke="{clr}" stroke-width="2.5" stroke-linecap="round"/><path d="M4 18H18" stroke="{clr}" stroke-width="2" stroke-linecap="round"/>',
    },
}

# Color mapping per category (matches the gradient accent)
CATEGORY_COLORS = {
    'PDF工具': '#f43145',
    '图片工具': '#27c27b',
    'AI工具': '#8b4cff',
    '开发工具': '#22b978',
    '文本工具': '#f59e0b',
    '视频工具': '#ec4899',
    '音频工具': '#3278ff',
    'SEO工具': '#0ea5e9',
    '生活工具': '#ffb324',
    '金融工具': '#10b981',
    '设计工具': '#ec4899',
    'JSON工具': '#eab308',
    '二维码工具': '#f97316',
    '综合工具': '#6b7280',
}

# Default fallback for uncategorized tools
DEFAULT_ICONS = CATEGORY_ICONS['综合工具']
DEFAULT_COLOR = '#6b7280'

# SVG template - uses CSS variables (--clr-tut) for dynamic coloring
SVG_TEMPLATE = '''
    <div class="tool-tutorial-svg reveal">
      <div class="tutorial-svg-head">
        <span class="tutorial-eyebrow">{eyebrow}</span>
        <h3>{title}</h3>
      </div>
      <svg viewBox="0 0 380 140" width="100%" height="140" xmlns="http://www.w3.org/2000/svg" style="display:block;max-width:420px;margin:0 auto">
        <!-- Step 1 -->
        <g transform="translate(20,20)">
          <circle cx="30" cy="30" r="32" fill="none" stroke="var(--clr-tut)" stroke-width="2.5"/>
          <text x="30" y="37" text-anchor="middle" font-size="22" font-weight="700" fill="var(--clr-tut)" font-family="system-ui">1</text>
          {icon1}
        </g>
        <!-- Arrow 1-2 -->
        <path d="M90 50 L140 50" stroke="var(--clr-tut)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <path d="M136 45 L142 50 L136 55" stroke="var(--clr-tut)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <!-- Step 2 -->
        <g transform="translate(150,20)">
          <circle cx="30" cy="30" r="32" fill="none" stroke="var(--clr-tut)" stroke-width="2.5"/>
          <text x="30" y="37" text-anchor="middle" font-size="22" font-weight="700" fill="var(--clr-tut)" font-family="system-ui">2</text>
          {icon2}
        </g>
        <!-- Arrow 2-3 -->
        <path d="M220 50 L270 50" stroke="var(--clr-tut)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <path d="M266 45 L272 50 L266 55" stroke="var(--clr-tut)" stroke-width="2" stroke-linecap="round" fill="none"/>
        <!-- Step 3 -->
        <g transform="translate(280,20)">
          <circle cx="30" cy="30" r="32" fill="none" stroke="var(--clr-tut)" stroke-width="2.5"/>
          <text x="30" y="37" text-anchor="middle" font-size="22" font-weight="700" fill="var(--clr-tut)" font-family="system-ui">3</text>
          {icon3}
        </g>
        <!-- Labels -->
        <text x="50" y="118" text-anchor="middle" font-size="14" fill="var(--text)" font-family="system-ui" font-weight="600">{label1}</text>
        <text x="180" y="118" text-anchor="middle" font-size="14" fill="var(--text)" font-family="system-ui" font-weight="600">{label2}</text>
        <text x="310" y="118" text-anchor="middle" font-size="14" fill="var(--text)" font-family="system-ui" font-weight="600">{label3}</text>
      </svg>
    </div>
'''

# CSS for the SVG block
TUTORIAL_CSS = '''
    .tool-tutorial-svg {
      padding: 28px 0 12px;
      text-align: center;
    }
    .tutorial-svg-head {
      margin-bottom: 16px;
    }
    .tutorial-eyebrow {
      display: inline-block;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.8px;
      text-transform: uppercase;
      color: var(--clr-tut);
      background: color-mix(in srgb, var(--clr-tut) 10%, transparent);
      padding: 4px 12px;
      border-radius: 10px;
      margin-bottom: 8px;
    }
    .tutorial-svg-head h3 {
      font-size: 18px;
      font-weight: 700;
      color: var(--text);
      margin: 0;
    }
    .tool-tutorial-svg svg text {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
    }
'''


def find_tool_path(tool):
    """Find the HTML file for a tool given its slug and category."""
    slug = tool['slug']
    # Check the url field first
    url = tool.get('url', '')
    if url:
        # Extract filename from URL path
        fname = url.rstrip('/').split('/')[-1]
        if fname.endswith('.html'):
            # Figure out the directory from the URL path
            # e.g., /pdf/pdf-merge.html -> pdf/pdf-merge.html
            parts = url.strip('/').split('/')
            if len(parts) >= 2:
                dir_name = parts[0]
                return os.path.join(TOOLS_DIR, dir_name, fname)
        return os.path.join(TOOLS_DIR, fname)
    # Fallback: look by slug
    for root, dirs, files in os.walk(TOOLS_DIR):
        for fname in files:
            if fname.endswith('.html') and slug in fname:
                # Check it's not the tools.html root page
                if fname != 'tools.html':
                    fpath = os.path.join(root, fname)
                    # Make sure the directory matches the category
                    cat_slug = tool.get('category', '')
                    # Map category to dir
                    cat_dir_map = {
                        'PDF工具': 'pdf', '图片工具': 'image', 'AI工具': 'ai',
                        '开发工具': 'dev', '文本工具': 'text', '视频工具': 'video',
                        '音频工具': 'audio', 'SEO工具': 'seo', '生活工具': 'life',
                        '金融工具': 'finance', '设计工具': 'design', 'JSON工具': 'json',
                        '二维码工具': 'qr', '综合工具': 'tools',
                    }
                    expected_dir = cat_dir_map.get(cat_slug, '')
                    rel = os.path.relpath(fpath, TOOLS_DIR)
                    if expected_dir and rel.startswith(expected_dir + '/'):
                        return fpath
    return None


def build_svg_block(tool):
    """Build the SVG block HTML for a tool page."""
    cat = tool.get('category', '')
    clr = CATEGORY_COLORS.get(cat, DEFAULT_COLOR)
    icons = CATEGORY_ICONS.get(cat, DEFAULT_ICONS)

    # Get i18n labels from the tool page
    # Default labels in Chinese
    label1 = '上传文件'
    label2 = '本地处理'
    label3 = '下载结果'
    eyebrow = '使用流程'
    title = '三步完成'

    # Try to extract from existing ZT_PAGE in the file
    file_path = find_tool_path(tool)
    if file_path and os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to find existing labels in ZT_PAGE
        # Look for step-related keys
        lang_keys = ['zh', 'en', 'ja', 'vi']
        for lk in lang_keys:
            # Search for step labels in ZT_PAGE dict
            pattern = re.compile(
                r'ZT_PAGE\s*=\s*\{[^}]*\}' +
                re.escape(lk) + r':\s*\{[^}]*\}',
                re.DOTALL
            )

    # Inject icons with current color
    icon1 = icons['upload'].format(clr=clr)
    icon2 = icons['process'].format(clr=clr)
    icon3 = icons['download'].format(clr=clr)

    svg = SVG_TEMPLATE.format(
        icon1=icon1, icon2=icon2, icon3=icon3,
        label1=label1, label2=label2, label3=label3,
        eyebrow=eyebrow, title=title,
    )
    return svg, clr, TUTORIAL_CSS


def process_file(filepath, tool):
    """Add SVG tutorial block to a tool HTML file."""
    if not os.path.exists(filepath):
        return False, f'File not found: {filepath}'

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if SVG block already exists
    if 'tool-tutorial-svg' in content:
        return False, 'Already has SVG'

    # Find insertion point: after the tool-box </div>
    # Look for the closing tag of tool-box
    tool_box_end = content.find('class="tool-box"')
    if tool_box_end == -1:
        # Fallback: look for the section with info-grid
        info_grid_pos = content.find('info-grid')
        if info_grid_pos == -1:
            # Last resort: insert before the footer
            footer_pos = content.find('<footer')
            if footer_pos == -1:
                # Second fallback: insert before </body>
                body_close = content.rfind('</body>')
                if body_close == -1:
                    return False, 'No insertion point found'
                insert_pos = body_close
            else:
                insert_pos = footer_pos
        else:
            # Find the closing div before info-grid
            insert_pos = info_grid_pos
    else:
        # Find the matching </div> for the tool-box
        # Walk backward from class="tool-box" to find the opening <div
        open_pos = content.rfind('<div', 0, tool_box_end)
        if open_pos == -1:
            # Can't find the opening div, fallback to info-grid or body close
            insert_pos = content.find('info-grid')
            if insert_pos == -1:
                insert_pos = content.rfind('</body>')
            if insert_pos == -1:
                return False, 'No insertion point found'
            # Insert before the tag
            if insert_pos > 0 and insert_pos < len(content):
                pass  # use as is
        else:
            # Count divs from the opening tag
            depth = 0
            i = open_pos
            while i < len(content):
                if content[i:i+6] == '<div ' or content[i:i+5] == '<div>':
                    depth += 1
                elif content[i:i+6] == '</div>':
                    depth -= 1
                    if depth == 0:
                        insert_pos = i + 6
                        break
                i += 1
            if depth != 0:
                insert_pos = content.find('info-grid', tool_box_end)
                if insert_pos == -1:
                    insert_pos = content.rfind('</body>')

    # Build SVG block
    svg_block, clr, css = build_svg_block(tool)

    # Get category name for eyebrow text
    cat = tool.get('category', '')
    tool_name = tool.get('name', tool.get('slug', '工具'))

    # Build SVG content with the actual color variable set
    svg_html = svg_block

    # Build insertion block: CSS + SVG
    insert_html = f'''
    <style>{css}</style>
    <style>.tool-tutorial-svg{{--clr-tut:{clr}}}</style>
    {svg_html}
    '''

    new_content = content[:insert_pos] + insert_html + content[insert_pos:]

    # Also add i18n entries for tutorial labels to ZT_PAGE if not present
    # We'll add them to each language block
    tutorial_i18n = {
        'zh': {'tutorialEyebrow': '使用流程', 'tutorialTitle': '三步完成',
               'tutorialStep1': '上传文件', 'tutorialStep2': '本地处理', 'tutorialStep3': '下载结果'},
        'en': {'tutorialEyebrow': 'HOW TO USE', 'tutorialTitle': 'Done in 3 Steps',
               'tutorialStep1': 'Upload', 'tutorialStep2': 'Process', 'tutorialStep3': 'Download'},
        'ja': {'tutorialEyebrow': '使い方', 'tutorialTitle': '3ステップで完了',
               'tutorialStep1': 'アップロード', 'tutorialStep2': '処理', 'tutorialStep3': 'ダウンロード'},
        'vi': {'tutorialEyebrow': 'CÁCH SỬ DỤNG', 'tutorialTitle': 'Hoàn thành 3 bước',
               'tutorialStep1': 'Tải lên', 'tutorialStep2': 'Xử lý', 'tutorialStep3': 'Tải xuống'},
    }

    for lang, keys in tutorial_i18n.items():
        # Find the language block in ZT_PAGE
        # Look for "  lang: {" pattern
        lang_pattern = re.compile(r'(' + re.escape(lang) + r':\s*\{)')
        m = lang_pattern.search(new_content)
        if m:
            start_pos = m.end()
            # Find the next closing } of this dict
            brace_count = 1
            j = start_pos
            while j < len(new_content) and brace_count > 0:
                if new_content[j] == '{':
                    brace_count += 1
                elif new_content[j] == '}':
                    brace_count -= 1
                j += 1
            dict_end = j - 1
            # Insert keys before the closing }
            keys_str = ',\n'.join(f"        {k}: '{v}'" for k, v in keys.items())
            new_content = new_content[:dict_end] + '\n' + keys_str + new_content[dict_end:]

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, f'SVG added (clr={clr})'


def main():
    dry_run = '--apply' not in sys.argv

    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    tools = data['tools']
    print(f'Total tools: {len(tools)}')

    stats = {'success': 0, 'skip': 0, 'error': 0}

    for tool in tools:
        filepath = find_tool_path(tool)
        if not filepath:
            print(f'[SKIP] {tool["slug"]}: file not found')
            stats['skip'] += 1
            continue

        if dry_run:
            print(f'[DRY-RUN] {tool["slug"]}: {filepath}')
            stats['success'] += 1
            continue

        try:
            ok, msg = process_file(filepath, tool)
            if ok:
                print(f'[OK] {tool["slug"]}: {msg}')
                stats['success'] += 1
            else:
                print(f'[SKIP] {tool["slug"]}: {msg}')
                stats['skip'] += 1
        except Exception as e:
            print(f'[ERROR] {tool["slug"]}: {e}')
            stats['error'] += 1

    print(f'\nSummary: {stats["success"]} added, {stats["skip"]} skipped, {stats["error"]} errors')


if __name__ == '__main__':
    main()
