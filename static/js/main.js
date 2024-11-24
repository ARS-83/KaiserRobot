const balance = document.querySelector(".content-balance");
const textConfig = document.querySelector("textarea");
const lightBox = document.querySelector(".light-box-res");
const confInfo = document.querySelectorAll(".conf-info")
function applyTheme(theme) {
    if (theme === "dark") {
        $(".sun-btn").addClass("d-none");
        $(".moon-btn").removeClass("d-none");
    } else if (theme === "light") {
        $(".sun-btn").removeClass("d-none");
        $(".moon-btn").addClass("d-none");
    }else if(theme==="dark-auto"){
        $(".auto-btn").addClass("d-none");
        $(".sun-btn").removeClass("d-none");
    }

    document.body.classList.remove("theme-auto", "theme-light", "theme-dark");
    document.body.classList.add(`theme-${theme}`);
    balance.classList.remove("theme-auto", "theme-light", "theme-dark");
    balance.classList.add(`theme-${theme}`);
    lightBox.classList.remove("theme-auto", "theme-light", "theme-dark");
    lightBox.classList.add(`theme-${theme}`);
    confInfo.forEach(element => {
        element.classList.remove("theme-auto", "theme-light", "theme-dark");
        element.classList.add(`theme-${theme}`);
    })
    textConfig.classList.remove("theme-auto", "theme-light", "theme-dark");
    textConfig.classList.add(`theme-${theme}`);

}

document.addEventListener("DOMContentLoaded", () => {
    const saveTheme = localStorage.getItem('theme') || "auto";
   
   
    applyTheme(saveTheme)

    for (const opationElement of document.querySelectorAll('.btn-mod')) {
        opationElement.selected = saveTheme === opationElement.getAttribute("data-mod");
       

    }


    $(".sun-btn").click("click", function () {
        localStorage.setItem("theme", this.getAttribute("data-mod1"))
        applyTheme(this.getAttribute("data-mod1"))
    })
    $(".moon-btn").click("click", function () {
        localStorage.setItem("theme", this.getAttribute("data-mod1"))
        applyTheme(this.getAttribute("data-mod1"))
    })
})