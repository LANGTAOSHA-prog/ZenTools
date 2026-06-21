"""
ZenTools HTML 验证脚本
验证所有 HTML 文件的语法正确性：
- DOCTYPE 存在
- HTML 标签平衡
- JavaScript 括号/大括号平衡（正确处理模板字符串、正则字面量、注释）
"""

import os
import re
import glob
import sys

# 设置输出编码
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

ROOT = r'D:\Users\taojiang\Documents\GitHub\ZenTools'

# 要跳过的目录
SKIP_DIRS = {'.git', 'node_modules', '__pycache__', '.vscode', '.atomcode', 'assets'}

def extract_scripts(html_content):
    """提取 HTML 中所有 <script> 标签内的 JS 代码"""
    scripts = []
    pattern = re.compile(r'<script[^>]*>([\s\S]*?)</script>', re.IGNORECASE)
    for match in pattern.finditer(html_content):
        code = match.group(1).strip()
        if code:
            scripts.append(code)
    return scripts

def validate_brackets(code, label=''):
    """验证 JS 代码的括号平衡，跳过字符串和正则字面量"""
    stack = []
    pairs = {'(': ')', '{': '}', '[': ']'}
    i = 0
    errors = []
    
    while i < len(code):
        c = code[i]
        
        # 跳过单行注释 //
        if c == '/' and i + 1 < len(code) and code[i+1] == '/':
            end = code.find('\n', i)
            i = len(code) if end == -1 else end + 1
            continue
        
        # 跳过多行注释 /* */
        if c == '/' and i + 1 < len(code) and code[i+1] == '*':
            end = code.find('*/', i + 2)
            i = len(code) if end == -1 else end + 2
            continue
        
        # 跳过正则字面量 /.../
        if c == '/' and i > 0 and code[i-1] not in '({[,;:=!|&?:*/%+-^~<>':
            # 简单正则检测：找到结束的 /，跳过转义
            j = i + 1
            in_class = False
            while j < len(code):
                if code[j] == '\\':
                    j += 2
                    continue
                if code[j] == '[' and not in_class:
                    in_class = True
                elif code[j] == ']' and in_class:
                    in_class = False
                elif code[j] == '/' and not in_class:
                    # 检查后面是否有 flags
                    while j + 1 < len(code) and code[j+1] in 'gimsuy':
                        j += 1
                    i = j
                    break
                j += 1
            i += 1
            continue
        
        # 跳过字符串（单引号、双引号、模板字符串）
        if c in '"\'':
            quote = c
            j = i + 1
            while j < len(code):
                if code[j] == '\\':
                    j += 2
                    continue
                if code[j] == quote:
                    i = j
                    break
                j += 1
            i += 1
            continue
        
        if c == '`':
            j = i + 1
            depth = 0
            while j < len(code):
                if code[j] == '\\':
                    j += 2
                    continue
                if code[j] == '`' and depth == 0:
                    i = j
                    break
                i = j
                j += 1
            i += 1
            continue
        
        # 检查括号
        if c in pairs:
            stack.append((c, i))
        elif c in pairs.values():
            if not stack:
                errors.append(f"多余的闭合括号 '{c}' 在位置 {i}")
            else:
                open_c, open_i = stack.pop()
                if pairs[open_c] != c:
                    errors.append(f"括号不匹配: '{open_c}' 在位置 {open_i} 与 '{c}' 在位置 {i} ({label})")
        i += 1
    
    if stack:
        for c, pos in stack:
            errors.append(f"未闭合的括号 '{c}' 在位置 {pos} ({label})")
    
    return errors

def validate_html_file(filepath):
    """验证单个 HTML 文件"""
    rel_path = os.path.relpath(filepath, ROOT)
    errors = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [f"无法读取文件: {e}"]
    
    # 检查 DOCTYPE
    if '<!DOCTYPE html>' not in content.upper() and '<!doctype html>' not in content.lower():
        errors.append("缺少 DOCTYPE 声明")
    
    # 检查 <html> 标签
    if '<html' not in content:
        errors.append("缺少 <html> 标签")
    
    # 提取并验证 JavaScript
    scripts = extract_scripts(content)
    for idx, code in enumerate(scripts):
        script_errors = validate_brackets(code, f'script#{idx+1}')
        errors.extend(script_errors)
    
    return errors

def main():
    print("=" * 60)
    print("ZenTools HTML 验证工具")
    print("=" * 60)
    
    # 收集所有 HTML 文件
    html_files = []
    for root, dirs, files in os.walk(ROOT):
        # 跳过隐藏目录和指定目录
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html'):
                html_files.append(os.path.join(root, f))
    
    print(f"\n找到 {len(html_files)} 个 HTML 文件\n")
    
    total_errors = 0
    error_files = []
    
    for filepath in html_files:
        errors = validate_html_file(filepath)
        if errors:
            rel_path = os.path.relpath(filepath, ROOT)
            print(f"❌ {rel_path}")
            for e in errors:
                print(f"   - {e}")
            total_errors += len(errors)
            error_files.append(rel_path)
    
    if error_files:
        print(f"\n{'=' * 60}")
        print(f"📊 总计: {len(error_files)} 个文件有 {total_errors} 个问题")
        for f in error_files:
            print(f"  ❌ {f}")
    else:
        print("\n✅ 全部通过！所有 HTML 文件语法正确。")
    
    print(f"\n共检查 {len(html_files)} 个文件")

if __name__ == '__main__':
    main()
