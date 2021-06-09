from flask import session, redirect
from functools import wraps
from nltk.stem import WordNetLemmatizer, wordnet
from fractions import Fraction
import re


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/auth/login")
        return f(*args, **kwargs)

    return decorated_function


def key_exists(obj, chain):
    _key = chain.pop(0)
    if _key in obj:
        return key_exists(obj[_key], chain) if chain else obj[_key]


def check_float(num):
    try:
        float(num)
        return True
    except:
        return False


def check_fract(num):
    try:
        Fraction(num)
        return True
    except:
        return False


def format_ingredient(ingredient):
    string = re.sub("[\(\[].*?[\)\]]", "", ingredient)

    # remove all punctuation except inbetween numbers
    regex = r"(?<!\d)[.,;:](?!\d)"
    string_reduced = re.sub(regex, "", string, 0)

    # remove remaining commass, brackets, whitespaces and tokenize
    tokenlist = string_reduced.replace(",", "").replace(")", "").rstrip().split(" ")

    # lemmatize words to base form
    word_lem = WordNetLemmatizer()
    lem_ing = [word_lem.lemmatize(word) for word in tokenlist]

    cooking_measures = [
        "teaspoon",
        "dessertspoon",
        "tablespoon",
        "fluid ounce",
        "cup",
        "pint",
        "quart",
        "gallon",
        "drop",
        "smidgen",
        "pinch",
        "dash",
        "saltspoon",
        "scruple",
        "coffespoon",
        "fluid dram",
        "wineglass",
        "gill",
        "teacup",
        "quart",
        "pottle",
        "millilitres",
        "inches",
        "litres",
        "litre",
        "g",
        "grams",
        "gram" "kilogram",
        "ounces",
        "pound",
        "piece",
        "slice",
        "big",
        "small",
        "jigger",
        "clove",
    ]

    koch_measures = [
        "kubikzentimeter",
        "liter",
        "deziliter",
        "milliliter",
        "tasse",
        "gramm",
        "dezigramm",
        "centigramm",
        "milligramm",
        "kilogramm",
        "pfund",
        "bund",
        "tropfen",
        "spritzer",
        "schuss",
        "teelöffel",
        "barlöffel",
        "esslöffel",
        "messerspitze",
        "prise",
        "dose",
        "karton",
        "stück",
        "packung",
        "päckchen",
        "klein",
        "groß",
        "mittelgroß" "achtel",
        "viertel",
        "halbe",
        "maß",
    ]

    abbreviations = [
        "cm",
        "l",
        "dl",
        "cl",
        "ml",
        "mls",
        "ta",
        "g",
        "dg",
        "mg",
        "kg",
        "tl",
        "tsp",
        "el",
        "tbsp",
        "msp",
        "pr",
        "oz",
    ]
    if len(lem_ing[0]) > 0:
        if (
            not check_float(lem_ing[0][0])
            and not lem_ing[0][0].isnumeric()
            and not check_fract(lem_ing[0][0])
        ):
            print(type(lem_ing[0][0]))
            print(lem_ing[0][0])
            lem_ing.insert(0, "no numerical measure")
        else:
            for i in range(len(lem_ing[0])):
                if str(lem_ing[0][i]).isalpha():
                    lem_ing.insert(1, lem_ing[0][i:])
                    lem_ing[0] = lem_ing[0][:i]
                    break

    else:
        lem_ing.remove(lem_ing[0])
        if not check_float(lem_ing[0][0]):
            lem_ing.insert(0, "no numerical measure")
    if (
        lem_ing[1] not in cooking_measures
        and lem_ing[1] not in koch_measures
        and lem_ing[1] not in abbreviations
    ):
        print(lem_ing[1])
        lem_ing.insert(1, "no measure")

    # convert to string
    ing = " ".join([str(ing) for ing in lem_ing[2:]])

    lem_ing.insert(2, ing)

    for item in lem_ing[3:]:
        lem_ing.remove(item)

    # problems and ideas for this function

    # measure is not recognized
    # quaters are not recognized

    return lem_ing
