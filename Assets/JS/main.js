const print = console.log
const gid = id_name=>document.getElementById(id_name)
const sum = (list, lambda=e=>e)=>list.reduce((acc,val)=>acc+lambda(val), 0)
const logtime = (stime, process, color="greenyellow")=>print(`%c${process}%c completed in %c${new Date()-stime}ms%c`, "background-color: white; color: black; font-weight: 700;", "", `color: ${color};`, "")