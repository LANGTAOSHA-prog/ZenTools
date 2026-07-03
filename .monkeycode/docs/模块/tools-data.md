# tools-data — 工具数据 JSON

> 文件: `data/tools-data.json` (654KB, 12619行) | JS版: `assets/js/tools-data.js` (12557行)
> 版本: 2.2 | 最后更新: 2026-06-21

## 概述

`tools-data.json` 是 ZenTools 的**单一数据源 (Source of Truth)**，定义了全站 279 个工具的所有元数据。所有页面渲染、搜索、推荐、统计均依赖此文件。

## JSON 结构

```json
{
  "version": "2.2",
  "lastUpdated": "2026-06-21",
  "categories": ["AI工具", "图片工具", "PDF工具", "文本工具", "视频工具", "音频工具", "开发工具", "SEO工具", "办公工具", "生活工具", "金融工具", "教育工具", "设计工具"],
  "categories__en": ["AI Tools", "Image Tools", "PDF Tools", "Text Tools", "Video Tools", "Audio Tools", "Dev Tools", "SEO Tools", "Office Tools", "Life Tools", "Finance Tools", "Education Tools", "Design Tools"],
  "categories__ja": ["AIツール", "画像ツール", "PDFツール", "テキストツール", "動画ツール", "音声ツール", "開発ツール", "SEOツール", "オフィスツール", "生活ツール", "金融ツール", "教育ツール", "デザインツール"],
  "categories__vi": ["Công cụ AI", "Công cụ hình ảnh", "Công cụ PDF", "Công cụ văn bản", "Công cụ video", "Công cụ âm thanh", "Công cụ phát triển", "Công cụ SEO", "Công cụ văn phòng", "Công cụ đời sống", "Công cụ tài chính", "Công cụ giáo dục"],
  "tools": [ /* 279 个 ToolEntry 对象 */ ]
}
```

> 注意: `categories__vi` 仅 12 项，缺少 "设计工具" 的翻译。

## 工具字段详解

### 必填字段 (16个顶层字段)

| 字段 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `name` | string | "BMI 计算器" | 中文名 |
| `name__en` | string | "BMI Calculator" | 英文名 |
| `name__ja` | string | "BMI計算機" | 日文名 |
| `name__vi` | string | "Máy tính BMI" | 越南文名 |
| `slug` | string | "bmi" | URL 友好标识 |
| `category` | string | "生活工具" | 所属分类 (中文) |
| `url` | string | "/life/bmi.html" | 页面相对路径 |
| `description` | string | "根据身高体重..." | 中文描述 (19-52字) |
| `description__en` | string | "Calculate BMI..." | 英文描述 |
| `description__ja` | string | "BMIを計算..." | 日文描述 |
| `description__vi` | string | "Tính chỉ số BMI..." | 越南文描述 |
| `icon` | string | "⚖️" | 单个 emoji |
| `featured` | boolean | false | 是否精选 |
| `new` | boolean | true | 是否新工具 |
| `keywords` | string | "bmi 体重指数" | 空格分隔关键词 |
| `ai` | object | {...} | AI/隐私元数据 (见下文) |

### `ai` 子对象 (19个字段)

| 字段 | 类型 | 示例 | 说明 |
|------|------|------|------|
| `free` | boolean | true | 是否免费 (全为 true) |
| `registration` | boolean | false | 是否需要注册 |
| `chinese` | boolean | true | 是否支持中文 |
| `languages` | string[] | ["zh","en","ja","vi"] | 支持语言 |
| `processing` | string | "browser-local" | 处理方式 ("browser-local" 或 "cloud") |
| `privacy` | string | "处理在浏览器本地完成" | 隐私说明 |
| `privacy__en/ja/vi` | string | ... | 多语言隐私说明 |
| `audience` | string | "普通用户、家庭用户" | 目标用户 |
| `audience__en/ja/vi` | string | ... | 多语言目标用户 |
| `useCases` | string | "日常计算、单位换算" | 使用场景 |
| `useCases__en/ja/vi` | string | ... | 多语言使用场景 |
| `limits` | string | "无严格限制" | 使用限制 |
| `limits__en/ja/vi` | string | ... | 多语言限制说明 |

### 多语言字段命名约定

所有多语言字段遵循 `字段名__语言代码` 模式:
- 无后缀 = 中文 (默认)
- `__en` = English
- `__ja` = 日本語
- `__vi` = Tiếng Việt

## 数据质量检查

### 校验脚本

```bash
python _check_json.py    # JSON 格式完整性
python _check_paths.py   # url 字段引用的 HTML 文件是否存在
python _check_data.py    # 数据一致性 (工具数/分类/必填字段)
```

### 已知问题

| 问题 | 影响 | 优先级 |
|------|------|--------|
| `categories__vi` 缺 "设计工具" | 越南语分类列表不完整 | 低 |
| "办公工具" 和 "教育工具" 类别无工具 | 分类页为空 | 低 |
| 部分页面使用旧版模板 (如 image-compressor.html) | 缺少统一导航/搜索/收藏 | 中 |

## tools-data.js 与 tools-data.json 的关系

- `tools-data.json`: JSON 格式源数据，供 Python 脚本处理和 fetch 加载
- `tools-data.js`: JS 格式，内容相同，以 `<script>` 标签直接引入，避免 fetch 延迟
- 两者需保持同步

## 添加工具的标准流程

1. 编辑 `data/tools-data.json` → 在 `tools` 数组中添加条目
2. 运行 `python _check_json.py` 验证
3. 创建对应的 HTML 工具页面
4. 运行 `python _check_paths.py` 验证路径
5. 同步更新 `assets/js/tools-data.js`
6. 重新生成 sitemap
