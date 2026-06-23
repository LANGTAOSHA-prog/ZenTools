import sys
sys.stdout.reconfigure(encoding='utf-8')
with open('assets/js/tool-ui.min.js', 'r', encoding='utf-8') as f:
    content = f.read()
print('File length:', len(content), 'chars')
print()
print('=== Last 300 chars ===')
print(content[-300:])
print()
print('initLang() call:', 'initLang()' in content)
print('ZT.applyLanguage:', 'ZT.applyLanguage' in content)
print('langNames:', 'langNames' in content)
