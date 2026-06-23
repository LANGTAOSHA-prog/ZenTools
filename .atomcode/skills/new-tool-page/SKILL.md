---
name: new-tool-page
description: 生成新工具页面（含导航、i18n 骨架、广告位）
disable_model_invocation: false
user_invocable: true
---

# 新工具页面生成指南

按照以下步骤生成一个完整的工具页面。

## 步骤

1. 询问用户工具名称、分类（PDF/图片/音频/视频/AI/开发/生活/金融）、用途
2. 用中文回答后，生成 HTML 文件到对应分类目录下
3. 文件命名：`{分类目录}/{工具英文slug}.html`
4. 文件必须包含：
   - `<title>` 和 `<meta description/keywords>`
   - 导航栏（带 `#langSelect`）
   - 面包屑导航
   - `<h1>` 标题（带 `.grad`）
   - `.tool-box` 容器存放工具核心功能
   - AdSense 广告位
   - 页脚（含备案号）
   - 引入 `tool-ui.min.js` 和 `anti-crash.min.js`
   - `data-i18n` 属性（key 命名：`crumbCur`, `eyebrow`, `h1Grad`, `h1Sub`, `pageDesc`, `toolTitle`, `toolNote`, `btnAction` 等）
5. 添加到 `data/tools-data.json` 中
6. 在 `.atomcode/memory.md` 中记录新建的工具路径
