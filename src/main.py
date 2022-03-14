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
first_hidrometers = []

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
    info["id"] = this_id
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
    
    this_hidrometer = hidrometers[this_id]
    if this_hidrometer["tipo"] in ("Início", "Intermediário") and this_hidrometer not in first_hidrometers:
        first_hidrometers.append(this_hidrometer)

def register_hidrometers():
    for time in range(1, 11):
        for data in db.get_data(time):
            register_hidrometer(data, time)

def sum_update(d, u):
    for k, v in u.items():
        if k in d:
            d[k] += v
        else:
            d[k] = v
    return d

def get_loss(h):
    return hidrometers[h["fonteid"]]["perca"]

def register_relations():
    for hidrometer in first_hidrometers:
        total_flows = hidrometer["valores"]
        used_flows = {}
        not_used_flows = {}
        proximo = hidrometer["proximo"]
        while proximo is not None:
            sum_update(used_flows, proximo["valores"])
            if proximo["tipo"] == "Intermediário":
                break
            proximo = proximo["proximo"]
        for time, total_flow in total_flows.items():
            not_used_flows[time] = total_flow - used_flows[time]
        hidrometer["valores não utilizados"] = not_used_flows
        not_used_flows_list = list(not_used_flows.values())
        hidrometer["perca"] = sum(not_used_flows_list[1:]) - not_used_flows_list[0]

def map_values():
    for hidrometer in hidrometers.values():
        tipo = hidrometer["tipo"]
        popup = tipo + ": "
        if tipo in ("Casa", "Fim"):
            popup += str(hidrometer["instalacao"])
        else:
            popup += f'Perca estimada: {hidrometer["perca"]}m³/s'

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

        if hidrometer["fonteid"] is None:
            perca = hidrometer["perca"]
        else:
            perca = get_loss(hidrometer)
        perca = max(5, perca/4)

        if next_hidrometer is not None:
            color = 'green' if perca == 5 else 'red'
            new_line = [hidrometer["x"], hidrometer["y"], next_hidrometer["x"], next_hidrometer["y"], perca, color]
            lines.append(new_line)

register_hidrometers()
register_relations()
map_values()

@app.route('/')
def root():

    return render_template('index.html', markers=markers, lines=lines)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
