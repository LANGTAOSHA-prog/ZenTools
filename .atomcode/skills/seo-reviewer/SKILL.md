---
name: seo-reviewer
description: 审查页面 SEO 要素（标题、描述、关键词、alt、结构化数据）
user_invocable: true
disable_model_invocation: false
---

# SEO 审查

审查指定 HTML 文件的 SEO 要素是否符合最佳实践。

## 检查项

1. **标题标签**：`<title>` 存在且长度 50-60 字符，包含主要关键词
2. **Meta 描述**：`<meta name="description">` 存在且长度 120-160 字符
3. **Meta 关键词**：`<meta name="keywords">` 存在且内容合理
4. **Canonical URL**：`<link rel="canonical">` 存在
5. **Heading 层级**：只有一个 `<h1>`，标题层级递进（h1 → h2 → h3）
6. **图片 alt 文本**：所有 `<img>` 标签都有 `alt` 属性
7. **结构化数据**：包含 `JSON-LD` 或 `microdata`
8. **Open Graph**：包含 `og:title`, `og:description`, `og:image` meta 标签
9. **移动端适配**：`viewport` meta 标签正确
10. **内链**：面包屑导航和页脚链接正常
11. **加载速度**：检查是否加载了过多外部资源
12. **Hreflang**：多语言页面应包含 `hreflang` 标签

## 输出格式

```
📋 SEO 审查报告 — [文件名]
────────────────────────────────────
🔴 严重: [问题]
🟡 建议: [改进点]
🟢 通过: [通过项]
────────────────────────────────────
SEO 评分: [X]/100
```

所有检查项通过则输出：
```
✅ SEO 审查通过 — 评分 100/100
```
