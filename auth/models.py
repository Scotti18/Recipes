import sqlite3


def get_user(username):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    user = db.execute("SELECT * FROM users WHERE username = (?)", [username]).fetchall()
    return user


def get_usernames():
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    users = db.execute("SELECT username FROM users")
    return users


def store_new_user(username, pw_hash):
    connection = sqlite3.connect("./recipes.db", check_same_thread=False)
    db = connection.cursor()
    db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", (username, pw_hash))
    connection.commit()
