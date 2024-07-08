import requests
from google.transit import gtfs_realtime_pb2

# GTFS RealtimeフィードのURL
feed_url = 'http://kumagaya.bus-go.com/GTFS-RT/encode_vehicle.php'

# HTTPリクエストを送信してデータを取得
response = requests.get(feed_url)

if response.status_code == 200:
    # GTFS Realtimeフィードをデコード
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(response.content)

    # デコードされたデータをテキスト形式に変換
    feed_text = str(feed)

    # テキストファイルに出力
    with open('realtime_data.txt', 'w', encoding='utf-8') as f:
        f.write(feed_text)

else:
    print(f"HTTPエラー: {response.status_code}")
