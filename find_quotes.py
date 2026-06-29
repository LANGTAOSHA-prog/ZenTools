import re, os

os.chdir(r'D:\Users\taojiang\Documents\GitHub\ZenTools')

with open('tutorials/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all slug entries and check if they have unescaped single quotes in string values
# Look for patterns like: 'text with ' inside string value
# Find lines with unescaped single quotes that could break the JS string

problem_pattern = re.compile(r"(?:titleEn|titleJa|titleVi|sumEn|sumJa|sumVi|tagsEn|tagsJa|tagsVi):'([^']*'[^',}\]]*'[^']*)'")
matches = problem_pattern.findall(content)
print(f"No matches - check complete" if not matches else f"Found {len(matches)} potential issues:")

# Look for unescaped single quotes in single-quoted JS string values
lines = content.split('\n')
import sys
for i, line in enumerate(lines):
    stripped = line.strip()
    if not stripped:
        continue
    # Find all single-quote positions
    quotes = [m.start() for m in re.finditer(r"'", stripped)]
    # Look for ':value' patterns where a ' appears inside
    for j in range(len(quotes)-1):
        start = quotes[j]
        end = quotes[j+1]
        segment = stripped[start:end+1]
        # Check if text before first quote contains ':'
        prefix = stripped[max(0,start-30):start]
        if ':' in prefix:
            inner = segment[1:-1]
            if "'" in inner:
                try:
                    print(f"Line {i+1}: {stripped[:150]}")
                except:
                    print(f"Line {i+1}: [contains non-ASCII chars]")
                break
