---
name: i18n-reviewer
description: 检查多语言翻译是否完整（zh/en/ja/vi）
user_invocable: true
disable_model_invocation: false
---

# 国际化审查

检查页面的 `data-i18n` 翻译是否在 4 种语言中都完整覆盖。

## 检查逻辑

1. 收集当前页面所有 `[data-i18n]` 属性的 key
2. 检查 `window.ZT_PAGE` 中每种语言（zh/en/ja/vi）是否都有这些 key
3. 如果某个 key 在某种语言中缺失，报告出来
4. 如果页面使用 `i18n.js`，检查 `translations` 对象中的 coverage

## 输出格式

```
📋 i18n 审查报告
─────────────────
data-i18n keys 总数: N
✅ 中文 (zh): N/N 完整
❌ 英文 (en): 缺失 key1, key2
❌ 日文 (ja): 缺失 key3
✅ 越南文 (vi): N/N 完整
─────────────────
```

全部通过则输出：
```
✅ 国际化审查通过 — 4 种语言翻译完整
```
