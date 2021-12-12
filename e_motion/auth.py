from flask import Blueprint
from flask import current_app
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import session
from flask import url_for

from e_motion.db import get_db

bp = Blueprint("auth", __name__)

def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
    	# Remove after db.
    	g.user = {"id": 1, "username" : "systemuser", "password" : "bulldogs"} 
    	# Uncomment once db is setup.
        #g.user = (
        #    get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        #)

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    # Add the system user for now, but once db is available read from that.
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["submit"]

        if action == "LogIn":
            current_app.logger.info("Logging in "+username)
            if do_login(username, password):
                return redirect(url_for("index"))

        elif action == "Register":
            current_app.logger.info("Registering "+username)
            if do_register(username, password):
                return redirect(url_for("auth.login"))

    return render_template("login.html")

# Do login and return true on success.
def do_login(username, password):
    # Fake approach, remove after db.
    # store the user id in a new session and return to the index
    session.clear()
    session["user_id"] = 1 # Using a fake user id (you should get this from db)
    return True

# Do register and return true on success.
def do_register(username, password):
    return True

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))