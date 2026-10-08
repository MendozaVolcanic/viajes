// Guarda la página del desierto florido y sus fotos para usarla sin señal.
const CACHE = 'df26-v1';
const PAGE = './desierto-florido-2026.html';

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.add(PAGE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('df26-') && k !== CACHE).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

// La página: primero la red (para tener la última versión), y si no hay señal, la copia guardada.
// Fotos y fuentes: primero la copia guardada.
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  const isPage = url.origin === location.origin && url.pathname.endsWith('/desierto-florido-2026.html');
  if (isPage) {
    e.respondWith(fetch(req).then(r => { const cp = r.clone(); caches.open(CACHE).then(c => c.put(PAGE, cp)); return r; })
      .catch(() => caches.match(PAGE)));
    return;
  }
  e.respondWith(caches.match(req, { ignoreSearch: false }).then(hit => hit || fetch(req).then(r => {
    if (r && (r.ok || r.type === 'opaque')) { const cp = r.clone(); caches.open(CACHE).then(c => c.put(req, cp)); }
    return r;
  })));
});

// La página pide guardar de una vez todas las fotos y fuentes.
self.addEventListener('message', e => {
  if (!e.data || e.data.type !== 'precache') return;
  const urls = e.data.urls || [];
  e.waitUntil(caches.open(CACHE).then(async c => {
    let ok = 0;
    for (const u of urls) {
      try {
        if (!(await c.match(u))) { const r = await fetch(u, { mode: 'no-cors' }); await c.put(u, r); }
        ok++;
      } catch (err) { /* sin señal o bloqueado: se intenta la próxima vez */ }
    }
    const cl = await self.clients.matchAll();
    cl.forEach(x => x.postMessage({ type: 'precached', ok, total: urls.length }));
  }));
});
