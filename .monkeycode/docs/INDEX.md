# ZenTools 项目文档索引

> 最后更新: 2026-07-03 | 代码版本: tools-data.json v2.2

## 文档导航

| 文档 | 描述 | 目标读者 |
|------|------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 系统架构：数据流、组件树、运行时流程、部署架构 | 开发者 |
| [INTERFACES.md](./INTERFACES.md) | 接口定义：数据模型、JS API、DOM 约定、CSS 变量 | 前端开发者 |
| [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) | 开发指南：环境搭建、编码规范、新增工具流程、排错 | 贡献者 |

## 模块文档

| 文档 | 描述 |
|------|------|
| [模块/tool-ui.md](./模块/tool-ui.md) | 工具页面共享 UI 模块：i18n 引擎、收藏系统、进度条、全局搜索 |
| [模块/anti-crash.md](./模块/anti-crash.md) | 防崩容错引擎：全局错误捕获、备用模式、JSON 校验、localStorage 备份 |
| [模块/common-i18n.md](./模块/common-i18n.md) | 国际化引擎：公共翻译字典、语言切换、`ZT_PAGE` 约定 |
| [模块/tools-data.md](./模块/tools-data.md) | 工具数据 JSON：279 个工具的完整数据模型与字段规范 |
| [模块/sw.md](./模块/sw.md) | PWA Service Worker：缓存策略、预缓存资源、离线支持 |

## 专有概念

| 文档 | 描述 |
|------|------|
| [专有概念/i18n-系统.md](./专有概念/i18n-系统.md) | 多语言系统完整设计：两层字典合并、翻译键命名、语言切换机制 |
| [专有概念/页面模板.md](./专有概念/页面模板.md) | 工具页面标准模板：新版/旧版差异、SEO 结构、PWA 集成 |
| [专有概念/数据驱动架构.md](./专有概念/数据驱动架构.md) | 单一数据源架构：tools-data.json 如何驱动首页、搜索、推荐 |
| [专有概念/毛玻璃主题.md](./专有概念/毛玻璃主题.md) | 暗色毛玻璃 UI 设计系统：CSS 变量、动画、响应式断点 |

## 项目概况

- **名称**: ZenTools - 免费在线工具箱
- **站点**: https://zentools.xyz
- **技术栈**: 纯静态 HTML5 + CSS3 + Vanilla JS (无框架依赖)
- **规模**: 13 个分类、279 款工具、410+ HTML 页面
- **部署**: GitHub Pages (main 分支根目录)
- **语言**: 简体中文/English/日本語/Tiếng Việt
