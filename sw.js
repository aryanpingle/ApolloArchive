// const log = (text, color = "white") => console.log(`%c${text}`, `color: black; background-color: ${color};`)
const log = e=>e

const VERSION = 2.30
const CURRENT_CACHE = `v${VERSION.toFixed(2)}`

self.addEventListener("install", event => {
    event.waitUntil(
        caches
            .open(CURRENT_CACHE)
            .then(cache => self.skipWaiting())
    )
});

self.addEventListener("activate", event => {
    log("activated")
    // Remove other caches
    event.waitUntil(
        caches.keys().then(cache_names => {
            return Promise.all(
                cache_names.map(cache_name => {
                    if (cache_name != CURRENT_CACHE) {
                        caches.delete(cache_name)
                    }
                })
            )
        })
    )
})

self.addEventListener("fetch", event => {
    event.respondWith(get_request(event))
});

async function get_request(request_event) {
    log("Performing Cache Request", "greenyellow")
    return get_cache_request(request_event).catch(err => {
        log("Cache request failed, attempting Network request", "rgb(0, 128, 255)")
        return get_network_request(request_event)
    })
}

async function get_cache_request(request_event) {
    return caches.open(CURRENT_CACHE).then(async cache => {
        let match = await cache.match(request_event.request, {ignoreVary: true})
        if (match == undefined) throw "match not found"
        return match
    }).catch(async err => {
        // Network Request time
        let match = fetch(request_event.request)
        // Check if it is an audio file
        if(request_event.request.url.includes("HZD")) {
            // It's an audio file, so send it without caching
            return match
        }
        // It's not an audio file, so cache it first then send it
        return match.then(response => {
            let response_clone = response.clone()
            caches.open(CURRENT_CACHE).then(cache => cache.put(request_event.request, response))
            return response_clone
        })
    })
}

async function get_network_request(request_event) {
    console.log(request_event.request.url)
    return fetch(request_event.request)
}