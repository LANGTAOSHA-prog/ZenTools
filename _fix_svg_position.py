#!/usr/bin/env python3
"""Fix SVG tutorial block inserted after </html> in AI tool pages."""
import os

ai_dir = '/workspace/ai'
fixed = 0

for fname in os.listdir(ai_dir):
    if not fname.endswith('.html') or fname == 'index.html':
        continue
    fpath = os.path.join(ai_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'tool-tutorial-svg' not in c:
        continue

    # Check if SVG block is after </body>
    body_pos = c.rfind('</body>')
    svg_pos = c.find('tool-tutorial-svg')
    if svg_pos <= body_pos:
        continue  # Already correctly placed

    # Find the SVG block start: whitespace + <style> before .tool-tutorial-svg
    svg_start = c.rfind('\n    <style>', 0, svg_pos)
    if svg_start == -1:
        continue

    # Find the SVG block end: after the last </div> and optional stray '>'
    # Count <div> from svg_start
    start_div = svg_start
    depth = 0
    i = start_div
    end_found = False
    while i < len(c):
        if c[i:i+5] == '<div ' or c[i:i+4] == '<div>':
            depth += 1
        elif c[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                svg_end = i + 6
                # Skip trailing whitespace and stray '>'
                while svg_end < len(c) and c[svg_end] in ' \n\r\t':
                    if c[svg_end] == '>':
                        svg_end += 1
                    else:
                        svg_end += 1
                end_found = True
                break
        i += 1
    if not end_found:
        continue

    # Extract and remove the SVG block
    svg_block = c[svg_start:svg_end]
    c = c[:svg_start] + c[svg_end:]

    # Insert before </body>
    body_pos = c.rfind('</body>')
    if body_pos != -1:
        c = c[:body_pos] + '\n    ' + svg_block + '\n' + c[body_pos:]
    else:
        html_pos = c.rfind('</html')
        if html_pos != -1:
            c = c[:html_pos] + '\n    ' + svg_block + '\n' + c[html_pos:]
        else:
            print(f'  WARN: no insertion point for {fname}')
            continue

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f'Fixed: {fname}')
    fixed += 1

print(f'\nTotal fixed: {fixed}')
