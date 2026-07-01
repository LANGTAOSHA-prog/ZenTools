import json
import os

filepath = os.path.join(os.path.dirname(__file__) or '.', 'data', 'tools-data.json')
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Current tools count: {len(data["tools"])}')
last = data['tools'][-1]
print(f'Last tool name: {last["name"]}')
print(f'Last slug: {last["slug"]}')
print(f'Last keywords: {last["keywords"]}')
print(f'JSON valid: OK')