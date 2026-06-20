const CACHE = 'zentools-v1';
const STATIC = [
  '/',
  '/index.html',
  '/assets/css/style.css',
  '/assets/css/tool-ui.css',
  '/assets/js/tool-ui.js',
  '/assets/js/anti-crash.js',
  '/assets/js/i18n.js',
  '/data/tools-data.json',
  '/data/categories.json',
  '/favicon.svg',
  '/manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => cache.addAll(STATIC))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  // Only cache same-origin requests
  if (url.origin !== location.origin) return;
  // Skip non-GET
  if (e.request.method !== 'GET') return;

  e.respondWith(
    caches.match(e.request).then(cached => {
      // Return cached response immediately, then update cache in background
      const fetchPromise = fetch(e.request).then(res => {
        if (res.ok) {
          const clone = res.clone();
          caches.open(CACHE).then(cache => cache.put(e.request, clone));
        }
        return res;
      }).catch(() => cached);
      return cached || fetchPromise;
    })
  );
});
