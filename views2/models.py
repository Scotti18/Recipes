import sqlite3


def get_user_recipes_name(session_id):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    users_recipes = db.execute(
        "SELECT r.title FROM recipes r JOIN user_rec ur ON r.id = ur.RecID JOIN users u ON ur.UserID = u.id WHERE u.id = ?",
        (session_id,),
    ).fetchall()

    return users_recipes


def get_user_recipes_all(user_id):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    user_recipes = db.execute(
        "SELECT r.title, r.instructions, r.id FROM recipes r JOIN user_rec ur ON r.id = ur.RecID JOIN users u ON ur.UserID = u.id WHERE u.id = ?",
        (user_id,),
    ).fetchall()
    return user_recipes


def get_all_ingredients():
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    all_ingredients = db.execute("SELECT ingredient FROM ingredients").fetchall()
    return all_ingredients


def insert_new_ingredient(new_ing):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    db.execute("INSERT INTO ingredients (ingredient) VALUES(?)", (new_ing,))
    connection.commit()


def get_ingredient_id(ing_name):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    ing_id = db.execute(
        "SELECT id FROM ingredients WHERE ingredient = ?", (ing_name,)
    ).fetchall()
    return ing_id


def get_all_recipes():
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    allRecipes = db.execute("SELECT r.title FROM recipes r").fetchall()
    return allRecipes


def insert_new_recipe(rec_title, rec_instructions):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    db.execute(
        "INSERT INTO recipes (title, instructions) VALUES(?, ?)",
        (rec_title, rec_instructions),
    )
    connection.commit()


def get_id_of_existing_or_inserted_recipe(rec_title):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    rec_id = db.execute(
        "SELECT id FROM recipes WHERE title = ?", (rec_title,)
    ).fetchall()
    return rec_id


def connect_recipe_with_ingredient(rec_id, iID):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    db.execute(
        "INSERT INTO ing_rec (RecipeID, IngID) VALUES(?, ?)",
        (rec_id, iID),
    )
    connection.commit()


def connect_user_with_recipe(user_id, rec_id):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    db.execute(
        "INSERT INTO user_rec (UserID, RecID) VALUES(?, ?)",
        (user_id, rec_id),
    )
    connection.commit()


def commit_con():
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    connection.commit()


def get_ingredients_for_recipe(rec_id):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    ingredients_tup_list = db.execute(
        "SELECT i.ingredient FROM ingredients i JOIN ing_rec ir ON i.id = ir.IngID JOIN recipes r ON ir.RecipeID = r.id WHERE r.id = ?",
        (rec_id,),
    ).fetchall()
    return ingredients_tup_list


def get_ingredients_for_user(user_id):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    shoplist = db.execute(
        "SELECT i.ingredient FROM ingredients i JOIN ing_rec ir ON i.id = ir.IngID JOIN recipes r ON ir.RecipeID = r.id JOIN user_rec ur ON r.id = ur.RecID JOIN users u ON ur.UserID = u.id WHERE u.id = ?",
        (user_id,),
    ).fetchall()
    return shoplist
