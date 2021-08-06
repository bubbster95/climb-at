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

    print("********** Response **********")
    print(radius, compound_url)

    if response: return response
    else: return None
