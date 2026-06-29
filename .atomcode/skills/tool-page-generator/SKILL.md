---
name: tool-page-generator
description: 生成完整的 ZenTools 工具页面（含 i18n、JSON 注册、重复检查）
disable_model_invocation: false
user_invocable: true
---

# 增强型工具页面生成器

按照以下步骤生成一个完整的 ZenTools 工具页面并注册到数据文件中。

## 步骤

### 1. 基本信息收集
询问用户：
- 工具名称（中文）
- 英文 slug（全小写，连字符分隔）
- 所属分类（图片/PDF/音频/视频/AI/开发/生活/金融/文本/SEO/二维码）
- 功能描述
- 输入类型（文件、文本、数字、选择等）
- 是否需 Canvas/Web Audio API

### 2. 重复检查
- 检查 `data/tools-data.json` 中是否已有同名工具（匹配 `name` 或 `slug`）
- 检查对应分类目录下是否已有同名 HTML 文件
- 如果存在重复，提示用户并中止

### 3. 生成 HTML 文件
- 文件路径：`{分类目录}/{slug}.html`
- 必须包含：
  - `<!DOCTYPE html>` + `<meta charset="UTF-8">`
  - 响应式 viewport
  - `<title>` 和 `<meta description/keywords>`
  - 导航栏（带 `#langSelect`）
  - 面包屑导航（`.breadcrumb`）
  - `<h1>` 标题带 `.grad` 类
  - `.tool-box` 容器
  - AdSense 广告位（`class="adsbygoogle"`）
  - 页脚（含备案号 `footerCopy`）
  - 引入 `tool-ui.min.js` 和 `anti-crash.min.js`
  - `data-i18n` 属性覆盖所有可见文本
  - CSS 使用 `:root{--bg:#0f172a;...}` 暗色变量体系
  - i18n 翻译对象 `window.ZT_PAGE` 含 zh/en/ja/vi 四种语言

### 4. 注册到数据文件
- 向 `data/tools-data.json` 对应分类的 `tools` 数组中添加新条目
- 条目格式：
  ```json
  {
    "name": "工具名称",
    "slug": "tool-slug",
    "desc": "简短描述",
    "icon": "🔧",
    "path": "分类目录/tool-slug.html"
  }
  ```

### 5. 记录
- 在 `.atomcode/memory.md` 中记录新建的工具名称和路径
