#!/usr/bin/env python3
"""从 GitHub push 事件的 commit 消息中提取 cl: 标记，写入 /tmp/cl_lines.txt。

用法：在 deploy.yml 的 changelog 步骤里调用，读取环境变量 GITHUB_EVENT_PATH
指向的 push 事件 JSON，遍历 commits 收集以 `cl:` 开头的行。
"""
import json
import os
import re

EVENT = os.environ.get('GITHUB_EVENT_PATH', '')
out = []
if EVENT and os.path.exists(EVENT):
    with open(EVENT, encoding='utf-8') as f:
        data = json.load(f)
    for c in data.get('commits', []):
        msg = c.get('message', '')
        for line in msg.splitlines():
            if re.match(r'^\s*cl:', line, re.IGNORECASE):
                out.append(line.strip())

with open('/tmp/cl_lines.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(out))

print('cl 标记:', out)
