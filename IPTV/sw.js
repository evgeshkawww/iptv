self.addEventListener("install", e => {
  console.log("SW install");
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  console.log("SW activate");
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  console.log("SW fetch:", e.request.url);
});
