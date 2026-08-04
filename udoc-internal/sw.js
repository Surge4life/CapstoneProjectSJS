/* G.O.D.S UDOC Internal PWA — network-first navigate; soft inject density scripts */
const CACHE = 'gods-udoc-pwa-v11';
const SHELL = ['/', '/index.html', '/manifest.webmanifest'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(SHELL).catch(() => {})).then(() => self.skipWaiting()));
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
  if (html.indexOf('eif-density.js') === -1)
    tags += '<script src="/eif-density.js"><\/script>\n';
  if (html.indexOf('policy-density.js') === -1)
    tags += '<script src="/policy-density.js"><\/script>\n';
  if (!tags) return html;
  if (html.indexOf('</body>') !== -1) return html.replace('</body>', tags + '</body>');
  return html + tags;
}
self.addEventListener('fetch', e => {
  const r = e.request;
  const u = new URL(r.url);
  if (r.method !== 'GET' || u.origin !== location.origin) return;
  if (r.mode === 'navigate' || (r.headers.get('accept') || '').includes('text/html')) {
    e.respondWith(
      fetch(r)
        .then(resp => {
          const ct = resp.headers.get('content-type') || '';
          if (!ct.includes('text/html')) return resp;
          return resp.text().then(t => {
            const body = injectEnhance(t);
            const headers = new Headers(resp.headers);
            headers.set('Cache-Control', 'no-store');
            return new Response(body, { status: resp.status, statusText: resp.statusText, headers: headers });
          });
        })
        .catch(() => caches.match('/index.html').then(c => c || caches.match('/')))
    );
    return;
  }
  if (/\.(js)$/i.test(u.pathname)) {
    e.respondWith(
      fetch(r).then(resp => {
        const cp = resp.clone();
        caches.open(CACHE).then(cc => cc.put(r, cp)).catch(() => {});
        return resp;
      }).catch(() => caches.match(r))
    );
    return;
  }
  e.respondWith(
    fetch(r).then(resp => {
      const cp = resp.clone();
      caches.open(CACHE).then(cc => cc.put(r, cp)).catch(() => {});
      return resp;
    }).catch(() => caches.match(r))
  );
});
