from flask import session, redirect
from functools import wraps


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
