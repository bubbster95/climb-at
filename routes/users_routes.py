from flask import render_template, flash, redirect, session, g, Blueprint
from models import db, User
from forms import UserAddForm, LoginForm, EditUserForm
from sqlalchemy.exc import IntegrityError

users_routes = Blueprint('users_routes', __name__)

CURR_USER_KEY = "curr_user"

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@users_routes.route("/user/signup", methods=["GET", "POST"])
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

@users_routes.route("/user/login", methods=["GET", "POST"])
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
        
@users_routes.route('/user/logout')
def logout():
    """Handle logout of user."""

    do_logout()

    return redirect('/')

@users_routes.route("/user/<int:user_id>")
def show_user_info(user_id):
    """User profile page."""
    
    this_user = User.query.get(user_id)

    return render_template("users/profile-page.html", user = this_user)

@users_routes.route("/user/<int:user_id>/edit", methods=["GET", "POST"])
def edit_user_profile(user_id):
    """Edit user profile info."""

    if CURR_USER_KEY in session:
        user = User.query.get(user_id)
    else:
        return redirect('/')

    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data

        if user.authenticate(user.username, password):
            user.username = username
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.bio = form.bio.data

            db.session.add(user)
            db.session.commit()
            
            return redirect(f'/user/{user_id}')
        else:
            return redirect('/')
    else:
        return render_template('/users/edit.html', user = user, form = form)

