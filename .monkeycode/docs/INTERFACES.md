# 接口定义

## 一、数据模型

### 1.1 tools-data.json 顶层结构

```typescript
interface ToolsDataRoot {
  version: string;              // 数据版本号, 如 "2.2"
  lastUpdated: string;          // 最后更新日期, 如 "2026-06-21"
  categories: string[];         // 13 个中文类别名
  categories__en: string[];     // 英文类别名
  categories__ja: string[];     // 日文类别名
  categories__vi: string[];     // 越南文类别名 (仅12项, 缺"设计工具")
  tools: ToolEntry[];           // 279 个工具条目
}
```

### 1.2 ToolEntry 工具条目模型

```typescript
interface ToolEntry {
  // ── 基础标识 ──
  name: string;                 // 中文名, e.g. "BMI 计算器"
  name__en: string;             // 英文名, e.g. "BMI Calculator"
  name__ja: string;             // 日文名, e.g. "BMI計算機"
  name__vi: string;             // 越南文名, e.g. "Máy tính BMI"
  slug: string;                 // URL 友好标识, e.g. "bmi"
  category: string;             // 所属类别 (中文名), e.g. "生活工具"
  url: string;                  // 页面路径, e.g. "/life/bmi.html"
  icon: string;                 // Emoji 图标, e.g. "⚖️"

  // ── 多语言描述 ──
  description: string;          // 中文描述 (~19-52字)
  description__en: string;
  description__ja: string;
  description__vi: string;

  // ── 状态标记 ──
  featured: boolean;            // 是否精选 (仅 66 个为 true)
  new: boolean;                 // 是否标记为新 (221 个为 true)

  // ── SEO ──
  keywords: string;             // 空格分隔的关键词, e.g. "bmi 体重指数 健康"

  // ── AI/隐私元数据 ──
  ai: AIMetadata;
}

interface AIMetadata {
  free: boolean;                // 是否免费 (全部为 true)
  registration: boolean;        // 是否需要注册
  chinese: boolean;             // 是否支持中文
  languages: string[];          // 支持语言代码 ["zh","en","ja","vi"]
  processing: "browser-local" | "cloud";  // 处理方式
  privacy: string;              // 隐私说明 (中文)
  privacy__en: string;
  privacy__ja: string;
  privacy__vi: string;
  audience: string;             // 目标用户 (中文)
  audience__en: string;
  audience__ja: string;
  audience__vi: string;
  useCases: string;             // 使用场景 (中文)
  useCases__en: string;
  useCases__ja: string;
  useCases__vi: string;
  limits: string;               // 限制说明 (中文)
  limits__en: string;
  limits__ja: string;
  limits__vi: string;
}
```

### 1.3 分类与目录映射

| 中文 category | 英文 | 目录 slug | 工具数 | 首页 URL |
|--------------|------|-----------|--------|----------|
| AI工具 | AI Tools | `/ai/` | 39 | `/ai/index.html` |
| 图片工具 | Image Tools | `/image/` | 55 | `/image/index.html` |
| PDF工具 | PDF Tools | `/pdf/` | 46 | `/pdf/index.html` |
| 文本工具 | Text Tools | `/text/` | 11 | `/text/index.html` |
| 视频工具 | Video Tools | `/video/` | 19 | `/video/index.html` |
| 音频工具 | Audio Tools | `/audio/` | 10 | `/audio/index.html` |
| 开发工具 | Dev Tools | `/dev/`, `/json/`, `/tools/` | 21 | `/dev/index.html` |
| SEO工具 | SEO Tools | `/seo/` | 14 | `/seo/index.html` |
| 办公工具 | Office Tools | (空) | 0 | `/categories.html` |
| 生活工具 | Life Tools | `/life/`, `/tools/` | 42 | `/life/index.html` |
| 金融工具 | Finance Tools | `/finance/`, `/life/` | 12 | `/categories.html` |
| 教育工具 | Education Tools | (空) | 0 | `/categories.html` |
| 设计工具 | Design Tools | `/qr/`, `/tools/` | 10 | `/categories.html` |

---

## 二、JavaScript API

### 2.1 `window.ZT` (tool-ui.js)

全站工具页共享的全局命名空间，挂载于 `window.ZT`。

```typescript
interface ZT {
  // ── i18n ──
  applyLanguage(lang: "zh" | "en" | "ja" | "vi"): void;
  // 合并 ZT_COMMON[lang] + ZT_PAGE[lang]，更新全页 [data-i18n] 元素
  // 同时更新 document.title, document.documentElement.lang, #langSelect

  // ── 收藏与最近使用 ──
  track: {
    init(): void;                    // 初始化，加载 _recent/_fav，添加当前工具
    add(name: string): void;         // 添加到最近使用 (去重, 上限20)
    toggleFav(name: string): boolean; // 切换收藏, 返回是否已收藏
    isFav(): boolean;                // 当前页是否已收藏
    addFavBtn(): void;               // 在 .page-header 注入收藏按钮
    _recent: string[];               // 最近使用列表 (从 localStorage 加载)
    _fav: string[];                  // 收藏列表 (从 localStorage 加载)
  };

  // ── 统计 ──
  clickTrack(url: string, name: string): void;
  // 记录工具点击到 localStorage

  // ── 浏览器检测 ──
  checkBrowser(): void;
  // 检测是否 Chrome/Edge，非推荐浏览器显示提示条

  // ── 文件检查 ──
  checkFileSize(files: FileList, warnEl: HTMLElement, opts?: {
    warnMB?: number;        // 警告阈值 (MB), 默认 50
    errorMB?: number;       // 错误阈值 (MB), 默认 200
    singleLimitMB?: number; // 单文件上限 (MB), 默认 100
  }): void;
  // 检查文件总大小，在 warnEl 上显示性能警告

  // ── 进度条 ──
  showProgress(text?: string, indeterminate?: boolean): void;
  // 显示进度条，indeterminate 为 true 时播放无限循环动画
  updateProgress(percent: number): void;
  // 更新进度 0-100
  hideProgress(): void;
  // 隐藏进度条
}
```

### 2.2 `window.ZT_COMMON` (common-i18n.js)

公共翻译字典，被 `tool-ui.js` 的 `applyLanguage()` 读取合并。

```typescript
interface ZT_COMMON {
  zh: Record<string, string>;  // 约 20 个翻译键
  en: Record<string, string>;
  ja: Record<string, string>;
  vi: Record<string, string>;
}
```

**关键翻译键** (部分):
```
"nav_home"       "nav_all_tools"    "nav_categories"
"search_placeholder"               "lang_label"
"footer_copyright"                 "footer_privacy"
"footer_terms"                     "footer_contact"
"breadcrumb_home"                  "back_to_top"
"theme_dark"     "theme_light"
```

### 2.3 `window.ZT_PAGE` (各页面内联定义)

页面专属翻译字典，每个工具页自行定义，格式与 `ZT_COMMON` 相同。

```typescript
// 典型结构
window.ZT_PAGE = {
  zh: {
    "page_title":       "PDF 压缩 - 在线压缩 PDF 文件",
    "tool_title":       "压缩 PDF 文件",
    "tool_desc":        "选择 PDF 文件进行压缩...",
    "btn_compress":     "开始压缩",
    "info_title_1":     "隐私安全",
    "info_desc_1":      "所有处理在浏览器本地完成...",
    // ...
  },
  en: { /* ... */ },
  ja: { /* ... */ },
  vi: { /* ... */ }
};
```

**命名约定**: 键名使用蛇形命名 (snake_case)，语义化，前后端一致。

### 2.4 `window.ZT_CRASH` (anti-crash.js)

防崩系统对外接口。

```typescript
interface ZT_CRASH {
  VERSION: string;                // "1.0.0"
  fallbackMode: boolean;          // 是否在备用模式
  errorCount: number;             // 累计错误数
  errorLog: ErrorEntry[];         // 错误日志 (上限50条)
  healthy: boolean;               // 页面是否健康
  FALLBACK_DATA: object;          // 备用数据 (8分类 + 8工具)

  validateJSON(jsonStr: string, name: string): boolean;
  validateAllJSON(): Promise<void>;
  backupLocalStorage(): void;
  restoreLocalStorage(): void;
  clearAllData(): void;
  dismissFallback(): void;        // 关闭备用模式横幅
  deactivateFallback(): void;     // 关闭备用模式 (恢复原始 fetch)
  getStatus(): StatusSnapshot;    // 系统状态快照
  help(): void;                   // 控制台输出帮助
}
```

### 2.5 `window.toolsData` (tools-data.js)

全局数组，包含 279 个 `ToolEntry` 对象。用于全局搜索和互补工具推荐。

```typescript
const toolsData: ToolEntry[] = [ /* 279 items */ ];
```

### 2.6 main.js 接口 (仅首页)

```typescript
// 无公开导出的 API，全部在模块作用域内
// 通过 DOM 操作渲染首页内容

// 内部函数签名:
async function loadJSON(path: string, fallback: any): Promise<any>;
function applyLanguage(lang: string): void;
function getLangFromURL(): string;
function renderCategories(categories: string[]): void;
function renderTools(tools: ToolEntry[]): void;
function toolCard(tool: ToolEntry): string;
function setupSearch(): void;
async function init(): void;       // 入口
```

---

## 三、DOM 约定

### 3.1 数据属性 (Data Attributes)

| 属性 | 用途 | 使用位置 |
|------|------|---------|
| `data-i18n="key"` | i18n 文本替换目标 (textContent) | 所有工具页 |
| `data-i18n-placeholder="key"` | i18n placeholder 替换 | input/textarea |
| `data-i18n-page="key"` | 页面专用 i18n (common-i18n.js 使用) | 旧版页面 |
| `data-theme="dark\|light"` | 主题标记 (loader.js 设置) | `<html>` 元素 |

### 3.2 关键 CSS 选择器

#### 新版工具页 (tool-ui 模板)

| 选择器 | 用途 | 注入者 |
|--------|------|--------|
| `#langSelect` | 语言切换下拉框 | 页面硬编码 |
| `.page-header` | 页面头部容器 | 收藏按钮注入目标 |
| `.tool-box` | 工具核心区 | 工具 UI 内容区 |
| `.nav-inner` | 导航栏内部 | 全局搜索注入目标 |
| `.breadcrumb` | 面包屑导航 | applyLanguage 更新 |
| `.info-grid` | 信息卡片网格 (3列) | 工具说明区 |
| `.zt-perf-warn` | 文件大小警告条 | ZT.checkFileSize |
| `.zt-progress-wrap` | 进度条容器 | ZT.showProgress |
| `.zt-browser-reco` | 浏览器推荐条 | ZT.checkBrowser |
| `.zt-backtop` | 回到顶部按钮 | tool-ui.js 注入 |
| `.zt-theme-toggle` | 主题切换按钮 | tool-ui.js 注入 |
| `.fav-btn` | 收藏按钮 | tool-ui.js 注入 |
| `.nav-search` | 导航栏搜索框 | tool-ui.js 注入 |

#### 首页

| 选择器 | 用途 |
|--------|------|
| `#categoryPreview` / `#categoryRibbon` | 分类区域容器 |
| `#toolsGrid` | 常规工具网格 |
| `#aiGrid` | AI 工具专用网格 |
| `#toolSearch` | 首页搜索框 |
| `#recentSection` / `#recentList` | 最近使用区域 |
| `#hotScroll` | 热门工具滚动条 |

### 3.3 事件约定

| 事件 | 触发者 | 监听者 | 用途 |
|------|--------|--------|------|
| `zt-setlang` (CustomEvent) | 语言选择器 | common-i18n.js | 语言切换 |
| `zt-langchange` (CustomEvent) | common-i18n.js | 各页面脚本 | 语言变更通知 |
| `zt-fallback-mode` (CustomEvent) | anti-crash.js | 各模块 | 备用模式激活通知 |
| `change` (lang select) | #langSelect | tool-ui.js | 语言切换 |
| `input` (search) | #toolSearch / .nav-search-input | main.js / tool-ui.js | 搜索过滤 |

---

## 四、CSS 自定义属性

### 4.1 主题变量 (全局 :root)

```css
:root {
  /* 背景 */
  --bg:       #06070d;                      /* 页面主背景 (极深蓝黑) */
  --glass:    rgba(255, 255, 255, 0.04);     /* 毛玻璃半透明背景 */
  --glass-b:  rgba(255, 255, 255, 0.08);     /* 毛玻璃悬停背景 */

  /* 品牌色 */
  --cyan:     #00e5ff;                       /* 主品牌 (青) */
  --purple:   #a855f7;                       /* 辅助品牌 (紫) */
  --pink:     #f43f5e;                       /* 辅助品牌 (粉) */

  /* 文字 */
  --text:     #f0f4ff;                       /* 主文字色 */
  --muted:    #6b7a9f;                       /* 弱化文字色 */

  /* 边框 */
  --border:   rgba(255, 255, 255, 0.07);     /* 边框基础色 */
  --border-h: rgba(0, 229, 255, 0.35);       /* 边框悬停 (青色) */

  /* 半径 */
  --r:        20px;                          /* 统一圆角 */

  /* 光晕 */
  --glow-c:   0 0 40px rgba(0, 229, 255, 0.18);  /* 阴影光晕 (仅 tool-ui.css) */
}
```

### 4.2 响应式断点

| 断点 | 行为 |
|------|------|
| `max-width: 1024px` | 4列网格 → 2列, hero 双列 → 单列 |
| `max-width: 768px` | 导航搜索框缩小 (仅 tool-ui.css) |
| `max-width: 640px` | 2列网格 → 1列, 内边距压缩, info-grid 1列 |

### 4.3 毛玻璃效果

```css
/* 导航栏 */
backdrop-filter: blur(24px) saturate(180%);

/* 卡片 */
backdrop-filter: blur(4px);
background: var(--glass);
border-radius: var(--r);
```

---

## 五、localStorage 键名

| 键名 | 类型 | 用途 | 使用者 |
|------|------|------|--------|
| `zentools_lang` | `"zh"\|"en"\|"ja"\|"vi"` | 语言偏好 | common-i18n.js, tool-ui.js |
| `zentools_theme` | `"dark"\|"light"` | 主题偏好 | loader.js, tool-ui.js |
| `zentools_recent` | `string[]` (JSON) | 最近使用工具列表 (最多5/20) | loader.js (5), ZT.track (20) |
| `zentools_fav` | `string[]` (JSON) | 收藏工具列表 | ZT.track |
| `zt_click_stats` | `object` (JSON) | 工具点击统计 | ZT.clickTrack |
| `zt_backup_data` | `object` (JSON) | localStorage 备份 | anti-crash.js |
| `zt_error_log` | `ErrorEntry[]` (JSON) | 错误日志 | anti-crash.js |
| `zt_fallback_mode` | `string` | 备用模式标记 | anti-crash.js |

---

## 六、Service Worker 缓存策略

`sw.js` 实现四层分类缓存:

| 缓存名 | 内容 | 策略 |
|--------|------|------|
| `zentools-v2-core` | `/`, `index.html`, `manifest.json`, 图标等 | 预缓存, Cache-First |
| `zentools-v2-html` | 所有 `.html` 工具页和教程页 | Cache-First (网络失败时回退) |
| `zentools-v2-data` | tools-data.json 等数据文件 | Network-First (网络失败时用缓存) |
| `zentools-v2-assets` | CSS, JS, 字体, 图片 | Cache-First |

---

## 七、SEO 结构化数据

每个工具页包含以下 JSON-LD:

### FAQPage

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "如何使用 [工具名]?",
      "acceptedAnswer": { "@type": "Answer", "text": "..." }
    }
  ]
}
```

### WebApplication

```json
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "[工具名]",
  "url": "https://zentools.xyz/[path]",
  "description": "[描述]",
  "applicationCategory": "UtilityApplication",
  "operatingSystem": "All",
  "offers": { "@type": "Offer", "price": "0", "priceCurrency": "CNY" }
}
```
