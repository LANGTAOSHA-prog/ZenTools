# tool-ui.js — 全局 JS 引擎

## 文件位置

`assets/js/tool-ui.js`（601 行），对应压缩版 `assets/js/tool-ui.min.js`

## 职责

`tool-ui.js` 是网站的核心 JavaScript 引擎，在每个页面加载时自动运行，提供以下全局功能。

## 功能模块

### 1. 国际化引擎（i18n Engine）

- `initLang()` — 从 localStorage 读取语言设置，默认为 `zh`
- `ZT.applyLanguage(lang)` — 运行时切换语言，遍历 `[data-i18n]` 元素替换文本
- 合并策略：`ZT_PAGE[key]` 覆盖 `ZT_COMMON[key]`
- 语言切换后派发 `zt-langchange` 自定义事件

### 2. 主题切换（Theme Toggle）

- 页面加载时注入暗色/亮色主题切换按钮（右上角）
- 读取 localStorage `zt_theme`，默认为 `dark`
- 通过 CSS 类 `light-mode` 控制 `<body>` 样式
- 切换时写入 localStorage 并更新的元素

### 3. 回到顶部（Back to Top）

- 页面加载时注入回到顶部按钮（右下角）
- 滚动超过 300px 时出现，渐入动画
- 点击平滑滚动到顶部

### 4. 全局搜索（Global Search）

- 注入搜索框到 `.nav-inner`
- 首次搜索时从内存中 fetch `tools-data.json` 并缓存
- 与工具名称、描述和关键词做子串匹配
- 搜索结果按分类分组展示
- 支持键盘导航（ESC 关闭）

### 5. 收藏与最近使用（Favorites & Recent）

- `ZT.track.toggleFav(name)` — 切换收藏，更新 localStorage `zt_favorites`
- `ZT.track.add(name)` — 添加最近使用，更新 localStorage `zt_recent`（最多 50 条）
- `ZT.track.isFav()` — 查询当前页面是否已收藏
- `ZT.track.addFavBtn()` — 在 `.page-header` 末尾注入收藏（★/☆）按钮

### 6. 滚动动画（Scroll Animations）

- IntersectionObserver 监听 `.reveal` 类元素
- 进入视口时添加 `.reveal-visible` 类触发渐入动画
- 用于所有分类页、工具页、教程页

### 7. 浮动光晕（Floating Blobs）

- 页面中 `.blob-1` 和 `.blob-2` 的浮动光晕动画
- 使用 CSS `@keyframes float` + `filter: blur(120px)` 实现
- 速度为 20s 和 25s 交替浮动

### 8. 工具跳转推荐（Tool Navigation）

- 根据 `relatedMap` 为当前工具提供互补工具推荐
- 上一页/下一页快捷导航（分类内）
- 响应式折叠导航栏（汉堡菜单，< 1024px）

### 9. 点击统计（Click Tracking）

- `ZT.clickTrack(url, name)` — 记录点击事件
- 统计数据写入 localStorage `zt_clicks`
- 用于展示热门工具排序

### 10. Service Worker 注册

- 检测 `navigator.serviceWorker`
- 注册 `/sw.js`，scope 为 `/`
- 更新检测：发现新 SW → 通知用户刷新

## 依赖

- `assets/js/common-i18n.js`（window.ZT_COMMON）
- 页面中的 `window.ZT_PAGE`
- `navigator.serviceWorker`（浏览器支持时）
- `IntersectionObserver` API（低版本浏览器降级处理）

## 使用方式

每个页面在 `<body>` 底部引入：

```html
<script src="../assets/js/tool-ui.min.js"></script>
```

无需额外初始化，IIFE 会自动执行所有注册逻辑。

## 注意事项

- `tool-ui.js` 必须在 `common-i18n.js` 之后加载
- 页面专属 JavaScript 逻辑应在 `tool-ui.js` 之后定义
- 重复功能（如自定义搜索框）不应在此实现，应复用全局搜索
- 修改源文件后，务必运行 `python3 _minify_assets.py` 重新生成压缩版
