import folium
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import database


m = folium.Map(location=[48.721900, 21.257537], zoom_start=14)


def overlap_polygons(po1, po2):
    diff = po2.difference(po1)
    return po2.difference(diff)


#  change these values to modify the visualization
data = [["Pošty", "fifteen"], ["supermarket", "five"], ["fast_food", "ten"], ["cafe", "ten"],
        ["Všeobecná ambulancia pre deti", "ten"], ["MS_štátna", "five"]]


polygons = []
for i in data:
    polygons.append(cascaded_union([Polygon(x) for x in database.retrieve(i[0], i[1])]))


overlap = None
for polygon in polygons:
    if overlap is None:
        overlap = polygon
    else:
        overlap = overlap_polygons(overlap, polygon)

lst = list(overlap.geoms)
for i in lst:
    geo_data = {"type": "FeatureCollection", "features": []}
    geo_data["features"].append({
        "type": "Feature",
        "id": "0",
        "properties": {
            "name": "visual"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                list(i.exterior.coords)
            ]
        }
    })

    m.add_child(folium.Choropleth(geo_data=geo_data, fill_opacity=0.4, line_opacity=0.1, fill_color="red"))

m.show_in_browser()
