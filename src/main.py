from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def root():
    markers = [
        {
            'lat': -23.6921055,
            'lon': -46.5536373,
            'popup': 'This is the middle of the map.',
            'color': 'red',
            'fillColor': '#f03',
            'fillOpacity': 0.5,
            'radius': 5
        }
    ]
    return render_template('index.html', markers=markers)


if __name__ == '__main__':
    app.run(host="localhost", port=8080, debug=True)
