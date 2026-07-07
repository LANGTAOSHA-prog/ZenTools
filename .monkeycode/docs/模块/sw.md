# sw.js — Service Worker

## 文件位置

`sw.js`（187 行）

## 职责

实现 PWA 离线缓存功能，确保工具页面在离线或网络不稳定时仍可访问。

## 架构

### 缓存策略：Cache-First

所有请求优先从缓存中获取。缓存命中直接返回；缓存未命中则 fetch 并写入缓存。

### 版本管理

```js
const VERSION = 'zentools-v2';
```

### 生命周期

```
install 事件
    │
    ├── 预缓存 -core（首页、manifest、图标）
    ├── 预缓存 -assets（CSS/JS 文件）
    ├── 预缓存 -data（tools-data.json）
    └── 预缓存 -pages（部分分类首页）

activate 事件
    │
    └── 清理旧版本缓存

fetch 事件
    │
    ├── 工具页面 → 缓存优先 → 写入 -html（LRU，最多 200）
    ├── 分类首页 → 缓存优先 → 写入 -pages
    └── 其他请求 → 不缓存（GA/AdSense）
```

### 工具页面缓存 LRU

`-html` 缓存使用 LRU 淘汰策略：
- 缓存 key 为页面完整 URL
- 维护有序列表记录最近访问时间
- 缓存满 200 条时自动删除最久未使用的条目

### 离线回退

当 fetch 失败且缓存未命中时，返回 `/offline.html`（需确保该文件存在）。

## 请求类型处理

| URL 模式 | 处理方式 |
|---------|---------|
| 匹配 `TOOL_PAGE_PATTERN` | 缓存到 `-html` |
| 分类首页（如 `/pdf/index.html`） | 缓存到 `-pages` |
| `assets/css/*`、`assets/js/*` | 安装时预缓存 |
| `data/tools-data.json` | 安装时预缓存 |
| Google Analytics / AdSense | 直接 fetch，不缓存 |

## 注册方式

每个页面自动注册（由 `tool-ui.js` 处理）：

```js
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/sw.js');
}
```

## 更新流程

1. 修改 `sw.js` 并部署
2. 浏览器检测到新的 Service Worker
3. 新 SW 进入 `install` → `waiting` 状态
4. 关闭所有旧标签页或调用 `skipWaiting`
5. 新 SW 进入 `activate` → 清理旧缓存
6. 下一次页面加载使用新缓存

## 注意事项

- Service Worker 仅在 HTTPS 环境下工作（GitHub Pages 提供 HTTPS）
- 开发时可用 Chrome DevTools → Application → Service Workers 调试
- `sw.js` 路径必须在根目录（scope 为 `/`）
- 修改 `sw.js` 后需等待旧 SW 过期或手动 skipWaiting
