from flask import Flask, render_template
from backend.database_interface import Database
import os

app = Flask(__name__)

this_dir = os.path.abspath(os.path.dirname(__file__))



@app.route('/')
def root():
    
    db = Database(os.path.join(this_dir, "backend", "database.db"), os.path.join(this_dir, "backend", "database.sql"))
    markers = []
    lines = []
    hidrometers = {}

    for data in db.get_data(1):
        this_id = data["id"]
        info = db.get_info(this_id)
        info["valor"] = data["valor"]

        next_id = info["idproximo"]
        if next_id is None:
            next_info = None
        else:
            next_info = db.get_info(next_id)
            if next_id in hidrometers:
                hidrometers[next_id].update(next_info)
            else:
                hidrometers[next_id] = next_info

            info["proximo"] = hidrometers[next_id]

        if this_id in hidrometers:
            hidrometers[this_id].update(info)
        else:
            hidrometers[this_id] = info

        new_marker = {
            'lat': info["x"],
            'lon': info["y"],
            'popup': f'Instalação: {info["instalacao"] or "N/A"} - {data["valor"]}m³/s',
            'color': 'green',
            # 'fillColor': '#f03',
            'fillOpacity': 1,
            'radius': 2
        }
        markers.append(new_marker)

        if next_info is not None:
            new_line = [info["x"], info["y"], next_info["x"], next_info["y"]]
            lines.append(new_line)

    return render_template('index.html', markers=markers, lines=lines)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
