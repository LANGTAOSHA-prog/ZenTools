#!/usr/bin/env python3
"""验证 tools/* 页面 ZT_PAGE 语句全部通过 node 校验。"""
import os
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))


def strip_strings(s):
    out, i, n, in_str, quote = [], 0, len(s), False, None
    while i < n:
        c = s[i]
        if in_str:
            if c == '\\':
                i += 2
                continue
            if c == quote:
                in_str = False
            i += 1
            continue
        if c in "\"'":
            in_str, quote = True, c
            i += 1
            continue
        out.append(c)
        i += 1
    return ''.join(out)


def node_ok(code):
    tmp = os.path.join(ROOT, '_tmp_verify.js')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(code)
    return subprocess.run(['node', '--check', tmp], capture_output=True, text=True).returncode == 0


def main():
    bad, ok, skipped = 0, 0, 0
    for fn in sorted(os.listdir(os.path.join(ROOT, 'tools'))):
        if not fn.endswith('.html'):
            continue
        text = open(os.path.join(ROOT, 'tools', fn), encoding='utf-8').read()
        start = text.find('window.pageTranslations')
        if start == -1:
            skipped += 1
            continue
        end = text.find('</script>', start)
        stmt = text[start:end]
        stripped = strip_strings(stmt)
        balanced = stripped.count('{') == stripped.count('}')
        valid = node_ok(stmt)
        if balanced and valid:
            ok += 1
        else:
            bad += 1
            print(f'  仍异常: {fn} 括号{stripped.count("{")}/{stripped.count("}")} node={valid}')
    print(f'ZT_PAGE 语句校验: {ok} 通过, {bad} 异常, {skipped} 无标记')
    return 1 if bad else 0


if __name__ == '__main__':
    raise SystemExit(main())
