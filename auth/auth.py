from .models import get_user, get_usernames, store_new_user
from flask import Blueprint, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, template_folder="templates/auth")


@auth.route("/login", methods=["GET", "POST"])
def login():
    # when login button is hit
    if request.method == "POST":

        # request and check for username
        username = request.form.get("username")
        if not username:
            return "Enter Username"

        # get and check for password
        password = request.form.get("password")
        if not password:
            return "Enter password"

        # check if username exists in database
        user = get_user(username)
        if len(user) == 0:
            return "Username does not exist"

        # check if entered password and stored password match
        if not check_password_hash(user[0][2], password):
            return "Username and password do not match"

        # assign a session to @login_required
        session["user_id"] = user[0][0]

        # redirect to main page with status logged in
        return redirect("/")

    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # get and check for a entered username
        new_user = request.form.get("username")
        if not new_user:
            return "Enter Username!"

        # check if username exists in database
        users = get_usernames()
        for user in users:
            print(user[0])
            if new_user == user[0]:
                return "Username already exists"

        # get and check for password
        password = request.form.get("password")
        if not password:
            return "Enter Password"

        # check if password and confirmation match
        if password != request.form.get("confirmation"):
            return "Passwords do not match"

        # store username, and a hased password in database
        pw_hash = generate_password_hash(password)
        store_new_user(new_user, pw_hash)

        return redirect("/")

    else:
        return render_template("register.html")
