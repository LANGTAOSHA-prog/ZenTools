import os, glob, re

root = r"D:\Users\taojiang\Documents\GitHub\ZenTools"

# Get the related tools script from hash-generator.html (which already has it)
src_path = os.path.join(root, "dev", "hash-generator.html")
with open(src_path, "r", encoding="utf-8") as f:
    src = f.read()

m = re.search(r'<script>\n// Related tools.*?</script>\n', src, re.DOTALL)
if not m:
    print("ERROR: could not extract script from hash-generator.html")
    exit(1)

related_script = m.group(0)

# Fix cameratest.html
fp = os.path.join(root, "dev", "cameratest.html")
with open(fp, "r", encoding="utf-8") as f:
    content = f.read()

if 'tools-data.json' not in content:
    content = content.replace(
        '</script>',
        '</script>\n' + related_script,
        1  # only replace the LAST occurrence (after tool functions, not ZT_PAGE)
    )
    # Actually, we need to replace after the LAST </script> before bookmark-float
    # Let's do it differently
    with open(fp, "r", encoding="utf-8") as f:
        lines = f.readlines()
    
    with open(fp, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line)
            if 'getMsg(k){const l' in line:
                f.write('</script>\n')
                f.write(related_script)
                break
            elif 'function getMsg' in line:
                f.write('</script>\n')
                f.write(related_script)
                break
    
    print("Fixed cameratest.html")
else:
    print("cameratest.html already has related tools")

# Now check all dev files
print("\nVerification:")
for fp in sorted(glob.glob(os.path.join(root, "dev", "*.html"))):
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    status = "✅" if 'tools-data.json' in content else "❌"
    print(f"{status} {os.path.basename(fp)}")
