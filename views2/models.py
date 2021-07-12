# from views2.views import ingredients
from typing import Counter
from requests.sessions import session, should_bypass_proxies
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Table
from sqlalchemy.engine import create_engine
import datetime

from sqlalchemy.orm import (
    declarative_base,
    lazyload,
    relationship,
    sessionmaker,
)
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.coercions import ColumnsClauseImpl
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.schema import ForeignKey

engine = create_engine(
    "sqlite:///D:\\Programming\\Own Projects\\Recipes_struct\\recipes_alq.db",
    echo=False,
)

Base = declarative_base()

Session = sessionmaker(bind=engine)


users_recipes = Table(
    "users_recipes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
)

users_shoplists = Table(
    "users_shoplists",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("shoplist_id", Integer, ForeignKey("shoplists.id")),
)

shoplist_ingredients = Table(
    "shoplist_ingredients",
    Base.metadata,
    Column("shoplist_id", Integer, ForeignKey("shoplists.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id")),
)

recipes_ingredients = Table(
    "recipes_ingredients",
    Base.metadata,
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
    Column("ingredient_id", Integer, ForeignKey("ingredients.id")),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    surname = Column(String)
    pw_hash = Column(String)
    email = Column(String)

    recipes = relationship("Recipe", secondary=users_recipes, back_populates="users")
    shoplists = relationship(
        "ShopList", secondary=users_shoplists, back_populates="users"
    )

    def __init__(self, username, first_name, surname, pw_hash, email):
        self.username = username
        self.first_name = first_name
        self.surname = surname
        self.pw_hash = pw_hash
        self.email = email


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    instructions = Column(String)
    url = Column(String)
    image = Column(String)
    calories = Column(String)
    carbs = Column(String)
    fibre = Column(String)
    sugar = Column(String)
    protein = Column(String)
    fats = Column(String)
    sat_fats = Column(String)
    serving_size = Column(String)

    users = relationship("User", secondary=users_recipes, back_populates="recipes")
    ingredients = relationship(
        "Ingredient", secondary=recipes_ingredients, back_populates="recipes"
    )

    def __init__(
        self,
        title,
        instructions,
        url,
        image,
        calories,
        carbs,
        fibre,
        sugar,
        protein,
        fats,
        sat_fats,
        serving_size,
    ):
        self.title = title
        self.instructions = instructions
        self.url = url
        self.image = image
        self.calories = calories
        self.carbs = carbs
        self.fibre = fibre
        self.sugar = sugar
        self.protein = protein
        self.fats = fats
        self.sat_fats = sat_fats
        self.serving_size = serving_size


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    ingredient = Column(String, unique=True)
    measure = Column(String)
    other_info = Column(String)

    recipes = relationship(
        "Recipe", secondary=recipes_ingredients, back_populates="ingredients"
    )
    shoplists = relationship(
        "ShopList", secondary=shoplist_ingredients, back_populates="ingredients"
    )

    def __init__(self, ingredient, measure, other_info):
        self.ingredient = ingredient
        self.measure = measure
        self.other_info = other_info


class ShopList(Base):
    __tablename__ = "shoplists"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    date = Column(String)

    ingredients = relationship(
        "Ingredient", secondary=shoplist_ingredients, back_populates="shoplists"
    )
    users = relationship("User", secondary=users_shoplists, back_populates="shoplists")

    def __init__(self, name, date):
        self.name = name
        self.date = date


Base.metadata.create_all(bind=engine)

# model functions connecting to the database


def get_user_recipes_all(session_id):
    session = Session()

    # get current user object
    user = session.query(User).filter(User.id == session_id).first()
    recipe_list = user.recipes
    session.close()
    # returns a list of recipe objects
    return recipe_list


def get_all_ingredients():
    session = Session()
    all_ingredients = session.query(Ingredient.ingredient).all()
    session.close()
    return all_ingredients


def insert_new_ingredient(new_ing):
    session = Session()
    new_ingredient = Ingredient(new_ing, "measure", "Other info")
    session.add(new_ingredient)
    session.commit()
    session.close()


def get_ingredient_id(ing_name):
    session = Session()
    ing_id = (
        session.query(Ingredient.id).filter(Ingredient.ingredient == ing_name).first()
    )
    session.close()
    ing_id = ing_id[0]
    return ing_id


def get_all_recipes():
    session = Session()
    allRecipes = session.query(Recipe.title).all()
    session.close()
    return allRecipes


def insert_new_recipe(
    rec_title,
    rec_instructions,
    rec_url,
    rec_img,
    calories,
    carbs,
    fibre,
    sugar,
    protein,
    fats,
    sat_fats,
    serving_size,
):
    session = Session()
    new_recipe = Recipe(
        rec_title,
        rec_instructions,
        rec_url,
        rec_img,
        calories,
        carbs,
        fibre,
        sugar,
        protein,
        fats,
        sat_fats,
        serving_size,
    )
    session.add(new_recipe)
    session.commit()
    session.close()


def get_id_of_existing_or_inserted_recipe(rec_title):
    session = Session()
    rec_id = session.query(Recipe.id).filter(Recipe.title == rec_title).first()
    session.close()
    rec_id = rec_id[0]
    return rec_id


def connect_recipe_with_ingredients(rec_id, ing_ids):
    session = Session()

    recipe = session.query(Recipe).filter(Recipe.id == rec_id).first()
    # get ingredients for recipe
    ingredients = session.query(Ingredient).filter(Ingredient.id.in_(ing_ids)).all()

    recipe.ingredients = ingredients
    session.add(recipe)
    session.commit()
    session.close()


def connect_user_with_recipe(user_id, rec_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    new_recipe = session.query(Recipe).filter(Recipe.id == rec_id).first()

    # get all current recipes
    all_recipes = user.recipes

    # append new recipe and add as new user.recipes
    all_recipes.append(new_recipe)
    user.recipes = all_recipes

    session.add(user)
    session.commit()
    session.close()


def get_ingredients_for_recipe(rec_id):
    session = Session()
    recipe = session.query(Recipe).filter(Recipe.id == rec_id).first()
    ingredients = recipe.ingredients
    session.close()
    return ingredients


def disconnect_recipe_from_user(rec_title, user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    recipe_todelete = session.query(Recipe).filter(Recipe.title == rec_title).first()

    new_recipes = []
    for recipe in user.recipes:
        if recipe != recipe_todelete:
            new_recipes.append(recipe)

    user.recipes = new_recipes

    if len(recipe_todelete.users) == 0:

        for ingredient in recipe_todelete.ingredients:
            if len(ingredient.recipes) == 1:
                session.delete(ingredient)

        session.delete(recipe_todelete)

    session.add(user)
    session.commit()
    session.close()


def disconnect_shoplist_from_user(rec_id, user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    shoplist_todelete = session.query(ShopList).filter(ShopList.id == rec_id).first()

    new_shoplists = []
    for shoplist in user.shoplists:
        if shoplist != shoplist_todelete:
            new_shoplists.append(shoplist)

    user.shoplists = new_shoplists

    if len(shoplist_todelete.users) == 0:
        for ingredient in shoplist_todelete.ingredients:
            if len(ingredient.recipes) == 0 and len(ingredient.shoplists) == 1:
                session.delete(ingredient)
        session.delete(shoplist_todelete)

    session.add(user)
    session.commit()
    session.close()


def connect_user_to_shoplist(user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()

    ingredients_list = []
    for recipe in user.recipes:
        for ingredient in recipe.ingredients:
            ingredients_list.append(ingredient)

    user.ingredients = ingredients_list
    session.add(user)
    session.commit()
    session.close()


def get_ingredients_for_user(user_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    shoplist = user.ingredients
    session.close()
    return shoplist


def get_ingredients_for_recipeList(recipe_titles):
    session = Session()

    # ingredientList = []
    # for rec_title in recipe_titles:
    #     recipe = session.query(Recipe).filter(Recipe.title == rec_title).first()
    #     for ing in recipe.ingredients:
    #         ingredientList.append(ing.ingredient)

    ingredientList = []

    recipe = session.query(Recipe).filter(Recipe.title == recipe_titles).first()
    for ing in recipe.ingredients:
        ingredientList.append(ing.ingredient)

    session.close()
    return ingredientList


def connect_shoplist_with_ingredients_and_user(ingredients, user_id, shoplist_name):
    session = Session()

    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d %H:%M:%S")

    newshopList = ShopList(shoplist_name, str(date))

    new_user = session.query(User).filter(User.id == user_id).first()
    new_ingredients = (
        session.query(Ingredient).filter(Ingredient.ingredient.in_(ingredients)).all()
    )

    old_ings = []
    for ing in new_ingredients:
        old_ings.append(ing.ingredient)

    for new_ing in ingredients:
        if new_ing not in old_ings:
            insert_new_ingredient(new_ing)

    new_ingredients = (
        session.query(Ingredient).filter(Ingredient.ingredient.in_(ingredients)).all()
    )

    newshopList.users.append(new_user)

    newshopList.ingredients.extend(new_ingredients)

    session.add(newshopList)
    session.commit()
    session.close()


def connect_recipe_with_ingredients_and_user(
    rec_title,
    rec_instructions,
    rec_ingredients,
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
    user_id,
):
    session = Session()

    newRecipe = Recipe(
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

    new_user = session.query(User).filter(User.id == user_id).first()
    new_ingredients = (
        session.query(Ingredient)
        .filter(Ingredient.ingredient.in_(rec_ingredients))
        .all()
    )

    old_ings = []
    for ing in new_ingredients:
        old_ings.append(ing.ingredient)

    for new_ing in rec_ingredients:
        if new_ing not in old_ings:
            insert_new_ingredient(new_ing)

    new_ingredients = (
        session.query(Ingredient)
        .filter(Ingredient.ingredient.in_(rec_ingredients))
        .all()
    )

    newRecipe.users.append(new_user)

    newRecipe.ingredients.extend(new_ingredients)

    session.add(newRecipe)
    session.commit()
    session.close()


def get_user_shoplists(user_id):
    session = Session()

    user = session.query(User).filter(User.id == user_id).first()

    ingList = []

    for shoplist in user.shoplists:
        # shop_ingList = []
        # # for ing in shoplist.ingredients:
        # #     shop_ingList.append(ing.ingredient)
        # # ingList.append(shop_ingList)
        list_dict = {}
        list_dict["id"] = shoplist.id
        list_dict["name"] = shoplist.name
        list_dict["date"] = shoplist.date
        shop_ingList = []
        for ing in shoplist.ingredients:
            shop_ingList.append(ing.ingredient)
        list_dict["ingredients"] = shop_ingList
        ingList.append(list_dict)

    session.close()
    return ingList
