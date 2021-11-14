document.querySelectorAll(".tablink").forEach(value => {
    value.addEventListener("click", evt => {
        let i, x, tablinks;
        const cityName = value.getAttribute("id").replace("tablink_", "");
        x = document.getElementsByClassName("form");
        for (i = 0; i < x.length; i++) {
            x[i].style.display = "none";
        }
        tablinks = document.getElementsByClassName("tablink");
        for (i = 0; i < x.length; i++) {
            tablinks[i].className = tablinks[i].className.replace(" active", "");
        }
        document.getElementById(cityName).style.display = "block";
        value.className += " active";
    })
});


document.querySelectorAll(".accordeon").forEach(value => {
    value.addEventListener("click", evt => {
        const accordeonItem = document.querySelector("#" + value.id + "-element");
        accordeonItem.classList.toggle("w3-show");
        accordeonItem.classList.toggle("w3-hide");
        evt.target.classList.toggle("fa-chevron-down");
        evt.target.classList.toggle("fa-chevron-up");
    });
});

document.querySelectorAll("#pagination a").forEach(value => {
    let pathname = window.location.pathname
    let urlParams = new URLSearchParams(window.location.search)
    let currentPage = getCurrentPage(urlParams)
    if (value.id === "prev") {
        urlParams.set("page", (currentPage - 1).toString());
    } else if (value.id === "next") {
        urlParams.set("page", (currentPage + 1).toString());
    } else {
        urlParams.set("page", value.textContent)
    }

    value.setAttribute("href", pathname + "?" + urlParams.toString())
})

function getCurrentPage(urlParams) {
    let currentPage = urlParams.get("page")

    if (!currentPage) {
        return 1;
    } else {
        return parseInt(currentPage);
    }
}