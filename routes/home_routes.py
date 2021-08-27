from flask import render_template, redirect, g, session, Blueprint
from models import User

CURR_USER_KEY = "curr_user"

home_routes = Blueprint('home_routes', __name__)

@home_routes.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


@home_routes.route("/")
def homepage():
    """Show homepage.
    
    * Anon Users goes to landing page
    * Logged in users get list of ToDos?"""
    if g.user:
        return redirect(f"/user/{g.user.id}")
    else:
        return redirect("/landing")

@home_routes.route("/landing")
def landing_page():
    """Show A Logo of the website then proceed to login screen"""

    return render_template('index.html')
