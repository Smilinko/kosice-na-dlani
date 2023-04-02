import folium
from shapely.geometry import Polygon
from shapely.ops import cascaded_union
import database

m = folium.Map(location=[48.721900, 21.257537], zoom_start=14)


def subtract_polygons(minuend, subtrahend):
    return minuend.difference(subtrahend)


#  change these values to modify the visualization
typ = "playground"
colors = ["green", "yellow", "orange", "red"]
opacities = [.35, .3, .4, .25]


polygons = []
for i in ["five", "ten", "fifteen", "twenty"]:
    polygons.append(cascaded_union([Polygon(x) for x in database.retrieve(typ, i)]))

new_polygons = []
for i in range(4):
    if i == 0:
        new_polygons.append(polygons[i])
    else:
        new_polygons.append(subtract_polygons(polygons[i], polygons[i-1]))


for j, polygon in enumerate(new_polygons):
    lst = list(polygon.geoms)
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

        pleth = folium.Choropleth(geo_data=geo_data, fill_opacity=opacities[j], line_opacity=.4, fill_color=colors[j])
        m.add_child(pleth)
        if j == 0:
            m.keep_in_front(pleth)

m.show_in_browser()
