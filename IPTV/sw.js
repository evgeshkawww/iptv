const mapping = {
  "/iptv/IPTV/bundle.js": "/iptv/IPTV/assets/index-rXCmlGUy.js",
  "/iptv/IPTV/style.css": "/iptv/IPTV/assets/index-JXv4NXlQ.css"
};

self.addEventListener("install", e => {
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  const u = new URL(e.request.url);
  if (mapping[u.pathname]) {
    e.respondWith(fetch(mapping[u.pathname]));
    return;
  }
  e.respondWith(fetch(e.request));
});
