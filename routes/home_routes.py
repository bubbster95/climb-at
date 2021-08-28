from flask import render_template, redirect, g, Blueprint

home_routes = Blueprint('home_routes', __name__)

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
