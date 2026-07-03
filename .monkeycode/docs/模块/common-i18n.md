# common-i18n.js — 国际化引擎

> 文件: `assets/js/common-i18n.js` (120行) | 压缩版: `assets/js/common-i18n.min.js`
> 加载位置: 所有新版工具页 `<body>` 结尾，在 `tool-ui.js` 之前
> 依赖: `window.ZT_PAGE` (页面内联定义)

## 概述

`common-i18n.js` 提供全站共享的公共翻译字典 (`ZT_COMMON`) 和一个独立的轻量 i18n 应用引擎。它定义了导航栏、页脚、搜索占位符、面包屑等跨页面通用的 UI 文本的四语言翻译。

## 数据结构: `window.ZT_COMMON`

```javascript
window.ZT_COMMON = {
  zh: {
    "nav_home": "首页",
    "nav_all_tools": "全部工具",
    "nav_categories": "分类",
    "search_placeholder": "搜索工具...",
    "lang_label": "语言",
    "footer_copyright": "© 2026 ZenTools",
    "footer_privacy": "隐私政策",
    "footer_terms": "服务条款",
    "footer_contact": "联系我们",
    "breadcrumb_home": "首页",
    "back_to_top": "回到顶部",
    "theme_dark": "暗色模式",
    "theme_light": "亮色模式",
    // 约 20 个键
  },
  en: {
    "nav_home": "Home",
    "nav_all_tools": "All Tools",
    // ...
  },
  ja: {
    "nav_home": "ホーム",
    "nav_all_tools": "すべてのツール",
    // ...
  },
  vi: {
    "nav_home": "Trang chủ",
    "nav_all_tools": "Tất cả công cụ",
    // ...
  }
};
```

## 核心函数: `applyLanguage(lang)`

这是一个**独立的** i18n 应用引擎 (比 `tool-ui.js` 中的版本更早实现)。

```javascript
function applyLanguage(lang) {
  // 1. 合并 ZT_COMMON[lang] + ZT_PAGE[lang] 为字典
  var dict = {};
  if (ZT_COMMON && ZT_COMMON[lang]) Object.assign(dict, ZT_COMMON[lang]);
  if (ZT_PAGE && ZT_PAGE[lang]) Object.assign(dict, ZT_PAGE[lang]);

  // 2. 设置 HTML lang 属性
  document.documentElement.lang = lang === 'zh' ? 'zh-CN' :
    lang === 'ja' ? 'ja-JP' : lang === 'vi' ? 'vi-VN' : 'en-US';

  // 3. 更新 [data-i18n] 元素的 textContent
  document.querySelectorAll('[data-i18n]').forEach(function(el) {
    var key = el.getAttribute('data-i18n');
    if (dict[key]) el.textContent = dict[key];
  });

  // 4. 更新 [data-i18n-page] 元素 (旧版页面使用)
  // ...

  // 5. 保存语言偏好
  localStorage.setItem('zentools_lang', lang);

  // 6. 派发事件通知其他模块
  document.dispatchEvent(new CustomEvent('zt-langchange', { detail: { lang: lang } }));
}
```

## 与 tool-ui.js 的关系

两者都包含 i18n 引擎，但配合使用:

| 模块 | `applyLanguage` | 职责 |
|------|----------------|------|
| common-i18n.js | 独立实现 | 提供字典 + 基础 DOM 更新 |
| tool-ui.js | `ZT.applyLanguage()` | 增强版: 同步 #langSelect, 更新 title, 支持 placeholder |

**实际运行**: `tool-ui.js` 加载后会接管语言切换逻辑。`common-i18n.js` 的 `applyLanguage` 函数可能在 `DOMContentLoaded` 时先执行一次 (确保第一时间应用翻译)，之后由 `tool-ui.js` 的 `ZT.applyLanguage()` 处理。

## 事件机制

| 事件 | 方向 | 用途 |
|------|------|------|
| `zt-setlang` | 外部 → common-i18n | 切换语言 (由 tool-ui.js 的语言选择器派发) |
| `zt-langchange` | common-i18n → 外部 | 语言已变更通知 (供其他脚本监听) |

## 语言检测优先级

```
localStorage.zentools_lang   (用户偏好)
    ↓ 未设置
navigator.language           (浏览器默认, 取前2字符)
    ↓ 无法识别
'zh'                         (默认中文)
```

## 新增公共翻译键

编辑 `assets/js/common-i18n.js`，在 4 种语言的字典中同时添加:

```javascript
// 在所有 4 个语言对象中添加
zh: { ..., "new_key": "新文本" }
en: { ..., "new_key": "New Text" }
ja: { ..., "new_key": "新しいテキスト" }
vi: { ..., "new_key": "Văn bản mới" }
```

同时需要在 HTML 中使用 `data-i18n="new_key"` 标记目标元素。

> 注意: 修改 `common-i18n.js` 后需重新运行 `_minify_assets.py` 更新 `.min.js` 文件。
