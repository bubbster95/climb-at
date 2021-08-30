from flask import render_template, flash, redirect, session, g, Blueprint

from models import User, ToDo, Completed, db
from helpers import query_sector, query_climbs
from config import CURR_USER_KEY

climb_routes = Blueprint('climb_routes', __name__)

@climb_routes.route("/climb/sector/<int:sector_id>")
def show_sector_profile(sector_id):
    "Show information about a sector and its climbs."

    sector = query_sector(sector_id)
    climb_ids = sector["mp_ids"]

    if g.user:
        this_user = User.query.get(session[CURR_USER_KEY])

        climbs = query_climbs(climb_ids, this_user)
        return render_template("/climbs/sector.html", sector = sector, climbs = climbs, user = this_user)
    else:
        climbs = query_climbs(climb_ids)
        return render_template("/climbs/sector.html", sector = sector, climbs = climbs)

@climb_routes.route("/climb/<int:climb_id>")
def show_climb_profile(climb_id):
    """Show information about a climb."""

    user = User.query.get(session[CURR_USER_KEY])

    climb = query_climbs(climb_id, user)[0]

    return render_template('/climbs/show.html', climb = climb, user = user)

@climb_routes.route("/add-to-todo/<int:climb_id>", methods=["POST"])
def add_climb_todo(climb_id):
    """Adds climb to current users todo list"""

    todos = User.query.get(session[CURR_USER_KEY]).todo

    for todo in todos:
        if todo.climb_id == climb_id:

            db.session.delete(todo)
            db.session.commit()

            flash(f'Removed climb number: {climb_id} from To-Do', 'success')
            return redirect(f"/climb/{climb_id}")

    if g.user:
        todo = ToDo(climb_id = climb_id, climber_to_do_it = session[CURR_USER_KEY])

        db.session.add(todo)
        db.session.commit()
        flash(f'Succefully added climb number: {climb_id} To-Do', 'success')
        return redirect(f"/climb/{climb_id}")
    else:
        flash("Please login to add climbs to User Profile.", 'warning')
        return redirect("/users/login")

@climb_routes.route("/add-to-complete/<int:climb_id>", methods=["POST"])
def add_climb_id(climb_id):

    """Adds climb to current users completed list"""

    completed = User.query.get(session[CURR_USER_KEY]).completed
    todos = User.query.get(session[CURR_USER_KEY]).todo
    for complete in completed:
        if complete.climb_id == climb_id:

            db.session.delete(complete)
            db.session.commit()

            flash(f'Removed climb number: {climb_id} from Completed', 'success')
        return redirect(f"/climb/{climb_id}")

    if g.user:
        for todo in todos:
            if todo.climb_id == climb_id:
                db.session.delete(todo)
        complete = Completed(climb_id = climb_id, climber_who_completed = session[CURR_USER_KEY])

        db.session.add(complete)
        db.session.commit()
        flash(f'Succefully added climb number: {climb_id} to Completed', 'success')
        return redirect(f"/climb/{climb_id}")
    else:
        flash("Please login to add climbs to User Profile.", 'warning')
        return redirect("/users/login")
