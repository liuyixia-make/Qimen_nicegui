// 缓存名称
const CACHE_NAME = 'qimen-cache-v1';

// 需要缓存的核心资源
const urlsToCache = [
  '/',
  '/static/favicon.ico',
  '/static/manifest.json'
];

// 安装Service Worker - 简化版本
self.addEventListener('install', event => {
  // 跳过等待，直接激活
  self.skipWaiting();
  
  // 缓存核心资源
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        return cache.addAll(urlsToCache);
      })
  );
});

// 激活Service Worker - 简化版本
self.addEventListener('activate', event => {
  // 立即接管所有客户端
  event.waitUntil(clients.claim());
});

// 简化的请求处理 - 网络优先策略
self.addEventListener('fetch', event => {
  // 只处理GET请求
  if (event.request.method !== 'GET') return;
  
  // 忽略浏览器扩展请求和其他域的请求
  const url = new URL(event.request.url);
  if (url.origin !== location.origin) return;
  
  event.respondWith(
    fetch(event.request)
      .catch(() => {
        // 网络请求失败时，尝试从缓存获取
        return caches.match(event.request);
      })
  );
}); 