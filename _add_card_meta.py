#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 tools-data.json 中每个工具补充 ai.batch（批量支持）与 ai.export（导出格式）元数据，
并同步重新生成 assets/js/tools-data.js（const toolsData = [...]）。
幂等：重复运行不会破坏已有字段，仅补齐 batch/export。

用法：
    python3 _add_card_meta.py
"""
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(ROOT, 'data', 'tools-data.json')
JS_PATH = os.path.join(ROOT, 'assets', 'js', 'tools-data.js')

# ---------- 启发式：批量支持 ----------
BATCH_HINTS = ['批量', '多文件', '多个文件', '多张', '一批', '一组', '一次处理', '同时处理',
                '合并', '拆分', '多页', '多条', 'bulk', 'batch', 'multiple', 'gallery']
# 已知明确支持批量的工具 slug（启发式漏网时兜底）
BATCH_OVERRIDE = {
    'pdf-merge', 'pdf-split', 'pdf-compress', 'image-compressor', 'image-resize',
    'image-watermark', 'image-converter', 'qr-batch', 'json-formatter', 'text-diff',
    'word-counter', 'image-cropper', 'image-rotate', 'image-flip', 'image-border',
    'pdf-page-rotate', 'pdf-extract-pages', 'pdf-delete-pages', 'jpg-to-pdf',
    'png-to-pdf', 'image-to-pdf', 'pdf-to-image', 'merge-images',
}

# ---------- 启发式：导出格式 ----------
FORMAT_TOKENS = ['PDF', 'Word', 'Excel', 'PPT', 'PNG', 'JPG', 'JPEG', 'GIF', 'MP4', 'MOV',
                  'MP3', 'WAV', 'TXT', 'HTML', 'SVG', 'CSV', 'ZIP', 'WebP', 'BMP', 'TIFF',
                  'EPUB', 'Markdown', 'JSON', 'XML', 'ICO', 'AVIF']
EXPORT_TRIGGER = ['转换', '转', '导出', '输出', '生成', '下载', '保存', 'convert', 'export', 'to ', '->']

# 已知转换/产出类分类（这些分类的工具通常可导出某种格式）
EXPORT_CATS = {'PDF工具', '图片工具', '视频工具', '音频工具', '文本工具', '开发工具', '设计工具', '办公工具'}


def compute_batch(t):
    if t.get('slug') in BATCH_OVERRIDE:
        return True
    hay = ' '.join([
        t.get('name', ''), t.get('keywords', ''), t.get('description', ''),
        t.get('name__en', ''), t.get('description__en', '')
    ]).lower()
    for h in BATCH_HINTS:
        if h.lower() in hay:
            return True
    return False


def compute_export(t):
    hay = ' '.join([
        t.get('name', ''), t.get('keywords', ''), t.get('description', '')
    ])
    cat = t.get('category', '')
    is_convert = any(tr in hay for tr in EXPORT_TRIGGER) or cat in EXPORT_CATS
    if not is_convert:
        return []
    found = []
    for tok in FORMAT_TOKENS:
        if tok.lower() in hay.lower():
            found.append(tok)
    # 去重保序
    seen = set()
    uniq = []
    for f in found:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    if not uniq:
        # 是转换类但没有识别到具体格式：给一个通用标签
        return ['多种格式']
    return uniq[:4]


def main():
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    tools = data['tools']
    n_batch = 0
    n_export = 0
    for t in tools:
        ai = t.setdefault('ai', {})
        if 'batch' not in ai:
            ai['batch'] = compute_batch(t)
        if 'export' not in ai:
            ai['export'] = compute_export(t)
        if ai.get('batch') is True:
            n_batch += 1
        if ai.get('export'):
            n_export += 1

    with open(JSON_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')

    # 同步生成 tools-data.js
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write('const toolsData = ')
        json.dump(tools, f, ensure_ascii=False, indent=2)
        f.write(';\n')

    print('总工具数:', len(tools))
    print('批量支持 (batch=true):', n_batch)
    print('有导出格式 (export 非空):', n_export)
    print('已写入:', JSON_PATH)
    print('已同步:', JS_PATH)


if __name__ == '__main__':
    main()
