import requests
from google.transit import gtfs_realtime_pb2
import json

# GTFS RealtimeフィードのURL
feed_url = 'http://kumagaya.bus-go.com/GTFS-RT/encode_vehicle.php'

# HTTPリクエストを送信してデータを取得
response = requests.get(feed_url)

if response.status_code == 200:
    # GTFS Realtimeフィードをデコード
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # デコードされたデータをJSON形式に変換
    feed_data = []
    for entity in feed.entity:
        entity_dict = {
            "id": entity.id,
            "is_deleted": entity.is_deleted,
            "vehicle": {
                "trip": {
                    "trip_id": entity.vehicle.trip.trip_id,
                    "route_id": entity.vehicle.trip.route_id,
                    "start_time": entity.vehicle.trip.start_time,
                    "start_date": entity.vehicle.trip.start_date,
                    "schedule_relationship": entity.vehicle.trip.schedule_relationship
                },
                "vehicle": {
                    "id": entity.vehicle.vehicle.id,
                    "label": entity.vehicle.vehicle.label,
                    "license_plate": entity.vehicle.vehicle.license_plate
                },
                "position": {
                    "latitude": entity.vehicle.position.latitude,
                    "longitude": entity.vehicle.position.longitude,
                    "bearing": entity.vehicle.position.bearing,
                    "odometer": entity.vehicle.position.odometer,
                    "speed": entity.vehicle.position.speed
                },
                "current_stop_sequence": entity.vehicle.current_stop_sequence,
                "current_status": entity.vehicle.current_status,
                "timestamp": entity.vehicle.timestamp,
                "stop_id": entity.vehicle.stop_id
            }
        }
        feed_data.append(entity_dict)

    # JSONファイルに出力
    with open('realtime_data.json', 'w', encoding='utf-8') as f:
        json.dump(feed_data, f, ensure_ascii=False, indent=2)

else:
    print(f"HTTPエラー: {response.status_code}")
