import csv
import json
import os

def read_csv(filename):
    with open(filename, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

# パスの設定
gtfs_path = r'C:\Users\COLOP\Desktop\BusRouteKumagaya\GTFS'
output_path = gtfs_path  # JSONファイルの保存先

# CSVファイルを読み込む
routes = read_csv(os.path.join(gtfs_path, 'routes.txt'))
shapes = read_csv(os.path.join(gtfs_path, 'shapes.txt'))
stops = read_csv(os.path.join(gtfs_path, 'stops.txt'))
trips = read_csv(os.path.join(gtfs_path, 'trips.txt'))

# ルート情報とトリップ情報をまとめる
data = {
    "routes": [],
    "trips": []
}

for route in routes:
    data["routes"].append({
        "route_id": route["route_id"],
        "route_long_name": route["route_long_name"],
        "route_color": route["route_color"],
        "route_text_color": route["route_text_color"]
    })

for trip in trips:
    data["trips"].append({
        "trip_id": trip["trip_id"],
        "trip_headsign": trip["trip_headsign"]
    })

# ルート情報とトリップ情報をJSONファイルとして出力
with open(os.path.join(output_path, 'gtfs_data.json'), 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# シェイプ情報をまとめる
shapes_data = {"shapes": []}
for shape in shapes:
    shapes_data["shapes"].append({
        "shape_id": shape["shape_id"],
        "shape_pt_lat": shape["shape_pt_lat"],
        "shape_pt_lon": shape["shape_pt_lon"],
        "shape_pt_sequence": shape["shape_pt_sequence"]
    })

# シェイプ情報をJSONファイルとして出力
with open(os.path.join(output_path, 'shapes_data.json'), 'w', encoding='utf-8') as f:
    json.dump(shapes_data, f, ensure_ascii=False, indent=2)

# バス停情報をまとめる
stops_data = {"stops": []}
for stop in stops:
    stops_data["stops"].append({
        "stop_name": stop["stop_name"],
        "stop_lat": stop["stop_lat"],
        "stop_lon": stop["stop_lon"]
    })

# バス停情報をJSONファイルとして出力
with open(os.path.join(output_path, 'stops_data.json'), 'w', encoding='utf-8') as f:
    json.dump(stops_data, f, ensure_ascii=False, indent=2)
