# ZenTools 开发守则文档索引

> 基于 ZT-DCA v1.0（ZenTools Data-Driven Category Architecture）
> 最后更新: 2026-07-07

## 文档导航

| 文档 | 描述 | 目标读者 |
|------|------|---------|
| [ARCHITECTURE.md](./ARCHITECTURE.md) | 系统架构：技术栈、项目结构、子系统、数据流、请求流程、部署架构 | 全部开发者 |
| [INTERFACES.md](./INTERFACES.md) | 接口规范：全局 JS API、数据规范、i18n 接口、页面结构、SW 缓存策略 | 全部开发者 |
| [DEVELOPER_GUIDE.md](./DEVELOPER_GUIDE.md) | 开发者指南：环境搭建、工作流、常见任务、编码规范、项目约束 | 贡献者 |
| [架构原则.md](./架构原则.md) | ZT-DCA 架构：核心原则、目录结构、数据规范、多语言、SEO（原始文档） | 全部开发者 |
| [编写守则.md](./编写守则.md) | 编写注意事项：i18n 细节、统计条、搜索框、UI 风格、常见踩坑（原始文档） | 贡献者 |
| [专有概念/](./专有概念/) | 核心概念详解：i18n 国际化引擎、数据层架构、PWA 离线策略 | 全部开发者 |
| [模块/](./模块/) | 核心模块说明：tool-ui.js、anti-crash.js、sw.js、自动化脚本 | 贡献者 |

## 项目概况

- **名称**: ZenTools - 免费在线工具箱
- **站点**: https://zentools.xyz
- **架构**: ZT-DCA（数据驱动分类架构）
- **技术栈**: 纯静态 HTML5 + CSS3 + Vanilla JS（无框架依赖）
- **规模**: 13 个分类、279 款工具、410+ HTML 页面
- **部署**: GitHub Pages（main 分支根目录）
- **语言**: 简体中文 / English / 日本語 / Tiếng Việt

## 一句话总结

**数据驱动 + 单工具页面 + 4 语 i18n + 本地优先 + 深色卡片 UI**。所有修改尽量不动首页核心代码，改 JSON 和新增页面即可。
