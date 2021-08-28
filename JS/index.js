window.onload = ()=>{
    document.getElementById("high-res-bkg").style.backgroundImage = getComputedStyle(document.getElementById("low-res-bkg")).backgroundImage.replace("%20", ' ').replace("%20-%20Low%20Res", "");
}