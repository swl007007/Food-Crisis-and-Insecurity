import pandas as pd
import numpy as np
import geopandas as gpd
import requests
import json
import tqdm
import datetime

df_2 = pd.read_csv(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\ACLED_GOSIF_GPP_CHIRPS_GOSIF_GPP_SD_FAO.csv')
# convert geo_df date to datetime
df_2['date'] = pd.to_datetime(df_2['date'])
from shapely import wkt

# Convert the 'geometry' column to shapely geometry
df_2['geometry'] = df_2['geometry'].apply(wkt.loads)

# Convert the DataFrame to a GeoDataFrame
gdf = gpd.GeoDataFrame(df_2, geometry='geometry')

# find the centroid of each polygon
gdf['centroid'] = gdf['geometry'].centroid

# extract the lat and lon from the centroid
gdf['lon'] = gdf['centroid'].apply(lambda p: p.x)
gdf['lat'] = gdf['centroid'].apply(lambda p: p.y)


new_df = gdf
# extract distinct lat and lon, and create a new df
lat_lon = new_df[['lat', 'lon']].drop_duplicates().reset_index(drop=True)
# round to two digits, and create a new column
lat_lon['lat_round'] = lat_lon['lat'].round(2)
lat_lon['lon_round'] = lat_lon['lon'].round(2)

# save lat_lon to csv
lat_lon.to_csv(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\lat_lon.csv', index=False)