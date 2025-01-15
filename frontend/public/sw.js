const CACHE_NAME = 'doctor-syria-v2-cache';
const urlsToCache = [
  '/doctor-syria-v2/',
  '/doctor-syria-v2/index.html',
  '/doctor-syria-v2/assets/index.css',
  '/doctor-syria-v2/assets/index.js',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', (event) => {
  event.respondWith(
    caches.match(event.request)
      .then((response) => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
