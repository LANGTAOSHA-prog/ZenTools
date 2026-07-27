// ZenTools PWA Service Worker - Cache-First Strategy
const CACHE_VERSION = 'zentools-v11';
const CORE_CACHE = CACHE_VERSION + '-core';
const HTML_CACHE = CACHE_VERSION + '-html';
const DATA_CACHE = CACHE_VERSION + '-data';
const ASSET_CACHE = CACHE_VERSION + '-assets';

// 预缓存的静态资源（应用外壳）
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/tools.html',
  '/manifest.json',
  '/favicon.svg',
  '/icon-192x192.png',
  '/icon-512x512.png',
];

// 预缓存的样式和脚本
const STATIC_ASSETS = [
  '/assets/css/style.min.css',
  '/assets/css/tool-ui.min.css',
  '/assets/js/common-i18n.min.js',
  '/assets/js/tool-ui.min.js',
  '/assets/js/anti-crash.min.js',
];

// 预缓存的分类首页（用户常用入口）
const CATEGORY_PAGES = [
  '/image/index.html',
  '/pdf/index.html',
  '/audio/index.html',
  '/video/index.html',
  '/text/index.html',
  '/dev/index.html',
  '/ai/index.html',
  '/life/index.html',
];

// 预缓存的核心数据
const DATA_FILES = [
  '/data/tools-data.json',
];

// 工具页面缓存正则（按需运行时缓存）
const TOOL_PAGE_PATTERN = /\/(image|pdf|audio|video|text|dev|ai|life|seo|finance|qr|tools|tutorials|json)\/.+\.html$/;

// 安装阶段：预缓存核心文件
self.addEventListener('install', (event) => {
  event.waitUntil(
    (async () => {
      const coreCache = await caches.open(CORE_CACHE);
      const assetCache = await caches.open(ASSET_CACHE);
      const dataCache = await caches.open(DATA_CACHE);

      await Promise.all([
        coreCache.addAll(CORE_ASSETS),
        assetCache.addAll(STATIC_ASSETS),
        dataCache.addAll(DATA_FILES),
        // 分类页面单独缓存，失败不影响
        caches.open(HTML_CACHE).then(c => Promise.allSettled(
          CATEGORY_PAGES.map(url => c.add(url).catch(() => {}))
        ))
      ]);
    })()
  );
  self.skipWaiting();
});

// 激活阶段：清理旧版本缓存
self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      const keys = await caches.keys();
      const validPrefixes = [CACHE_VERSION];
      await Promise.all(
        keys
          .filter(key => !validPrefixes.some(p => key.startsWith(p)))
          .map(key => caches.delete(key))
      );
    })()
  );
  self.clients.claim();
});

// 请求处理
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // 只处理同源 GET 请求
  if (url.origin !== location.origin) return;
  if (request.method !== 'GET') return;

  // 策略 1：静态资源 - Cache First（缓存优先，永不过期）
  if (isStaticAsset(url.pathname)) {
    event.respondWith(cacheFirst(ASSET_CACHE, CORE_CACHE, request));
    return;
  }

  // 策略 2：数据文件 - Network First（网络优先，缓存兜底）
  if (url.pathname === '/data/tools-data.json') {
    event.respondWith(networkFirst(DATA_CACHE, request));
    return;
  }

  // 策略 3：HTML 页面 - Stale While Revalidate（缓存即返，后台更新）
  if (isHTMLPage(url.pathname)) {
    event.respondWith(staleWhileRevalidate(HTML_CACHE, request));
    return;
  }

  // 策略 4：其他资源（图片等）- Cache First
  event.respondWith(cacheFirst(ASSET_CACHE, CORE_CACHE, request));
});

// ===== 缓存策略函数 =====

// Cache First：优先返回缓存，缓存不存在则网络请求并缓存
async function cacheFirst(cacheName, fallbackCacheName, request) {
  let cached = await caches.match(request);
  if (!cached && fallbackCacheName) {
    cached = await caches.match(request, { cacheName: fallbackCacheName });
  }
  if (cached) return cached;

  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (e) {
    return cached || new Response('Offline', { status: 503 });
  }
}

// Network First：优先网络，失败时返回缓存
async function networkFirst(cacheName, request) {
  try {
    const response = await fetch(request);
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  } catch (e) {
    const cached = await caches.match(request);
    return cached || new Response('Offline', { status: 503 });
  }
}

// Stale While Revalidate：立即返回缓存，同时后台更新
async function staleWhileRevalidate(cacheName, request) {
  const cached = await caches.match(request);

  const fetchPromise = fetch(request).then(async (response) => {
    if (response.ok) {
      const cache = await caches.open(cacheName);
      cache.put(request, response.clone());
    }
    return response;
  }).catch(() => cached);

  return cached || fetchPromise;
}

// ===== 辅助函数 =====

function isStaticAsset(pathname) {
  return /\.(css|js|png|svg|ico|woff2?|ttf|jpg|webp|gif)$/.test(pathname) ||
         pathname === '/manifest.json';
}

function isHTMLPage(pathname) {
  return pathname === '/' ||
         pathname.endsWith('.html') ||
         pathname.endsWith('/');
}

// 消息事件：允许客户端触发更新
self.addEventListener('message', (event) => {
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
  }
});
