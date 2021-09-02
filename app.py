import json
import os

from flask import Flask, session, g
from models import User, connect_db, db

from config import CURR_USER_KEY

from routes.climb_routes import climb_routes
from routes.home_routes import home_routes
from routes.search_routes import search_routes
from routes.users_routes import users_routes

app = Flask(__name__)

@app.before_request
def add_user_to_g():
    """If user is logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None

app.register_blueprint(climb_routes)
app.register_blueprint(home_routes)
app.register_blueprint(search_routes)
app.register_blueprint(users_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///climb-at-users')).replace("://", "ql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "itsasecret")

connect_db(app)

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req