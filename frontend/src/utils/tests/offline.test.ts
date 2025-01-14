describe('Service Worker Tests', () => {
  beforeAll(async () => {
    await navigator.serviceWorker.register('/doctor-syria-v2/sw.js');
  });

  test('service worker is registered', async () => {
    const registration = await navigator.serviceWorker.ready;
    expect(registration.active).toBeTruthy();
  });

  test('caches static assets', async () => {
    const cache = await caches.open('doctor-syria-v2-cache');
    const keys = await cache.keys();
    expect(keys.length).toBeGreaterThan(0);
  });

  test('handles offline mode', async () => {
    const cache = await caches.open('doctor-syria-v2-cache');
    const response = await cache.match('/doctor-syria-v2/');
    expect(response).toBeTruthy();
  });
});
