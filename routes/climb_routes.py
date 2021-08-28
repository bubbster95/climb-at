from flask import render_template, flash, redirect, session, g, Blueprint

from models import User, ToDo, Completed, db
from helpers import get_climb_specific_response
from config import CURR_USER_KEY

climb_routes = Blueprint('climb_routes', __name__)

@climb_routes.route("/climb/<int:climb_id>")
def show_climb_profile(climb_id):
    """Show information about a climb."""

    user = User.query.get(session[CURR_USER_KEY])

    climb = get_climb_specific_response(climb_id, user)

    return render_template('/climbs/show.html', climb = climb, user = user)

@climb_routes.route("/add-to-todo/<int:climb_id>", methods=["POST"])
def add_climb_todo(climb_id):
    """Adds climb to current users todo list"""

    todos = User.query.get(session[CURR_USER_KEY]).todo

    for todo in todos:
        if todo.climb_to_do == climb_id:

            db.session.delete(todo)
            db.session.commit()

            flash(f'Removed climb number: {climb_id} from To-Do', 'success')
            return redirect("/")

    if g.user:
        todo = ToDo(climb_to_do = climb_id, climber_to_do_it = session[CURR_USER_KEY])

        db.session.add(todo)
        db.session.commit()
        flash(f'Succefully added climb number: {climb_id} To-Do', 'success')
        return redirect("/")
    else:
        flash("Please login to add climbs to User Profile.", 'warning')
        return redirect("/users/login")


@climb_routes.route("/add-to-complete/<int:climb_id>", methods=["POST"])
def add_completed_climb(climb_id):

    """Adds climb to current users completed list"""

    completed = User.query.get(session[CURR_USER_KEY]).completed
    todos = User.query.get(session[CURR_USER_KEY]).todo
    for complete in completed:
        if complete.completed_climb == climb_id:

            db.session.delete(complete)
            db.session.commit()

            flash(f'Removed climb number: {climb_id} from Completed', 'success')
            return redirect("/")

    if g.user:
        for todo in todos:
            if todo.climb_to_do == climb_id:
                db.session.delete(todo)
        complete = Completed(completed_climb = climb_id, climber_who_completed = session[CURR_USER_KEY])

        db.session.add(complete)
        db.session.commit()
        flash(f'Succefully added climb number: {climb_id} to Completed', 'success')
        return redirect("/")
    else:
        flash("Please login to add climbs to User Profile.", 'warning')
        return redirect("/users/login")
