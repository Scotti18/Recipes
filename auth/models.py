from sqlalchemy import create_engine, Column, Integer, String, Sequence, Table
from sqlalchemy.engine import create_engine

from sqlalchemy.orm import declarative_base, relation, relationship, sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.coercions import ColumnsClauseImpl
from sqlalchemy.sql.schema import ForeignKey

engine = create_engine(
    "sqlite:///D:\\Programming\\Projects\\Recipes_struct\\recipes_alq.db",
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
    ingredient = Column(String)
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


def get_user(username):
    session = Session()
    user = session.query(User).filter(User.username == username).first()
    session.close()
    return user


def get_usernames():
    session = Session()
    usernames = session.query(User.username).all()
    session.close()
    return usernames


def store_new_user(username, pw_hash):
    session = Session()
    new_user = User(username, "firstname", "surname", pw_hash)
    session.add(new_user)
    session.commit()
    session.close()
