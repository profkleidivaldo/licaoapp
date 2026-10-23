/* Service worker da Escola Sabatina
   Guarda a própria página (e ícones) no aparelho para o site abrir sem internet.
   Os textos das versões (ACF/AA/NVI) e a lição são guardados pela página no Cache Storage
   (caches "ess-biblia-v1" e "ess-licoes-v1"), que este arquivo não toca. */

const SHELL = "ess-shell-v4";
const ASSETS = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
  "./data/licao.json",
  "./data/capas.json"
];

self.addEventListener("install", event => {
  event.waitUntil(
    caches.open(SHELL)
      .then(cache => cache.addAll(ASSETS))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", event => {
  event.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k.startsWith("ess-shell-") && k !== SHELL).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", event => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);
  // Só cuida de arquivos do próprio site. Os JSON das versões e o VLibras
  // (outros domínios) seguem o caminho normal.
  if (url.origin !== self.location.origin) {
    // Imagens de outros sites (capas da CPB / repositório): guarda para ver offline.
    if (/\.(png|jpe?g|webp|gif)$/i.test(url.pathname)) {
      event.respondWith(caches.open("ess-img-v1").then(c => c.match(req).then(hit => hit ||
        fetch(req).then(res => { if (res && (res.ok || res.type === "opaque")) c.put(req, res.clone()); return res; }))));
    }
    return;
  }

  // Dados da lição: rede primeiro (para pegar atualizações) e, sem internet, a cópia guardada.
  if (url.pathname.includes("/data/")) {
    event.respondWith(
      fetch(req).then(res => {
        if (res && res.ok) { const copy = res.clone(); caches.open(SHELL).then(c => c.put(req, copy)); }
        return res;
      }).catch(() => caches.match(req))
    );
    return;
  }

  // Abrir o site: responde na hora com a página guardada e atualiza em segundo plano.
  if (req.mode === "navigate") {
    event.respondWith(
      caches.match("./index.html").then(cached => {
        const refresh = fetch(req)
          .then(res => {
            if (res && res.ok && !res.redirected) {
              const copy = res.clone();
              caches.open(SHELL).then(c => c.put("./index.html", copy));
            }
            return res;
          })
          .catch(() => cached);
        return cached || refresh;
      })
    );
    return;
  }

  // Demais arquivos do site: usa o guardado e, se não houver, busca e guarda.
  event.respondWith(
    caches.match(req).then(hit =>
      hit || fetch(req).then(res => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(SHELL).then(c => c.put(req, copy));
        }
        return res;
      })
    )
  );
});
