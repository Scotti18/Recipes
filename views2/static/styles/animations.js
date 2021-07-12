function openNav() {
    document.querySelector("#mynav").style.height = "100%";
}

function closeNav() {
    document.querySelector("#mynav").style.height = "0";
}

window.onbeforeunload = () => {
    if (window.scrollTo) window.scrollTo(0, 0);
    if (history && history.scrollRestoration) history.scrollRestoration = "manual";
}


window.addEventListener('DOMContentLoaded', function () {
    window.scrollTo(0, 0);

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


    async function get_recipes(rec_title) {
        try {
            let checked_recipe = JSON.stringify(rec_title);
            url_rec = "/views/ing_list/".concat(checked_recipe)
            console.log(url_rec);
            let recipes = await fetch(url_rec)
            let recipe_text = await recipes.json()
            console.log(recipe_text)

            const node_ul = document.querySelector(".ings");

            recipe_text.forEach((ing) => {
                let node_li = document.createElement("li");
                node_li.classList.add("ing_list");

                let node_label = document.createElement("label");
                node_label.classList.add("ing_lbl");

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

            const goto_shoplists = document.querySelector("#create_shoplist");
            if (goto_shoplists.style.color != "black") {
                goto_shoplists.style.backgroundColor = "rgb(204, 172, 124)";
                goto_shoplists.style.color = "black";
                goto_shoplists.setAttribute("disabled", true)
            }


        });
    });


    // shopping list buttons 

    let mark_button = document.querySelector("#mark_ing");
    if (mark_button) {
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
    }



    // Delete Button for Ingredients in Shopping List

    let delete_button = document.querySelector("#delete_ing");
    if (delete_button) {
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


            // Store ingredient list as value of a hidden form to be accessed by flask
            // every time user adds ingredient (and deletes one)
            let hidden_form = document.querySelector("#store_ingredients")

            // Only for creation of recipe -> if hidden form exists
            if (hidden_form) {
                // All ingredients added to the list
                let ing_labels = document.querySelectorAll(".ing_lbl");

                // Create new array with the actual ingredients names
                let ing_list = [];
                ing_labels.forEach((ing) => {
                    ing_list.push(ing.textContent);
                });


                // set value of hidden form to all ingredients
                hidden_form.value = ing_list;
            }

        });
    }


    // Add new ingredient by pressing enter or clicking the button

    let add_ing_func = () => {

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
            label_item.classList.add("ing_lbl");

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

            // Store ingredient list as value of a hidden form to be accessed by flask
            // every time user adds ingredient (and deletes one)
            let hidden_form = document.querySelector("#store_ingredients")

            // Only for creation of recipe -> if hidden form exists
            if (hidden_form) {
                // All ingredients added to the list
                let ing_labels = document.querySelectorAll(".ing_lbl");

                // Create new array with the actual ingredients names
                let ing_list = [];
                ing_labels.forEach((ing) => {
                    ing_list.push(ing.textContent);
                });


                // set value of hidden form to all ingredients
                hidden_form.value = ing_list;
            }
        }

        ing_form.value = "";
    }

    // Add new ingredient-button

    let newIng_button = document.querySelector("#new_ing");
    if (newIng_button) {
        newIng_button.addEventListener("click", () => {
            add_ing_func();
        });
    }



    // Add new ingredient by pressing enter

    let newIng_form = document.querySelector("#new_ing_form");
    if (newIng_form) {
        newIng_form.addEventListener("keyup", (event) => {
            if (event.keyCode == 13) {
                add_ing_func();
            }
        });
    }







    // Send fetch request with shopping list

    async function send_shopList(ing_list, shoplist_name) {

        // let checked_ingList = JSON.stringify(ing_list);
        // url_rec = "/views/shopList/".concat(checked_ingList);


        // try {
        //     let response = await fetch(url_rec);
        //     let response_text = await response.json();
        //     console.log(response_text);
        // } catch (err) {
        //     console.log(err);
        // }

        fetch("/views/savedLists", {

            // Type of data
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },

            method: 'POST',

            body: JSON.stringify({
                'ing_list': ing_list,
                'shoplist_name': shoplist_name

            })
        })
            .then(response => response.text())
            .then((text) => {
                console.log("Response: ");
                console.log(text);
            })
            .catch((err) => {
                console.log(err)
            })


    }



    // Create and save shopping List and open new html page with saved shopping lists
    let renderShoplist_button = document.querySelector("#render_shoplist");
    if (renderShoplist_button) {
        renderShoplist_button.addEventListener("click", event => {
            let ing_labels = document.querySelectorAll(".ing_lbl");
            let shoplist_name = document.querySelector("#shoplist_name").value

            let ing_list = [];

            ing_labels.forEach((ing) => {
                ing_list.push(ing.textContent);
            });

            console.log(ing_list);


            document.querySelector("#create_shoplist").removeAttribute("disabled");

            send_shopList(ing_list, shoplist_name);

            const goto_shoplists = document.querySelector("#create_shoplist");
            goto_shoplists.style.backgroundColor = "rgba(62, 165, 62, 0.61)";
            goto_shoplists.style.color = "white";

            let ing_checkboxes = document.querySelectorAll(".ing_check")
            ing_checkboxes.forEach((checkbox) => {
                checkbox.closest("li").remove();
            });

            let recipe_checkboxes = document.querySelectorAll(".recipe_checkbox");
            recipe_checkboxes.forEach((checkbox) => {
                checkbox.checked = false;
            });

            document.querySelector("#shoplist_name").value = "";


            let green_checkmark = document.querySelector(".checkmark");
            green_checkmark.style.height = "100px";

            setTimeout(() => {
                green_checkmark.style.height = 0;
            }, 4500);


        });
    }


    // Upload image for creation of recipe

    let image_field = document.querySelector('input[type="file"]');
    if (image_field) {
        image_field.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                let img = document.querySelector('img');
                img.onload = () => {
                    URL.revokeObjectURL(img.src);  // no longer needed, free memory
                }

                img.src = URL.createObjectURL(this.files[0]); // set src to blob url
            }
        });
    }

    // async function send_createRecipe(ing_list, shoplist_name, instructions, nutrients, image) {
    //     fetch("/views/create_recipe", {

    //         // Type of data
    //         headers: {
    //             'Content-Type': 'application/json',
    //             'Accept': 'application/json'
    //         },

    //         method: 'POST',

    //         body: JSON.stringify({
    //             'ing_list': ing_list,
    //             'name': shoplist_name,
    //             'instructions': instructions,
    //             'nutrients': nutrients,
    //             'image': image
    //         })
    //     })
    //         .then(response => response.text())
    //         .then((text) => {
    //             console.log("Response: ");
    //             console.log(text);
    //         })
    //         .catch((err) => {
    //             console.log(err)
    //         })
    // }



    // q





});