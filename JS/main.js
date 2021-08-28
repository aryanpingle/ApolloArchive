const print = console.log



function get_params() {
    let url = window.location.href
    return url.substr(url.indexOf("?")+1).split("&")
}

document.body.onclick = event=>{
    document.getElementsByTagName("audio")[0].src = "Audio/HZD A 27.mp3";
}
// src: url(/content/dam/global_pdc/site-furniture/horizon/HunterW05-Condensed.woff2) format('woff2'),url(/content/dam/global_pdc/site-furniture/horizon/HunterW05-Condensed.woff) format('woff')