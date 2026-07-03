# anti-crash.js — 防崩容错引擎

> 文件: `assets/js/anti-crash.js` (464行) | 压缩版: `assets/js/anti-crash.min.js`
> 加载位置: `<head>` 中最先加载 (必须在所有其他脚本之前)
> 版本: 1.0.0
> 依赖: 无 (完全独立)

## 概述

`anti-crash.js` 是 ZenTools 的**核心安全气囊**。当 JSON 数据加载失败、运行时出现大量 JS 错误或关键 DOM 元素缺失时，自动切换到内置备用数据，确保站点核心功能不崩溃。

## 核心机制

### 1. 全局错误捕获

```javascript
// 同步错误
window.onerror = function(msg, url, line, col, error) { ... }

// Promise 拒绝
window.addEventListener('unhandledrejection', function(event) { ... })
```

**行为**: 每次错误 → `errorCount++`，写入 `errorLog` (上限 50 条) → 检查是否达到阈值。

### 2. 备用模式触发条件

任一条件满足即触发:
- `errorCount >= 5` (累计 5 次 JS 错误)
- JSON 数据校验失败
- 健康检查连续 3 次失败

### 3. 备用模式行为

```javascript
_activateFallbackMode(reason)
  ├── 设置 fallbackMode = true
  ├── 显示红色横幅 "备用模式已激活"
  ├── 拦截 window.fetch → 对配置的 JSON URL 返回 FALLBACK_DATA
  ├── 广播 zt-fallback-mode 自定义事件
  └── 记录到 localStorage
```

### 4. 健康检查

每 30 秒执行一次:
```javascript
_checkHealth()
  ├── 检查关键 DOM 元素存在性: #toolsContainer, #statsBar, #megaMenu, nav .logo
  ├── 连续 3 次失败 → 激活备用模式
  └── 任一元素存在 → 重置失败计数
```

## 配置

```javascript
const CONFIG = {
  MAX_ERRORS: 5,              // 最大错误数
  MAX_ERROR_LOG: 50,          // 错误日志上限
  HEALTH_INTERVAL: 30000,     // 健康检查间隔 (ms)
  JSON_URLS: [                // 需要监控的 JSON 文件
    '/data/tools-data.json',
    '/data/tools.json',
    '/data/translations.json',
    '/data/categories.json'
  ],
  KEY_ELEMENTS: [             // 健康检查目标
    '#toolsContainer',
    '#statsBar',
    '#megaMenu',
    'nav .logo'
  ]
};
```

## 备用数据 (FALLBACK_DATA)

内置 8 个核心分类 + 8 个基础工具，确保即使完全崩溃也有基础内容:

```javascript
FALLBACK_DATA = {
  categories: ['PDF工具', '图片工具', '文本工具', '开发工具', 'AI工具', '视频工具', '音频工具', '生活工具'],
  tools: [
    { name: 'PDF 合并', url: '/pdf/pdf-merge.html', icon: '📄', category: 'PDF工具' },
    { name: '图片压缩', url: '/image/image-compress.html', icon: '📦', category: '图片工具' },
    { name: '文本对比', url: '/text/diff.html', icon: '📝', category: '文本工具' },
    { name: 'JSON 格式化', url: '/dev/json-formatter.html', icon: '💻', category: '开发工具' },
    { name: 'AI 写作', url: '/ai/ai-writer.html', icon: '🤖', category: 'AI工具' },
    { name: '视频压缩', url: '/video/video-compress.html', icon: '🎬', category: '视频工具' },
    { name: '音频裁剪', url: '/audio/audio-trim.html', icon: '🎵', category: '音频工具' },
    { name: 'BMI 计算', url: '/life/bmi.html', icon: '⚖️', category: '生活工具' }
  ]
};
```

## 公开 API

```javascript
// 系统状态
ZT_CRASH.VERSION        // "1.0.0"
ZT_CRASH.fallbackMode   // boolean
ZT_CRASH.errorCount     // number
ZT_CRASH.errorLog       // array (最多50条)
ZT_CRASH.healthy        // boolean

// 数据校验
ZT_CRASH.validateJSON(jsonStr, name)  // → boolean
ZT_CRASH.validateAllJSON()            // → Promise<void>

// localStorage 管理
ZT_CRASH.backupLocalStorage()
ZT_CRASH.restoreLocalStorage()
ZT_CRASH.clearAllData()

// 备用模式控制
ZT_CRASH.dismissFallback()      // 关闭横幅 (淡出动画)
ZT_CRASH.deactivateFallback()   // 完全关闭备用模式 (恢复原始 fetch)

// 诊断
ZT_CRASH.getStatus()            // → { version, fallbackMode, errorCount, healthy, ... }
ZT_CRASH.help()                 // 控制台输出可用命令
```

## localStorage 数据

| 键名 | 内容 | 用途 |
|------|------|------|
| `zt_error_log` | `ErrorEntry[]` (JSON) | 错误日志, 每条含时间戳、消息、堆栈 |
| `zt_fallback_mode` | `"true"` | 备用模式标记 |
| `zt_backup_data` | `object` (JSON) | localStorage 备份快照 |
| `zt_health_fails` | `number` | 健康检查连续失败次数 |

## 调试

浏览器控制台:

```javascript
// 查看完整状态
ZT_CRASH.getStatus()

// 手动触发备用模式
ZT_CRASH.errorCount = 10;  // 下次健康检查/错误时触发

// 关闭备用模式
ZT_CRASH.deactivateFallback();

// 清除所有数据
ZT_CRASH.clearAllData();

// 查看帮助
ZT_CRASH.help();
```
