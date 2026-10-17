// Service Worker for Livi Jewelry static site
const CACHE_NAME = 'livi-jewelry-v2';

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => caches.delete(key))
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  const isHtml = request.mode === 'navigate' ||
                 request.destination === 'document' ||
                 request.url.includes('.html') ||
                 request.url.endsWith('/');

  if (isHtml) {
    // Network-first for all HTML pages so cart and shop are never stale
    event.respondWith(
      fetch(request).catch(() => caches.match(request))
    );
  } else {
    // Cache-first for images and static assets
    event.respondWith(
      caches.match(request).then((response) => response || fetch(request))
    );
  }
});
