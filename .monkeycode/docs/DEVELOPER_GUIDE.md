# 开发者指南

## 环境搭建

### 前置条件

- Python 3.6+ (用于数据校验脚本和本地开发服务器)
- Git
- 任何现代浏览器 (Chrome/Edge 推荐)

### 本地运行

```bash
# 克隆仓库
git clone <repo-url> zentools
cd zentools

# 启动开发服务器 (端口 8000)
python -m http.server 8000

# 访问 http://localhost:8000
```

### 数据校验

```bash
# 验证 JSON 格式完整性
python _check_json.py

# 检查文件路径正确性
python _check_paths.py

# 检查数据一致性
python _check_data.py
```

### 资源压缩

```bash
# 压缩 JS 资源
python _minify_assets.py
```

---

## 项目约定

### 核心原则

1. **搜索优先**: 修改前先搜索现有代码 (`components/`, `tools/`, `assets/js/`)，确认不存在重复实现
2. **复用优先**: 发现已有实现时必须扩展而非重写
3. **无框架**: 纯 Vanilla JS，禁止引入 React/Vue/jQuery
4. **使用压缩版**: 页面中引用 `.min.js` / `.min.css`，非压缩源文件
5. **禁止创建**: 临时测试文件、重复页面、非 `/tutorials/` 目录下的教程文件

### 文件命名

- 工具页: `{category}/{tool-slug}.html` (如 `pdf/pdf-compress.html`)
- 教程页: `tutorials/{tutorial-slug}.html`
- JS 模块: `assets/js/{module-name}.js` 和 `assets/js/{module-name}.min.js`
- CSS: `assets/css/{name}.css` 和 `assets/css/{name}.min.css`

### 代码风格

- 使用 `LF` 换行符
- JavaScript: `use strict` 模式, 函数优先于 class, IIFE 包裹避免全局污染
- HTML: 2 空格缩进, 语义化标签
- CSS: 使用 CSS 自定义属性 (`var(--xxx)`), 遵循 `:root` 变量定义

---

## 新增工具流程

### 步骤 1: 更新工具数据

编辑 `data/tools-data.json`，在 `tools` 数组中添加新条目:

```json
{
  "name": "我的新工具",
  "name__en": "My New Tool",
  "name__ja": "私の新しいツール",
  "name__vi": "Công cụ mới của tôi",
  "slug": "my-new-tool",
  "category": "开发工具",
  "url": "/dev/my-new-tool.html",
  "description": "这是一个新工具的描述",
  "description__en": "Description of the new tool",
  "description__ja": "新しいツールの説明",
  "description__vi": "Mô tả công cụ mới",
  "icon": "🔧",
  "featured": false,
  "new": true,
  "keywords": "工具 关键词",
  "ai": {
    "free": true,
    "registration": false,
    "chinese": true,
    "languages": ["zh", "en", "ja", "vi"],
    "privacy": "所有处理在浏览器本地完成",
    "privacy__en": "All processing is done locally in the browser",
    "privacy__ja": "すべての処理はブラウザでローカルに完了します",
    "privacy__vi": "Tất cả xử lý được thực hiện cục bộ trong trình duyệt",
    "processing": "browser-local",
    "audience": "开发者、普通用户",
    "audience__en": "Developers, general users",
    "audience__ja": "開発者、一般ユーザー",
    "audience__vi": "Nhà phát triển, người dùng phổ thông",
    "useCases": "日常开发、数据处理",
    "useCases__en": "Daily development, data processing",
    "useCases__ja": "日常開発、データ処理",
    "useCases__vi": "Phát triển hàng ngày, xử lý dữ liệu",
    "limits": "无严格限制",
    "limits__en": "No strict limits",
    "limits__ja": "厳格な制限はありません",
    "limits__vi": "Không có giới hạn nghiêm ngặt"
  }
}
```

### 步骤 2: 使用自动化脚本 (可选)

```bash
python _add_tools.py
```

### 步骤 3: 创建工具 HTML 页面

**必须使用新版模板** (`tool-ui` 模式)。参考 `pdf/pdf-compress.html` 作为模板。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>我的新工具 - ZenTools</title>
  <meta name="description" content="..." />

  <!-- Open Graph -->
  <meta property="og:title" content="..." />
  <meta property="og:description" content="..." />
  <meta property="og:url" content="https://zentools.xyz/dev/my-new-tool.html" />

  <!-- PWA -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="theme-color" content="#00e5ff" />

  <!-- Canonical -->
  <link rel="canonical" href="https://zentools.xyz/dev/my-new-tool.html" />

  <!-- 样式 -->
  <link rel="stylesheet" href="../assets/css/tool-ui.min.css" />
  <style>
    /* 仅写页面特有样式 */
  </style>

  <!-- 结构化数据 -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [{
      "@type": "Question",
      "name": "如何使用我的新工具?",
      "acceptedAnswer": { "@type": "Answer", "text": "..." }
    }]
  }
  </script>
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebApplication",
    "name": "我的新工具",
    "url": "https://zentools.xyz/dev/my-new-tool.html",
    "description": "...",
    "applicationCategory": "UtilityApplication",
    "operatingSystem": "All",
    "offers": { "@type": "Offer", "price": "0", "priceCurrency": "CNY" }
  }
  </script>
</head>
<body>
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="z-wrap">

    <!-- 导航栏 -->
    <nav>
      <div class="nav-inner">
        <a class="logo" href="/">ZenTools<span>2.0</span></a>
        <div class="nav-links">
          <a href="/" data-i18n="nav_home">首页</a>
          <a href="/dev/index.html" data-i18n="nav_dev">开发工具</a>
          <a href="/tools.html" data-i18n="nav_all_tools">全部工具</a>
          <select id="langSelect" class="lang-select">
            <option value="zh">中文</option>
            <option value="en">English</option>
            <option value="ja">日本語</option>
            <option value="vi">Tiếng Việt</option>
          </select>
        </div>
      </div>
    </nav>

    <!-- 页面头部 -->
    <div class="page-header reveal">
      <div class="breadcrumb">
        <a href="/" data-i18n="breadcrumb_home">首页</a>
        <span> › </span>
        <a href="/dev/index.html">开发工具</a>
        <span> › </span>
        <span data-i18n="page_title">我的新工具</span>
      </div>
      <span class="page-eyebrow" data-i18n="category_label">开发工具</span>
      <h1>
        <span class="grad" data-i18n="heading_grad">我的新工具</span><br/>
        <span data-i18n="heading_sub">副标题描述</span>
      </h1>
      <p data-i18n="page_desc">页面描述文字...</p>
    </div>

    <!-- 工具核心区 -->
    <div class="tool-box reveal">
      <h2 data-i18n="tool_title">工具标题</h2>
      <p class="note" data-i18n="tool_desc">工具说明</p>

      <!-- 工具具体 UI 在这里 -->
      <div class="file-input-row">
        <input type="file" id="fileInput" />
        <button class="btn-primary" id="btnAction" data-i18n="btn_action">执行</button>
      </div>

      <div class="zt-perf-warn" data-i18n="perf_warn"></div>
      <div id="status"></div>
    </div>

    <!-- 说明区 -->
    <div class="section">
      <div class="section-head">
        <h2 data-i18n="info_heading">使用说明</h2>
      </div>
      <div class="info-grid">
        <div class="info-card">
          <h4 data-i18n="info_title_1">隐私安全</h4>
          <p data-i18n="info_desc_1">所有处理在浏览器本地完成，文件不上传服务器。</p>
        </div>
        <div class="info-card">
          <h4 data-i18n="info_title_2">完全免费</h4>
          <p data-i18n="info_desc_2">无使用次数限制，无水印，无需注册。</p>
        </div>
        <div class="info-card">
          <h4 data-i18n="info_title_3">多语言支持</h4>
          <p data-i18n="info_desc_3">支持中文、英语、日语、越南语。</p>
        </div>
      </div>
    </div>

    <!-- 页脚 -->
    <footer>
      <div class="footer-inner">
        <div class="footer-links">
          <a href="/privacy.html" data-i18n="footer_privacy">隐私政策</a>
          <a href="/terms.html" data-i18n="footer_terms">服务条款</a>
          <a href="/contact" data-i18n="footer_contact">联系我们</a>
        </div>
        <p class="footer-copy">&copy; 2026 ZenTools</p>
      </div>
    </footer>
  </div>

  <!-- 翻译 -->
  <script>
    window.ZT_PAGE = {
      zh: {
        "page_title": "我的新工具",
        "heading_grad": "我的新工具",
        "heading_sub": "工具副标题",
        "page_desc": "工具描述...",
        "tool_title": "使用我的新工具",
        "tool_desc": "上传文件开始处理",
        "btn_action": "开始处理",
        "perf_warn": "文件较大，处理可能需要一些时间",
        "info_heading": "使用说明",
        "info_title_1": "隐私安全",
        "info_desc_1": "所有处理在浏览器本地完成",
        "info_title_2": "完全免费",
        "info_desc_2": "无限制使用",
        "info_title_3": "多语言支持",
        "info_desc_3": "支持中/英/日/越"
      },
      en: {
        "page_title": "My New Tool",
        "heading_grad": "My New Tool",
        "heading_sub": "Tool Subtitle",
        "page_desc": "Tool description...",
        "tool_title": "Use My New Tool",
        "tool_desc": "Upload files to start processing",
        "btn_action": "Start Processing",
        "perf_warn": "Large files may take some time",
        "info_heading": "Instructions",
        "info_title_1": "Privacy Safe",
        "info_desc_1": "All processing done locally",
        "info_title_2": "Free",
        "info_desc_2": "Unlimited usage",
        "info_title_3": "Multi-language",
        "info_desc_3": "Supports ZH/EN/JA/VI"
      },
      ja: {
        "page_title": "私の新しいツール",
        "heading_grad": "私の新しいツール",
        "heading_sub": "ツールのサブタイトル",
        "page_desc": "ツールの説明...",
        "tool_title": "私の新しいツールを使う",
        "tool_desc": "ファイルをアップロードして処理を開始",
        "btn_action": "処理開始",
        "perf_warn": "大きなファイルは時間がかかる場合があります",
        "info_heading": "使用方法",
        "info_title_1": "プライバシー安全",
        "info_desc_1": "すべての処理はローカルで完了",
        "info_title_2": "無料",
        "info_desc_2": "無制限に使用可能",
        "info_title_3": "多言語対応",
        "info_desc_3": "ZH/EN/JA/VI対応"
      },
      vi: {
        "page_title": "Công cụ mới của tôi",
        "heading_grad": "Công cụ mới của tôi",
        "heading_sub": "Phụ đề công cụ",
        "page_desc": "Mô tả công cụ...",
        "tool_title": "Sử dụng công cụ mới",
        "tool_desc": "Tải tệp lên để bắt đầu xử lý",
        "btn_action": "Bắt đầu xử lý",
        "perf_warn": "Tệp lớn có thể mất thời gian",
        "info_heading": "Hướng dẫn",
        "info_title_1": "An toàn bảo mật",
        "info_desc_1": "Tất cả xử lý cục bộ",
        "info_title_2": "Miễn phí",
        "info_desc_2": "Không giới hạn sử dụng",
        "info_title_3": "Đa ngôn ngữ",
        "info_desc_3": "Hỗ trợ ZH/EN/JA/VI"
      }
    };
  </script>
  <script src="../assets/js/common-i18n.min.js"></script>
  <script src="../assets/js/tool-ui.min.js"></script>
  <script>
    // 工具业务逻辑
    document.getElementById('btnAction').addEventListener('click', async () => {
      const file = document.getElementById('fileInput').files[0];
      if (!file) return;

      ZT.showProgress('处理中...', true);
      // ... 处理逻辑 ...
      ZT.hideProgress();
    });

    // 注册 Service Worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker.register('/sw.js');
    }
  </script>
</body>
</html>
```

### 步骤 4: 数据校验

```bash
python _check_json.py
```

### 步骤 5: 更新 sitemap

```bash
python -c "
import os, xml.etree.ElementTree as ET
base = 'https://zentools.xyz'
root_elem = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
for r, d, f in os.walk('.'):
    d[:] = [x for x in d if x[0] != '.' and x != 'node_modules' and x != 'pdf_tools']
    for fn in f:
        if fn.endswith('.html'):
            u = ET.SubElement(root_elem, 'url')
            ET.SubElement(u, 'loc').text = base + '/' + os.path.relpath(os.path.join(r, fn), '.')
with open('sitemap.xml', 'w') as f:
    f.write(ET.tostring(root_elem, encoding='unicode'))
"
```

### 步骤 6: 刷新 tools-data.js

确保 `assets/js/tools-data.js` 与 `data/tools-data.json` 保持同步。如使用构建脚本同步，请执行相应命令。

---

## i18n 国际化规范

### 翻译键命名

- 使用 `snake_case` 命名
- 语义化命名，描述该文本的用途而非内容
- 分类前缀: `nav_` (导航), `footer_` (页脚), `info_` (信息卡), `btn_` (按钮)

### 新增公共翻译键

编辑 `assets/js/common-i18n.js`，在所有 4 种语言中添加对应翻译:

```javascript
window.ZT_COMMON = {
  zh: { "new_key": "新翻译", ... },
  en: { "new_key": "New Translation", ... },
  ja: { "new_key": "新しい翻訳", ... },
  vi: { "new_key": "Bản dịch mới", ... }
};
```

### 翻译优先级

`ZT_PAGE` 的同名键会覆盖 `ZT_COMMON` 的同名键。页面专用文本应放在 `ZT_PAGE` 中。

---

## 常见问题

### Q: tools-data.json 修改后首页没有更新?

A: 检查浏览器缓存，硬刷新 (Ctrl+Shift+R)。如果使用了 Service Worker，可能需要清除 SW 缓存。

### Q: 为什么我的工具页导航栏没有出现?

A: 确保你使用了新版模板 (加载了 `tool-ui.min.css` 和 `tool-ui.min.js`)，而不是旧版的全内联模式。

### Q: 语言切换后页面文本没有更新?

A: 检查:
1. `window.ZT_PAGE` 是否正确定义在 `tool-ui.min.js` 之前
2. `common-i18n.min.js` 是否在 `tool-ui.min.js` 之前加载
3. 所有需翻译的元素是否都有 `data-i18n="key"` 属性
4. 翻译键名是否在 `ZT_PAGE` 或 `ZT_COMMON` 中存在

### Q: 旧版页面 (如 image-compressor.html) 想迁移到新版模板?

A: 核心步骤:
1. 用新版 HTML 模板包裹现有内容
2. 提取内联样式到 `<style>` 标签 (保留在页面内，不修改 tool-ui.css)
3. 将 `window.pageTranslations` 改为 `window.ZT_PAGE` 格式
4. 添加 `<script src="tool-ui.min.js">` 和 `<script src="common-i18n.min.js">`
5. 移除手动编写的导航/页脚代码
6. 用 `ZT.showProgress/hideProgress` 替换手动进度条

### Q: 如何调试备用模式?

A: 在浏览器控制台:
```javascript
// 查看系统状态
ZT_CRASH.getStatus()

// 手动触发备用模式
ZT_CRASH.errorCount = 10

// 查看帮助
ZT_CRASH.help()
```

---

## 辅助脚本说明

| 脚本 | 功能 |
|------|------|
| `_check_json.py` | 校验 `data/tools-data.json` 及所有 JSON 文件的结构完整性 |
| `_check_paths.py` | 检查 tools-data.json 中所有 url 字段对应的 HTML 文件是否存在 |
| `_check_data.py` | 检查数据一致性 (工具数量、分类匹配、必填字段) |
| `_add_tools.py` | 交互式添加新工具到 tools-data.json |
| `_minify_assets.py` | 压缩 JS 资源为 `.min.js` 版本 |
| `_opt_index.py` | 首页 HTML 优化 |
| `_update_readme.py` | 更新 README 中的工具统计数字 |
| `_gen_tutorials.py` | 教程页面批量生成 |
