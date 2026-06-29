import re
f = open(r'D:\Users\taojiang\Documents\GitHub\ZenTools\tutorials\index.html', 'r', encoding='utf-8')
lines = f.readlines()
f.close()

for i, line in enumerate(lines):
    if "claude-ai" in line and "cat:'tools'" in line:
        sys.stdout.buffer.write(f"Line {i+1}: ".encode('utf-8'))
        sys.stdout.buffer.write((line.rstrip()[:300] + "\n").encode('utf-8'))
        # Check for unescaped single quotes in single-quoted strings
        # Find all ' positions
        positions = [j for j, c in enumerate(line) if c == "'"]
        for k in range(0, len(positions)-1, 2):
            if k+1 < len(positions):
                inner = line[positions[k]+1:positions[k+1]]
                if "'" in inner:
                    sys.stdout.buffer.write(f"  -> Unescaped quote in segment: ...{inner[:80]}...\n".encode('utf-8'))
