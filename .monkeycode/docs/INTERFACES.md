# ZenTools 接口文档

ZenTools 为纯静态网站，本文档描述了页面间共享的 JavaScript API、数据规范、i18n 翻译数据结构以及 PWA 缓存策略。

---

## 一、全局 JS API（`window.ZT` 命名空间）

所有 API 通过 `tool-ui.js` 注入到 `window.ZT` 对象，在页面加载后自动可用。

### ZT.applyLanguage(lang)

运行时切换显示语言。

- **参数**: `lang` — `'zh'` | `'en'` | `'ja'` | `'vi'`
- **行为**: 合并 `window.ZT_COMMON[lang]` 与 `window.ZT_PAGE[lang]`（后者覆盖前者），遍历页面中所有 `[data-i18n]` 和 `[data-i18n-placeholder]` 元素替换文本内容，更新 `document.title`，写入 `localStorage('zentools_lang')`，触发 `zt-langchange` 自定义事件。
- **示例**:
```js
ZT.applyLanguage('en');
```

### 事件：zt-langchange

语言切换完成后触发，携带新语言和合并后的翻译字典。

- **detail.lang**: 当前语言代码（`'zh'`/`'en'`/`'ja'`/`'vi'`）
- **detail.dict**: 合并后的翻译字典对象

```js
window.addEventListener('zt-langchange', function(e) {
  console.log('语言已切换到:', e.detail.lang);
  // 在此重新渲染依赖动态内容的 DOM
});
```

### ZT.track（收藏与最近使用）

- `ZT.track.add(name)` — 将当前页面加入"最近使用"
- `ZT.track.toggleFav(name)` — 切换当前页面的收藏状态，返回 `true`=已收藏, `false`=已取消
- `ZT.track.isFav()` — 查询当前页面是否已被收藏
- `ZT.track.addFavBtn()` — 在 `.page-header` 末尾注入收藏按钮

### ZT.clickTrack(url, name)

记录工具点击统计到 localStorage，内部函数，一般由事件委托自动调用。

---

## 二、数据规范（tools-data.json）

### 根结构

```json
{
  "version": "2.2",
  "lastUpdated": "2026-06-21",
  "categories": ["AI工具", "图片工具", ...],
  "categories__en": ["AI Tools", ...],
  "categories__ja": ["AIツール", ...],
  "categories__vi": ["Công cụ AI", ...],
  "tools": [...]   // 工具数组
}
```

### 工具对象字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `name` | string | 是 | 中文名称 |
| `name__en` | string | 是 | 英文名称 |
| `name__ja` | string | 是 | 日文名称 |
| `name__vi` | string | 是 | 越南文名称 |
| `slug` | string | 是 | URL 唯一标识（如 `pdf-merge`） |
| `category` | string | 是 | 所属分类（中文） |
| `url` | string | 是 | 页面相对路径（如 `/pdf/pdf-merge.html`） |
| `description` | string | 否 | 中文描述 |
| `description__en` | string | 否 | 英文描述 |
| `description__ja` | string | 否 | 日文描述 |
| `description__vi` | string | 否 | 越南文描述 |
| `icon` | string | 否 | Emoji 图标 |
| `featured` | boolean | 否 | 是否在首页"热门工具"中展示 |
| `new` | boolean | 否 | 是否标记为"新" |
| `keywords` | string | 否 | 空格分隔的搜索关键词 |
| `ai` | object | 否 | AI 工具专属属性（见下方） |

### AI 工具专属属性

```json
{
  "free": true,
  "registration": false,
  "chinese": true,
  "languages": ["zh", "en", "ja", "vi"],
  "privacy": "所有处理在浏览器本地完成",
  "processing": "browser-local",
  "audience": "普通用户、内容创作者",
  "useCases": "日常办公、内容处理",
  "limits": "无严格限制"
}
```

---

## 三、i18n 翻译数据接口

### window.ZT_COMMON（公共翻译）

由 `common-i18n.js` 定义，包含导航栏、页脚、面包屑和语言选择器等全局元素的翻译。结构：

```js
window.ZT_COMMON = {
  zh: { navHome: '首页', navAll: '全部工具', ... },
  en: { navHome: 'Home', navAll: 'All Tools', ... },
  ja: { navHome: 'ホーム', navAll: 'すべてのツール', ... },
  vi: { navHome: 'Trang chủ', navAll: 'Tất cả công cụ', ... }
};
```

### window.ZT_PAGE（页面专属翻译）

每个页面在 `<script>` 标签中内联定义，需要包含当前语言下的所有动态文本 key。

```js
window.ZT_PAGE = {
  zh: { pageTitle: '...', h1Grad: '...', ... },
  en: { pageTitle: '...', h1Grad: '...', ... },
  ja: { ... },
  vi: { ... }
};
```

### HTML 标记规范

- `data-i18n="key"` — 替换元素的 `textContent`
- `data-i18n-placeholder="key"` — 替换元素的 `placeholder` 属性
- Fallback 文字必须与 `ZT_PAGE` 中对应 key 的值一致

---

## 四、工具页面结构规范

每个工具页面必须遵循以下 HTML 骨架：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <title data-i18n="pageTitle">工具名称 - ZenTools</title>
  <meta name="description" content="..." />
  <meta name="keywords" content="..." />
  <link rel="canonical" href="https://zentools.xyz/cat/tool.html" />

  <!-- 资源（相对路径引用） -->
  <link rel="stylesheet" href="../assets/css/tool-ui.min.css" />
  <script src="../assets/js/common-i18n.min.js"></script>

  <!-- 页面专属 JS 配置 -->
  <script>
  window.ZT_PAGE = { zh: {...}, en: {...}, ja: {...}, vi: {...} };
  </script>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>

  <div class="z-wrap">
    <nav>...</nav>

    <!-- 页面头部 -->
    <div class="page-header reveal">
      <div class="breadcrumb">
        <a href="/" data-i18n="crumbHome">首页</a>
        <span>/</span>
        <a href="/cat/">分类</a>
        <span>/</span>
        <span data-i18n="crumbCur">当前工具</span>
      </div>
      <h1 data-i18n="pageTitle">工具名称</h1>
      <p data-i18n="pageDesc">工具描述</p>
    </div>

    <!-- 工具区域 -->
    <div class="tool-box reveal">...</div>

    <!-- 使用说明区域 -->
    <div class="section">
      <div class="section-head">
        <h2 data-i18n="infoTitle">使用说明</h2>
      </div>
      <div class="info-grid">...</div>
    </div>

    <footer>...</footer>
  </div>

  <script src="../assets/js/tool-ui.min.js"></script>
  <script>
    // 工具专属逻辑
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js');
    }
  </script>
</body>
</html>
```

---

## 五、Service Worker 缓存策略

`sw.js` 采用 cache-first 策略，5 层缓存命名空间：

| 缓存名 | 匹配规则 | 过期策略 | 大小限制 |
|--------|---------|---------|---------|
| `zentools-v2-core` | `/`, `index.html`, `tools.html`, manifest, 图标 | 版本号变更时清除 | 无限制 |
| `zentools-v2-assets` | `assets/css/*`, `assets/js/*` | 版本号变更时清除 | 无限制 |
| `zentools-v2-data` | `data/tools-data.json` | 版本号变更时清除 | 无限制 |
| `zentools-v2-html` | 匹配 TOOL_PAGE_PATTERN 的页面 | LRU，最多 200 条 | 200 条 |
| `zentools-v2-pages` | 分类首页（`/pdf/index.html` 等） | 版本号变更时清除 | 无限制 |

### 工具页面正则

```js
const TOOL_PAGE_PATTERN = /\/(image|pdf|audio|video|text|dev|ai|life|seo|finance|qr|tools|tutorials|json)\/.+\.html$/;
```

---

## 六、自动化脚本 CLI 接口

### _add_tool.py

```bash
python3 _add_tool.py --slug pdf-ocr --category "PDF工具" \
  --name-zh "PDF OCR" --name-en "PDF OCR" --name-ja "PDF OCR" --name-vi "PDF OCR" \
  --desc-zh "OCR文字提取" --desc-en "Extract text from PDF" \
  --desc-ja "PDFからテキスト抽出" --desc-vi "Trích xuất văn bản từ PDF" \
  --keywords "ocr pdf"
```

### _gen_sitemap.py

```bash
python3 _gen_sitemap.py   # 生成 sitemap.xml，包含所有 .html 文件
```

### _check_json.py

```bash
python3 _check_json.py    # 校验 data/ 下的 JSON 文件完整性
```

### _sync_tools_data_js.py

```bash
python3 _sync_tools_data_js.py   # 将 tools-data.json 同步为 tools-data.js
```
