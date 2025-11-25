self.addEventListener('install', event => {
  event.waitUntil(
    caches.open('iptv-cache').then(cache => {
      return cache.addAll([
        '/bundle.js',
        '/style.css'
      ]);
    })
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(self.clients.claim());
});

// Подмена путей
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Подмена bundle.js → реальный JS
  if (url.pathname === '/bundle.js') {
    event.respondWith(fetch('/iptv/IPTV/assets/index-rXCmlGUy.js'));
    return;
  }

  // Подмена style.css → реальный CSS
  if (url.pathname === '/style.css') {
    event.respondWith(fetch('/iptv/IPTV/assets/index-JXv4NXlQ.css'));
    return;
  }

  // Остальные запросы — как обычно
  event.respondWith(fetch(event.request));
});
