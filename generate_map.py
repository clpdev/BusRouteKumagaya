import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium

# GTFSデータの読み込み
stops = pd.read_csv('stops.txt')
routes = pd.read_csv('routes.txt')
trips = pd.read_csv('trips.txt')
stop_times = pd.read_csv('stop_times.txt')
shapes = pd.read_csv('shapes.txt')

# 使用する路線名のリスト
desired_route_names = [
    'さくら号', 'グライダー号', 'グライダーワゴン　妻沼循環', 
    'グライダーワゴン', 'ムサシトミヨ号　籠原駅', 'ムサシトミヨ号　上之荘', 
    'ひまわり号', '直実号', 'ほたる号　熊谷駅南口', 
    'ほたる号　籠原駅南口', 'くまぴあ号'
]

# 路線名でフィルタリング
matching_routes = routes[routes['route_long_name'].isin(desired_route_names)]

if not matching_routes.empty:
    route_ids = matching_routes['route_id'].tolist()

    # 該当するtrip_idを取得
    trip_ids = trips[trips['route_id'].isin(route_ids)]['trip_id'].unique()
    
    # 該当するstop_idを取得
    stop_ids = stop_times[stop_times['trip_id'].isin(trip_ids)]['stop_id'].unique()
    
    # stop_idでフィルタリング
    stops = stops[stops['stop_id'].isin(stop_ids)]

    # ジオデータフレームの作成
    stops['geometry'] = stops.apply(lambda x: Point((x.stop_lon, x.stop_lat)), axis=1)
    stops_gdf = gpd.GeoDataFrame(stops, geometry='geometry')

    # フォリウムを使ったマップの作成
    m = folium.Map(location=[stops['stop_lat'].mean(), stops['stop_lon'].mean()], zoom_start=12)

    # 停留所のプロットとバッファの作成
    for _, row in stops_gdf.iterrows():
        buffer = row.geometry.buffer(0.015)  # 15mのバッファ（必要に応じて調整）

        folium.GeoJson(buffer.__geo_interface__,
                       style_function=lambda x: {
                           'fillColor': '#00ff00',    # 塗りつぶしの色
                           'fillOpacity': 0.3,         # 塗りつぶしの透明度を調整
                           'color': '#00ff00',        # 線の色
                           'weight': 1,               # 線の太さ
                           'opacity': 0.5,            # 線の透明度を調整
                       }).add_to(m)

        # 停留所マーカーを追加
        folium.Marker(location=[row['stop_lat'], row['stop_lon']], popup=row['stop_name']).add_to(m)

    # 地図を保存
    m.save('transit_map_selected_routes.html')
else:
    print("No routes found for the specified route names.")
