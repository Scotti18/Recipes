from sys import set_asyncgen_hooks
from sqlalchemy.util.langhelpers import ellipses_string
from .helpers import format_ingredient, key_exists, login_required
import requests
from flask import (
    Blueprint,
    render_template,
    request,
    session,
    redirect,
    flash,
    jsonify,
    url_for,
    current_app,
)
from werkzeug.utils import secure_filename
from recipe_scrapers import scrape_me
import json
import os


from .models import (
    connect_recipe_with_ingredients,
    connect_recipe_with_ingredients_and_user,
    connect_shoplist_with_ingredients_and_user,
    connect_user_to_shoplist,
    connect_user_with_recipe,
    disconnect_shoplist_from_user,
    get_all_ingredients,
    get_all_recipes,
    get_id_of_existing_or_inserted_recipe,
    get_ingredient_id,
    get_ingredients_for_recipe,
    get_ingredients_for_recipeList,
    get_ingredients_for_user,
    get_user_recipes_all,
    get_user_shoplists,
    insert_new_ingredient,
    insert_new_recipe,
    disconnect_recipe_from_user,
)

views = Blueprint(
    "views",
    __name__,
    template_folder="../views2/templates/views2",
    static_folder="../views2/static/styles",
)

ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


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
        try:
            r = requests.get(search_url, params=search_params)
            results = r.json()["items"]
        except:
            flash("No search results found")
            return redirect("/views")

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
            flash("Scraping failed. Please try a different recipe")
            return redirect("/views")

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
        rec_image = scraper.image()
        if not rec_image:
            rec_image = "/static/images/beach.JPG"
        rec_nutrients = scraper.nutrients()
        if not rec_nutrients:
            rec_nutrients = "No nutrition available"

        # get all nutritional information from webpage
        if "calories" in rec_nutrients:
            rec_calories = rec_nutrients["calories"]
        else:
            rec_calories = "N/A"
        if "carbohydrateContent" in rec_nutrients:
            rec_carbs = rec_nutrients["carbohydrateContent"]
        else:
            rec_carbs = "N/A"
        if "fibreContent" in rec_nutrients:
            rec_fibre = rec_nutrients["fiberContent"]
        else:
            rec_fibre = "N/A"
        if "sugarContent" in rec_nutrients:
            rec_sugar = rec_nutrients["sugarContent"]
        else:
            rec_sugar = "N/A"
        if "proteinContent" in rec_nutrients:
            rec_protein = rec_nutrients["proteinContent"]
        else:
            rec_protein = "N/A"
        if "fatContent" in rec_nutrients:
            rec_fats = rec_nutrients["fatContent"]
        else:
            rec_fats = "N/A"
        if "saturatedFatContent" in rec_nutrients:
            rec_sat_fats = rec_nutrients["saturatedFatContent"]
        else:
            rec_sat_fats = "N/A"
        if "servingSize" in rec_nutrients:
            rec_serving = rec_nutrients["servingSize"]
        else:
            rec_serving = "N/A"

        # check if recipe is already in the active users' database
        users_recipes = get_user_recipes_all(session["user_id"])
        if len(users_recipes) != 0:
            for user_recipe in users_recipes:
                # if user has already added recipe -> redirect to cookbook without changing
                if rec_title == user_recipe.title:
                    return redirect("/views/ingredients")

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
            insert_new_recipe(
                rec_title,
                rec_instructions,
                scrape_url,
                rec_image,
                rec_calories,
                rec_carbs,
                rec_fibre,
                rec_sugar,
                rec_protein,
                rec_fats,
                rec_sat_fats,
                rec_serving,
            )

        # get id of that particular recipe
        rec_id = get_id_of_existing_or_inserted_recipe(rec_title)

        # only if recipe doesnt exist already
        if counter2 == 0:
            # connect recipe with all its ingredients
            connect_recipe_with_ingredients(rec_id, ing_ids)

        # connect user to the recipe
        connect_user_with_recipe(session["user_id"], rec_id)

        # redirect to coobook using GET
        flash("Recipe added to Cookbook", "info")
        return redirect("/views/ingredients")

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
            recipe_dict["url"] = recipe.url
            recipe_dict["img"] = recipe.image

            # nutrition information
            recipe_dict["calories"] = recipe.calories
            recipe_dict["carbs"] = recipe.carbs
            recipe_dict["fibre"] = recipe.fibre
            recipe_dict["sugar"] = recipe.sugar
            recipe_dict["protein"] = recipe.protein
            recipe_dict["fats"] = recipe.fats
            recipe_dict["sat_fats"] = recipe.sat_fats
            recipe_dict["serving_size"] = recipe.serving_size

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
@views.route("/delete", methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        recipe = request.form.get("delete")
        disconnect_recipe_from_user(recipe, session["user_id"])

        flash("Recipe removed from cookbook", "info")
        return redirect("/views/ingredients")

    if request.method == "GET":
        return redirect("/views/ingredients")


@login_required
@views.route("/delete_shoplist", methods=["GET", "POST"])
def delete_shoplist():
    if request.method == "POST":
        shoplist_id = request.form.get("delete_shoplist")
        disconnect_shoplist_from_user(shoplist_id, session["user_id"])

        flash("Shoplist successfully removed")
        return redirect("/views/savedLists")

    if request.method == "GET":
        return redirect("/views/savedLists")


@login_required
@views.route("/shoplist", methods=["GET", "POST"])
def shoplist():
    if request.method == "POST":
        pass

    if request.method == "GET":
        recipelist = get_user_recipes_all(session["user_id"])

        recipeList = []
        for item in recipelist:
            recipeList.append(item.title)

        return render_template("shoppingList.html", recipeList=recipeList)


@login_required
@views.route("/ing_list/<recipes_checked>", methods=["GET", "POST"])
def ing_list(recipes_checked):
    if request.method == "POST":
        pass

    if request.method == "GET":
        # connect_user_to_shoplist(session["user_id"])

        # shoplist = get_ingredients_for_user(session["user_id"])

        # shoppingList = []
        # for item in shoplist:
        #     ingredient = format_ingredient(item.ingredient)
        #     shoppingList.append(ingredient)

        # print(shoppingList)

        recipes = json.loads(recipes_checked)

        ingredients = get_ingredients_for_recipeList(recipes)

        return jsonify(ingredients)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@login_required
@views.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    if request.method == "POST":
        print("Incoming")

        # recipe_data = request.get_json()

        # rec_title = recipe_data["name"]
        # rec_instructions = recipe_data["instructions"]
        # rec_ingredients = recipe_data["ing_list"]
        # scrape_url = "None"
        # rec_image = recipe_data["image"]
        # rec_calories = recipe_data["nutrients"]

        rec_title = request.form.get("recipe_name")
        rec_instructions = request.form.get("recipe_instructions")
        rec_ingredients_cs = request.form.get("store_ingredients")
        rec_ingredients = rec_ingredients_cs.split(",") if rec_ingredients_cs else []

        # Nutrtion information
        rec_calories = request.form.get("recipe_calories")
        rec_carbs = request.form.get("recipe_carbs")
        rec_protein = request.form.get("recipe_protein")
        rec_fats = request.form.get("recipe_fats")
        rec_fibre = "N/A"
        rec_sugar = "N/A"
        rec_sat_fats = "N/A"
        rec_serving = "1"

        scrape_url = "None"

        # Dealing with the image -> a little more complicated

        if "file" not in request.files:
            flash("No File Part")
            return redirect(request.url)

        file = request.files["file"]
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            file_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            recipe_image = "styles/images/" + filename

        if not (recipe_image):
            recipe_image = "styles/images/" + "food_platter.jpg"

        connect_recipe_with_ingredients_and_user(
            rec_title,
            rec_instructions,
            rec_ingredients,
            scrape_url,
            recipe_image,
            rec_calories,
            rec_carbs,
            rec_fibre,
            rec_sugar,
            rec_protein,
            rec_fats,
            rec_sat_fats,
            rec_serving,
            session["user_id"],
        )

        return redirect("/views/ingredients")

    if request.method == "GET":
        return redirect("/views/ingredients")


@login_required
@views.route("/savedLists", methods=["GET", "POST"])
def shopList():
    if request.method == "POST":
        print("Incoming")

        ing_list = request.get_json()
        ingredients = ing_list["ing_list"]

        shoplist_name = ing_list["shoplist_name"]

        connect_shoplist_with_ingredients_and_user(
            ingredients, session["user_id"], shoplist_name
        )

        return "OK", 200

    if request.method == "GET":

        ingList_dicts = get_user_shoplists(session["user_id"])

        return render_template("savedLists.html", ingLists=ingList_dicts)

        # return render_template("savedLists.html", ingList=ingredients)

    # if request.method == "GET":
    #     ingredientList = json.loads(ingredient_list)
    #     print(ingredientList)

    #     return render_template("savedLists.html", ingList=ingredientList)