# anti-crash.js — 防崩引擎

## 文件位置

`assets/js/anti-crash.js`（464 行），对应压缩版 `assets/js/anti-crash.min.js`

## 职责

`anti-crash.js` 是网站的防御性基础设施，必须在 `<head>` 中最早加载，用于捕获全局异常、自动切换备用模式，确保即使在出现 JavaScript 错误的情况下用户仍能正常浏览。

## 防御机制

### 1. 全局错误捕获

```js
window.onerror = function(message, source, lineno, colno, error) { ... };
window.addEventListener('unhandledrejection', function(event) { ... });
```

捕获所有未处理的 JavaScript 错误和 Promise rejection，记录到 `localStorage('zt_crash_log')`。

### 2. JSON 自动校验

拦截 `XMLHttpRequest` 和 `fetch` 对 `tools-data.json` 的请求，在返回前校验 JSON 格式完整性。若 JSON 格式错误，阻止后续代码使用损坏的数据。

### 3. 备用模式（Fallback Mode）

当 5 秒内连续出现 5+ 个错误时，自动启用备用模式：
- 设置 `localStorage('zt_fallback_active', '1')`
- 禁用动态渲染（只显示静态 HTML 内容）
- 显示恢复提示横幅
- 用户可通过"恢复正常模式"按钮或 `recovery-console.html` 手动恢复

### 4. 健康检查（Health Check）

每 30 秒运行一次关键 DOM 元素健康检查：
- 导航栏
- 主要内容区
- 页脚

若关键元素丢失，尝试从 localStorage 缓存的快照恢复。

### 5. localStorage 备份与恢复

- 每次写入 localStorage 时同步备份到 `zt_ls_backup` 键
- 页面加载时检测 localStorage 是否可用
- 若 localStorage 被清空，从备份恢复

### 6. 恢复控制台

`recovery-console.html` 提供独立的恢复界面：
- 查看崩溃日志
- 手动清除崩溃状态
- 重置所有 localStorage 数据
- 手动切回正常模式

## 依赖

- 无外部依赖（必须最先加载）
- `localStorage` API
- `XMLHttpRequest` / `fetch`（拦截）
- `console` API

## 加载顺序

在所有页面 `<head>` 中必须第一个加载：

```html
<head>
  <script src="../assets/js/anti-crash.min.js"></script>
  <!-- 其他脚本和样式 -->
</head>
```

## 日志格式

崩溃日志写入 `localStorage('zt_crash_log')`，JSON 数组格式：

```json
[
  {
    "time": "2026-07-07T12:00:00.000Z",
    "message": "TypeError: Cannot read property 'xxx' of undefined",
    "source": "https://zentools.xyz/pdf/pdf-merge.html",
    "lineno": 245,
    "colno": 12
  }
]
```

最多保留 50 条日志，超出自动丢弃最旧条目。

## 注意事项

- 必须在所有其他脚本之前加载
- 备用模式主要影响动态渲染（搜索、分类页），对静态工具页面影响较小
- 用户手动关闭备用模式后，需刷新页面生效
- 健康检查可能被浏览器 throttling 延迟
