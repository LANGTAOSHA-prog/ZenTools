import sys, json, os
sys.stdout.reconfigure(encoding='utf-8')

d = json.load(open('data/tools-data.json', 'r', encoding='utf-8'))
tools = d.get('tools', [])

# Check URL paths exist
missing_files = []
for t in tools:
    url = t.get('url', '')
    if not url or url == '#':
        continue
    # Convert URL to relative file path
    filepath = url.lstrip('/')
    if not os.path.exists(filepath):
        missing_files.append((t.get('name','?'), url))

print(f"Total tools: {len(tools)}")
print(f"Missing files: {len(missing_files)}")
if missing_files:
    print("\nFirst 20 missing:")
    for name, url in missing_files[:20]:
        print(f"  {name}: {url}")
else:
    print("  All URLs point to existing files ✅")

# Check category mapping
cats_from_data = set(t.get('category','') for t in tools)
cats_from_list = set(d.get('categories', []))
print(f"\nCategories in tools: {sorted(cats_from_data)}")
print(f"Categories in list: {sorted(cats_from_list)}")
unmapped = cats_from_data - cats_from_list
if unmapped:
    print(f"Categories used by tools but NOT in categories list: {unmapped}")

# Check icon assignment
no_icon = [t['name'] for t in tools if not t.get('icon')]
if no_icon:
    print(f"\nTools missing icon ({len(no_icon)}): {no_icon[:5]}...")
