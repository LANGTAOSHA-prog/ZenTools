#!/usr/bin/env python3
"""修复 tools/* 页面 ZT_PAGE 语句语法损坏：
1. 去掉无返回值的 IIFE (function(){var pt=...;})() —— 它是语法错误的根源
2. 类型 B：修正 zh 块后的多余 }},"en" 括号
3. 类型 A：把 h1_title/stat_*/footer_copy 六个键合并回各语言块内
每修一个文件都用 node --check 验证，失败则跳过并报告。
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TOOLS_DIR = os.path.join(ROOT, 'tools')

IIFE_RE = re.compile(r'\(function\(\)\{var pt=window\.pageTranslations=window\.ZT_PAGE;\}\)\(\)')
COMMENT_RE = re.compile(r'// Compatibility: map pageTranslations keys\n?')
DOUBLE_EN_RE = re.compile(r'\}\},"en":\{')
H1_GROUP_RE = re.compile(r'\},\s*\n\s*("h1_title":)')
H1_GROUP_SAME_LINE_RE = re.compile(r'\},\s*("h1_title":)')
CATNAME_DECL = 'var catName = "";'


def node_ok(code: str) -> bool:
    tmp = os.path.join(ROOT, '_tmp_fix_check.js')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(code)
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True)
    return r.returncode == 0


def fix_file(path: str) -> str:
    """返回 'ok' / 'skip(无标记)' / 'fail: <原因>'"""
    text = open(path, encoding='utf-8', errors='replace').read()
    start = text.find('window.pageTranslations')
    if start == -1:
        return 'skip(无 window.pageTranslations)'
    end = text.find('</script>', start)
    if end == -1:
        return 'fail: 找不到 </script> 边界'
    stmt = text[start:end]

    new_stmt = IIFE_RE.sub('', stmt)
    new_stmt = COMMENT_RE.sub('', new_stmt)
    new_stmt = re.sub(r'\n{3,}', '\n\n', new_stmt)

    if '"h1_title"' in new_stmt:
        # 类型 A：先把 }, 换行 "h1_title": 的多余 } 去掉
        new_stmt = H1_GROUP_RE.sub(r',\n    \1', new_stmt)
        new_stmt = H1_GROUP_SAME_LINE_RE.sub(r', \1', new_stmt)
    if '}},"en":{' in new_stmt:
        new_stmt = DOUBLE_EN_RE.sub('},"en":{', new_stmt, count=1)

    # 反转义 \' -> ' （仅存在于损坏的 zh 块，如 (catName||\'\')+\'工具'）
    if "\\'" in new_stmt:
        new_stmt = new_stmt.replace("\\'", "'")

    # 运行时安全：语句内引用未声明的 catName 会抛 ReferenceError
    if re.search(r'\bcatName\b', new_stmt) and 'var catName' not in new_stmt:
        new_stmt = CATNAME_DECL + '\n' + new_stmt

    if not node_ok(new_stmt):
        return 'fail: node --check 仍报错'

    # 写回：替换原始段（保留 </script>）
    new_text = text[:start] + new_stmt + text[end:]
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(new_text)
    return 'ok'


def main():
    files = sorted(f for f in os.listdir(TOOLS_DIR) if f.endswith('.html'))
    ok, fail = [], []
    for fn in files:
        result = fix_file(os.path.join(TOOLS_DIR, fn))
        if result == 'ok':
            ok.append(fn)
        else:
            fail.append((fn, result))
    print(f'✓ 修复成功 {len(ok)} 个:')
    for fn in ok:
        print(f'  {fn}')
    if fail:
        print(f'\n✗ 失败 {len(fail)} 个:')
        for fn, why in fail:
            print(f'  {fn}: {why}')
        sys.exit(1)


if __name__ == '__main__':
    main()
