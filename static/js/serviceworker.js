var staticCacheName = 'sgu-static-v1';
var pagesCacheName = 'sgu-pages-v1';

self.addEventListener('install', function(event) {
    self.skipWaiting();
    event.waitUntil(
        caches.open(staticCacheName).then(function(cache) {
            return cache.addAll([
                '/',
                '/static/css/styles.css',
            ]);
        })
    );
});

self.addEventListener('activate', function(event) {
    var cacheWhitelist = [staticCacheName, pagesCacheName];
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});

self.addEventListener('fetch', function(event) {
    var request = event.request;
    if (request.method === 'GET') {
        event.respondWith(
            caches.match(request).then(function(response) {
                return response || fetch(request).then(function(fetchResponse) {
                    return caches.open(pagesCacheName).then(function(cache) {
                        cache.put(request, fetchResponse.clone());
                        return fetchResponse;
                    });
                });
            })
        );
    }
});

// --- NOTIFICAÇÕES PUSH ---
self.addEventListener('push', function(event) {
    var data = {};
    if (event.data) {
        try {
            data = event.data.json();
        } catch(e) {
            data = { title: event.data.text() };
        }
    }

    var title = data.title || 'Solicita Cidadão';
    var options = {
        body: data.body || 'Você tem uma nova atualização.',
        icon: data.icon || '/static/images/icon-144x144.png',
        badge: '/static/images/icon-144x144.png',
        vibrate: [200, 100, 200],
        data: {
            url: data.url || '/'
        }
    };

    event.waitUntil(
        self.registration.showNotification(title, options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    var url = event.notification.data.url || '/';
    event.waitUntil(
        clients.matchAll({type: 'window'}).then(function(windowClients) {
            for (var i = 0; i < windowClients.length; i++) {
                var client = windowClients[i];
                if (client.url === url && 'focus' in client) {
                    return client.focus();
                }
            }
            if (clients.openWindow) {
                return clients.openWindow(url);
            }
        })
    );
});
