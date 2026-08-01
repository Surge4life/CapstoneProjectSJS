/* G.O.D.S UDOC Internal PWA — injects admin-v7-enhance.js + intel-density.js */
const CACHE = 'gods-udoc-pwa-v7';
const SHELL = ['/', '/index.html', '/manifest.webmanifest', '/icon-192.png', '/icon-512.png', '/admin-v7-enhance.js', '/intel-density.js'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())
  );
});
function injectEnhance(html) {
  var tags = '';
  if (html.indexOf('admin-v7-enhance.js') === -1)
    tags += '<script src="/admin-v7-enhance.js"><\/script>\n';
  if (html.indexOf('intel-density.js') === -1)
    tags += '<script src="/intel-density.js"><\/script>\n';
  if (!tags) return html;
  if (html.indexOf('serviceWorker') !== -1) {
    return html.replace(
      '<script>if("serviceWorker"',
      tags + '<script>if("serviceWorker"'
    );
  }
  return html.replace('</body>', tags + '</body>');
}
self.addEventListener('fetch', e => {
  const r = e.request;
  const u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;
  if (r.mode === 'navigate') {
    e.respondWith(
      fetch(r)
        .then(resp => {
          const ct = resp.headers.get('content-type') || '';
          if (!ct.includes('text/html')) return resp;
          return resp.text().then(t => {
            const body = injectEnhance(t);
            return new Response(body, {
              status: resp.status,
              statusText: resp.statusText,
              headers: resp.headers
            });
          });
        })
        .catch(() => caches.match('/index.html'))
    );
    return;
  }
  if (u.pathname.endsWith('/admin-v7-enhance.js') || u.pathname.endsWith('/intel-density.js')) {
    e.respondWith(
      fetch(r).then(resp => {
        const cp = resp.clone();
        caches.open(CACHE).then(cc => cc.put(r, cp));
        return resp;
      }).catch(() => caches.match(r))
    );
    return;
  }
  e.respondWith(
    caches.match(r).then(c =>
      c ||
      fetch(r).then(resp => {
        const cp = resp.clone();
        caches.open(CACHE).then(cc => cc.put(r, cp));
        return resp;
      }).catch(() => c)
    )
  );
});
