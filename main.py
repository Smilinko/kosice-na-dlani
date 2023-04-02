import folium
import database

m = folium.Map(location=[48.721900, 21.257537], zoom_start=14)


#  change these values to modify the visualization
data = [{"type": "playground", "time": "fifteen", "color": "blue", "opacity": 0.4},
        {"type": "Pošta", "time": "twenty", "color": "red", "opacity": 0.2}]


for i in data:
    geo_data = {"type": "FeatureCollection", "features": []}

    geo_data["features"].append({
        "type": "Feature",
        "id": "0",
        "properties": {
            "name": "visual"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates":
                database.retrieve(i["type"], i["time"])
        }
    })

    m.add_child(folium.Choropleth(geo_data=geo_data, fill_opacity=i["opacity"], line_opacity=0.1, fill_color=i["color"]))

m.show_in_browser()
