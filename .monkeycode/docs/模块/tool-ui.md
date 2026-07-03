# tool-ui.js — 工具页面共享 UI 模块

> 文件: `assets/js/tool-ui.js` (601行) | 压缩版: `assets/js/tool-ui.min.js`
> 加载位置: 所有新版工具详情页 `<body>` 结尾
> 依赖: `window.ZT_COMMON` (common-i18n.js), `window.ZT_PAGE` (页面内联), `toolsData` (可选)

## 概述

`tool-ui.js` 是 ZenTools 工具详情页的**统一 UI 运行时框架**。它提供了工具页面所需的所有通用基础设施，页面开发者只需关注工具本身的业务逻辑。

## 自动执行的功能 (无需手动调用)

工具页面加载 `tool-ui.js` 后，以下功能自动激活:

1. **i18n 初始化**: 从 `localStorage` 读取语言偏好，调用 `ZT.applyLanguage()` 更新页面
2. **光晕动画**: `.blob-1` 和 `.blob-2` 元素的浮动动画 (requestAnimationFrame)
3. **滚动渐入**: IntersectionObserver 监听 `.reveal` 元素，进入视口时显示
4. **回到顶部**: 在页面右下角注入返回顶部按钮 (`.zt-backtop`)
5. **主题切换**: 注入暗色/亮色主题切换按钮 (`.zt-theme-toggle`)
6. **键盘快捷键**: Escape 关闭菜单, `Ctrl+K` 或 `/` 聚焦搜索
7. **全局搜索**: 在 `.nav-inner` 中注入搜索输入框 (`.nav-search`)，提供下拉建议
8. **骨架屏**: 将 `.skeleton-card` 等元素替换为实际内容
9. **收藏按钮**: 在 `.page-header` 注入收藏按钮 (★)
10. **最近使用**: 将当前工具添加到 localStorage 记录
11. **浏览器检测**: 检测非 Chrome/Edge 浏览器并提示
12. **Google Analytics**: 注入 GA4 脚本 (`G-YOUR_MEASUREMENT_ID`)
13. **页面浏览统计**: 当天访问计数
14. **版本信息**: 在 footer 注入构建版本号
15. **互补工具推荐**: 根据预定义的 `relatedMap` 加载相关工具

## 公开 API

### `ZT.applyLanguage(lang)`

```javascript
/**
 * 应用指定语言的翻译到页面
 * @param {"zh"|"en"|"ja"|"vi"} lang - 语言代码
 */
ZT.applyLanguage(lang);
```

**执行流程**:
1. 合并 `ZT_COMMON[lang]` 和 `ZT_PAGE[lang]` 为字典 (ZT_PAGE 优先级高)
2. 设置 `document.documentElement.lang`
3. 更新 `document.title`
4. 遍历所有 `[data-i18n]` 元素 → 设置 `textContent`
5. 遍历所有 `[data-i18n-placeholder]` 元素 → 设置 `placeholder`
6. 保存到 `localStorage.zentools_lang`
7. 同步更新 `#langSelect` 选项文本
8. 派发 `zt-langchange` 自定义事件

### `ZT.track` — 收藏与最近使用

```javascript
ZT.track.init();                    // 初始化，从 localStorage 加载数据
ZT.track.add("PDF 压缩");           // 添加到最近使用 (去重，上限 20)
ZT.track.toggleFav("PDF 压缩");     // 切换收藏状态, 返回 boolean
ZT.track.isFav();                   // 当前页是否已收藏, 返回 boolean
ZT.track.addFavBtn();               // 注入收藏按钮到 .page-header
```

**内部状态**:
- `ZT.track._recent: string[]` — 最近使用工具名列表
- `ZT.track._fav: string[]` — 收藏工具名列表

### `ZT.checkBrowser()`

检测浏览器是否为 Chrome 或 Edge，非推荐浏览器时在页面顶部显示提示条 (`.zt-browser-reco`)。

### `ZT.checkFileSize(files, warnEl, opts)`

```javascript
/**
 * @param {FileList} files - 用户选择的文件列表
 * @param {HTMLElement} warnEl - 警告信息显示元素
 * @param {Object} [opts]
 * @param {number} [opts.warnMB=50] - 警告阈值 (MB)
 * @param {number} [opts.errorMB=200] - 错误阈值 (MB)
 * @param {number} [opts.singleLimitMB=100] - 单文件上限 (MB)
 */
ZT.checkFileSize(files, document.querySelector('.zt-perf-warn'));
```

### `ZT.showProgress` / `ZT.updateProgress` / `ZT.hideProgress`

```javascript
// 显示不确定模式进度条 (无限循环动画)
ZT.showProgress('处理中...', true);

// 显示确定模式进度条
ZT.showProgress('');
ZT.updateProgress(50); // 50%
ZT.updateProgress(100);

// 隐藏
ZT.hideProgress();
```

## 内部架构

### 核心数据结构

#### `relatedMap` — 互补工具推荐

预定义了 30+ 对工具互补关系:

```javascript
const relatedMap = {
  "pdf-merge": ["pdf-split", "pdf-compress"],
  "image-compress": ["image-resize", "image-convert"],
  // ...
};
```

加载规则: 从 toolsData 中找到当前工具的 `relatedMap` 键，将推荐的 slug 匹配到完整 `ToolEntry` 对象并渲染为卡片网格。

#### 全局搜索

`loadTools(cb)` 懒加载 toolsData 用于搜索:

```javascript
loadTools(function(tools) {
  // tools = window.toolsData 或 fetch 的结果
  // 用于按 name/description/category 多语言搜索
});
```

搜索逻辑: 输入文本 → 在 toolsData 中查找匹配 name/name__en/name__ja/name__vi/description/category → 渲染下拉建议列表。

### 语言选择器

`initLang()` 绑定 `#langSelect` 的 `change` 事件:
1. 读取选中值
2. 调用 `ZT.applyLanguage(lang)`
3. 派发 `zt-setlang` 事件 (供 common-i18n.js 监听)

## 使用前提

页面必须满足以下条件, `tool-ui.js` 才能正常工作:

1. **加载顺序**: `common-i18n.js` → `tool-ui.js`
2. **DOM 结构**: 必须有 `.nav-inner`, `.page-header`, `#langSelect`
3. **样式**: 加载 `tool-ui.min.css`
4. **翻译**: 必须定义 `window.ZT_PAGE`
