const CACHE_NAME = 'pwa-cache-v1';
const OFFLINE_URL = '/static/offline.html';

// Liste des ressources à mettre en cache
const CACHE_ASSETS = [
    OFFLINE_URL,
    '/static/images/icon-192x192.png',
    '/static/images/icon-512x512.png',
    // Ajoutez d'autres fichiers nécessaires ici
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            console.log('Caching offline page and assets');
            return cache.addAll(CACHE_ASSETS);
        })
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cache) => {
                    if (cache !== CACHE_NAME) {
                        console.log('Deleting old cache:', cache);
                        return caches.delete(cache);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', (event) => {
    event.respondWith(
        fetch(event.request).catch(() => {
            // Retourne la page hors ligne en cas d'erreur réseau
            return caches.match(OFFLINE_URL);
        })
    );
});
