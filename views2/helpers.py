from flask import session, redirect
from functools import wraps
from nltk.stem import WordNetLemmatizer, wordnet
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

    return lem_ing
