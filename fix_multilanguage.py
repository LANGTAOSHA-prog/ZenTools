# 多语言修复脚本
# 批量修复所有指南页面的多语言功能

#!/usr/bin/env python3
import os
import re
import sys

def fix_page_language(filepath):
    """Fix language switching for a single page"""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if already fixed
    if 'data-i18n-page=' in content or 'applyLanguage()' in content:
        print(f"✓ {os.path.basename(filepath)} already fixed")
        return False
    
    # Replace data-i18n with data-i18n-page for page-specific translations
    content = re.sub(r'data-i18n="(\w+)"', r'data-i18n-page="\1"', content)
    
    # Add script tag before closing </script> of ZT_PAGE config
    zt_page_pattern = r'(window\.ZT_PAGE\s*=\s*\{[^}]+\};)(\s*</script>)'
    match = re.search(zt_page_pattern, content, re.DOTALL)
    
    if match:
        insert_pos = match.end(2)
        
        # Language switcher HTML
        lang_switcher = '''
        
        <!-- Language Switcher -->
        <div style="position:fixed;top:20px;right:20px;z-index:1000;background:white;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);padding:10px;">
          <select id="langSwitcher" onchange="switchLanguage(this.value)" style="padding:8px 12px;border:1px solid #e2e8f0;border-radius:6px;font-size:14px;cursor:pointer;">
            <option value="zh">中文</option>
            <option value="en">English</option>
            <option value="ja">日本語</option>
            <option value="vi">Tiếng Việt</option>
          </select>
        </div>
        
        <script>
        // Apply language on page load
        function applyPageLanguage(lang) {
          const currentLang = lang || localStorage.getItem('zentools_lang') || navigator.language.slice(0, 2) || 'zh';
          
          // Apply page-specific translations from window.ZT_PAGE
          if (window.ZT_PAGE && window.ZT_PAGE[currentLang]) {
            document.querySelectorAll('[data-i18n-page]').forEach(function(elem) {
              const key = elem.getAttribute('data-i18n-page');
              if (window.ZT_PAGE[currentLang][key]) {
                elem.textContent = window.ZT_PAGE[currentLang][key];
              }
            });
            
            // Update language selector
            const selector = document.getElementById('langSwitcher');
            if (selector) {
              selector.value = currentLang;
            }
          }
          
          // Dispatch event for TOC updates
          window.dispatchEvent(new CustomEvent('zt-langchange', { detail: { lang: currentLang } }));
        }
        
        // Switch language function
        function switchLanguage(lang) {
          localStorage.setItem('zentools_lang', lang);
          applyPageLanguage(lang);
        }
        
        // Apply on DOM ready
        document.addEventListener('DOMContentLoaded', function() {
          applyPageLanguage();
        });
        </script>'''
        
        content = content[:insert_pos] + lang_switcher + content[insert_pos:]
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Fixed {os.path.basename(filepath)}")
    return True

def main():
    guides_dir = '/workspace/guides'
    files_to_fix = []
    
    # Find all HTML files except index.html and templates
    for filename in os.listdir(guides_dir):
        if filename.endswith('.html') and not filename.startswith('index') and not filename.startswith('guides-template'):
            filepath = os.path.join(guides_dir, filename)
            files_to_fix.append(filepath)
    
    print(f"Found {len(files_to_fix)} files to fix\n")
    
    for filepath in files_to_fix:
        try:
            fix_page_language(filepath)
        except Exception as e:
            print(f"✗ Error fixing {filepath}: {e}")
    
    print("\n✅ All pages fixed!")

if __name__ == '__main__':
    main()
