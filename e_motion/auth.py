import functools

from flask import Blueprint
from flask import flash
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
    	# g.user = {"id": 1, "username" : "systemuser", "password" : "bulldogs"} 
    	# Uncomment once db is setup.
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )

@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    # Add the system user for now, but once db is available read from that.
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        action = request.form["submit"]

        if action == "LogIn":
            if do_login(get_db(), username, password):
                return redirect(url_for("index"))

        elif action == "Register":
            do_register(get_db(), username, password)
            return redirect(url_for("auth.login"))

    return render_template("login.html")

# Do login and return true on success.
def do_login(db, username, password):
    error = None
    # Fetch user record from database.
    user = db.execute(
        "SELECT * FROM user WHERE username = ?", (username,)
    ).fetchone()
    if user is None:
        error = "Incorrect username."
    elif user["password"] != password:
        error = "Incorrect password."

    if error is None:
        # store the user id in a new session and return to the index
        session.clear()
        session["user_id"] = user["id"]
        return True

    flash(error)
    return False

# Do register and return true on success.
def do_register(db, username, password):
    error = None
    if not username:
        error = "Username is required!"
    elif not password:
        error = "Password is required!"

    if error is None:
        try:
            db.execute(
                "INSERT INTO user (username, password) VALUES (?, ?)",
                (username, password),
            )
            db.commit()
        except db.IntegrityError:
            # The username was already taken, which caused the
            # commit to fail. Show a validation error.
            error = f"User {username} is already registered."
        else:
            # Success.
            flash("Registration Successful!")
            return True

        flash(error)
    return False

@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))