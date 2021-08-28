from flask import render_template, request, session, g, Blueprint
from forms import SearchForClimbsForm
from models import User
from helpers import compound_climb_responses, create_api_response
from config import CURR_USER_KEY

search_routes = Blueprint('search_routes', __name__)

@search_routes.route("/search", methods=["GET", "POST"])
def filter_search_page():
    """Allows users to filter climbs in the area."""
    data = None
    form = SearchForClimbsForm()
   
    if form.validate_on_submit():
        data = request.form

        if g.user:
            this_user = User.query.get(session[CURR_USER_KEY])
    
            compund_climbs = compound_climb_responses(data, this_user)
            return render_template("/climbs/search.html", form=form, climbs = compund_climbs, user = this_user)
        else:
            climbs = create_api_response(data)
            return render_template("/climbs/search.html", form=form, climbs = climbs)

    else: 
        return render_template('/climbs/search.html', form=form)
