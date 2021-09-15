const print = console.log
const gid = id_name=>document.getElementById(id_name)
const sum = (list, lambda=e=>e)=>list.reduce((acc,val)=>acc+lambda(val), 0)
const logtime = (stime, process, color="greenyellow")=>print(`%c${process}%c completed in %c${new Date()-stime}ms%c`, "background-color: white; color: black; font-weight: 700;", "", `color: ${color};`, "")

var mobile_mode = true;

function setup_main() {
    if(window.innerWidth >= 1024) {
        mobile_mode = false;
    }
    set_mobile_nav_delays()
    set_mobile_links()
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

function set_mobile_links() {
    for(const ele of document.querySelectorAll(".nav-body > *")) {
        if(ele.innerHTML.toLowerCase() == window.location.href.replace(".html", "").split(/[\W\.]/).pop().toLowerCase()) {
            ele.classList.add("current")
        }
        print()
    }
}

function go_to_previous_page() {
    let sib = document.querySelector("#desktop-nav .current").previousElementSibling
    if (sib==null) {
        document.querySelector("#desktop-nav .nav-body").lastElementChild.click()
    }
    else {
        sib.click()
    }
}

function go_to_next_page() {
    let sib = document.querySelector("#desktop-nav .current").nextElementSibling
    if (sib==null) {
        document.querySelector("#desktop-nav .nav-body").firstElementChild.click()
    }
    else {
        sib.click()
    }
}

function setup_navigation_buttons() {
    gid("navigate-left").onclick = go_to_previous_page
    gid("navigate-right").onclick = go_to_next_page
}