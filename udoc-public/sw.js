/* G.O.D.S UDOC PWA service worker — installable + offline shell, never caches the API. */
const CACHE = 'gods-udoc-pwa-v7';
const SHELL = ['/', '/index.html', '/app-client.js', '/client-knowledge-density.js', '/manifest.webmanifest', '/icon-192.png', '/icon-512.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const r = e.request;
  const u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;
  if (u.pathname.endsWith('/app-client.js') || u.pathname.endsWith('/client-knowledge-density.js')) {
    e.respondWith(
      fetch(r).then(resp => {
        const cp = resp.clone();
        caches.open(CACHE).then(cc => cc.put(r, cp));
        return resp;
      }).catch(() => caches.match(r))
    );
    return;
  }
  if (r.mode === 'navigate') {
    e.respondWith(fetch(r).catch(() => caches.match('/index.html')));
    return;
  }
  e.respondWith(
    caches.match(r).then(c => c || fetch(r).then(resp => {
      const cp = resp.clone();
      caches.open(CACHE).then(cc => cc.put(r, cp));
      return resp;
    }).catch(() => c))
  );
});
