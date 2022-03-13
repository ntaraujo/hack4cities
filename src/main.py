from flask import Flask, render_template
from backend.database_interface import Database
from collections.abc import Mapping
from os import path

app = Flask(__name__)

this_dir = path.abspath(path.dirname(__file__))

db = Database(path.join(this_dir, "backend", "database.db"), path.join(this_dir, "backend", "database.sql"))
markers = []
lines = []
hidrometers = {}

def deep_update(d, u):
    for k, v in u.items():
        if isinstance(v, Mapping):
            d[k] = deep_update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def register_hidrometer(data, time):
    this_id = data["id"]
    info = db.get_info(this_id)
    info["valores"] = {time: data["valor"]}

    next_id = info["idproximo"]
    if next_id is not None:
        next_info = db.get_info(next_id)
        if next_id in hidrometers:
            deep_update(hidrometers[next_id], next_info)
        else:
            hidrometers[next_id] = next_info

        info["proximo"] = hidrometers[next_id]
    else:
        info["proximo"] = None

    if this_id in hidrometers:
        deep_update(hidrometers[this_id], info)
    else:
        hidrometers[this_id] = info

def register_hidrometers():
    for time in range(1, 6):
        for data in db.get_data(time):
            register_hidrometer(data, time)

def map_values():
    for hidrometer in hidrometers.values():
        popup = hidrometer["tipo"]
        if popup == "casa":
            popup += ": " + str(hidrometer["instalacao"])

        new_marker = {
            'lat': hidrometer["x"],
            'lon': hidrometer["y"],
            'popup': popup,
            'color': 'green',
            # 'fillColor': '#f03',
            'fillOpacity': 1,
            'radius': 2
        }
        markers.append(new_marker)

        next_hidrometer = hidrometer["proximo"]
        if next_hidrometer is not None:
            new_line = [hidrometer["x"], hidrometer["y"], next_hidrometer["x"], next_hidrometer["y"]]
            lines.append(new_line)

register_hidrometers()
map_values()

@app.route('/')
def root():

    return render_template('index.html', markers=markers, lines=lines)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
