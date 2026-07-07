# 设计文档：首页更新目录自动同步

## 架构概述

在现有 Python 脚本（`_add_tool.py`、`_add_tutorial.py`、`_add_guide.py`）的执行流程末尾，增加对 `data/site-info.json` 的自动更新调用。同时提供一个独立的 `_sync_changelog.py` 脚本用于手动修复/重建 changelog 数据。

## 数据流

```
_add_tool.py  ──→  更新 tools-data.json  ──→  更新 site-info.json (changelog)
_add_tutorial.py ─→  生成 HTML              ──→  更新 site-info.json (changelog)
_add_guide.py  ──→  生成 HTML              ──→  更新 site-info.json (changelog)

_sync_changelog.py ──→  扫描 tools-data.json + HTML 文件  ──→  重建 site-info.json
```

## 组件设计

### 1. 新增模块：`_changelog_utils.py`

提取 changelog 操作公共逻辑为独立模块，供所有脚本复用。

```python
# changelog 操作函数
def load_site_info() -> dict                          # 读取 site-info.json
def save_site_info(data: dict) -> None                # 写入 site-info.json
def append_changelog_item(entries: list[dict]) -> None # 追加变更条目（当日聚合）
def build_tool_entry(name, cat, desc, slug, lang) -> dict  # 构建单语言变更项
def build_tutorial_entry(title, cat, slug, lang) -> dict
def build_guide_entry(title, type, slug, lang) -> dict
def sync_tool_count(data: dict) -> None               # 同步 toolCount
def sync_last_updated(data: dict) -> None              # 同步 lastUpdated
```

### 2. 修改 `_add_tool.py`

在 `update_tools_data_json()` 成功后，调用 changelog 更新：

```python
from _changelog_utils import append_changelog_item, build_tool_entry

# 在 main() 中 update_tools_data_json() 之后：
if not args.no_json:
    ...
    if update_tools_data_json(entry):
        sync_tools_data_js()
        # 新增：更新 changelog
        append_changelog_item([build_tool_entry(...)])  # REQ-1
```

### 3. 修改 `_add_tutorial.py`

在生成 HTML 文件后，追加 changelog 更新：

```python
from _changelog_utils import append_changelog_item, build_tutorial_entry

# 在 main() 中 write HTML 之后：
print(f'✓ 教程页面已生成: {out_path}')
append_changelog_item([build_tutorial_entry(...)])  # REQ-2
```

### 4. 修改 `_add_guide.py`

同理：

```python
from _changelog_utils import append_changelog_item, build_guide_entry

# 在 main() 中 write HTML 之后：
print(f'✓ 指南页面已生成: {out_path}')
append_changelog_item([build_guide_entry(...)])  # REQ-3
```

### 5. 新增脚本：`_sync_changelog.py`

独立脚本，用于手动修复/重建 changelog（REQ-6）：

```bash
python3 _sync_changelog.py          # 扫描差异并更新
python3 _sync_changelog.py --reset  # 完全重建 changelog
```

逻辑：
1. 读取 `tools-data.json`，获取工具总数和 `new: true` 标记的工具
2. 扫描 `tutorials/` 和 `guides/` 目录中的 HTML 文件，对比 `site-info.json` 的 changelog
3. 对缺失的条目进行追加
4. 更新 `lastUpdated` 和 `toolCount`

## changelog 条目格式

### 工具变更项

```json
{
  "zh": "新增PDF工具：PDF OCR（OCR文字提取）",
  "en": "New PDF tool: PDF OCR (Extract text via OCR)",
  "ja": "新規PDFツール：PDF OCR（OCRテキスト抽出）",
  "vi": "Công cụ PDF mới: PDF OCR (Trích xuất văn bản OCR)"
}
```

### 教程变更项

```json
{
  "zh": "新增PDF工具教程：如何使用PDF OCR提取文字",
  "en": "New PDF tutorial: How to use PDF OCR for text extraction",
  "ja": "新規PDFチュートリアル：PDF OCRで文字を抽出する方法",
  "vi": "Hướng dẫn PDF mới: Cách sử dụng PDF OCR để trích xuất văn bản"
}
```

### 指南变更项

```json
{
  "zh": "新增对比评测：PDF工具横向评测",
  "en": "New review: PDF Tools Comparison",
  "ja": "新規比較レビュー：PDFツール比較",
  "vi": "Đánh giá mới: So sánh công cụ PDF"
}
```

## 当日聚合策略（REQ-4）

```python
def append_changelog_item(entries):
    data = load_site_info()
    today = date.today().isoformat()

    # 查找当日是否已有条目
    latest = data['changelog'][0] if data['changelog'] else None
    if latest and latest['date'] == today:
        # 聚合到当日条目
        for entry in entries:
            for lang in ['zh', 'en', 'ja', 'vi']:
                if entry[lang] not in latest['items'][lang]:
                    latest['items'][lang].append(entry[lang])
    else:
        # 创建新条目
        new_entry = {
            'version': data['version'],
            'date': today,
            'zh': entries[0]['zh'],
            'en': entries[0]['en'],
            'ja': entries[0]['ja'],
            'vi': entries[0]['vi'],
            'items': {lang: [e[lang] for e in entries] for lang in ['zh','en','ja','vi']}
        }
        data['changelog'].insert(0, new_entry)

    save_site_info(data)
```

## 关键设计决策

1. **公共模块提取**：changelog 操作逻辑放入 `_changelog_utils.py` 而非在每个脚本中复制代码，使用 `sys.path.insert(0, SCRIPT_DIR)` 导入
2. **非侵入式修改**：只在脚本末尾追加 changelog 更新，不影响现有流程
3. **当日聚合**：同一天多次添加内容时合并到同一 changelog 条目
4. **不新增依赖**：所有操作仅使用 Python 标准库（`json`、`os`、`datetime`）
5. **四语言覆盖**：每个变更项同时生成 zh/en/ja/vi 四种语言的描述

## 文件变更清单

| 文件 | 操作 | 说明 |
|------|------|------|
| `_changelog_utils.py` | 新增 | changelog 公共操作模块 |
| `_add_tool.py` | 修改 | 追加 changelog 更新调用 |
| `_add_tutorial.py` | 修改 | 追加 changelog 更新调用 |
| `_add_guide.py` | 修改 | 追加 changelog 更新调用 |
| `_sync_changelog.py` | 新增 | 独立同步/修复脚本 |
| `data/site-info.json` | 自动更新 | 脚本运行后自动写入 |
