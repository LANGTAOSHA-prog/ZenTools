# 项目状态总结

## Goal
- 首页更新目录自动同步：新增 `_changelog_utils.py` 公共模块，修改三个生成脚本使 changelog 自动更新，创建独立同步脚本，并重新设计 `tools.html` 和 `index.html` 布局。

## Constraints & Preferences
- 纯静态 HTML/CSS/JS，不引入框架
- zh/en/ja/vi 四语言支持
- 使用 tool-ui.min.css / common-i18n.min.js / tool-ui.min.js 共享资源
- 提交并推送到 `origin/main`
- 变更项需四语言，当日聚合到同一 changelog 条目

## Progress
### Done
- 需求文档 + 设计文档 + 任务列表：`.monkeycode/specs/260707-auto-changelog/` (`f66450a`)
- `_changelog_utils.py` 创建：`load_site_info`、`save_site_info`、`build_tool_entry`、`build_tutorial_entry`、`build_guide_entry`、`append_changelog`（当日聚合）、`sync_metadata` (`f66450a`)
- `test_changelog_utils.py` 创建：8 个用例全部通过（四语言条目、当日聚合、跨日新建、去重、元数据同步）(`f66450a`)
- `_add_tool.py` 修改：JSON 写入成功后自动追加 changelog (`f66450a`)
- `_add_tutorial.py` 修改：HTML 生成后自动追加 changelog (`f66450a`)
- `_add_guide.py` 修改：HTML 生成后自动追加 changelog (`f66450a`)
- `_sync_changelog.py` 创建：`--scan` 扫描 `new: true` 工具追加 / `--reset` 重建元数据 (`f66450a`)
- `test_sync_changelog.py` 创建：2 个用例全部通过 (`f66450a`)
- 端到端验证：`_add_tool.py --slug test-auto-changelog` 后 `site-info.json` 的 `lastUpdated`、`toolCount`、`changelog` 均正确更新，当日聚合成功
- AGENTS.md 更新：添加脚本加载顺序、工具页面骨架、CSS 变量规则、校验流水线等 (`f66450a`)
- `compare/index.html` 重新设计：对比主题 "The Duel"、VS 双色调卡片、水平 pill 推荐资源 (`a2e118f`)
- `index.html` 主页重新设计：全屏居中 Hero、面包屑行、Changelog 仅保留页面底部卡片式布局 (`1f21e45` → `a2e118f`)
- 以上均已推送至 `origin/main`

### In Progress
- (none)

### Blocked
- (none)

## Key Decisions
- changelog 操作提取为独立模块 `_changelog_utils.py`，供三个脚本和 `_sync_changelog.py` 复用
- 当日聚合策略：同一日多次添加合并到同一 changelog 条目，追加到 `items` 数组而非创建新条目
- 非侵入式修改：三个生成脚本的 changelog 更新用 try/except 包裹，失败时打印警告不中断主流程
- `tools.html` 从自定义 `site-header` 对齐为标准 ZenTools 页面骨架（blobs + z-wrap + breadcrumb + footer-inner）
- `index.html` 全新设计风格：全屏居中 Hero、时间轴 Changelog，不跟随 tools.html 风格

## Next Steps
- (all tasks completed)

## Critical Context
- 项目为纯静态 HTML/CSS/JS 工具箱网站（ZT-DCA 架构），13 分类、279 工具
- i18n 引擎：`ZT_PAGE`（页面翻译）+ `ZT_COMMON`（公共翻译）合并后由 `ZT.applyLanguage()` 渲染
- `data/site-info.json` 是 changelog 的唯一数据源，主页 `index.html` 从它读取并渲染时间轴
- 三个生成脚本：`_add_tool.py`、`_add_tutorial.py`、`_add_guide.py`
- Post-edit 校验流水线：`_check_json.py` → `_sync_tools_data_js.py` → `_gen_sitemap.py` → `_minify_assets.py`
- 上一个会话（已暂停）：Dify vs n8n 对比评测文章已完成，Project Wiki 文档已生成，发布流程暂停

## Relevant Files
- `_changelog_utils.py` — changelog 公共操作模块（新增）
- `_sync_changelog.py` — 独立同步/修复脚本（新增）
- `_add_tool.py` — 已修改：集成 changelog 自动更新
- `_add_tutorial.py` — 已修改：集成 changelog 自动更新
- `_add_guide.py` — 已修改：集成 changelog 自动更新
- `data/site-info.json` — changelog 数据源，脚本自动写入
- `tools.html` — 已重新设计布局
- `index.html` — 已重新设计：全屏 Hero、面包屑、Changelog 时间轴
- `AGENTS.md` — 已更新项目开发指南
- `.monkeycode/specs/260707-auto-changelog/` — 需求/设计/任务文档