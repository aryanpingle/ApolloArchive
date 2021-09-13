const all_audios = {
    "A": new Array(63),
    "H": new Array(22)
}
var current_audio = null

var focused_datapoint = null
var selected_datapoint = null
var datapoints = []

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

function setup_local() {
    print("Starting local setup")
    
    // Set up the SIDEBAR constant
    SIDEBAR = {}
    let [TITLE, DESCRIPTION, IMAGE] = gid("desktop-sidebar").children
    SIDEBAR.title = TITLE
    SIDEBAR.description = DESCRIPTION
    SIDEBAR.image = IMAGE
    
    // Set up the POPUP constant
    let POPUP_ELEMENT = gid("datapoint-popup")
    let [header, dtype, audio, text] = gid("popup-info").children
    POPUP = {
        element: POPUP_ELEMENT,
        header: header,
        dtype: dtype,
        audio: audio,
        text: text
    }
    
    setup_datatype_links() // Verified
    setup_close_buttons() // Verified
    set_datapoint_events() // Verified
    set_datapoint_expansion_sizes() // Verified
    setup_key_presses()
    document.body.classList.add("classic-layout")
}

function resize_handler_local() {
    set_datapoint_expansion_sizes()
}

/**
* Returns true if the the datapoints are displayed in classic layout, else false.
*/

function is_classic_layout() {
    return !mobile_mode && document.body.classList.contains("classic-layout");
}

/**
* Adds onclick events to all div.datapoint-choice elements such that when they're clicked, the correct datatype section pops up
* If classic layout is enabled, then the first element of that section is given the 'focused' class
*/

function setup_datatype_links() {
    let stime = new Date()
    for(const datatype_choice of gid("datapoint-types-inner").children) {
        datatype_choice.onclick = event=>{
            // If you clicked on the currently selected datatype choice, then ignore
            let current_datatype_choice = document.getElementsByClassName("datatype-selected")[0]
            if(current_datatype_choice == datatype_choice) return
            // If it is another choice, de-select it and hide its corresponding section
            if(current_datatype_choice) {
                current_datatype_choice.classList.remove("datatype-selected")
                gid(current_datatype).classList.remove("shown")
                // EXTRA: Stop the currently playing audio and de-select the selected datapoint
                stop_audio()
                if(selected_datapoint) {
                    selected_datapoint.classList.remove("selected")
                    selected_datapoint = null
                }
            }
            datatype_choice.classList.add("datatype-selected")
            current_datatype = datatype_choice.getAttribute("target");
            // Update the poster
            [...document.getElementsByClassName("datatype-poster")].forEach(ele=>{
                ele.src = `Images/${current_datatype.startsWith("Text")?"text":current_datatype.toLowerCase()}-poster.png`
            })
            // Show the container for the datatype
            gid("datatype-container").classList.add("shown")
            // Show the section with all the datapoints
            gid(current_datatype).classList.add("shown")
            // Hide the datatype-choser section (this too is for mobile only)
            gid("datapoint-types").classList.remove("shown")
            // Update the datapoints array
            datapoints = gid(current_datatype).querySelector(".datapoint-container").children
            
            // If classic layout is enabled, focus the first one
            if(is_classic_layout()) {
                focus_datapoint(datapoints[0])
            }
        }
    }
    logtime(stime, "setup_datatype_links")
}

/**
* Adds onclick events to the 'X' images in each datatype section's header, such that they'll remove the 'shown' class from the datatype-container
*/

function setup_close_buttons() {
    let stime = new Date()
    for(const ele of document.querySelectorAll(".datatype-title > img")) {
        ele.onclick = event=>{
            let datatype_section = ele.parentElement.parentElement
            datatype_section.classList.remove("shown")
            gid("datatype-container").classList.remove("shown")
            gid("datapoint-types").classList.add("shown")
            // Stop playing audio, if at all
            stop_audio()
        }
    }
    logtime(stime, "setup_close_buttons")
}

/**
* Assigns a position attribute to every datapoint under every datapoint-container, starting from 1
*/

function setup_datapoint_numbers() {
    let stime = new Date();
    // All the datapoints
    // logtime(stime, "setup_datapoint_numbers (I)")
    // Just the popup element
    let datapoint = gid("popup-content")
    let datapoint_audio = datapoint.querySelector(".datapoint-audio")
    let play_button = datapoint_audio.children[1]
    // print(play_button)
    play_button.onclick = event=>{
        event.stopPropagation()
        toggle_audio_playback()
    }
    let audio = datapoint.querySelector("audio")
    audio.addEventListener("timeupdate", function yuh() {
        update_progress_bar(this)
    })
    audio.onended = event=>{
        audio.parentElement.classList.remove("playing")
    }
    logtime(stime, "setup_datapoint_numbers")
}

/* AUDIO HANDLERS */

function toggle_audio_playback() {
    if(current_audio.paused) {
        play_audio()
    }
    else {
        pause_audio()
    }
}

function update_progress_bar() {
    if(selected_datapoint) selected_datapoint.getElementsByClassName("progress-bar")[0].style.setProperty("--perc", 100 * current_audio.currentTime / current_audio.duration)
}

/**
* Returns the audio associated with the selected_datapoint. If the audio has not been loaded yet, it is loaded. If the datapoint isn't a media-type datapoint, returns `null`
*/

function play_audio() {
    current_audio.play()
    selected_datapoint.classList.add("playing")
}

/**
* Pauses the currently playing datapoint audio. No arguments to be passed as the global `current_audio` refers to it anyway.
*/

function pause_audio() {
    if(current_audio) {
        current_audio.pause()
        selected_datapoint.classList.remove("playing")
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

/**
* Loads the audio associated with the selected_datapoint
*/

function load_audio() {
    let media_type = selected_datapoint.getAttribute("media-type")
    if(!media_type) {
        current_audio = null
        return null
    }
    let datapoint_position = parseInt(selected_datapoint.getAttribute("position"))
    
    if(all_audios[media_type][datapoint_position-1]) {
        // If the audio is already loaded:
        current_audio = all_audios[media_type][datapoint_position-1]
        return current_audio
    }
    // Since the audio hasn't been loaded yet, load it now
    let audio = new Audio(`../Audio/HZD ${media_type} ${datapoint_position}.mp3`)
    audio.ontimeupdate = update_progress_bar
    audio.onended = stop_audio
    all_audios[media_type][datapoint_position-1] = audio
    current_audio = audio
    return all_audios[media_type][datapoint_position-1]
}

/**
* Adds a css variable `--datapoint-text-size` to all datapoint elements which indicates how much the datapoint-content will expand to.
* It's based on the height of the text element inside .datapoint-content
*/

function set_datapoint_expansion_sizes() {
    // IM A FUCKING GOD
    // Reading the height of an element causes a reflow to happen so that the layout isn't 'stale'. But the next read won't cause a reflow because the layout isn't stale anymore.
    // Previous code: (read then write) repeat = N read reflows + N style set reflows
    // Current code: read all then write all = 1 read reflow + N style set reflows
    
    let stime = new Date()
    let arr = Array.from(document.getElementsByClassName("datapoint"))
    let heights = arr.map(ele=>ele.getElementsByTagName("text")[0].offsetHeight)
    arr.forEach((ele, index)=>ele.style.setProperty('--datapoint-text-size', heights[index]))
    logtime(stime, "set_expansion_sizes");
}

/**
* Multipurpose function
* 1. Sets onclick events to datapoint titles such that in list mode when clicked, select_element() is called on that datapoint. Actually, you don't need to check for list mode here, since titles are shown ONLY in list mode anyway.
* 2. Sets onmouseover events to datapoints such that when hovered, focus_element() is called on that datapoint
* 3. Sets onclick events to datapoints such that in classic mode when clicked, select_element() is called on that datapoint
* 
* So to recap, select_element() is called on an element if the header is clicked in list mode, or if the datapoint is clicked in classic mode
*/

function set_datapoint_events() {
    let stime = new Date();
    [...document.getElementsByClassName("datapoint")].forEach((datapoint, index)=>{
        datapoint.setAttribute("position", (index%63)+1)

        // 1. Set onclick event for datapoint titles
        let datapoint_title = datapoint.firstElementChild
        datapoint_title.onclick = event=>{
            event.stopPropagation()
            select_datapoint()
        }
        
        // 2. Set onmouseover event for datapoints
        datapoint.onmouseover = event=>{
            focus_datapoint(datapoint)
        }
        
        // 3. Set onclick event for datapoints
        datapoint.onclick = event=>{
            if(event.target.matches(".play-button")) {
                toggle_audio_playback()
            }
            else if(is_classic_layout()) {
                init_popup(datapoint)
            }
            else select_datapoint()
        }
    })
    logtime(stime, "set_datapoint_events")
}

/* POPUP HANDLERS */

function init_popup(datapoint) {
    POPUP_MODE = true
    // Due to the layout of datapoints and my shit naming system, #popup-content acts like the datapoint div, so add the media-type to it
    let mt = datapoint.getAttribute("media-type")
    if(mt) gid("popup-content").setAttribute("media-type", mt)
    else gid("popup-content").removeAttribute("media-type")
    // Set the header
    POPUP.header.innerHTML = datapoint.firstElementChild.firstElementChild.innerHTML
    // Set the datatype
    POPUP.dtype.innerHTML = current_datatype
    // Set the audio
    // if(mt) POPUP.audio.firstElementChild.src = datapoint.getElementsByTagName("audio")[0].src
    // Set the text
    POPUP.text.innerHTML = datapoint.lastElementChild.lastElementChild.innerHTML
    
    POPUP.element.classList.add("shown")
}

function close_popup() {
    POPUP_MODE = false
    POPUP.element.classList.remove("shown")
    // Pause if playing
    if(gid("popup-content").getAttribute("media-type")) {
        POPUP.audio.classList.remove("playing")
        POPUP.audio.firstElementChild.pause()
        POPUP.audio.firstElementChild.currentTime = 0
    }
}

function focus_datapoint(datapoint) {
    if(focused_datapoint == datapoint) return;
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
        stop_audio()
        selected_datapoint = null
        return
    }
    if(selected_datapoint) {
        // De-select currently focused datapoint
        selected_datapoint.classList.remove("selected")
        stop_audio()
    }
    // Select the currently focused datapoint
    focused_datapoint.classList.add("selected")
    selected_datapoint = focused_datapoint
    load_audio()
}

/*
Aight
So
When you hover over a datapoint, you give them a selected class and put their value into the info sidebar
But only when you click it does the popup get initialized
it's good because on mobile hover = click so they become yellow + their datapoint content is shown
*/

function prepare_datapoint_expansions() {
    for(const ele of document.getElementsByClassName("datapoint-title")) {
        // Set the onclick event
        let parent = ele.parentElement
        // The following onclick handler is ONLY for list layout, where if you click the header, the content expands
        ele.onclick = event=>{
            if(is_classic_layout()) return;
            if(parent.classList.contains("selected")) {
                parent.classList.remove("selected")
                return
            }
            document.querySelector(".selected")?.classList.remove("selected")
            parent.classList.add("selected");
        }
    }
    // The following onmouseover handler is ONLY for classic layout. If a datapoint is hovered over, it gets the class 'selected', 
    for(const ele of document.getElementsByClassName("datapoint")) {
        ele.onmouseover = event=>{
            if(!is_classic_layout() || ele.classList.contains("selected")) return;
            // print("MOUSEOVERED")
            document.querySelector(".selected").classList.remove("selected")
            ele.classList.add("selected");
            new Audio("click2.mp3").play()
        }
        ele.onclick = event=>{
            if(!is_classic_layout()) return;
            activate_datapoint(ele)
        }
    }
}

// Overrides the main.js setup_key_presses()

function setup_key_presses() {
    document.body.onkeydown = event=>{
        let key = event.key
        
        // If popup is enabled
        if(POPUP_MODE) {
            if(key == "f") {
                toggle_audio_playback(POPUP.audio.firstElementChild)
            }
            else if(key == "Escape") {
                close_popup()
            }
            return;
        }
        
        if (key == "q") {
            go_to_previous_page()
        }
        else if (key=="e") {
            go_to_next_page()
        }
        else if(key == "Tab") {
            event.preventDefault()
            
            toggle_layout()
        }
        else if(key == "f") {
            if(is_classic_layout()) init_popup(focused_datapoint)
            else select_datapoint()
        }
        else if(is_classic_layout()) {
            // Since this is a classic layout, we need to traverse the grid
            let columns = parseInt(getComputedStyle(gid(current_datatype).querySelector(".datapoint-container")).getPropertyValue("--columns"))
            let new_index = 0;
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
            // print(`New Index: ${new_index}`)
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
}

function toggle_layout() {
    // print("Tab pressed")
    
    if (document.body.classList.contains("classic-layout")) {
        // Switch to list layout
        document.body.classList.remove("classic-layout")
    }
    else {
        document.body.classList.add("classic-layout")
    }
    
    // Necessary because display: none causes the first time to not work
    // set_datapoint_expansion_sizes()
}