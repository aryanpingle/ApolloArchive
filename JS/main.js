const print = console.log
const get_params = ()=>{
    let url = window.location.href
    return url.indexOf("?")==-1?[""]:url.substr(url.indexOf("?")+1).split("&")
}
const gid = id_name=>document.getElementById(id_name)
const sum = (list, lambda=e=>e)=>list.reduce((acc,val)=>acc+lambda(val), 0)

var mobile_mode = true;

function setup_main() {
    if(window.innerWidth >= 1024) {
        mobile_mode = false;
    }
    set_mobile_nav_delays()
    set_mobile_links()
    setup_key_presses()
    setup_navigation_buttons()
}

/**
 * Rechecks whether this is a mobile mode or not
 */

function resize_handler_main() {
    if(window.innerWidth >= 1024) {
        mobile_mode = false;
    }
}

// Mobile Values
mobile_nav_shown = false

function toggle_nav() {
    mobile_nav_shown = !mobile_nav_shown;
    if(mobile_nav_shown) {
        document.body.classList.add("nav-expanded")
    } else {
        document.body.classList.remove("nav-expanded")
    }
}

function set_mobile_nav_delays() {
    let arr = document.querySelectorAll("#mobile-nav .nav-body > *")
    document.body.style = `--base-delay: ${250 / arr.length}ms`
    arr.forEach((ele, index)=>{
        // '250 + ...' is the time taken for the page to disappear
        ele.style = `--delay: ${250 + (index * 250 / arr.length)}ms`
    })
}

const $ = query=>document.querySelectorAll(query)

function set_mobile_links() {
    for(const ele of $(".nav-body > *")) {
        if(ele.innerHTML == window.location.href.replace(".html", "").split(/[\W\.]/).pop()) {
            ele.classList.add("current")
        }
        print()
    }
}

function go_to_previous_page() {
    let sib = $("#desktop-nav .current")[0].previousElementSibling
    if (sib==null) {
        $("#desktop-nav .nav-body")[0].lastElementChild.click()
    }
    else {
        sib.click()
    }
}

function go_to_next_page() {
    let sib = $("#desktop-nav .current")[0].nextElementSibling
    if (sib==null) {
        $("#desktop-nav .nav-body")[0].firstElementChild.click()
    }
    else {
        sib.click()
    }
}

function setup_key_presses() {
    document.body.onkeydown = event=>{
        let key = event.key
        if (key == "q") {
            go_to_previous_page()
        }
        else if (key=="e") {
            go_to_next_page()
        }
    }
}

function setup_navigation_buttons() {
    gid("navigate-left").onclick = go_to_previous_page
    gid("navigate-right").onclick = go_to_next_page
}