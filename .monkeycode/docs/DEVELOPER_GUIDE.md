# ZenTools 开发者指南

## 项目目的

ZenTools 是一个面向普通用户的免费在线工具箱，提供 300+ 款浏览器端工具。它的核心诉求是 **所有处理在浏览器本地完成，文件不上传服务器**。本指南面向贡献者，涵盖环境搭建、开发工作流、编码规范和常见任务。

**核心职责**:
- 提供 PDF、图片、AI、音视频、文本、开发、生活、金融等 13 个分类的在线工具
- 支持 zh/en/ja/vi 四语言即时切换
- 保持纯静态 Gatsby Pages 直接部署能力
- 所有新功能不引入框架依赖（Vanilla JS only）

## 环境搭建

### 前置条件

- Python 3.x（仅用于辅助脚本，非必须）
- 现代浏览器（Chrome/Firefox/Safari/Edge 最新版）
- Git

### 安装

```bash
# 克隆仓库
git clone https://github.com/LANGTAOSHA-prog/ZenTools.git
cd ZenTools

# 启动本地开发服务器
python3 -m http.server 8000
```

开发服务器启动后，访问 `http://localhost:8000` 即可预览。

### 无需构建

项目为纯静态 HTML，**无需 npm install、无需 webpack/Vite 构建**。所有页面直接在浏览器中打开即可运行。

## 开发工作流

### 本地测试

```bash
# 启动 HTTP 服务器
python3 -m http.server 8000

# 验证 JSON 数据完整性
python3 _check_json.py

# 同步工具数据格式
python3 _sync_tools_data_js.py

# 重新生成站点地图
python3 _gen_sitemap.py

# 压缩 JS/CSS 资源（修改后执行）
python3 _minify_assets.py
```

### 分支策略

| 分支 | 用途 |
|------|------|
| `main` | 生产环境，GitHub Pages 自动部署 |

项目采用单分支主干开发（Trunk-Based），所有改动直接推送到 `main`。

### 提交规范

提交信息格式：

```
<type>: <简短描述>
```

| 类型 | 说明 |
|------|------|
| `docs` | 文档、教程、指南内容变更 |
| `refactor` | 页面重构、UI 调整 |
| `seo` | SEO 相关（sitemap、meta 标签、交叉引用） |
| `fix` | Bug 修复 |
| `chore` | 工具脚本、配置维护 |

### CI 备份

`.github/workflows/backup.yml` 自动备份：
- 触发条件：每次 push 到 main + 每日 00:00 UTC
- 备份内容：`data/` 目录、根目录配置文件和核心脚本

---

## 常见任务

### 添加新工具

**需修改的文件**:
1. **创建工具 HTML 页面**（可使用 `_add_tool.py` 生成骨架）
2. `data/tools-data.json` — 添加工具元数据条目
3. `sitemap.xml` — 执行 `_gen_sitemap.py` 重新生成

**使用脚本快速生成**:

```bash
python3 _add_tool.py --slug pdf-ocr --category "PDF工具" \
  --name-zh "PDF OCR" --name-en "PDF OCR" --name-ja "PDF OCR" --name-vi "PDF OCR" \
  --desc-zh "OCR文字提取" --desc-en "Extract text from PDF" \
  --desc-ja "PDFからテキスト抽出" --desc-vi "Trích xuất văn bản từ PDF" \
  --keywords "ocr pdf"
```

**手动步骤**:
1. 在对应分类目录下创建 `<slug>.html`
2. 在 `tools-data.json` 的 `tools` 数组中添加条目
3. 运行 `python3 _gen_sitemap.py` 更新站点地图
4. 运行 `python3 _check_json.py` 校验数据完整性
5. 运行 `python3 _sync_tools_data_js.py` 同步 JS 版数据
6. 运行 `python3 _minify_assets.py` 压缩资源

### 添加新教程

```bash
python3 _add_tutorial.py --slug pdf-ocr-tutorial --category "PDF工具" \
  --title-zh "PDF OCR教程" --desc-zh "使用OCR提取文字" \
  --tool-url "/pdf/pdf-ocr.html"
```

教程统一放在 `/tutorials/` 目录，禁止放在 `/articles/`、`/blog/`、`/posts/`。

### 添加新指南/评测

```bash
python3 _add_guide.py --slug pdf-tools-review --type review \
  --title-zh "PDF工具评测" --desc-zh "PDF工具横向对比" \
  --word-count 2500 --read-minutes 20
```

### 添加新 i18n 翻译 key

**需修改的文件**:
1. 页面 HTML 中 `window.ZT_PAGE` — 在四种语言（zh/en/ja/vi）中都添加新 key

**注意事项**:
- 全局通用翻译添加到 `assets/js/common-i18n.js`
- 页面专属翻译添加到对应页面的 `window.ZT_PAGE`
- Fallback 文字必须与 `ZT_PAGE` 中对应 key 的值一致
- 语言切换通过 `zt-langchange` 事件触发，动态内容需监听该事件

### 修复 Bug

1. 定位问题文件（工具页面、JS 引擎或 CSS 样式）
2. 用最小改动修复
3. 本地 `python3 -m http.server 8000` 验证
4. 必要时运行 `python3 _minify_assets.py` 重新压缩

---

## 编码规范

### 文件组织

- 工具页面按分类放在对应目录：`/pdf/`、`/image/`、`/ai/` 等
- 教程统一放在 `/tutorials/`
- 指南统一放在 `/guides/`
- 对比评测统一放在 `/compare/` 或 `/tutorials/`（对比文章）
- 共享资源放在 `/assets/css/` 和 `/assets/js/`

### 命名

| 类型 | 约定 | 示例 |
|------|------|------|
| 工具 HTML 文件 | kebab-case | `pdf-merge.html` |
| CSS 类名 | kebab-case | `tool-box`, `page-header` |
| JS 命名空间 | UPPER_SNAKE（全局） | `ZT`, `ZT_CRASH` |
| JS 变量/函数 | camelCase | `applyLanguage()`, `initLang()` |
| i18n key | camelCase | `navHome`, `pageTitle` |
| Python 脚本 | snake_case 前缀 `_` | `_add_tool.py`, `_gen_sitemap.py` |

### HTML/CSS 规范

- 始终引用 `.min` 压缩版资源（`tool-ui.min.css`、`tool-ui.min.js`、`common-i18n.min.js`、`anti-crash.min.js`）
- 页面专属 CSS 写在 `<style>` 标签中，不修改全局 CSS 文件
- 使用 CSS 变量（`var(--cyan)` 等），不硬编码颜色值
- 响应式布局优先，移动端断点 `max-width: 640px` / `max-width: 768px`

### JavaScript 规范

- 使用 IIFE（`(function() { 'use strict'; ... })();`）包裹全局逻辑
- 通过 `window.ZT` 命名空间暴露公共 API
- 不在页面中引入新框架或第三方库（Google Analytics/AdSense 除外）
- localStorage key 使用 `zt_` 前缀（`zt_lang`、`zt_favorites`、`zt_recent`）
- 不重复实现已有功能（搜索、收藏、i18n 等优先复用 `tool-ui.js`）

### 多语言规范

- 所有页面必须支持 zh/en/ja/vi 四种语言
- 使用 `data-i18n="key"` 标记翻译元素
- `window.ZT_PAGE` 必须包含四种语言的翻译
- Fallback 文字与 `ZT_PAGE` 中的值必须一致

---

## 项目约束

### 禁止事项

- **不引入框架**：禁止 jQuery、React、Vue、Angular 等
- **不创建重复功能**：搜索、收藏、i18n 等全局功能已在 `tool-ui.js` 中实现
- **不创建重复页面**：每个工具只有一个 HTML 文件
- **不创建临时测试文件**
- **教程不放在 `/articles/`、`/blog/`、`/posts/`**：统一 `/tutorials/`
- **不硬编码文本**：所有用户可见文本必须通过 i18n 系统管理

### 数据一致性

修改首页推荐工具等展示逻辑时，优先修改 `tools-data.json` 中的数据字段（如 `featured`、`new`），而不是修改 HTML 或 JS 渲染代码。

---

## 页面架构模式

### 工具页面模式

每个工具页面遵循统一骨架：
1. 导航栏（`<nav>` + `.nav-inner`）
2. 页面头部（`.page-header` + 面包屑 + h1 + 描述）
3. 工具区域（`.tool-box`，核心交互区）
4. 使用说明区域（`.section` + `.info-grid`，3 列卡片）
5. 页脚（`<footer>` + `.footer-inner`）

### 分类首页模式

每个分类目录下的 `index.html` 作为该类别的导航页，读取 `tools-data.json` 过滤出该分类的工具并渲染卡片网格。

### 列表页面模式（compare/guides/tutorials）

采用 data-driven 渲染：JS 数组定义数据 → `renderXxx(lang)` 函数动态生成 HTML → 监听 `zt-langchange` 事件触发重新渲染。

---

## 关键文件速查

| 文件 | 作用 |
|------|------|
| `data/tools-data.json` | 工具元数据主数据源 |
| `assets/js/tool-ui.js` | 全局 JS 引擎（i18n、主题、搜索、收藏）|
| `assets/js/common-i18n.js` | 公共翻译字典 |
| `assets/css/tool-ui.css` | 全局 UI 样式系统 |
| `assets/js/main.js` | 首页渲染逻辑 |
| `assets/js/anti-crash.js` | 防崩引擎 |
| `sw.js` | PWA Service Worker |
| `_add_tool.py` | 工具页面生成器 |
| `_gen_sitemap.py` | 站点地图生成器 |
| `_check_json.py` | JSON 数据校验器 |
