from re import search
from flask import render_template, request, Blueprint
from flask.helpers import flash
from werkzeug.utils import redirect
from forms import SearchByCoordinate, SearchByAddress
from helpers import query_many_sectors, geocode_adress

search_routes = Blueprint('search_routes', __name__)

@search_routes.route("/search", methods=["GET"])
def choose_search_method():
    """Choose between two search methods"""
    return render_template("/climbs/search.html")

@search_routes.route("/search/coordinates", methods=["GET", "POST"])
def search_by_coordinate():
    """Allows users to search for crags by coordinates."""
    sector_form = SearchByCoordinate()
    if request.args.get('lat'):
        sector_form.lat.data = float(request.args.get('lat'))
        sector_form.lng.data = float(request.args.get('lng'))
        if request.args.get('radius'):
            sector_form.radius.data = int(request.args.get('radius'))

    if sector_form.validate_on_submit():
        data = request.form
        lat = data['lat'].replace(" ", "")
        lng = data["lng"].replace(" ", "")
        rad = data["radius"].replace(" ", "")
        if data["radius"] == "":
            result = query_many_sectors(lat, lng)
        else :
            result = query_many_sectors(lat, lng, rad)
      
        return render_template("/climbs/search_form.html", sector_form=sector_form, sectors=result)
    else: 
        return render_template('/climbs/search_form.html',  sector_form=sector_form)

@search_routes.route('/search/address', methods=["GET", "POST"])
def search_by_address():
    """Allows users to search for crags by address"""
    data = None 
    sector_form = SearchByAddress()

    if sector_form.validate_on_submit():
        data = request.form

        number = data["number"]
        street = data["street"]
        town = data["town"]
        state = data["state"]
        rad = data["radius"].replace(" ", "")

        response = geocode_adress(number, street, town, state)
        status = response["status"]
        
        if status == 'OK' :
            coordinates = response["results"][0]["geometry"]["location"]
            lat = coordinates["lat"]
            lng = coordinates["lng"]
            if not rad == '':
                rad = f"&radius={rad}"

            return redirect(f"/search/coordinates?lat={lat}&lng={lng}{rad}")
        elif status == 'ZERO_RESULTS':
            flash(f"Zero results found for {number} {street} {town} {state}")
            return render_template('/climbs/search_form.html',  sector_form=sector_form)
        else: 
            flash(f"The address feature is currently unavailable at this time. Sorry for the inconvenience. Please use the coordinate search")
            print("***** Status *****")
            print(response)
            return redirect(f"/search/coordinates")
    else: 
        return render_template('/climbs/search_form.html',  sector_form=sector_form)
