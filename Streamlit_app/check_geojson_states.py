import requests

geojson_url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
india_geojson = requests.get(geojson_url).json()

geo_states = sorted({feature["properties"]["ST_NM"] for feature in india_geojson["features"]})

for state in geo_states:
    print(state)