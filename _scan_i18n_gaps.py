#!/usr/bin/env python3
"""扫描多语种未覆盖内容 v2：兼容 ZT_PAGE/pageTranslations/translations/IIFE 写法，检测真实语言缺口与编码损坏。"""
import os
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
REQUIRED = ('zh', 'en', 'ja', 'vi')
SKIP_DIRS = {'.git', '.github', '.atomcode', '.agent', '.claude', '.vscode', '__pycache__',
             'assets', 'data', 'pdf_tools', 'chrome-extension'}

# 顶层语言键匹配：zh: 或 "zh": 或 'zh': 后面跟 {
LANG_DEF = re.compile(r"""["']?(zh|en|ja|vi)["']?\s*:\s*\{""", re.IGNORECASE)


def find_matching_brace(text, start):
    depth = 0
    for idx in range(start, len(text)):
        c = text[idx]
        if c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                return idx
    return -1


def extract_langs_from_map(text):
    """从翻译对象内文本中找出 zh/en/ja/vi 顶层键。"""
    return {m.group(1).lower() for m in LANG_DEF.finditer(text)}


def find_translation_region(text):
    """返回翻译对象的内部文本（已去除大括号），找不到返回 None。"""
    patterns = [
        re.compile(r'window\.ZT_PAGE\s*=\s*\{', re.IGNORECASE),
        re.compile(r'window\.pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'(?:var|const|let)\s+pageTranslations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'(?:var|const|let)\s+translations\s*=\s*\{', re.IGNORECASE),
        re.compile(r'(?:var|const|let)\s+pageTranslations\s*=\s*window\.ZT_PAGE\s*=', re.IGNORECASE),
    ]
    for p in patterns:
        m = p.search(text)
        if not m:
            continue
        ob = text.find('{', m.start())
        if ob == -1:
            continue
        cb = find_matching_brace(text, ob)
        if cb != -1:
            return text[ob + 1:cb], m.group(0)
    # IIFE 写法: window.pageTranslations=window.ZT_PAGE=\n// comment\n(function(){...})(){"zh":{...},"en":{...}}
    m = re.search(r'window\.pageTranslations\s*=\s*window\.ZT_PAGE\s*=', text, re.IGNORECASE)
    if m:
        after = text[m.end():]
        # 找到 IIFE 结束标记 })() 之后的对象字面量起点
        for iife_end in re.finditer(r'\)\s*\(\s*\)', after):
            tail = after[iife_end.end():]
            brace = tail.find('{')
            if brace != -1:
                cb = find_matching_brace(tail, brace)
                if cb != -1:
                    inner = tail[brace + 1:cb]
                    # 确认里面真的含语言键，避免误取
                    if LANG_DEF.search(inner):
                        return inner, 'IIFE pattern'
        # 兜底：直接找第一个含语言键的大括号块
        for brace in re.finditer(r'\{', after):
            cb = find_matching_brace(after, brace.start())
            if cb != -1:
                inner = after[brace.start() + 1:cb]
                if LANG_DEF.search(inner):
                    return inner, 'IIFE pattern (fallback)'
    # ZT_PAGE 别名: window.ZT_PAGE = someVar;
    m = re.search(r'window\.ZT_PAGE\s*=\s*([A-Za-z_$]\w*)\s*;', text, re.IGNORECASE)
    if m:
        d = re.search(r'(?:var|const|let)\s+' + m.group(1) + r'\s*=\s*\{', text)
        if d:
            ob = text.find('{', d.start())
            cb = find_matching_brace(text, ob)
            if cb != -1:
                return text[ob + 1:cb], 'alias'
    return None, None


def rel(path):
    return path.replace(ROOT + os.sep, '').replace(ROOT + '/', '')


def main():
    missing_ja_vi = []
    missing_more = []
    no_translations = []
    parse_fail = []
    encoding_bad = []
    ok = 0

    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            if not fn.lower().endswith('.html'):
                continue
            full = os.path.join(dirpath, fn)
            try:
                raw = open(full, 'rb').read()
            except OSError:
                continue
            # 编码损坏检测：有效 UTF-8 比例
            try:
                text = raw.decode('utf-8')
                utf8_ok = True
            except UnicodeDecodeError:
                utf8_ok = False
                try:
                    text = raw.decode('gbk', errors='replace')
                except Exception:
                    text = raw.decode('utf-8', errors='replace')
            if '\ufffd' in text:
                encoding_bad.append((full, '包含 U+FFFD 替换符' if utf8_ok else '非 UTF-8 编码'))

            has_marker = ('window.ZT_PAGE' in text or 'pageTranslations' in text
                          or re.search(r'(?:var|const|let)\s+translations\s*=', text))
            if not has_marker:
                no_translations.append(full)
                continue

            region, kind = find_translation_region(text)
            if region is None:
                parse_fail.append((full, kind))
                continue
            found = extract_langs_from_map(region)
            missing = [l for l in REQUIRED if l not in found]
            if not missing:
                ok += 1
            elif missing == ['ja', 'vi']:
                missing_ja_vi.append(full)
            else:
                missing_more.append((full, missing))

    print(f'✓ 完整四语: {ok} 个页面')
    print(f'\n【缺 ja+vi（仅中英）】{len(missing_ja_vi)} 个:')
    for p in sorted(missing_ja_vi):
        print('  ' + rel(p))
    print(f'\n【缺更多语言】{len(missing_more)} 个:')
    for p, m in sorted(missing_more):
        print(f'  {rel(p)}: 缺 {m}')
    print(f'\n【翻译对象无法解析】{len(parse_fail)} 个:')
    for p, k in sorted(parse_fail):
        print(f'  {rel(p)} ({k})')
    print(f'\n【完全没有翻译对象】{len(no_translations)} 个:')
    for p in sorted(no_translations):
        print('  ' + rel(p))
    print(f'\n【编码损坏/非UTF-8】{len(encoding_bad)} 个:')
    for p, note in sorted(encoding_bad):
        print(f'  {rel(p)} ({note})')


if __name__ == '__main__':
    main()
