# 系统架构

## 概述

ZenTools 是一个纯前端静态工具箱网站，采用**数据驱动 + 渐进增强**架构。核心特征：

- **单一数据源**: `data/tools-data.json` 定义全站 279 个工具的元数据
- **零框架依赖**: 仅使用 HTML5/CSS3/Vanilla JS，无 React/Vue/jQuery
- **本地处理**: 工具逻辑在浏览器端执行，文件不上传服务器
- **多层容错**: anti-crash 引擎提供全局错误捕获和备用模式
- **PWA 支持**: Service Worker 缓存优先策略，支持离线访问

---

## 一、整体架构图

```
┌─────────────────────────────────────────────────────────────────┐
│                        Cloudflare CDN                            │
│                    (zentools.xyz → GitHub Pages)                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS
┌───────────────────────────▼─────────────────────────────────────┐
│                        浏览器端                                  │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Homepage     │  │  Tool Pages   │  │  Category / Search    │  │
│  │  (index.html) │  │  (279 pages)  │  │  (categories.html)   │  │
│  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘  │
│         │                 │                      │               │
│         └────────┬────────┴──────────┬───────────┘               │
│                  │                   │                            │
│  ┌───────────────▼───────────────────▼─────────────────────────┐ │
│  │                    运行时层 (Runtime)                        │ │
│  │                                                              │ │
│  │  ┌────────────┐  ┌───────────┐  ┌────────────┐             │ │
│  │  │ main.js    │  │ tool-ui.js│  │ anti-crash │             │ │
│  │  │ (首页渲染) │  │ (工具UI)  │  │ (全局容错) │             │ │
│  │  └─────┬──────┘  └─────┬─────┘  └──────┬─────┘             │ │
│  │        │               │               │                    │ │
│  │  ┌─────▼───────────────▼───────────────▼─────┐              │ │
│  │  │            common-i18n.js                  │              │ │
│  │  │         (公共翻译字典 + 语言引擎)           │              │ │
│  │  └──────────────────┬───────────────────────┘              │ │
│  └─────────────────────┼──────────────────────────────────────┘ │
│                        │                                         │
│  ┌─────────────────────▼──────────────────────────────────────┐ │
│  │                    数据层 (Data)                            │ │
│  │                                                              │ │
│  │  ┌──────────────────────┐  ┌────────────────────────────┐   │ │
│  │  │  tools-data.json     │  │  localStorage               │   │ │
│  │  │  (279条工具元数据)    │  │  语言/主题/收藏/最近使用     │   │ │
│  │  └──────────┬───────────┘  └─────────────────────────────┘  │ │
│  │             │                                                │ │
│  │  ┌──────────▼───────────┐                                    │ │
│  │  │  tools-data.js       │                                    │ │
│  │  │  (编译后的 JS 数组)   │                                    │ │
│  │  └──────────────────────┘                                    │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    持久化层 (PWA)                            │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │ │
│  │  │ sw.js        │  │ manifest.json│  │ Cache Storage    │   │ │
│  │  │ (SW 主逻辑)  │  │ (PWA 配置)   │  │ (4层缓存策略)    │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────┘   │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    工具执行层 (Tool Runtime)                 │ │
│  │                                                              │ │
│  │  浏览器原生 API: Canvas API / Web Audio API / FileReader     │ │
│  │  第三方 CDN: pdf-lib / JSZip / FileSaver.js                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────────────────┘
```

---

## 二、数据流

### 2.1 工具数据加载流程

```
tools-data.json (654KB, JSON)
       │
       ├─── fetch() ──→ main.js ──→ 首页渲染 (分类卡片 + 工具网格)
       │                          ──→ 全局搜索索引构建
       │
       ├─── <script> ─→ tools-data.js ──→ window.toolsData (279项数组)
       │                                  ──→ tool-ui.js 读取 ──→ 互补工具推荐
       │                                  ──→ 导航搜索下拉列表
       │
       └─── anti-crash.js ──→ JSON 结构校验
                            ──→ 加载失败时激活备用模式 (FALLBACK_DATA)
```

### 2.2 国际化数据流

```
common-i18n.min.js               各页面内联
───────────────                 ──────────
window.ZT_COMMON                window.ZT_PAGE
{ zh: {...}, en: {...},         { zh: {...}, en: {...},
  ja: {...}, vi: {...} }         ja: {...}, vi: {...} }
          │                            │
          └────────┬────────────────────┘
                   │ 合并 (ZT_PAGE 优先级更高)
                   ▼
         ZT.applyLanguage(lang)
                   │
         ┌─────────┼──────────┐
         ▼         ▼          ▼
   [data-i18n]  <title>   #langSelect
   textContent  更新      选项文本更新

触发条件:
  1. DOMContentLoaded (自动)
  2. zt-setlang 自定义事件
  3. #langSelect change 事件
```

### 2.3 页面渲染数据流 (工具详情页)

```
浏览器请求 PDF 压缩页 (/pdf/pdf-compress.html)
       │
       ▼
  HTML 解析开始
       │
       ├── <head>
       │    ├── tool-ui.min.css     (统一 UI 样式)
       │    ├── 内联 <style>         (页面特有样式)
       │    └── SEO 元标签           (OG, Twitter Card, Schema.org)
       │
       ├── <body>
       │    ├── .blob × 2           (光晕背景)
       │    └── .z-wrap
       │         ├── <nav>           (sticky 导航栏, 全局搜索)
       │         ├── .page-header    (面包屑 + 标题 + 描述)
       │         ├── .tool-box       (工具核心 UI)
       │         ├── .section        (说明区: 信息卡片 + 详情)
       │         └── <footer>        (版权 + 链接)
       │
       ├── <script> window.ZT_PAGE = {...}           (页面翻译)
       ├── <script src="common-i18n.min.js">          (公共翻译)
       ├── <script src="tool-ui.min.js">              (UI 框架)
       │    └── 自动执行:
       │         ├── applyLanguage()       (i18n 初始化)
       │         ├── ZT.track.init()       (最近使用记录)
       │         ├── ZT.checkBrowser()     (浏览器兼容检测)
       │         ├── IntersectionObserver   (滚动渐入动画)
       │         ├── 全局搜索注入到 nav
       │         ├── 主题切换按钮注入
       │         ├── 回到顶部按钮注入
       │         ├── 收藏按钮注入
       │         ├── 光晕动画启动
       │         ├── 键盘快捷键注册
       │         ├── 进度条组件注册
       │         └── 互补工具推荐 fetch
       │
       └── <script> (内联业务逻辑)
            ├── 工具核心算法 (如 PDF 压缩、JSON 对比)
            ├── DOM 事件绑定
            ├── Service Worker 注册
            └── 相关工具网格渲染
```

---

## 三、模块分层与职责

### 3.1 核心 JS 模块

| 模块 | 文件 | 行数 | 加载位置 | 职责 |
|------|------|------|---------|------|
| 防崩引擎 | `anti-crash.min.js` | 464 | `<head>` 最先 | 全局错误捕获、JSON 校验、备用模式、健康检查 |
| 国际化引擎 | `common-i18n.min.js` | 120 | 页面底部 | 公共翻译字典 (`ZT_COMMON`)、独立 i18n 应用 |
| 工具 UI 框架 | `tool-ui.min.js` | 601 | 页面底部 | i18n 引擎、收藏/最近使用、进度条、全局搜索、动画、GA |
| 首页渲染 | `main.js` | 227 | 仅首页 | 分类卡片、工具网格、首页搜索、首页 i18n |
| 工具数据 | `tools-data.js` | 12557 | 页面底部 | 279 工具完整数据 (编译自 tools-data.json) |
| 通用工具 | `loader.js` | 143 | 部分页面 | 备用主题系统、渲染函数 |
| 性能辅助 | `app.js` | 13 | 部分页面 | 回到顶部按钮 (轻量辅助) |

### 3.2 加载顺序与依赖

```
加载阶段 (浏览器解析 HTML，顺序加载 <script>):

  [阶段1] <head> 同步加载
    anti-crash.min.js  ← 必须在所有脚本之前，拦截全局错误
       └── 暴露 window.ZT_CRASH
       └── 注册 window.onerror + unhandledrejection
       └── 定期健康检查 (30s 间隔)

  [阶段2] <body> 结尾加载
    common-i18n.min.js ← 翻译字典和基础 i18n 引擎
       └── 暴露 window.ZT_COMMON、applyLanguage()
       └── 自动在 DOMContentLoaded 应用语言

    tools-data.js (如页面需要)
       └── 暴露 window.toolsData[] (279 条)

    tool-ui.min.js ← 工具页面主框架
       └── 依赖: ZT_COMMON (读取), ZT_PAGE (读取), toolsData (可选)
       └── 暴露 window.ZT

    内联 <script> ← 页面业务逻辑
       └── 依赖: ZT (tool-ui.js), ZT_COMMON
       └── 可调用: ZT.showProgress(), ZT.hideProgress(), ZT.checkFileSize()
```

### 3.3 CSS 层

```
style.css (287行)               tool-ui.css (313行)
────────────────                ────────────────
• :root 主题变量                  • :root 主题变量 (复用)
• 首页/分类页/文章页布局           • 工具详情页布局
• .hero / .section / .footer     • nav / .page-header / .tool-box
• 卡片系统 (.tool-card 等)        • .info-grid / .info-card
• 网格系统 (4列 → 2列 → 1列)      • .zt-perf-warn / .zt-progress-wrap
• 动画 (骨架屏 shimmer)            • body::before 噪点纹理
• 全局搜索组件 (nav 内)            • .blob 光晕效果
• 响应式: 1024px, 640px           • 响应式: 1024px, 768px, 640px
```

---

## 四、运行时流程

### 4.1 首次访问首页

```
1. DNS 解析 zentools.xyz → GitHub Pages IP
2. HTTP GET /index.html
3. 浏览器解析 HTML
   ├── <head> anti-crash.min.js 加载并初始化
   │    ├── 拦截 window.fetch (备用模式时)
   │    ├── 注册全局错误处理器
   │    └── 启动 30s 健康检查定时器
   ├── CSS 加载 (style.min.css)
   └── <body> 渲染
4. DOMContentLoaded
   ├── main.js → init()
   │    ├── fetch /data/tools-data.json
   │    │    ├── 成功 → renderCategories() + renderTools()
   │    │    └── 失败 → 使用内联 fallbackCategories + fallbackTools
   │    ├── setupSearch() (首页搜索绑定)
   │    └── getLangFromURL() → applyLanguage()
   └── loader.js → loadData() (备用数据加载)
5. Service Worker 注册 (由 sw.js 处理)
   ├── 首次访问: 安装 → 预缓存核心资源
   └── 后续访问: Fetch 事件 → Cache-First 策略
```

### 4.2 访问工具页面

```
1. 用户点击工具卡片或直接访问 /pdf/pdf-compress.html
2. 浏览器请求 HTML
3. 如已安装 SW: Cache-First → 若命中则直接返回缓存
4. 解析 HTML
   ├── 页面内联 window.ZT_PAGE 定义 (翻译字典)
   ├── 加载 common-i18n.min.js → window.ZT_COMMON
   ├── 加载 tool-ui.min.js
   │    ├── DOMContentLoaded → ZT.applyLanguage()
   │    ├── ZT.track.init() → 添加到最近使用
   │    ├── 注入收藏按钮 (★)
   │    ├── 注入全局搜索到导航栏
   │    ├── 注入主题切换按钮
   │    ├── 注入返回顶部按钮
   │    ├── 启动光晕动画
   │    ├── IntersectionObserver → 滚动渐入
   │    ├── GA 脚本注入
   │    └── 互补工具推荐 fetch
   └── 内联业务逻辑执行 (如 PDF 压缩算法初始化)
5. 用户操作工具 → Canvas API / pdf-lib 等处理
6. ZT.showProgress() / ZT.updateProgress() 显示进度
7. 结果展示 / 文件下载
```

### 4.3 容错降级流程

```
[正常] ──────────────────────────────────────────────────────►

[异常1] JSON 加载失败 (网络错误 / 文件损坏)
  anti-crash.js 捕获 fetch 错误
  └── 错误计数累加
      └── 达到阈值 (5次) → _activateFallbackMode()
          ├── 显示 "备用模式已激活" 红色横幅
          ├── 拦截后续 fetch 请求 → 返回 FALLBACK_DATA
          └── 广播 zt-fallback-mode 事件

[异常2] 运行时 JS 错误
  anti-crash.js 捕获 window.onerror / unhandledrejection
  └── 同上逻辑 → 计数 → 可能激活备用模式

[异常3] 关键 DOM 元素缺失 (健康检查失败)
  _checkHealth() 每 30s 检查 #toolsContainer 等元素
  └── 连续 3 次失败 → 激活备用模式

[备用模式行为]:
  - FALLBACK_DATA 包含 8 个核心分类 + 8 个基础工具
  - 页面可继续浏览基本功能
  - 用户可手动关闭横幅 → ZT_CRASH.dismissFallback()
```

---

## 五、部署架构

```
开发者本地
   │
   │ git push
   ▼
┌─────────────────────────────┐
│  GitHub Repository          │
│  (main branch, 根目录部署)   │
│                             │
│  ├── index.html             │
│  ├── data/tools-data.json   │
│  ├── assets/ (JS/CSS/图片)  │
│  ├── {category}/ (工具页面) │
│  └── tutorials/ (教程)      │
└──────────┬──────────────────┘
           │ GitHub Pages 构建
           ▼
┌─────────────────────────────┐
│  GitHub Pages (github.io)   │
│  ↓ CNAME DNS                 │
│  zentools.xyz               │
└──────────┬──────────────────┘
           │
           ▼
┌─────────────────────────────┐
│  Cloudflare (推测)           │
│  ├── CDN 分发               │
│  ├── HTTPS 终止              │
│  └── 可能的 Workers 处理     │
└─────────────────────────────┘
           │
           ▼
      最终用户浏览器
```

### 部署配置文件

| 文件 | 作用 |
|------|------|
| `.htaccess` | Apache 服务器规则: CSP 安全头, HSTS, Gzip 压缩, 缓存控制 |
| `CNAME` | 域名映射: `zentools.xyz` |
| `.nojekyll` | 禁用 GitHub Pages 的 Jekyll 处理 |
| `robots.txt` | 搜索引擎爬虫规则 |
| `sitemap.xml` | 站点地图 (410 个 URL) |

---

## 六、关键技术决策

### 为什么不用框架？

- **体积为零**: 无 React/Vue 运行时开销，纯 HTML 直接渲染
- **极速首屏**: HTML 量很小 (~5KB Gzip 典型工具页)，无 JS Bundle 解析
- **兼容性**: 不受框架版本升级影响，长期稳定
- **代价**: 组件复用依赖手动维护 HTML 模板一致性

### 为什么用 tools-data.json 而非数据库？

- **无后端**: GitHub Pages 仅支持静态文件
- **便携性**: 一个 JSON 文件描述全站，方便批量编辑和版本控制
- **即时性**: 纯前端 fetch，无 API 延迟
- **代价**: 654KB 文件首次加载较大，但可利用 SW 缓存

### 为什么有 tools-data.json 和 tools-data.js 两份？

- `tools-data.json`: 源数据，供 Python 脚本处理 (校验/统计/添加工具)
- `tools-data.js`: 编译产物，直接以 `<script>` 标签加载，避免 fetch 延迟和跨域问题
- 两者内容一致，仅格式不同

### 为什么有旧版和新版两种页面模板？

- **旧版** (如 image-compressor.html): 全内联 CSS/JS，无导航栏，无标准化结构
- **新版** (如 pdf-compress.html): 加载 tool-ui.css/tool-ui.js，统一导航/页脚/SEO
- 迁移策略: 新工具用新版模板，旧工具逐步重构
