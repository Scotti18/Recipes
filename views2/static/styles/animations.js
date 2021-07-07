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


        if (prevScrollPos > currScrollPos) {
            document.querySelector(".navbar-container").style.top = "0";

        } else {
            if (currScrollPos > 650) {
                document.querySelector(".navbar-container").style.top = "-63px";
            }
        }

        if (prevScrollPos > currScrollPos) {
            let backToTop = document.querySelector(".back-to-top");
            if (backToTop) {
                backToTop.style.opacity = "1";
            }

        } else {
            let backToTop = document.querySelector(".back-to-top");
            if (backToTop) {
                backToTop.style.opacity = "0";
            }
        }

        prevScrollPos = currScrollPos;

    }


    // async function get_ingredients() {
    //     try {
    //         const shoplist = await fetch("/views/ing_list")
    //         const text = await shoplist.json()
    //         console.log(text)
    //     } catch (err) {
    //         console.log(err)
    //     }
    // }

    async function get_recipes(rec_title) {
        try {
            let checked_recipe = JSON.stringify(rec_title);
            url_rec = "/views/ing_list/".concat(checked_recipe)
            let recipes = await fetch(url_rec)
            let recipe_text = await recipes.json()
            console.log(recipe_text)

            const node_ul = document.querySelector(".ings");

            recipe_text.forEach((ing) => {
                let node_li = document.createElement("li");
                node_li.classList.add("ing_list");

                let node_label = document.createElement("label");

                let node_input = document.createElement("input");
                node_input.type = "checkbox";
                node_input.classList.add("ing_check");
                node_input.classList.add("checkbox");
                node_input.value = rec_title;

                node_label.appendChild(node_input);
                let label_text = document.createTextNode(ing);
                node_label.appendChild(label_text);

                node_li.appendChild(node_label);

                node_ul.appendChild(node_li);

            });

        } catch (err) {
            console.log(err)
        }
    }

    function delete_recipes(rec_title) {
        let recipe_checkboxes = document.querySelectorAll(".ing_check");
        recipe_checkboxes.forEach((checkbox) => {
            if (checkbox.value == rec_title) {
                checkbox.closest("label").remove();
            }
        });
    }

    // make request everytime when a checkbox is clicked

    let checkboxes_forListener = document.querySelectorAll(".recipe_checkbox");
    checkboxes_forListener.forEach((checkbox_forListerner) => {
        checkbox_forListerner.addEventListener("change", (event) => {

            recipe_title = event.target.value;

            console.log(recipe_title);
            console.log(JSON.stringify(recipe_title));

            if (event.target.checked) {
                get_recipes(recipe_title);
            } else {
                delete_recipes(recipe_title);
            }

        });
    });


    // shopping list buttons 

    let mark_button = document.querySelector("#mark_ing");
    mark_button.addEventListener("click", () => {

        let ing_checkboxes = document.querySelectorAll(".ing_check")

        if (mark_button.value == "mark") {
            ing_checkboxes.forEach((checkbox) => {
                checkbox.checked = true;
            });
            mark_button.value = "unmark";
            mark_button.textContent = "Unmark All";
        } else {
            ing_checkboxes.forEach((checkbox) => {
                checkbox.checked = false;
            });
            mark_button.value = "mark";
            mark_button.textContent = "Mark All";
        }
    });


    // Delete Button for Ingredients in Shopping List

    let delete_button = document.querySelector("#delete_ing");
    delete_button.addEventListener("click", () => {

        let ing_checkboxes = document.querySelectorAll(".ing_check")

        ing_checkboxes.forEach((checkbox) => {
            if (checkbox.checked) {
                checkbox.closest("li").remove();
            }
        });

        let mark_button = document.querySelector("#mark_ing");
        mark_button.value = "mark";
        mark_button.textContent = "Mark All";
    });


    // Add new ingredient-button

    let newIng_button = document.querySelector("#new_ing");
    newIng_button.addEventListener("click", () => {

        // Create a new div if it does not exist yet 
        if (document.querySelector(".ings_new") == null) {

            // Create new div for added ingredients
            let newIng_UL = document.createElement("ul");
            newIng_UL.classList.add("ings_new");

            // Append new div to all ingredients ul
            let ing_container = document.querySelector(".all_new_ingredients");

            // Insert before shoplist buttons
            ing_container.appendChild(newIng_UL);
        }




        let ing_form = document.querySelector("#new_ing_form");
        let value = ing_form.value;

        if (value == "") {
            ing_form.placeholder = "You have to type in something";
        } else {
            let list_item = document.createElement("li");
            list_item.classList.add("ing_list");

            let label_item = document.createElement("label");

            let checkbox_item = document.createElement("input");
            checkbox_item.type = "checkbox";
            checkbox_item.value = "str";
            checkbox_item.classList.add("ing_check");
            checkbox_item.classList.add("checkbox");


            label_item.appendChild(checkbox_item);

            let value_item = document.createTextNode(value);
            label_item.appendChild(value_item);

            list_item.appendChild(label_item);

            let list_ing = document.querySelector(".ings_new");
            list_ing.appendChild(list_item);
        }

        ing_form.value = "";
    });



    document.onselectionchange = () => {
        console.log("Selection change");
    }
});