# sw.js — PWA Service Worker

> 文件: `sw.js` (187行) | 代理: `service-worker.js` (2行, 委托到 sw.js)
> 注册: 各工具页面内联 `navigator.serviceWorker.register('/sw.js')`

## 概述

`sw.js` 是 ZenTools 的 PWA Service Worker，采用**分层缓存优先 (Cache-First)** 策略，支持离线访问和快速加载。

## 缓存架构

### 四层分类缓存

| 缓存名 | 策略 | 内容 | 用途 |
|--------|------|------|------|
| `zentools-v2-core` | 预缓存 + Cache-First | 首页, manifest.json, 图标 | 应用外壳 |
| `zentools-v2-html` | Cache-First + 网络回退 | 所有 `.html` 工具页和教程页 | 页面快速加载 |
| `zentools-v2-data` | Network-First + 缓存回退 | tools-data.json 等数据文件 | 数据实时性 |
| `zentools-v2-assets` | Cache-First | CSS, JS, 字体, 图片 | 静态资源加速 |

### 预缓存资源 (install 事件)

```javascript
const CORE_ASSETS = [
  '/', '/index.html', '/tools.html',
  '/manifest.json', '/favicon.svg',
  '/icon-192x192.png', '/icon-512x512.png'
];

const STATIC_ASSETS = [
  '/assets/css/style.min.css', '/assets/css/tool-ui.min.css',
  '/assets/js/common-i18n.min.js', '/assets/js/tool-ui.min.js',
  '/assets/js/anti-crash.min.js'
];

const CATEGORY_PAGES = [
  '/image/index.html', '/pdf/index.html', '/ai/index.html',
  '/dev/index.html', '/life/index.html', '/text/index.html',
  '/audio/index.html', '/video/index.html', '/seo/index.html',
  '/finance/index.html', '/qr/index.html'
];
```

## 缓存策略说明

### Cache-First (HTML / Assets)

```
请求 → 检查缓存
  ├── 命中 → 返回缓存
  └── 未命中 → 网络请求
       ├── 成功 → 存入缓存 + 返回
       └── 失败 → 返回离线页面
```

### Network-First (Data)

```
请求 → 网络请求
  ├── 成功 → 更新缓存 + 返回
  └── 失败 → 检查缓存
       ├── 命中 → 返回缓存
       └── 未命中 → 错误
```

## 生命周期

```
install  → 预缓存 CORE_ASSETS + STATIC_ASSETS + CATEGORY_PAGES
activate → 清理旧版本缓存
fetch    → 根据 URL 类型选择缓存策略
```

## manifest.json 配置

```json
{
  "name": "ZenTools - 免费在线工具箱",
  "short_name": "ZenTools",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#06070d",
  "theme_color": "#00e5ff",
  "icons": [
    { "src": "/icon-192x192.png", "sizes": "192x192" },
    { "src": "/icon-512x512.png", "sizes": "512x512" }
  ],
  "shortcuts": [
    { "name": "图片工具", "url": "/image/" },
    { "name": "PDF工具", "url": "/pdf/" },
    { "name": "AI工具", "url": "/ai/" },
    { "name": "开发工具", "url": "/dev/" }
  ]
}
```

## 调试

```javascript
// 查看缓存状态
caches.keys().then(console.log);

// 清除所有缓存
caches.keys().then(keys => keys.forEach(k => caches.delete(k)));

// 查看 SW 状态
navigator.serviceWorker.getRegistration().then(reg => {
  console.log(reg.active ? '活跃' : '等待中');
});
```
