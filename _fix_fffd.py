#!/usr/bin/env python3
"""D 类修复：把 HEAD 中每个 U+FFFD 从 git 干净版本恢复为正确字符。

源版本：
- 7 个文件用 d87ba1f4（干净 UTF-8，内容接近 HEAD）
- 12 个 pdf 别名文件用 52db1378（干净 UTF-8）

只替换 U+FFFD 字符，其余内容一律不动（保留 E-E-A-T、教程区块等合法改动）。
"""
import os
import re
import subprocess
import sys
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
FFFD = '\ufffd'

# 文件 -> (git 源版本)
FILES = {
    'articles/my-first-pdf-tool.html': 'd87ba1f4',
    'life/cny-jpy.html': 'd87ba1f4',
    'pdf/compress.html': 'd87ba1f4',
    'pdf/merge.html': 'd87ba1f4',
    'pdf/pdf-tools.html': 'd87ba1f4',
    'pdf/split.html': 'd87ba1f4',
    'tools/worldtime.html': 'd87ba1f4',
}

# 别名文件 -> 对应 pdf-xxx.html（内容错误的「图片转PDF」副本，用主文件恢复）
ALIAS_COPY = {
    'pdf/batch.html': 'pdf/pdf-batch.html',
    'pdf/decrypt.html': 'pdf/pdf-decrypt.html',
    'pdf/delete-pages.html': 'pdf/pdf-delete-pages.html',
    'pdf/encrypt.html': 'pdf/pdf-encrypt.html',
    'pdf/extract-pages.html': 'pdf/pdf-extract-pages.html',
    'pdf/metadata.html': 'pdf/pdf-metadata.html',
    'pdf/ocr.html': 'pdf/pdf-ocr.html',
    'pdf/remove-watermark.html': 'pdf/pdf-remove-watermark.html',
    'pdf/rotate.html': 'pdf/pdf-rotate.html',
    'pdf/sign.html': 'pdf/pdf-sign.html',
    'pdf/sort.html': 'pdf/pdf-sort.html',
    'pdf/watermark.html': 'pdf/pdf-watermark.html',
}


def git_show_bytes(rev, path):
    r = subprocess.run(['git', 'show', f'{rev}:{path}'], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout


def decode_clean(raw):
    for enc in ('utf-8', 'utf-16-le', 'utf-16', 'gb18030'):
        try:
            t = raw.decode(enc)
            if t.count('\x00') < len(t) * 0.1:
                return t, enc
        except Exception:
            continue
    return raw.decode('utf-8', errors='replace'), 'utf-8-replace'


def repair_file(path, rev):
    git_path = os.path.relpath(path, ROOT).replace('\\', '/')
    clean_raw = git_show_bytes(rev, git_path)
    if clean_raw is None:
        return 'fail: 源版本不存在'
    clean, _ = decode_clean(clean_raw)
    if FFFD in clean:
        return 'fail: 源版本自身含 U+FFFD'
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        head = f.read()
    if FFFD not in head:
        return 'skip: 无 U+FFFD'

    # 归一化（越南语 NFC/NFD 差异）后匹配
    clean_norm = unicodedata.normalize('NFC', clean)
    head_norm = unicodedata.normalize('NFC', head)

    out = list(head)
    replaced = 0
    ctx_len = 30
    positions = [m.start() for m in re.finditer(FFFD, head_norm)]
    for pos in reversed(positions):
        # 上下文：取 pos 之前、最近一个 U+FFFD 之后（跳过 '?'）的干净片段
        prev_fffd = max([p for p in positions if p < pos], default=-1)
        # 若前一个 U+FFFD 后紧跟 '?'，从 '?' 之后开始取
        skip = 0
        if prev_fffd >= 0 and prev_fffd + 1 < len(head_norm) and head_norm[prev_fffd + 1] == '?':
            skip = 2
        start = max(prev_fffd + skip, pos - ctx_len, 0)
        before = head_norm[start:pos]
        ok = False
        for cl in (ctx_len, 20, 12, 6):
            b = before[-cl:]
            idx = clean_norm.rfind(b)
            if idx != -1 and idx + len(b) < len(clean_norm):
                correct = clean_norm[idx + len(b)]
                if correct not in (FFFD, '\r', '\n'):
                    # 映射回原始（非归一化）字符
                    out[pos] = correct
                    if pos + 1 < len(head) and head[pos + 1] == '?':
                        out[pos + 1] = ''
                    replaced += 1
                    ok = True
                    break
        if not ok:
            print(f'  ⚠ 未修复 {path} @{pos}: ...{head[max(0,pos-12):pos+4]!r}...')

    repaired = ''.join(out)
    if FFFD in repaired:
        return f'fail: 仍有 {repaired.count(FFFD)} 个 U+FFFD 未修复'
    with open(path, 'w', encoding='utf-8', newline='') as f:
        f.write(repaired)
    return f'ok: 修复 {replaced} 处'


def main():
    ok, fail = 0, []

    # 1) 7 个 d87ba1f4 源文件：字符级修复 U+FFFD
    for f, rev in FILES.items():
        full = os.path.join(ROOT, f)
        if not os.path.exists(full):
            fail.append((f, '文件不存在'))
            continue
        result = repair_file(full, rev)
        print(f'  {f}: {result}')
        if result.startswith('ok') or result.startswith('skip'):
            ok += 1
        else:
            fail.append((f, result))

    # 2) 12 个 pdf 别名文件：内容为错误的「图片转PDF」副本 + U+FFFD，用 pdf-xxx.html 主文件恢复
    for alias, orig in ALIAS_COPY.items():
        alias_full = os.path.join(ROOT, alias)
        orig_full = os.path.join(ROOT, orig)
        if not os.path.exists(orig_full):
            fail.append((alias, f'主文件 {orig} 不存在'))
            continue
        content = open(orig_full, 'rb').read()
        with open(alias_full, 'wb') as f:
            f.write(content)
        print(f'  {alias}: ok: 已从 {orig} 恢复 ({len(content)}B)')
        ok += 1

    print(f'\n完成: {ok} 成功, {len(fail)} 失败')
    for f, why in fail:
        print(f'  ✗ {f}: {why}')
    return 1 if fail else 0


if __name__ == '__main__':
    sys.exit(main())
