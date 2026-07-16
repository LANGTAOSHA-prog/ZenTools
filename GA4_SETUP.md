# Google Analytics 4 (GA4) 配置指南

## 快速开始

### 1. 获取 GA4 Measurement ID

1. 访问 [Google Analytics](https://analytics.google.com/)
2. 创建账号和数据流（Web）
3. 复制 Measurement ID，格式为 `G-XXXXXXXXXX`

### 2. 更新网站代码

> **已接入说明**：站点已通过 `assets/js/tool-ui.min.js` 动态注入 GA4，当前生效的 Measurement ID 为 **`G-V3MP20S9Z3`**。无需在 `index.html` 手动粘贴 gtag 片段。

如需更换 ID，编辑 `assets/js/tool-ui.js` 顶部的常量即可（构建后会同步到 `tool-ui.min.js`）：

```js
var GA_ID = 'G-V3MP20S9Z3';  // ← 替换为你的真实 Measurement ID
```

注入逻辑（自动执行，无需手动调用）：

```javascript
if (GA_ID && !window.gtag) {
  var s = document.createElement('script');
  s.async = true;
  s.src = 'https:' + '/www.googletagmanager.com/gtag/js?id=' + GA_ID;
  document.head.appendChild(s);
  window.dataLayer = window.dataLayer || [];
  window.gtag = function(){ dataLayer.push(arguments); };
  gtag('js', new Date());
  gtag('config', GA_ID);
}
```

GA4 默认已自动采集 `page_location` 与 `page_title`，无需额外配置。

### 2.1 多语言切换事件

当用户通过同页 JS 切换语言（zh / en / ja / vi）时，`assets/js/main.js` 的 `applyLanguage()` 会发送自定义事件，便于在 GA4 中分析各语种参与度：

```javascript
if (window.gtag) {
  gtag('event', 'language_switch', { new_language: lang });
}
```

在 GA4 中查看路径：报告 → 参与度 → 事件 → 筛选 `language_switch`，或创建「新语言」维度下钻。

### 3. 验证安装

1. 打开网站
2. 在浏览器开发者工具 Console 中查看是否有 GA4 相关日志
3. 在 GA4 实时报告中查看是否显示活跃用户

## 追踪事件

### 自动追踪的事件

- **页面浏览** - 每个页面的访问
- **出站链接点击** - 点击外部链接
- **工具点击** - 点击使用工具（通过 `trackToolClick()`）
- **搜索行为** - 使用站内搜索（通过 `trackSearch()`）

### 自定义事件参数

#### 工具点击事件 (`tool_click`)
```javascript
{
  tool_url: string,      // 工具 URL
  tool_name: string,     // 工具名称
  referrer: string,      // 来源网址
  device: string,        // 设备信息 (viewport)
  time_of_day: number,   // 小时 (0-23)
  day_of_week: number    // 星期几 (0-6)
}
```

## 数据分析维度

### 1. 来源分析
- 直接访问 (direct)
- 搜索引擎 (google, bing, baidu 等)
- 社交媒体
- 友情链接

### 2. 设备分析
- 屏幕分辨率
- 视口大小
- 操作系统
- 浏览器语言

### 3. 时间分析
- 一天中的时间段
- 一周中的天数
- 首次/最后访问时间

## 导出数据

访问 `/stats.html` 页面可以：
- 查看本地统计数据汇总
- 导出 JSON 格式的完整数据
- 分析热门工具和趋势

## 常见问题

**Q: 为什么看不到实时数据？**
A: GA4 数据处理可能需要几分钟到几小时。

**Q: 如何禁用追踪？**
A: 设置 `window.ga_disable = true` 或在 GA4 管理界面设置排除规则。

**Q: 隐私合规怎么办？**
A: 需要添加 Cookie 同意横幅，并在用户拒绝后不初始化 GA4。
