from flask import render_template, request, Blueprint
from forms import SearchForSectorsForm
from helpers import query_many_sectors

search_routes = Blueprint('search_routes', __name__)

@search_routes.route("/search", methods=["GET", "POST"])
def filter_search_page():
    """Allows users to filter climbs in the area."""
    data = None
    sector_form = SearchForSectorsForm()

    if sector_form.validate_on_submit():
        data = request.form
        lat = data['lat'].replace(" ", "")
        lng = data["lng"].replace(" ", "")
        rad = data["radius"].replace(" ", "")
        if data["radius"] == "":
            result = query_many_sectors(lat, lng)
        else :
            result = query_many_sectors(lat, lng, rad)
      
        return render_template("/climbs/crag_search.html", sector_form=sector_form, sectors=result)
    else: 
        return render_template('/climbs/crag_search.html',  sector_form=sector_form)
