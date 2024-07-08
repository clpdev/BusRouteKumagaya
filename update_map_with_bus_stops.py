from flask import Flask, request, jsonify, render_template_string
import pandas as pd
import folium
from datetime import datetime, timedelta

app = Flask(__name__)

def create_map(time_value):
    # GTFSデータの読み込み
    stops = pd.read_csv('stops.txt')
    routes = pd.read_csv('routes.txt', dtype={'agency_id': str})
    trips = pd.read_csv('trips.txt')
    stop_times = pd.read_csv('stop_times.txt')
    print("Loading GTFS data...")

    # 例として特定の運行会社のデータを選択
    agency_id = '3000020112020'
    matching_routes = routes[routes['agency_id'] == agency_id]

    if matching_routes.empty:
        print("No matching routes found for agency_id:", agency_id)
        return None, None, None, None

    # フォリウムを使ったマップの作成
    m = folium.Map(location=[stops['stop_lat'].mean(), stops['stop_lon'].mean()], zoom_start=14)  # ズームレベルを14に設定

    # バス停のプロット
    for _, row in stops.iterrows():
        folium.Marker(location=[row['stop_lat'], row['stop_lon']], popup=row['stop_name']).add_to(m)

    circles = []
    print(f"Updating map for time: {time_value}")
    time_dt = datetime.strptime(time_value, '%H:%M')
    for _, route in matching_routes.iterrows():
        route_id = route['route_id']
        route_trips = trips[trips['route_id'] == route_id]

        for _, trip in route_trips.iterrows():
            trip_id = trip['trip_id']
            trip_headsign = trip['trip_headsign']
            trip_stops = stop_times[stop_times['trip_id'] == trip_id].sort_values(by='stop_sequence')

            for _, stop in trip_stops.iterrows():
                stop_data = stops[stops['stop_id'] == stop['stop_id']].iloc[0]
                stop_time = stop['arrival_time']
                stop_time_dt = datetime.strptime(stop_time, '%H:%M:%S')

                # 指定された時間の15分前と比較
                if stop_time_dt.time() >= (time_dt - timedelta(minutes=15)).time() and stop_time_dt.time() < time_dt.time():
                    circle = {
                        'lat': stop_data['stop_lat'],
                        'lon': stop_data['stop_lon'],
                        'radius': 1500,
                        'color': '#00FF00' if trip_headsign in ['熊谷駅南口行き', '籠原駅南口行き', '籠原駅北口行き', '熊谷駅東口行き'] else '#FF0000',
                        'fillColor': '#00FF00' if trip_headsign in ['熊谷駅南口行き', '籠原駅南口行き', '籠原駅北口行き', '熊谷駅東口行き'] else '#FF0000',
                        'fillOpacity': 0.3
                    }
                    circles.append(circle)

    return m, stops['stop_lat'].mean(), stops['stop_lon'].mean(), circles

@app.route('/')
def index():
    m, center_lat, center_lon, _ = create_map('06:00')

    if m is None:
        return "No matching routes found for the specified agency_id."

    map_html = m._repr_html_()
    slider_html = """
    <label for="timeSlider">Select time:</label>
    <input type="range" id="timeSlider" min="0" max="95" step="1" value="24" title="Select time">
    <output id='timeOutput'>06:00</output>
    <div id="map-container">{}</div>
    <script>
        var slider = document.getElementById('timeSlider');
        var output = document.getElementById('timeOutput');
        output.innerHTML = '06:00';

        slider.oninput = function() {{
            var value = this.value;
            var hours = Math.floor(value / 4);
            var minutes = (value % 4) * 15;
            var timeValue = (hours < 10 ? '0' : '') + hours + ':' + (minutes < 10 ? '0' : '') + minutes;
            output.innerHTML = timeValue;

            updateMap(timeValue);
        }};

        function updateMap(timeValue) {{
            fetch('/update_map?time=' + timeValue)
                .then(response => response.json())
                .then(data => {{
                    if (window.mymap) {{
                        window.mymap.eachLayer(function (layer) {{
                            if (layer instanceof L.Circle) {{
                                window.mymap.removeLayer(layer);
                            }}
                        }});
                        data.forEach(circle => {{
                            L.circle([circle.lat, circle.lon], {{
                                color: circle.color,
                                fillColor: circle.fillColor,
                                fillOpacity: circle.fillOpacity,
                                radius: circle.radius
                            }}).addTo(window.mymap);
                        }});
                    }}
                }})
                .catch(error => {{
                    console.error('Failed to update map:', error);
                }});
        }};

        document.addEventListener('DOMContentLoaded', function() {{
            window.mymap = L.map('map-container').setView([{lat}, {lon}], 14);
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }}).addTo(window.mymap);
        }});
    </script>
    """.format(map_html, lat=center_lat, lon=center_lon)

    html_content = f"""
    <!DOCTYPE html>
    <html lang="ja">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>レスポンシブマップ</title>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
        <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
    </head>
    <body>
        {slider_html}
    </body>
    </html>
    """

    return render_template_string(html_content)

@app.route('/update_map')
def update_map():
    time_value = request.args.get('time', '06:00')
    _, _, _, circles = create_map(time_value)
    return jsonify(circles)

if __name__ == '__main__':
    app.run(debug=True)
