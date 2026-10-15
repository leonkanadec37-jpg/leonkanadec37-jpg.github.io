// Service Worker for Livi Jewelry static site
// Cache core assets and images for offline support
const CACHE_NAME = 'livi-jewelry-v1';
const CORE_ASSETS = [
  '/',
  '/index.html',
  '/shop.html',
  '/cart.html',
  '/site.webmanifest',
  '/favicon.svg',
  // Add more assets as needed
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  const { request } = event;
  // Network-first for HTML pages, cache-first for assets
  if (request.destination === 'document') {
    event.respondWith(fetch(request).catch(() => caches.match(request)));
  } else {
    event.respondWith(
      caches.match(request).then((response) => response || fetch(request))
    );
  }
});
