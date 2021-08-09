import requests
import json

def create_api_response(data):

    ROOT_URL = "https://climb-api.openbeta.io/geocode/v1/climbs"
    compound_url = f"{ROOT_URL}"
    queries = []

    name = data['name']
    fa = data['fa']
    lat = data['lat']
    long = data['long']
    radius = data['radius'] 

    if len(name) > 0:queries.append(f"name={name}")
    if len(fa) > 0: queries.append(f"fa={fa}")
    if len(long) > 0 and len(lat) > 0:
        queries.append(f"latlng={lat},{long}")
    if len(radius) > 0: queries.append(f"radius={radius}")

    for query in queries:
        if compound_url == ROOT_URL:
            compound_url += f"?{query}"
        else:
            compound_url += f"&{query}"

    getClimb = requests.get(compound_url)

    response = getClimb.json()

    if response: return response
    else: return None

def compound_climb_responses(data, user):
    climbs = create_api_response(data)

    filtered_climbs = [] 

    for climb in climbs:
        climb['toggle'] = "null"
        for todo in user.todo:
            if int(climb['meta_mp_route_id']) == int(todo.climb_to_do):
                climb['toggle'] = "todo"
        for completed in user.completed:
            if int(climb['meta_mp_route_id']) == int(completed.completed_climb):
                climb['toggle'] = 'completed'

        filtered_climbs.append(climb)

    return filtered_climbs

def get_climb_specific_response(id, user):
    ROOT_URL = "https://climb-api.openbeta.io/geocode/v1/climbs"

    climb = requests.get(f"{ROOT_URL}/{id}")

    climb = climb.json()[0]
    
    climb['toggle'] = "null"
    for todo in user.todo:
        if int(climb['meta_mp_route_id']) == int(todo.climb_to_do):
            climb['toggle'] = "todo"
    for completed in user.completed:
        if int(climb['meta_mp_route_id']) == int(completed.completed_climb):
            climb['toggle'] = 'completed'

    return climb