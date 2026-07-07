# PWA 离线策略

## 概述

ZenTools 实现了完整的 Progressive Web App（PWA）能力，支持独立安装到设备主屏幕和离线访问。核心组件是 `sw.js`（Service Worker）和 `manifest.json`（Web App Manifest）。

## Service Worker 架构

`sw.js` 在页面首次加载时注册，采用 cache-first（缓存优先）策略。

### 版本管理

```js
const VERSION = 'zentools-v2';
```

版本号用于命名缓存空间。更改版本号后，旧缓存自动清除，新缓存重新建立。

### 5 层缓存体系

| 缓存名 | 内容 | 安装时机 | 清理触发 |
|--------|------|---------|---------|
| `zentools-v2-core` | 首页、tools.html、about.html、manifest.json、图标、favicon、offline.html | install 事件 | 版本号变更 |
| `zentools-v2-assets` | `assets/css/*`、`assets/js/*` | install 事件 | 版本号变更 |
| `zentools-v2-data` | `data/tools-data.json` | install 事件 | 版本号变更 |
| `zentools-v2-html` | 匹配 TOOL_PAGE_PATTERN 的工具页面 | fetch 事件（动态） | LRU（最多 200 条） |
| `zentools-v2-pages` | 分类首页 + tutorials/guides 列表页 | install 事件（部分）+ fetch（追加） | 版本号变更 |

### 请求拦截策略

```
用户发起请求
     │
     ▼
┌────────────┐   匹配工具页面 URL    ┌─────────────┐
│ sw.js      │ ─────────────────→   │ 检查缓存     │
│ fetch 事件  │                      │             │
└────────────┘                      │ 命中 → 返回  │
     │                              │ 未中 → fetch │
     │ 不匹配                       │ 并缓存       │
     ▼                              └─────────────┘
┌────────────┐
│ 直接 fetch  │  (不缓存，如 GA/AdSense 请求)
└────────────┘
```

## Web App Manifest

```json
{
  "name": "ZenTools - 在线工具箱",
  "short_name": "ZenTools",
  "start_url": "/",
  "display": "standalone",
  "theme_color": "#0a1628",
  "background_color": "#0a1628",
  "icons": [
    { "src": "/icon-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icon-512x512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

## 离线体验

当用户离线访问工具页面时：
1. 若页面已在 `-html` 缓存中 — 直接从缓存返回
2. 若页面未缓存 — 返回 `offline.html`（离线提示页）
3. 所有页面加载后自动注册 `sw.js`，下次访问即可离线使用

## 清理与更新

- 更改 `VERSION` 常量即可触发全量清理
- 工具页面缓存（`-html`）采用 LRU 策略，自动淘汰最久未使用的条目
- 用户需要在新版本 Service Worker 激活后刷新页面才能获得最新缓存

## 注意事项

- Service Worker 仅在 HTTPS 环境下注册（GitHub Pages 提供 HTTPS）
- 开发环境（localhost）可以正常注册和测试
- `sw.js` 不缓存 Google Analytics 和 AdSense 请求
- 修改 `sw.js` 后，旧 Service Worker 会在下一次页面加载时自动更新
