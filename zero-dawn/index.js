"use strict"

const all_audios = {
    "/zero-dawn": {
        "A": new Array(63).fill(null),
        "H": new Array(22).fill(null)
    },
    "/zero-dawn/the-frozen-wilds": {
        "A": new Array(25).fill(null),
        "H": new Array(3).fill(null)
    }
}
var audio_durations = {"/zero-dawn": {"A":[20,20,32,24,33,32,44,8,39,46,52,19,31,37,20,23,51,58,45,54,25,20,32,46,66,23,118,81,72,46,68,43,55,50,85,59,65,70,61,65,61,91,66,76,71,76,97,16,25,77,91,66,97,17,14,22,25,63,85,69,81,62,52],"H":[24,10,45,52,44,55,59,74,85,163,244,60,55,70,45,25,41,35,84,218,143,106]},"/zero-dawn/the-frozen-wilds": {"A":[16,23,30,28,29,19,110,20,26,36,19,19,25,29,15,15,10,28,8,19,139,16,22,25,12],"H":[92,29,25]}}
var current_audio = null

var focused_datapoint = null
var selected_datapoint = null
var datapoints = []
var all_texts = null

var current_datatype = ""

var POPUP_MODE = false

var SIDEBAR = {
    title: null,
    description: null,
    image: null
}

var POPUP = {
    element: null,
    header: null,
    dtype: null,
    audio: null,
    text: null
}

// Mobile Values
var mobile_nav_shown = false
var mobile_mode = false

window.onresize = () => {
    if(window.innerWidth <= 1024) {
        mobile_mode = true
    }
    else {
        mobile_mode = false
    }
    document.body.clientWidth
}

function setup_local() {
    set_mobile_nav_delays()

    if(window.navigator.onLine) {
        document.getElementById("network-status").classList.remove("offline")
    }
    else
    {
        document.getElementById("network-status").classList.add("offline")
    }
    window.onoffline = () => {
        document.getElementById("network-status").classList.add("offline")
    }
    window.ononline = () => {
        document.getElementById("network-status").classList.remove("offline")
    }
    
    init_popup()
    create_audio_elements()
    setup_datatype_links()
    setup_close_buttons()
    prepare_datapoints()
    setup_key_presses()
    document.body.classList.add("classic-layout")
}

function toggle_nav() {
    mobile_nav_shown = !mobile_nav_shown;
    if(mobile_nav_shown) {
        document.body.classList.add("nav-expanded")
    } else {
        document.body.classList.remove("nav-expanded")
    }
}

function set_mobile_nav_delays() {
    let arr = document.querySelectorAll("#mobile-nav > .nav-body  > .nav__link")
    document.body.style.setProperty(`--base-delay`, `${250 / arr.length}ms`)
    arr.forEach((ele, index)=>{
        // '250 + ...' is the time taken for the page to disappear
        ele.style.setProperty("--delay", `${250 + (index * 250 / arr.length)}ms`)
    })
}

function go_to_previous_page() {
    let sib = document.querySelector(".nav__link--current").previousElementSibling
    sib ? sib.click() : document.querySelector(".nav-body.desktop-nav__child").lastElementChild.click()
}

function go_to_next_page() {
    let sib = document.querySelector(".nav__link--current").nextElementSibling
    sib ? sib.click() : document.querySelector(".nav-body.desktop-nav__child").firstElementChild.click()
}

/**
* Returns true if the the datapoints are displayed in classic layout, else false.
*/

function is_classic_layout() {
    return !mobile_mode && document.body.classList.contains("classic-layout")
}

/**
* Adds onclick events to all div.datapoint-choice elements such that when they're clicked, the correct datatype section pops up
* NEW: Loads the relevant Texts/[target].json file
* If classic layout is enabled, then the first element of that section is given the 'focused' class
*/

function setup_datatype_links() {
    let stime = new Date()
    for(const datatype_choice of document.querySelector("#datapoint-types-inner").children) {
        datatype_choice.onclick = async event=>{
            event.stopPropagation()
            let stime = new Date()
            // If you clicked on the currently selected datatype choice, then ignore
            let current_datatype_choice = datatype_choice.parentElement.querySelector(".datatype-selected")
            if(current_datatype && current_datatype_choice == datatype_choice) return
            // If it is another choice, de-select it and hide its corresponding section
            if(current_datatype) {
                current_datatype_choice.classList.remove("datatype-selected")
                document.getElementById(current_datatype).classList.remove("shown")
                pause_audio()
                if(selected_datapoint) {
                    selected_datapoint.classList.remove("selected")
                    selected_datapoint = null
                }
            }
            
            datatype_choice.classList.add("datatype-selected")
            current_datatype = datatype_choice.getAttribute("target")
            all_texts = await (await fetch(`${base}/texts/${current_datatype}.json`)).json()
            // Update the poster
            Array.from(document.getElementsByClassName("datatype-poster")).forEach(ele=>{
                ele.src = `/zero-dawn/images/poster-${current_datatype.startsWith("Text")?"text":current_datatype.toLowerCase()}.png`
            })
            // Show the container for the datatype
            document.getElementById("datatype-container").classList.add("shown")
            // Show the section with all the datapoints
            document.getElementById(current_datatype).classList.add("shown")
            // Hide the datatype-choser section (this too is for mobile only)
            document.getElementById("datapoint-types").classList.remove("shown")
            // Update the datapoints array
            datapoints = document.getElementById(current_datatype).getElementsByClassName("datapoint-container")[0].children
            
            focus_datapoint(datapoints[0])
            
            // logtime(stime, "link_event")
        }
    }
    // logtime(stime, "setup_datatype_links")
}

/**
* Adds onclick events to the 'X' images in each datatype section's header, such that they'll remove the 'shown' class from the datatype-container
*/

function setup_close_buttons() {
    // TODO: Make the thing hide when you click close, but somehow it should be shown in desktop mode
    let stime = new Date()
    for(const ele of document.querySelectorAll(".datatype-title > img")) {
        ele.onclick = event=>{
            let datatype_section = ele.parentElement.parentElement
            datatype_section.classList.remove("shown")
            document.getElementById("datatype-container").classList.remove("shown")
            document.getElementById("datapoint-types").classList.add("shown")
            document.getElementById("datapoint-types").querySelector(".datatype-selected").classList.remove("datatype-selected")
            current_datatype = null
            // Pause the playing audio, if at all
            pause_audio()
        }
    }
    // logtime(stime, "setup_close_buttons")
}

/**
* Multipurpose function
* 1. Sets the audio duration
* 2. Sets onmouseover events to datapoints such that when hovered, focus_element() is called on that datapoint
* 3. Sets onclick events to datapoints such that in classic mode when clicked, select_element() is called on that datapoint
* 
* So to recap, select_element() is called on an element if the header is clicked in list mode, or if the datapoint is clicked in classic mode
*/

function prepare_datapoints() {
    let stime = new Date()
    Array.from(document.querySelectorAll(".datapoint-container")).forEach(datapoint_container => {
        Array.from(datapoint_container.querySelectorAll(".datapoint")).forEach((datapoint, index)=>{
            datapoint.setAttribute("position", index+1)
    
            // 1. Set the audio duration
            if(datapoint.getAttribute("media-type")) datapoint.querySelector(".ratio").textContent = `0:00 / ${getTimeStamp(audio_durations[base][datapoint.getAttribute("media-type")][index])}`
            
            // 2. Set onmouseover event for datapoints
            datapoint.onmouseover = event=>{
                focus_datapoint(datapoint)
            }
            
            // 3. Set onclick event for datapoints
            datapoint.onclick = event=>{
                if(event.target.matches(".play-button")) {
                    toggle_audio_playback()
                }
                else if(event.target.matches(".progress-bar")) {
                    current_audio.currentTime = current_audio.duration * event.offsetX / event.srcElement.clientWidth
                }
                else if(event.target.matches(".datapoint, .datapoint-title, .datapoint-title > header")) {
                    select_datapoint()
                }
            }
        })
    })
    // logtime(stime, "set_datapoint_events")
}

/* AUDIO HANDLERS */

function toggle_audio_playback() {
    if(!current_audio) return

    if(current_audio.paused) {
        play_audio()
    }
    else {
        pause_audio()
    }
}

function getTimeStamp(time) {
    if(time == undefined || time == null) return `0:00`
    let played = parseInt(time)
    let zeros = (n, dig) => Array(`${10**(dig-1)}`.length - `${n?n:0}`.length).fill(0).join("") + "" + n
    return `${parseInt(played / 60)}:${zeros(played % 60, 2)}`
}

function update_progress_bar() {
    if(!selected_datapoint || !current_audio) return
    
    // Update the progress bar
    let perc = 100 * current_audio.currentTime / current_audio.duration
    selected_datapoint.getElementsByClassName("progress-bar")[0].style.setProperty("--perc", perc)
    POPUP.audio.children[1].style.setProperty("--perc", perc)
    // Update the played / length text
    if(current_audio) {
        let current_timestamp = getTimeStamp(current_audio.currentTime)
        let duration_timestamp = getTimeStamp(audio_durations[base][selected_datapoint.getAttribute("media-type")][parseInt(selected_datapoint.getAttribute("position")) - 1])
        // Apply to the default datapoint audio element
        selected_datapoint.querySelector(".ratio").textContent = `${current_timestamp} / ${duration_timestamp}`
        // Apply to the popup datapoint audio element
        POPUP.audio.querySelector(".ratio").textContent = `${current_timestamp} / ${duration_timestamp}`
    }
}

/**
* Returns the audio associated with the selected_datapoint. If the audio has not been loaded yet, it is loaded. If the datapoint isn't a media-type datapoint, returns `null`
*/

function play_audio() {
    current_audio.play()
    if(selected_datapoint) {
        selected_datapoint.classList.add("playing")
    }
    POPUP.audio.classList.add("playing")
}

/**
* Pauses the currently playing datapoint audio. No arguments to be passed as the global `current_audio` refers to it anyway.
*/

function pause_audio() {
    if(current_audio) {
        current_audio.pause()
        if(selected_datapoint) {
            selected_datapoint.classList.remove("playing")
        }
        POPUP.audio.classList.remove("playing")
    }
}

/**
* Stops the currently playing datapoint audio. No arguments to be passed as the global `current_audio` refers to it anyway.
*/

function stop_audio() {
    if(current_audio) {
        pause_audio()
        current_audio.currentTime = 0
    }
}

function create_audio_elements() {
    for(let audios of Object.values(all_audios[base])) {
        for(let i = 0; i < audios.length; ++i) {
            let audio = document.createElement("AUDIO")
            audio.ontimeupdate = update_progress_bar
            audio.onended = stop_audio
            audios[i] = audio
        }
    }
}

/**
* Sets current_audio to the audio associated with the datapoint
* If the datapoint is not a media type, sets current_audio to null
*/

function load_audio() {
    let media_type = selected_datapoint.getAttribute("media-type")
    if(!media_type) {
        current_audio = null
        return null
    }
    
    let datapoint_position = parseInt(selected_datapoint.getAttribute("position"))
    current_audio = all_audios[base][media_type][datapoint_position-1]
    return current_audio
}

/* POPUP HANDLERS */

/**
* Initializes the popup format
*/

function init_popup() {
    let stime = new Date()

    // Set up the SIDEBAR constant
    SIDEBAR = {}
    let [TITLE, DESCRIPTION, IMAGE] = document.getElementById("desktop-sidebar").children
    SIDEBAR.title = TITLE
    SIDEBAR.description = DESCRIPTION
    SIDEBAR.image = IMAGE
    
    // Set up the POPUP constant
    let POPUP_ELEMENT = document.getElementById("datapoint-popup")
    let [header, dtype, audio, text] = document.getElementById("popup-info").children
    POPUP = {
        element: POPUP_ELEMENT,
        header: header,
        dtype: dtype,
        audio: audio,
        text: text
    }
    // Just the popup element
    let play_button = POPUP.element.querySelector(".play-button")
    play_button.onclick = toggle_audio_playback
    play_button.nextElementSibling.onclick = event => {
        current_audio.currentTime = current_audio.duration * event.offsetX / event.srcElement.clientWidth
    }
    // logtime(stime, "setup_datapoint_numbers")
}

/**
* Intialize the popup with the selected datapoint's attributes 
*/

function update_popup() {
    // Set the datapoint title
    POPUP.header.textContent = selected_datapoint.querySelector("header").textContent
    // Set the datatype
    POPUP.dtype.innerHTML = current_datatype
    
    let media_type = selected_datapoint.getAttribute("media-type")
    
    // Set the popup text
    POPUP.text.querySelector("text").innerHTML = all_texts[parseInt(selected_datapoint.getAttribute("position")) - 1]
    
    if(media_type) {
        // Reset progress bar
        POPUP.audio.children[1].style.setProperty("--perc", 100 * current_audio.currentTime / current_audio.duration)
        
        // Set ratio
        let current_timestamp = getTimeStamp(current_audio.currentTime)
        let duration_timestamp = getTimeStamp(audio_durations[base][media_type][parseInt(selected_datapoint.getAttribute("position")) - 1])
        POPUP.audio.querySelector(".ratio").textContent = `${current_timestamp} / ${duration_timestamp}`
        
        // Set media type attribute
        document.getElementById("popup-content").setAttribute("media-type", media_type)
        document.getElementById("popup-main").setAttribute("media-type", media_type)
    }
    else {
        // Remove media type attribute
        document.getElementById("popup-content").removeAttribute("media-type")
        document.getElementById("popup-main").removeAttribute("media-type")
    }
    
    show_popup()
}

function show_popup() {
    POPUP_MODE = true
    POPUP.element.classList.add("shown")
}

function close_popup() {
    POPUP_MODE = false
    // Pause if playing
    pause_audio()
    POPUP.element.classList.remove("shown")
}

function focus_datapoint(datapoint) {
    if(focused_datapoint == datapoint) return
    // print("Changing focused_datapoint")
    if(focused_datapoint) {
        focused_datapoint.classList.remove("focused")
    }
    focused_datapoint = datapoint
    datapoint.classList.add("focused")
    // Add details to the sidebar
    SIDEBAR.title.innerHTML = datapoint.firstElementChild.firstElementChild.innerHTML
    SIDEBAR.description.innerHTML = datapoint.getAttribute("description")
}

function select_datapoint() {
    if(selected_datapoint == focused_datapoint) {
        // De-select currently focused datapoint
        selected_datapoint.classList.remove("selected")
        // Now that the datapoint has display: none, changes to its children won't cause reflow
        stop_audio()
        close_popup()
        selected_datapoint = null
        return
    }
    // So now, we know it's a new datapoint that's been selected
    if(selected_datapoint) {
        // De-select currently focused datapoint
        selected_datapoint.classList.remove("selected")
        // Now that the datapoint has display: none, changes to its children won't cause reflow
        pause_audio()
    }
    
    // First of all, select the currently focused datapoint
    selected_datapoint = focused_datapoint
    let media_type = selected_datapoint.getAttribute("media-type")
    
    // Set current_audio
    if(!media_type) {
        current_audio = null
    }
    else {
        let datapoint_position = parseInt(selected_datapoint.getAttribute("position"))
        current_audio = all_audios[base][media_type][datapoint_position-1]
        if(!all_audios[base][media_type][datapoint_position-1].src) {
            current_audio.src = `${base}/audio/HZD ${media_type} ${datapoint_position}.mp3`
        }
    }
    // If the text hasn't been set, do it now
    if(!selected_datapoint.querySelector("text").textContent) {
        selected_datapoint.querySelector("text").innerHTML = all_texts[parseInt(selected_datapoint.getAttribute("position")) - 1]
    }
    
    update_popup()
    
    // After selecting the datapoint, changes to the datapoint will cause reflow
    selected_datapoint.classList.add("selected")
    selected_datapoint.scrollIntoView()
}

// Overrides the main.js setup_key_presses()

function setup_key_presses() {
    let stime = new Date()
    window.onkeydown = event=>{
        let key = event.key
        
        // If popup is enabled
        if(POPUP_MODE && is_classic_layout()) {
            if(key == "f" || key == "Enter") {
                toggle_audio_playback(POPUP.audio.firstElementChild)
            }
            else if(key == "Escape") {
                close_popup()
            }
            else {
                print(key)
            }
            return
        }
        // POPUP is definitely not enabled
        else if (key == "q") {
            go_to_previous_page()
        }
        else if (key=="e") {
            go_to_next_page()
        }
        else if(key == "CapsLock") {
            event.preventDefault()
            
            toggle_layout()
        }
        else if(key == "f" || key == "Enter") {
            select_datapoint()
        }
        else if(is_classic_layout()) {
            if(!["w", "a", "s", "d", "ArrowUp", "ArrowLeft", "ArrowDown", "ArrowRight"].includes(key)) return
            // Since this is a classic layout, we need to traverse the grid
            let columns = parseInt(getComputedStyle(document.getElementById(current_datatype).querySelector(".datapoint-container")).getPropertyValue("--columns"))
            let new_index = 0
            let position = parseInt(focused_datapoint.getAttribute("position"))
            if(key == "w" || key == "ArrowUp") {
                new_index = position-columns
            }
            else if(key == "s" || key == "ArrowDown") {
                new_index = position+columns
            }
            else if(key == "d" || key == "ArrowRight") {
                new_index = position+1
            }
            else if(key == "a" || key == "ArrowLeft") {
                new_index = position-1
            }
            else {
                return
            }
            focus_datapoint(datapoints[Math.max(1, Math.min(datapoints.length, new_index))-1])
        }
        // At this point it definitely isn't classic layout, so assume this is all for list layout
        else if(key == "w" || key == "ArrowUp") {
            let new_element = focused_datapoint.previousElementSibling
            if(new_element) {
                focus_datapoint(new_element)
                new_element.parentElement.click()
                new_element.scrollIntoView({ block: 'center' })
            }
        }
        else if(key == "s" || key == "ArrowDown") {
            let new_element = focused_datapoint.nextElementSibling
            if(new_element) {
                focus_datapoint(new_element)
                new_element.parentElement.click()
                new_element.scrollIntoView({ block: 'center' })
            }
        }
        else {
            print(key)
        }
    }
    // logtime(stime, "setup_key_presses")
}

function toggle_layout() {
    if (document.body.classList.contains("classic-layout")) {
        document.body.classList.remove("classic-layout")
    }
    else {
        document.body.classList.add("classic-layout")
    }
}