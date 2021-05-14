from requests.sessions import session
from sqlalchemy import create_engine, Column, Integer, String, Sequence, Table
from sqlalchemy.engine import create_engine

from sqlalchemy.orm import (
    declarative_base,
    lazyload,
    relation,
    relationship,
    sessionmaker,
)
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.coercions import ColumnsClauseImpl
from sqlalchemy.sql.functions import user
from sqlalchemy.sql.schema import ForeignKey

engine = create_engine(
    "sqlite:///D:\\Programming\\Projects\\Recipes_struct\\recipes_alq.db", echo=False
)

Base = declarative_base()

Session = sessionmaker(bind=engine)


users_recipes = Table(
    "users_recipes",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("recipe_id", Integer, ForeignKey("recipes.id")),
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

    recipes = relationship("Recipe", secondary=users_recipes, back_populates="users")

    def __init__(self, username, first_name, surname, pw_hash):
        self.username = username
        self.first_name = first_name
        self.surname = surname
        self.pw_hash = pw_hash


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    instructions = Column(String)
    nutrition = Column(String)
    url = Column(String)
    image = Column(String)

    users = relationship("User", secondary=users_recipes, back_populates="recipes")
    ingredients = relationship(
        "Ingredient", secondary=recipes_ingredients, back_populates="recipes"
    )

    def __init__(self, title, instructions, nutrition, url, image):
        self.title = title
        self.instructions = instructions
        self.nutrition = nutrition
        self.url = url
        self.image = image


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    ingredient = Column(String, unique=True)
    measure = Column(String)
    other_info = Column(String)

    recipes = relationship(
        "Recipe", secondary=recipes_ingredients, back_populates="ingredients"
    )

    def __init__(self, ingredient, measure, other_info):
        self.ingredient = ingredient
        self.measure = measure
        self.other_info = other_info


Base.metadata.create_all(bind=engine)


def get_user_recipes_all(session_id):
    session = Session()
    user_and_recipes = (
        session.query(User)
        .options(lazyload(User.recipes))
        .filter(User.id == session_id)
        .all()
    )

    user_recipes = user_and_recipes[0].recipes
    session.close()
    # returns a list of recipe objects
    return user_recipes


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


def insert_new_recipe(rec_title, rec_instructions):
    session = Session()
    new_recipe = Recipe(rec_title, rec_instructions, "nutri", "Url", "Img")
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
    ingredients = session.query(Ingredient).filter(Ingredient.id.in_(ing_ids)).all()
    recipe.ingredients = ingredients
    session.add(recipe)
    session.commit()
    session.close()


def connect_user_with_recipe(user_id, rec_id):
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    new_recipe = session.query(Recipe).filter(Recipe.id == rec_id).first()

    all_recipes = (
        session.query(User)
        .options(lazyload(User.recipes))
        .filter(User.id == user_id)
        .all()
    )
    all_recipes = all_recipes[0].recipes

    all_recipes.append(new_recipe)
    user.recipes = all_recipes

    session.add(user)
    session.commit()
    session.close()


def get_ingredients_for_recipe(rec_id):
    session = Session()
    ingredients_tup_list = (
        session.query(Recipe)
        .options(lazyload(Recipe.ingredients))
        .filter(Recipe.id == rec_id)
        .all()
    )
    ingredients_list = ingredients_tup_list[0].ingredients
    session.close()
    return ingredients_list


def get_ingredients_for_user(user_id):
    session = Session()
    user_recipes = (
        session.query(User)
        .options(lazyload(User.recipes))
        .filter(User.id == user_id)
        .all()
    )
    user_recipes = user_recipes[0].recipes
    shoplist = []
    for recipe in user_recipes:
        ingredients = (
            session.query(Recipe)
            .options(lazyload(Recipe.ingredients))
            .filter(Recipe.id == recipe.id)
            .all()
        )
        ingredients = ingredients[0].ingredients
        for ing in ingredients:
            shoplist.append(ing)
    session.close()
    return shoplist
