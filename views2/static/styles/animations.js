function openNav() {
    document.querySelector("#mynav").style.height = "100%";
}

function closeNav() {
    document.querySelector("#mynav").style.height = "0";
}



window.addEventListener('DOMContentLoaded', function () {

    let scroll = window.requestAnimationFrame ||
        function (callback) { window.setTimeout(callback, 1000 / 60) };

    // add .recipe_header within the quotation marks, comma separated and before card 
    let elementsToShow = document.querySelectorAll(".card, .recipe_header");

    // Helper function from: http://stackoverflow.com/a/7557433/274826
    function isElementInViewport(el) {
        // special bonus for those using jQuery
        if (typeof jQuery === "function" && el instanceof jQuery) {
            el = el[0];
        }
        var rect = el.getBoundingClientRect();
        return (
            (rect.top <= 0
                && rect.bottom >= 0)
            ||
            (rect.bottom >= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.top <= (window.innerHeight || document.documentElement.clientHeight))
            ||
            (rect.top >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight))
        );
    }

    function loop() {
        elementsToShow.forEach(function (element) {
            if (isElementInViewport(element)) {
                element.classList.add("is-visible");
            }
            // else {
            //     element.classList.remove("is-visible");
            // }
        });

        scroll(loop);
    }

    loop();

    // Collapsible Cookbook

    let collapsibles = document.querySelectorAll(".collapse-button");

    collapsibles.forEach(function (collapsible, index) {
        collapsible.addEventListener("click", () => {
            collapsible.classList.toggle("active");
            let collap_fields = document.querySelectorAll(".collapse-field");

            if (collap_fields[index].classList.contains("open_coll")) {
                collap_fields[index].classList.remove("open_coll");
            } else {
                collap_fields[index].classList.add("open_coll");
            }
        });
    });

    window.onresize = function () {
        let screen_width = window.innerWidth;
        if (screen_width < 600) {
            let collapsibles = document.querySelectorAll(".collapse-field");
            collapsibles.forEach(function (collapsible) {
                if (collapsible.classList.contains("open_coll")) {
                    collapsible.classList.remove("open_coll");
                }

            });
        }
        if (screen_width > 600) {
            let collapsibles = document.querySelectorAll(".collapse-field");
            collapsibles.forEach(function (collapsible) {
                if (!collapsible.classList.contains("open_coll")) {
                    collapsible.classList.add("open_coll");
                }

            });
        }
    }






    let flash = document.querySelector(".flash");
    setTimeout(function () {
        if (flash) {
            flash.style.opacity = "0";
        }

    }, 3000);

    let prevScrollPos = window.pageYOffset;

    window.onscroll = function () {
        let currScrollPos = window.pageYOffset;
        console.log(currScrollPos)

        if (currScrollPos > 665) {
            if (prevScrollPos > currScrollPos) {
                document.querySelector(".navbar-container").style.top = "0";

            } else {
                document.querySelector(".navbar-container").style.top = "-63px";

            }
        }

        if (prevScrollPos > currScrollPos) {
            backToTop = document.querySelector(".back-to-top");
            if (backToTop) {
                backToTop.style.opacity = "1";
            }

        } else {
            backToTop = document.querySelector(".back-to-top");
            if (backToTop) {
                backToTop.style.opacity = "0";
            }
        }

        prevScrollPos = currScrollPos;

    }




});