import pandas as pd

# shapes.txtを読み込み
shapes_df = pd.read_csv('GTFS/shapes.txt')

# shape_idが1のデータをフィルタリング
shape_id_1_df = shapes_df[shapes_df['shape_id'] == 1]

# 必要なカラム(shape_pt_lat, shape_pt_lon, shape_pt_sequence)を抽出
lat_lon_sequence_df = shape_id_1_df[['shape_pt_lat', 'shape_pt_lon', 'shape_pt_sequence']]

# 抽出したデータをCSV形式で出力
lat_lon_sequence_df.to_csv('shape_lat_lon_sequence_shape_id_1.csv', index=False)
