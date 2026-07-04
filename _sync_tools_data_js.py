#!/usr/bin/env python3
"""同步 assets/js/tools-data.js 与 data/tools-data.json"""

import json
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(SCRIPT_DIR, 'data', 'tools-data.json')
JS_PATH = os.path.join(SCRIPT_DIR, 'assets', 'js', 'tools-data.js')


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tools = data['tools']
    js = 'const toolsData = ' + json.dumps(tools, ensure_ascii=False, indent=2) + ';\n'
    with open(JS_PATH, 'w', encoding='utf-8', newline='\n') as f:
        f.write(js)
    print(f'✓ tools-data.js 已同步 ({len(tools)} 条)')


if __name__ == '__main__':
    main()