---
name: html-reviewer
description: 检查 HTML 页面结构是否符合 ZenTools 规范
user_invocable: true
disable_model_invocation: false
---

# HTML 结构审查

审查指定 HTML 文件是否符合 ZenTools 项目规范。

## 检查项

1. **DOCTYPE 和编码**：`<!DOCTYPE html>` + `<meta charset="UTF-8">`
2. **响应式 viewport**：`<meta name="viewport" content="width=device-width, initial-scale=1.0">`
3. **data-i18n 属性**：所有可见文本使用了 `data-i18n` 属性
4. **导航栏**：包含 `#langSelect` 语言切换下拉框
5. **面包屑导航**：`.breadcrumb` 结构完整
6. **标题层级**：`<h1>` 带 `.grad` 类，内容不为空
7. **广告位**：包含 AdSense 插入点（`class="adsbygoogle"`）
8. **页脚**：包含备案号链接和 `footerCopy`
9. **脚本加载**：加载了 `tool-ui.min.js` 和 `anti-crash.min.js`
10. **暗色主题兼容**：使用 CSS 变量体系（`var(--bg)`, `var(--card)` 等）

## 输出格式

对于每个问题，输出：
```
❌ [问题类型] [具体描述] → [第几行]
```
全部通过则输出：
```
✅ HTML 结构审查通过
```
