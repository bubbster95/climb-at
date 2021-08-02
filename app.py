import json
import os

from flask import Flask, render_template, request, flash, redirect, session, g
from models import db, connect_db, User, ToDo, Completed
from forms import UserAddForm, LoginForm, EditUserForm
from sqlalchemy.exc import IntegrityError
# from helpers import

CURR_USER_KEY = "curr_user"

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///climb-at-users'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


###############
# Home Routes #
###############

@app.route("/")
def homepage():
    """Show homepage.
    
    * Anon Users goes to landing page
    * Logged in users get list of ToDos?"""
    if g.user:
        return redirect(f"/user/{g.user.id}")
    else:
        return redirect("/landing")

@app.route("/landing")
def landing_page():
    """Show A Logo of the website then proceed to login screen"""

    return render_template('index.html')

###############
# User Routes #
###############

@app.route("/user/signup", methods=["GET", "POST"])
def sign_up_user():
    """Sign up user form."""
    if g.user:
        return redirect("/")

    form = UserAddForm()

    if form.validate_on_submit():
        try: 
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg
            )
            db.session.commit()
            
        except IntegrityError:
            flash("Username already taken", 'danger')
            return redirect('/user/login')

        do_login(user)

        return redirect("/")
    else: 
        return render_template("users/sign-up.html", form=form)

@app.route("/user/login", methods=["GET", "POST"])
def log_in_user():
    """Login user form."""
    if g.user:
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)

        
@app.route('/user/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    return redirect('/')

@app.route("/user/<int:user_id>")
def show_user_info(user_id):
    """User profile page."""

    return render_template("users/profile-page.html")

@app.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user_profile(user_id):
    """Edit user profile info."""

#################
# Search Routes #
#################

@app.route("/search", methods=["GET", "POST"])
def filter_search_page():
    """Allows users to filter climbs in the area."""

##############
# Climb Routes #
##############

@app.route("/climb/<int:climb_id>")
def show_climb_profile(climb_id):
    """Show information about a climb."""

@app.route("/climb/<int:climb_id>/status", methods=["POST"])
def edit_climb_status(climb_id):
    """Allow users to add/remove climb to users to-do, complete lists."""




@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req