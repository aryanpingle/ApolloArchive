var bruh = new Audio("click.mp3")

var focused_datapoint = null
var datapoints = []

var current_datatype = ""

var POPUP_MODE = false

var SIDEBAR = {
    title: 0,
    description: 0,
    image: 0
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
    setup_datapoint_numbers() // Verified
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
    for(const datatype_choice of gid("datapoint-types-inner").children) {
        datatype_choice.onclick = event=>{
            document.querySelector(".datatype-selected")?.classList.remove("datatype-selected")
            datatype_choice.classList.add("datatype-selected")
            if(current_datatype) gid(current_datatype).classList.remove("shown")
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
            
            // If classic layout is enabled, select the first one
            if(is_classic_layout()) {
                focus_datapoint(datapoints[0])
            }
        }
    }
}

/**
* Adds onclick events to the 'X' images in each datatype section's header, such that they'll remove the 'shown' class from the datatype-container
*/

function setup_close_buttons() {
    for(const ele of document.querySelectorAll(".datatype-title > img")) {
        ele.onclick = event=>{
            let datatype_section = ele.parentElement.parentElement
            datatype_section.classList.remove("shown")
            gid("datatype-container").classList.remove("shown")
            gid("datapoint-types").classList.add("shown")
            // Stop playing audio, if at all
            if(focused_datapoint && focused_datapoint.getAttribute("media-type")) {
                let cum = focused_datapoint.querySelector("audio")
                cum.pause()
                cum.currentTime = 0
            }
        }
    }
}

/**
* Assigns a position attribute to every datapoint under every datapoint-container, starting from 1
*/

function setup_datapoint_numbers() {
    // All the datapoints
    [...document.getElementsByClassName("datapoint-container")].forEach(datapoint_container=>{
        [...datapoint_container.children].forEach((datapoint, index)=>{
            datapoint.setAttribute("position", index+1)
            
            let media_type = datapoint.getAttribute("media-type")
            if(media_type) {
                // Prep the play-button
                let datapoint_audio = datapoint.querySelector(".datapoint-audio")
                datapoint_audio.onclick = event=>event.stopPropagation()
                let play_button = datapoint_audio.firstElementChild
                play_button.onclick = event=>{
                    event.stopPropagation()
                    toggle_audio_playback(play_button.previousElementSibling)
                }
                // Create the audio element
                let audio = document.createElement("AUDIO")
                audio.preload = "metadata"
                datapoint.lastElementChild.firstElementChild.prepend(audio)
                audio.src = `Audio/HZD ${media_type} ${index+1}.mp3`
                audio.addEventListener("timeupdate", function yuh() {
                    update_progress_bar(this)
                })
                audio.onended = event=>{
                    audio.parentElement.classList.remove("playing")
                }
            }
        })
    })
    // Just the popup element
    let datapoint = gid("popup-content")
    let datapoint_audio = datapoint.querySelector(".datapoint-audio")
    let play_button = datapoint_audio.children[1]
    // print(play_button)
    play_button.onclick = event=>{
        event.stopPropagation()
        toggle_audio_playback(play_button.previousElementSibling)
    }
    let audio = datapoint.querySelector("audio")
    audio.addEventListener("timeupdate", function yuh() {
        update_progress_bar(this)
    })
    audio.onended = event=>{
        audio.parentElement.classList.remove("playing")
    }
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

/**
* Adds a css variable `--datapoint-text-size` to all datapoint elements which indicates how much the datapoint-content will expand to.
* It's based on the height of the text element inside .datapoint-content
*/

function set_datapoint_expansion_sizes() {
    for(const ele of document.getElementsByClassName("datapoint")) {
        // Set the expansion height based on the content size
        let height = ele.querySelector("text").offsetHeight
        ele.style = `--datapoint-text-size: ${height}px`
    }
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
    for(const datapoint of document.getElementsByClassName("datapoint")) {
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
            if(is_classic_layout()) {
                init_popup(datapoint)
            }
            else select_datapoint()
        }
    }
}

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
    if(mt) POPUP.audio.firstElementChild.src = datapoint.getElementsByTagName("audio")[0].src
    // Set the text
    POPUP.text.innerHTML = datapoint.lastElementChild.lastElementChild.innerHTML
    
    POPUP.element.classList.add("shown")
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
    let current_selected = document.querySelector(".datapoint.selected")
    if(current_selected == focused_datapoint) {
        // print("Removing selection")
        current_selected.classList.remove("selected")
        if(current_selected.getAttribute("media-type")) {
            current_selected.getElementsByTagName("audio")[0].pause()
            current_selected.getElementsByTagName("audio")[0].currentTime = 0
            current_selected.getElementsByTagName("audio")[0].parentElement.classList.remove("playing")
        }
        return
    }
    if(current_selected) {
        if(current_selected.getAttribute("media-type")) current_selected.getElementsByTagName("audio")[0].pause()
        current_selected.classList.remove("selected")
    }
    // print("Selecting focused_datapoint")
    focused_datapoint.classList.add("selected")
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
            document.querySelector(".datapoint.selected")?.classList.remove("selected")
            parent.classList.add("selected");
        }
    }
    // The following onmouseover handler is ONLY for classic layout. If a datapoint is hovered over, it gets the class 'selected', 
    for(const ele of document.getElementsByClassName("datapoint")) {
        ele.onmouseover = event=>{
            if(!is_classic_layout() || ele.classList.contains("selected")) return;
            // print("MOUSEOVERED")
            document.querySelector(".datapoint.selected").classList.remove("selected")
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
            let columns = parseInt(getComputedStyle(gid(current_datatype).getElementsByClassName("datapoint-container")[0]).getPropertyValue("--columns"))
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

function toggle_audio_playback(audio_element) {
    if(audio_element.paused) {
        audio_element.play()
        audio_element.parentElement.classList.add("playing")
    }
    else {
        audio_element.pause()
        audio_element.parentElement.classList.remove("playing")
    }
}

function update_progress_bar(audio_element) {
    audio_element.parentElement.style = `--perc: ${100 * audio_element.currentTime / audio_element.duration}%`
}