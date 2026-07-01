# 免费 AI 模型聚合平台 - 配置说明

## 📋 快速配置指南

### 1. 基本配置

编辑 `index.html` 文件中的 `SOURCES` 数组：

```javascript
const SOURCES = [
    {
        name: 'Mistral 7B (Free)',           // 显示名称
        url: 'https://openrouter.ai/api/v1/chat/completions',  // API 地址
        model: 'mistralai/mistral-7b-instruct:free',            // 模型标识符
        headers: { 
            'Content-Type': 'application/json' 
        }
    },
    // 添加更多源...
];
```

### 2. 添加认证信息

如果 API 需要认证，在 `headers` 中添加：

```javascript
{
    name: 'My Paid API',
    url: 'https://api.example.com/v1/chat',
    model: 'my-model',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_API_KEY_HERE'
    }
}
```

**安全提示**：不要将包含真实 API Key 的代码提交到公共仓库！

### 3. 自定义超时时间

默认超时为 15 秒，修改第 248 行：

```javascript
const timeoutId = setTimeout(() => controller.abort(), 15000); // 改为 30000 表示 30 秒
```

### 4. 调整响应长度

默认最大 token 数为 500，修改第 236 行：

```javascript
const payload = {
    model: src.model,
    messages: [{ role: 'user', content: prompt }],
    max_tokens: 1000,  // 增加到 2000 或更大
    temperature: 0.7,
};
```

### 5. 修改请求顺序

直接调整 `SOURCES` 数组的顺序即可。OpenRouter 的源会被优先尝试（因为成功率较高）。

### 6. 添加额外请求头

某些 API 可能需要额外的 header：

```javascript
{
    name: 'Custom API',
    url: 'https://api.example.com/v1/chat',
    model: 'custom-model',
    headers: {
        'Content-Type': 'application/json',
        'X-API-Version': '2024-01-01',
        'X-Client-ID': 'my-app-id'
    }
}
```

## 🔧 高级配置

### 并发请求模式

默认是串行请求（一个接一个），如需并发修改核心函数：

```javascript
// 替换 fetchWithFallback 函数中的循环部分
const results = await Promise.allSettled(
    sources.map(async (src) => {
        try {
            const resp = await fetch(src.url, { /* ... */ });
            return { source: src.name, success: true, data: await resp.json() };
        } catch (err) {
            return { source: src.name, success: false, error: err.message };
        }
    })
);

// 找到第一个成功的结果
const successResult = results.find(r => r.status === 'fulfilled' && r.value.success);
```

### 添加日志记录

在浏览器控制台添加详细日志：

```javascript
// 在循环开始前添加
console.group('API 轮询调试');
console.log('总源数量:', sources.length);
sources.forEach((s, i) => console.log(`源 ${i + 1}:`, s.name));

// 在每个请求后添加
console.log(`✅ ${src.name} 成功`, content);
console.warn(`❌ ${src.name} 失败`, err.message);
```

### 添加缓存机制

避免重复请求相同的问题：

```javascript
// 在文件顶部添加
const requestCache = new Map();

// 在 fetchWithFallback 函数开头添加
if (requestCache.has(prompt)) {
    setStatus('从缓存加载...', 'idle');
    responseBox.innerHTML = requestCache.get(prompt);
    return requestCache.get(prompt);
}

// 在成功获取响应后添加
requestCache.set(prompt, content);
// 限制缓存大小（最多 100 条）
if (requestCache.size > 100) {
    const firstKey = requestCache.keys().next().value;
    requestCache.delete(firstKey);
}
```

### 添加速率限制

防止短时间内发送过多请求：

```javascript
// 在文件顶部添加
let lastRequestTime = 0;
const MIN_REQUEST_INTERVAL = 3000; // 最小间隔 3 秒

// 在 handleSend 函数开头添加
const now = Date.now();
const timeSinceLastRequest = now - lastRequestTime;
if (timeSinceLastRequest < MIN_REQUEST_INTERVAL) {
    const waitTime = Math.ceil((MIN_REQUEST_INTERVAL - timeSinceLastRequest) / 1000);
    setStatus(`请等待 ${waitTime} 秒后再试`, 'error');
    return;
}
lastRequestTime = now;
```

## 🌐 添加新的免费 API 源

### OpenRouter 免费模型

访问 https://openrouter.ai/keys 获取更多信息，支持以下免费模型：

```javascript
{
    name: 'Llama 3 8B (Free)',
    url: 'https://openrouter.ai/api/v1/chat/completions',
    model: 'meta-llama/llama-3-8b-instruct:free',
    headers: { 'Content-Type': 'application/json' }
},
{
    name: 'Phi-3 Mini (Free)',
    url: 'https://openrouter.ai/api/v1/chat/completions',
    model: 'microsoft/phi-3-mini-4k-instruct:free',
    headers: { 'Content-Type': 'application/json' }
},
{
    name: 'Command R (Free)',
    url: 'https://openrouter.ai/api/v1/chat/completions',
    model: 'cohere/command-r:free',
    headers: { 'Content-Type': 'application/json' }
}
```

### Hugging Face Inference API

需要申请 API Key（免费额度）：

```javascript
{
    name: 'HuggingFace Llama 3',
    url: 'https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct/v1/chat/completions',
    model: 'meta-llama/Meta-Llama-3-8B-Instruct',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_HUGGINGFACE_TOKEN'
    }
}
```

### Groq API（超高速推理）

需要申请 API Key（目前免费测试中）：

```javascript
{
    name: 'Groq Llama 3 8B',
    url: 'https://api.groq.com/openai/v1/chat/completions',
    model: 'llama3-8b-8192',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_GROQ_TOKEN'
    }
}
```

### Google Gemini（社区代理）

注意：社区代理可能不稳定，建议作为备用源：

```javascript
{
    name: 'Gemini Pro (Proxy)',
    url: 'https://your-proxy-server.com/gemini-api',
    model: 'gemini-pro',
    headers: {
        'Content-Type': 'application/json'
    }
}
```

## ⚠️ 常见问题与解决方案

### Q1: CORS 跨域错误

**问题**：浏览器报错 "Access-Control-Allow-Origin"

**解决方案 A**：使用反向代理服务器
```javascript
const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
const resp = await fetch(proxyUrl + src.url, { /* ... */ });
```

**解决方案 B**：安装浏览器插件（仅开发环境）
- Chrome: "Allow CORS: Access-Control-Allow-Origin"
- Firefox: "Allow-Control-Allow-Origin"

**解决方案 C**：部署后端转发服务
```python
# Python Flask 示例
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/proxy', methods=['POST'])
def proxy():
    response = requests.post(
        request.json['url'],
        json=request.json['data'],
        headers=request.headers
    )
    return jsonify(response.json()), response.status_code
```

### Q2: API 返回空内容

检查返回数据结构：

```javascript
// 在解析响应后添加调试代码
console.log('原始响应:', data);

// 兼容多种返回格式
let content = null;
if (data && data.choices && data.choices.length > 0) {
    content = data.choices[0].message?.content || data.choices[0].text || null;
} else if (data && data.content) {
    content = data.content;
} else if (data && data.response) {
    content = data.response;
} else if (data && data.output) {
    content = data.output;
}

if (!content) {
    throw new Error('无法解析响应内容');
}
```

### Q3: 请求超时

增加超时时间：

```javascript
const timeoutId = setTimeout(() => controller.abort(), 30000); // 30 秒
```

或使用更智能的超时策略：

```javascript
// 根据模型大小动态设置超时
const modelTimeoutMap = {
    '7b': 20000,
    '8b': 20000,
    '9b': 25000,
    'default': 15000
};

const getModelSize = (modelName) => {
    const match = modelName.match(/(\d+)b/i);
    return match ? modelTimeoutMap[match[1] + 'b'] : modelTimeoutMap.default;
};

const timeout = getModelSize(src.model);
const timeoutId = setTimeout(() => controller.abort(), timeout);
```

### Q4: 免费额度用完

监控使用情况：

```javascript
// 检查响应头中的配额信息
const remaining = resp.headers.get('x-ratelimit-remaining');
const limit = resp.headers.get('x-ratelimit-limit');

if (remaining === '0') {
    throw new Error('免费额度已用完，请稍后重试');
}
```

## 📊 性能优化建议

### 1. 优先级排序

将最稳定、最快的源放在前面：

```javascript
const SOURCES = [
    // 第一梯队：高成功率 + 快速响应
    { name: 'Groq Llama 3', ... },      // 最快
    { name: 'Mistral 7B', ... },        // 稳定
    
    // 第二梯队：中等表现
    { name: 'Gemma 2 9B', ... },
    
    // 第三梯队：备用源
    { name: 'Phi-3 Mini', ... },
    { name: 'Demo Proxy', ... }         // 可能不稳定
];
```

### 2. 减少不必要的请求

只在必要时才发起请求：

```javascript
// 检查网络状态
if (!navigator.onLine) {
    setStatus('❌ 网络连接中断', 'error');
    return;
}

// 检查是否正在处理其他请求
if (isProcessing) {
    setStatus('⏳ 正在处理中，请稍候', 'loading');
    return;
}
```

### 3. 优化 UI 渲染

使用 DocumentFragment 批量更新 DOM：

```javascript
function renderBadge() {
    const fragment = document.createDocumentFragment();
    const names = SOURCES.map(s => s.name);
    
    names.forEach(name => {
        const span = document.createElement('span');
        span.textContent = name;
        span.className = 'model-tag';
        fragment.appendChild(span);
    });
    
    modelBadge.innerHTML = '';
    modelBadge.appendChild(fragment);
}
```

## 🔒 安全最佳实践

### 1. 不要硬编码敏感信息

**错误做法** ❌：
```javascript
const SOURCES = [
    {
        headers: {
            'Authorization': 'Bearer sk-abc123xyz789'  // 暴露的 API Key
        }
    }
];
```

**正确做法** ✅：
```javascript
// 从环境变量读取
const API_KEY = import.meta.env?.VITE_API_KEY || 
                localStorage.getItem('my_api_key') ||
                prompt('请输入 API Key:');

const SOURCES = [
    {
        headers: {
            'Authorization': `Bearer ${API_KEY}`
        }
    }
];
```

### 2. 使用 .env 文件（本地开发）

创建 `.env` 文件：
```
OPENROUTER_API_KEY=your_key_here
GROQ_API_KEY=your_key_here
```

使用环境变量加载器（如 `dotenv`）读取。

### 3. 限制缓存敏感数据

```javascript
// 不要在 localStorage 中存储 API Key
// 使用内存变量而非持久化存储
let apiKey = null;

function setApiKey(key) {
    apiKey = key;
    // 不在 localStorage 中保存
}
```

## 📈 监控与分析

### 添加使用统计

```javascript
// 统计每个源的成功率
const stats = {
    totalRequests: 0,
    successfulRequests: 0,
    sourceSuccessRate: {}
};

function recordRequest(sourceName, success) {
    stats.totalRequests++;
    if (success) stats.successfulRequests++;
    
    if (!stats.sourceSuccessRate[sourceName]) {
        stats.sourceSuccessRate[sourceName] = { success: 0, total: 0 };
    }
    stats.sourceSuccessRate[sourceName].total++;
    if (success) stats.sourceSuccessRate[sourceName].success++;
}

// 定期输出统计
setInterval(() => {
    console.table(stats.sourceSuccessRate);
    console.log(`总体成功率：${((stats.successfulRequests / stats.totalRequests * 100).toFixed(2))}%`);
}, 60000); // 每分钟输出一次
```

## 🎨 主题定制

### 修改配色方案

在 `<style>` 标签中添加：

```css
/* 深色主题 */
@media (prefers-color-scheme: dark) {
    body {
        background: #1a1a2e;
        color: #eee;
    }
    .card {
        background: #16213e;
        box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
    }
    .input-area input {
        background: #0f3460;
        border-color: #533483;
        color: #fff;
    }
}

/* 自定义主色调 */
:root {
    --primary-color: #ff6b6b;  /* 珊瑚红 */
    --secondary-color: #4ecdc4; /* 青绿色 */
}

.input-area button {
    background: var(--primary-color);
}
```

## 🚀 部署到生产环境

### 静态托管（GitHub Pages）

1. 推送到 GitHub 仓库
2. 在仓库设置中启用 GitHub Pages
3. 访问 `https://username.github.io/repo/free-ai-aggregator/`

### Netlify/Vercel

1. 连接到 GitHub 仓库
2. 自动部署
3. 配置自定义域名

### 自建服务器

```bash
# 使用 Python 启动简单服务器
cd free-ai-aggregator
python -m http.server 8000

# 或使用 Node.js
npx serve .
```

---

**最后更新**: 2026-06-30  
**维护者**: 云创 - 免费云情报站
