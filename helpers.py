import requests
import json
import os

from requests.api import request

from secret import API_KEY_LOCAL
from config import ROOT_URL, BASE_URL

def query_climbs(climb_ids, user = None):
    """Receives array of ids returns info about those climbs."""

    climbs = requests.get(f"{ROOT_URL}/climbs/{climb_ids}")

    result = []
    for climb in climbs.json(): 

        # Refactor Type input for UI
        types = climb['type'].keys()
        climb['type'] = ''
        for type in types:
            if climb['type'] == '':
                climb['type'] += type
            else:
                climb['type'] += f", {type}"

        # If user, show which climbs have been completed / selected todo
        if not user == None:
            climb['toggle'] = ""
            for todo in user.todo:
                if int(climb['meta_mp_route_id']) == int(todo.climb_id):
                    climb['toggle'] = "todo"
            for completed in user.completed:
                if int(climb['meta_mp_route_id']) == int(completed.climb_id):
                    climb['toggle'] = 'completed'

        result.append(climb)
    
    return result

def query_many_sectors(lat, lng, rad = 3):
    """Receives an id then returns the data for that one sector"""

    SECTOR_URL = f"{ROOT_URL}/sectors?latlng={lat},{lng}&radius={rad}"
    result = requests.get(SECTOR_URL)

    return result.json()

def query_sector(id):
    """Receives an id then returns the data for that one sector"""

    SECTOR_URL = f"{ROOT_URL}/sectors/{id}" 
    result = requests.get(SECTOR_URL)
    return result.json()

def join_climb_ids(ids):
    """Take a list of Id instances and format them into a '|' separated list"""
    id_string = ''
    
    for id in ids:
        if id_string == '':
            id_string += str(id.climb_id)
        else: 
            id_string += f"|{str(id.climb_id)}"
    return id_string

def geocode_adress(number, street, town, state):
    street = street.replace(" ", '%20')
    """Converts Adress to GeoCode"""
    
    API_KEY = os.environ.get('API_KEY', f"{API_KEY_LOCAL}")
    GOOGLE_GEOCODE = f"{BASE_URL}{number}+{street}+{town}+{state}{API_KEY}" 
    
    result = requests.get(GOOGLE_GEOCODE)
    return result.json()
