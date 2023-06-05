import geopandas as gpd
import pandas as pd
import re

# Read in the data
areas_gdf = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\downloads_chirps\chirps_1.geojson')
areas_gdf_2 = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\downloads_chirps\chirps_2.geojson')

areas_gdf_3 = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\downloads_chirps\chirps_3.geojson')

areas_gdf_4 = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\downloads_chirps\chirps_4.geojson')

merged_gdf = pd.concat([areas_gdf, areas_gdf_2, areas_gdf_3, areas_gdf_4])



# read the output file
output = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\\2.merge_data\output_2.geojson')

output_geom = gpd.read_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\\1.Initilization\output.geojson')
# drop the geometry column
output = output.drop('geometry', axis=1)

# keep only geometry and title columns
output_geom = output_geom[['title', 'geometry']]

# remove duplicates accoridng to title and geometry

output_geom = output_geom.drop_duplicates(subset=['title', 'geometry'])


# merge output with output_geom
output = output.merge(output_geom, on='title', how='left')

gdf = merged_gdf
def extract_year_month(file_name):
    pattern = r"(\d{4})\.(\d{2})"
    match = re.search(pattern, file_name)

    if match:
        year = int(match.group(1))
        month = int(match.group(2))
        return year, month
    else:
        return None, None

# Use the apply method to apply the function to the 'file_name' column
gdf['year_month'] = gdf['time'].apply(extract_year_month)

# Split the 'year_month' tuple into separate 'year' and 'month' columns
gdf[['year', 'month']] = gdf['year_month'].apply(pd.Series)


# Drop the 'year_month', 'time', 'year' and 'month' columns
gdf['date'] = pd.to_datetime(gdf[['year', 'month']].assign(DAY=1))
gdf.drop(columns='year_month', inplace=True)
gdf.drop(columns='time', inplace=True)
gdf.drop(columns='year', inplace=True)
gdf.drop(columns='month', inplace=True)

gdf1 = output
gdf2 = gdf

# Check if gdf1 and gdf2 are GeoDataFrames; if not, convert them
if not isinstance(gdf1, gpd.GeoDataFrame):
    gdf1 = gpd.GeoDataFrame(gdf1, geometry='geometry', crs="EPSG:3857")

if not isinstance(gdf2, gpd.GeoDataFrame):
    gdf2 = gpd.GeoDataFrame(gdf2, geometry='geometry', crs="EPSG:4326")

# Make sure both GeoDataFrames have the same CRS (Coordinate Reference System)
if gdf1.crs != gdf2.crs:
    gdf2 = gdf2.to_crs(gdf1.crs)

# Perform a spatial join between gdf1 and gdf2 based on intersection
spatial_join_gdf = gpd.sjoin(gdf1, gdf2, how='left', op='intersects')


# filter date_left and date_right, so that date_right is three mothns within date_left
spatial_join_gdf = spatial_join_gdf[(spatial_join_gdf['date_right'] >= spatial_join_gdf['date_left'] - pd.DateOffset(months=3))&(spatial_join_gdf['date_right'] <= spatial_join_gdf['date_left'])]

# drop date_right, and rename date_left to date
spatial_join_gdf.drop(columns='date_right', inplace=True)
spatial_join_gdf.rename(columns={'date_left': 'date'}, inplace=True)


# drop the index_right and FID column
spatial_join_gdf.drop(columns='index_right', inplace=True)
spatial_join_gdf.drop(columns='FID', inplace=True)


# remove duplicates
spatial_join_gdf = spatial_join_gdf.drop_duplicates(subset=['title', 'date', 'geometry'])

# save the output
spatial_join_gdf.to_file(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\\2.merge_data\output_3.geojson', driver='GeoJSON')