import sys, json
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('data/tools-data.json', 'r', encoding='utf-8'))
print(f"Categories: {len(d.get('categories',[]))}")
print(f"Tools: {len(d.get('tools',[]))}")

cats = set()
urls = set()
bad = []
for t in d.get('tools', []):
    cats.add(t.get('category'))
    url = t.get('url','')
    if url in urls:
        bad.append(f"DUPE url: {url}")
    urls.add(url)
    if not url or url == '#':
        bad.append(f"MISSING url: {t.get('name','?')}")

print(f"Categories: {sorted(cats)}")
print()
print('Issues:')
for b in bad[:20]:
    print(f"  {b}")
if not bad:
    print("  None found")
