from .helpers import key_exists, login_required
import requests
from flask import Blueprint, render_template, request, session, redirect
from recipe_scrapers import scrape_me

from .models import (
    connect_recipe_with_ingredients,
    connect_user_with_recipe,
    get_all_ingredients,
    get_all_recipes,
    get_id_of_existing_or_inserted_recipe,
    get_ingredient_id,
    get_ingredients_for_recipe,
    get_ingredients_for_user,
    get_user_recipes_all,
    insert_new_ingredient,
    insert_new_recipe,
)

views = Blueprint("views", __name__, template_folder="templates/views2")


@views.route("/", methods=["GET", "POST"])
@login_required
def index():
    # if search bar is used
    if request.method == "POST":
        # google custom search api
        search_url = "https://customsearch.googleapis.com/customsearch/v1"

        # get and check for search term
        search_term = request.form.get("query")
        if not search_term:
            return "Enter search term"

        # see google json search api docs
        search_params = {
            "key": "AIzaSyC0xxkN4Rvtv98kbutBoyRdPif6FfJe4eA",
            "cx": "df59488f5a82f2c83",
            "q": search_term,
            "num": 9,
        }

        # request results and convert to json
        r = requests.get(search_url, params=search_params)
        results = r.json()["items"]

        websites = []

        # for each of results extract information and store as list of dicts
        for result in results:

            search_data = {
                "url": result["link"],
                "title": result["title"],
            }

            # check if it has an image (helpe functions)
            if key_exists(result, ["pagemap", "cse_thumbnail"]) != None:
                search_data["image"] = result["pagemap"]["cse_thumbnail"][0]["src"]
            # if no image -> set image
            else:
                image = "/static/images/beach.JPG"
                search_data["image"] = image

            websites.append(search_data)

        # render index.html with search results
        return render_template("index.html", websites=websites)

    else:
        # render index.html without search results
        return render_template("index.html")


# cookbook -> all saved recipes
@views.route("/ingredients", methods=["GET", "POST"])
@login_required
def ingredients():
    # if "add to coobook is hit"
    if request.method == "POST":
        # get url for scraping from the button that was clicked
        scrape_url = request.form.get("search_url")

        # check if the scraper works on the website
        try:
            scraper = scrape_me(scrape_url, wild_mode=True)
        except:
            return "Not possible to fetch ingredients. If you would like you can copy and paste ingedients from website or try another recipe"

        # extract information: title, instructions, and ingredients
        rec_title = scraper.title()
        if not rec_title:
            rec_title = "No Name Recipe"
        rec_instructions = scraper.instructions()
        if not rec_instructions:
            rec_instructions = "No Instructions for recipe (Visit website)"
        rec_ingredients = scraper.ingredients()
        if not rec_ingredients:
            rec_ingredients = "No ingredients for recipe"

        # check if recipe is already in the active users' database
        users_recipes = get_user_recipes_all(session["user_id"])
        if len(users_recipes) != 0:
            for user_recipe in users_recipes:
                # if user has already added recipe -> redirect to cookbook without changing
                if rec_title == user_recipe.title:
                    return redirect("/ingredients")

        # get all ingredients from database
        ing_ids = []
        all_ingredients = get_all_ingredients()

        # iterate over all ingredients to avoid redundancy
        for ingredient in rec_ingredients:
            counter = 0

            # check if there are and ingredients in database
            if len(all_ingredients) != 0:

                # if ingredient already exists -> dont add it to databse
                for ing in all_ingredients:
                    if str(ingredient) == str(ing[0]):
                        counter += 1
                if counter == 0:
                    insert_new_ingredient(ingredient)
            else:
                insert_new_ingredient(ingredient)

            # get id for that particular ingredient and store in ingredient id list
            ing_id = get_ingredient_id(ingredient)
            if ing_id:
                ing_ids.append(ing_id)

        # add recipe to database only if not already in database
        allRecipes = get_all_recipes()
        counter2 = 0
        for recipe in allRecipes:
            if rec_title == recipe[0]:
                counter2 += 1
        if counter2 == 0:
            insert_new_recipe(rec_title, rec_instructions)

        # get id of that particular recipe
        rec_id = get_id_of_existing_or_inserted_recipe(rec_title)

        # only if recipe doesnt exist already
        if counter2 == 0:
            # connect recipe with all its ingredients
            connect_recipe_with_ingredients(rec_id, ing_ids)

        # connect user to the recipe
        connect_user_with_recipe(session["user_id"], rec_id)

        # redirect to coobook using GET
        return redirect("/ingredients")

    # when GET
    else:
        # get everything expect ingredients from users' recipes
        user_recipes = get_user_recipes_all(session["user_id"])

        recipe_list = []

        # iterate over each recipe
        for recipe in user_recipes:
            # create dictionary of the recipe
            recipe_dict = {}
            ingredient_list = []
            recipe_dict["id"] = recipe.id
            recipe_dict["title"] = recipe.title
            recipe_dict["instructions"] = recipe.instructions

            # select all ingredients for that recipe
            ingredients_list = get_ingredients_for_recipe(recipe.id)

            # add ingredients to a list of ingredients and add to recipe dict
            for ing in ingredients_list:
                ingredient_list.append(ing.ingredient)
            recipe_dict["ingredients"] = ingredient_list

            # add dict of recipe to a list of recipes dicts
            recipe_list.append(recipe_dict)

        # render cookbook.html with recipes
        return render_template("cookbook.html", recipes=recipe_list)


@login_required
@views.route("/shoplist", methods=["GET", "POST"])
def shoplist():
    shoplist = get_ingredients_for_user(session["user_id"])

    shoppingList = []
    for item in shoplist:
        shoppingList.append(item.ingredient)

    return render_template("shoppingList.html", shopList=shoppingList)
