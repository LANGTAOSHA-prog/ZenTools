import json
import os

filepath = r'D:\Users\taojiang\Documents\GitHub\ZenTools\data\tools-data.json'
with open(filepath, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f'Current tools count: {len(data["tools"])}')
last = data['tools'][-1]
print(f'Last tool name: {last["name"]}')
print(f'Last slug: {last["slug"]}')
print(f'Last keywords: {last["keywords"]}')
