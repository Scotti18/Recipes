from flask import Flask, session, Blueprint, request
from flask_session import Session
from tempfile import mkdtemp
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    # templates
    app.config["TEMPLATES_AUTO_RELOAD"] = True

    # stop caches
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

    @app.after_request
    def store_urls(response):
        if "urls" in session:
            session["urls"].append(request.url)
            if len(session["urls"]) > 5:
                session["urls"].pop(0)
            session.modified = True
        return response

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_FILE_DIR"] = mkdtemp()
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["SECRET_KEY"] = "some_random_key"
    Session(app)

    from .views2.views import views
    from .auth.auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")

    return app
