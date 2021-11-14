document.querySelectorAll(".tablink").forEach(value => {
    value.addEventListener("click", evt => {
        var i, x, tablinks;
        var cityName = value.getAttribute("id").replace("tablink_", "");
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
        var accordeonItem = document.querySelector("#" + value.id + "-element");
        accordeonItem.classList.toggle("w3-show");
        accordeonItem.classList.toggle("w3-hide");
        evt.target.classList.toggle("fa-chevron-down");
        evt.target.classList.toggle("fa-chevron-up");
    });
});