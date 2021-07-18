from .models import get_user, get_usernames, store_new_user
from flask import Blueprint, request, session, redirect, render_template, flash
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__, template_folder="templates/auth")


@auth.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        pass

    if request.method == "GET":
        return render_template("cover.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    # when login button is hit
    if request.method == "POST":

        # request and check for username
        username = request.form.get("username")
        if not username:
            flash("Enter Username")
            return redirect("/auth/login")

        # get and check for password
        password = request.form.get("password")
        if not password:
            flash("Enter Password")
            return redirect("/auth/login")

        # check if username exists in database
        user = get_user(username)
        if not user:
            flash("Username does not exist")
            return redirect("/auth/login")
        if user.username != username:
            flash("Username does not exist")
            return redirect("/auth/login")

        # check if entered password and stored password match
        if not check_password_hash(user.pw_hash, password):
            flash("Username and Password do not match")
            return redirect("/auth/login")

        # assign a session to @login_required
        session["user_id"] = user.id
        session["urls"] = []

        # redirect to main page with status logged in
        flash("Login Successfull", "info")
        return redirect("/views/")

    else:
        return render_template("login.html")


@auth.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    flash("Logout Successfull", "info")
    return redirect("/")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":
        # get and check for a entered username
        new_user = request.form.get("username")
        if not new_user:
            flash("Enter Username")
            return redirect("/auth/register")

        # check if username exists in database
        users = get_usernames()
        for user in users:
            print(user[0])
            if new_user == user[0]:
                flash("Username already exists")
                return redirect("/auth/register")

        # get and check for password
        password = request.form.get("password")
        if not password:
            flash("Enter Password")
            return redirect("/auth/register")

        # check if password and confirmation match
        if password != request.form.get("confirmation"):
            flash("Passwords do not match")
            return redirect("/auth/register")

        # store username, and a hased password in database
        pw_hash = generate_password_hash(password)
        store_new_user(new_user, "firstname", "surname", pw_hash, "email")

        flash("Registered successfully", "info")
        return redirect("/auth/login")

    else:
        return render_template("register.html")
