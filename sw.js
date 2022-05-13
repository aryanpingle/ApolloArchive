///////////////////////////////////
//  The best(er) service worker  //
//         on the planet         //
//                               //
//       Suck it WorkboxJS       //
///////////////////////////////////

const APP_VERSION = 6.00

// Document Cache is a cache of document files - html, js, css, etc
const DOCUMENT_CACHE_NAME = `DOC`
var DOCUMENT_CACHE = null
// Resource Cache is a cache of almost always static resources - images, fonts, and everything in the Texts folder
const RESOURCE_VERSION = 6.00
const RESOURCE_CACHE_NAME = `RESv${RESOURCE_VERSION.toFixed(2)}`
var RESOURCE_CACHE = null

// Custom extensions
String.prototype.containsAny = function (substrings=[]) {
    return substrings.some(substring => this.includes(substring))
}

// For Debugging
STOP_CACHING = self.registration.scope.includes("127.0.0.1")
var log = (text, color="white") => console.log(`%c${text}`, `color: black; background-color: ${color};`)
log = e => e // Comment for testing

self.addEventListener("install", event => {
    event.waitUntil((async () => {
        await self.skipWaiting()
    })())
});

self.addEventListener("activate", event => {
    log("Service Worker activated")
    // Remove obsolete caches
    event.waitUntil((async () => {
        await Promise.allSettled([clients.claim(), load_both_caches(), delete_obsolete_caches()])
    })())
});

async function load_both_caches() {
    await caches.open(`${APP_VERSION.toFixed(2)}`)
    DOCUMENT_CACHE = await caches.open(DOCUMENT_CACHE_NAME)
    RESOURCE_CACHE = await caches.open(RESOURCE_CACHE_NAME)
}

async function delete_obsolete_caches() {
    let cache_names = await caches.keys()
    await Promise.all(cache_names.map(cache_name => {
        if (![DOCUMENT_CACHE_NAME, RESOURCE_CACHE_NAME, `${APP_VERSION.toFixed(2)}`].includes(cache_name)) {
            log(`Deleting obsolete cache: '${cache_name}'`, "rgb(255, 128, 128)")
            return caches.delete(cache_name)
        }
    }))
}

self.addEventListener("fetch", request_event => {
    request_event.respondWith(STOP_CACHING ? fetch(request_event.request) : get_request(request_event))
});

async function get_request(request_event) {
    let request = request_event.request
    let url = request.url
    
    if(DOCUMENT_CACHE == null || RESOURCE_CACHE == null) {
        await load_both_caches()
    }
    
    // Check if the request is for a document
    if(url.match(/\/$/) || url.containsAny([".html", ".js", ".css"]) && !url.includes(".json") && !url.includes("apis.google.com")) {
        /**
        * So here's the game plan:
        * Check if a cache version exists.
        * | --- If it doesn't, then return a simple fetch request with no timeout
        * | --- If it does call a fetch request that times out after 'x' seconds, defaulting to the cache version
        * This ensures that the user gets the latest possible version, as fast as possible
        * 
        * PS: In all possible cases, cache the request after network-fetching it
        */
        
        // Check if a cache version exists
        let cache_match = await DOCUMENT_CACHE.match(request, { ignoreVary: true })
        if(cache_match == undefined || cache_match == null) {
            // A cached version DOESN'T exist
            log("A cached version DOESN'T exist, performing a network request", "rgb(128, 128, 255)")
            let network_match = await fetch(request).catch(err => null)
            if(network_match) {
                DOCUMENT_CACHE.put(request, network_match.clone())
            }
            return network_match
        }
        else {
            // A cached version DOES exist
            log("A cached version DOES exist", "rgb(128, 128, 255)")

            log("Performing network match *in background*")
            const SECONDS_TO_TIMEOUT = 5
        
            const abort_controller = new AbortController()
            const abort_signal = abort_controller.signal
            const timeout_id = setTimeout(() => abort_controller.abort(), SECONDS_TO_TIMEOUT*1000)
            
            // Perform a network request
            fetch(request, {signal: abort_signal}).then(data => {
                clearTimeout(timeout_id)
                log("Network match completed before timeout", "rgb(128, 255, 128)")
                return data
            }).catch(err => {
                if(err.name == "AbortError") {
                    log("Network request took too long, returning cached version", "rgb(255, 128, 128)")
                    return null
                }
                throw err
            }).catch(err => null).then(data => {
                if(data == undefined || data == null) {
                    // Do nothing if it fails
                }
                else {
                    // Save it to cache for next time
                    DOCUMENT_CACHE.put(request, data.clone())
                    return data
                }
            })

            // Send cached match regardless
            return cache_match
        }
    }
    // Check if the request is for a resource
    else if(url.containsAny([".json", "fonts/", "images/", "fonts.googleapis.com"])) {
        // Perform a cache request
        let match = await RESOURCE_CACHE.match(request, { ignoreVary: true })
        if (match != undefined && match != null) return match
        // Since a cached version doesn't exist, perform a network request
        match = await fetch(request)
        RESOURCE_CACHE.put(request, match.clone())
        return match
    }
    
    // Doesn't belong to either type of cache, so perform a network request

    return await fetch(request)
}