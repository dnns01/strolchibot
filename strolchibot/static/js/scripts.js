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

document.querySelectorAll(".clip-edit").forEach(value => {
    value.addEventListener("click", evt => {
        const clipEditModal = document.querySelector("#clip-edit-modal");
        clipEditModal.style.display = "block";
    });
});

document.querySelectorAll("input.w3-multiple-choice").forEach(value => {
    value.addEventListener("change", evt => {
        setLabelClass(evt.target);
    })

    setLabelClass(value);
})

function setLabelClass(input) {
    let label = input.parentElement;
    let isChecked = input.checked;
    if (isChecked) {
        label.classList.add("w3-multiple-choice-checked")
    } else {
        label.classList.remove("w3-multiple-choice-checked")
    }
}


function commandSetActive(checkbox, command) {
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    let payload = {
        command: command,
        active: checkbox.checked
    };

    console.log(payload);
    console.log(JSON.stringify(payload));

    fetch('/commands/active', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        credentials: 'same-origin',
        body: JSON.stringify(payload)
    }).then(response => response.json()).then(data => checkbox.checked = data.active);
}