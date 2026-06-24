#!/usr/bin/env python3
"""Unify old i18n pattern (translations+languageSelect+siteLanguage) to new pattern
   and also add window.pageTranslations alias for cross-page compatibility."""

import os, re

AI_DIR = '/workspace/ai'

OLD_PATTERN_FILES = [
    'ai-code-explain.html', 'ai-email.html', 'ai-interview.html',
    'ai-japanese-essay.html', 'ai-resume.html', 'ai-summary.html', 'ai-title.html'
]

def migrate_old_pattern(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Already has new pattern?
    if 'window.pageTranslations' in c:
        return False
    
    # 1. Change select ID: languageSelect -> langSelect
    c = c.replace('id="languageSelect"', 'id="langSelect"')
    c = c.replace("document.getElementById('languageSelect')", "document.getElementById('langSelect')")
    c = c.replace('document.getElementById("languageSelect")', "document.getElementById('langSelect')")
    
    # 2. Change getElementById for langSelect
    c = re.sub(r'const\s+languageSelect\s*=\s*document\.getElementById\(["\']langSelect["\']\)',
               'var langSelect = document.getElementById("langSelect")', c)
    c = re.sub(r'languageSelect\.addEventListener', 'langSelect.addEventListener', c)
    
    # 3. Change localStorage key from siteLanguage to zentools_lang
    c = c.replace('"siteLanguage"', '"zentools_lang"')
    c = c.replace("'siteLanguage'", "'zentools_lang'")
    
    # 4. Add window.pageTranslations alias after the translations definition
    # Find the closing of the translations object
    m = re.search(r'const translations=({[^;]+});', c)
    if m:
        alias = '\nwindow.pageTranslations = translations;'
        end = m.end(1) + 1  # after the closing brace + semicolon
        c = c[:end] + alias + c[end:]
    
    # 5. Update the setLanguage function to also handle meta description
    # The old setLanguage doesn't update meta description
    old_func = '''localStorage.setItem("zentools_lang",lang);
}'''
    new_func = '''var mc=document.querySelector('meta[name="description"]');if(mc&&data.metaDesc)mc.content=data.metaDesc;
 localStorage.setItem("zentools_lang",lang);
}'''
    c = c.replace(old_func, new_func)
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

# Also update the new-pattern files to add window.pageTranslations alias if missing
def add_alias_to_new(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if 'window.pageTranslations' in c or not 'pageTranslations' in c:
        return False
    
    # Check if pageTranslations already has window alias
    if 'var pageTranslations=' in c and 'window.pageTranslations' not in c:
        c = c.replace('var pageTranslations=', 'window.pageTranslations=')
    
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)
    return True

# Process old pattern files
migrated = []
for fn in OLD_PATTERN_FILES:
    fpath = os.path.join(AI_DIR, fn)
    if migrate_old_pattern(fpath):
        migrated.append(fn)

# Add window.pageTranslations alias to new-style files
aliased = []
for fn in sorted(os.listdir(AI_DIR)):
    if not fn.endswith('.html') or fn in OLD_PATTERN_FILES:
        continue
    fpath = os.path.join(AI_DIR, fn)
    if add_alias_to_new(fpath):
        aliased.append(fn)

print(f"Migrated old pattern: {len(migrated)}")
for f in migrated: print(f"  {f}")
print(f"\nAdded window alias to new pattern: {len(aliased)}")
for f in aliased: print(f"  {f}")