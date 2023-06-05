import geopandas as gpd
from tqdm import tqdm
import fiona

#change working directory
import os
os.chdir(r'C:\Users\WeilunShi\OneDrive - CGIAR\Desktop\Food Crisis and Insecurity\\1.Initilization')

def convert_geojson_to_unique_polygons(input_geojson, output_shapefile):
    # Read the GeoJSON file and convert it to a GeoDataFrame
    geodata = gpd.read_file(input_geojson)

    # Filter by polygon geometry type
    filtered_geodata = geodata[geodata.geometry.type == 'Polygon']

    # Remove any other features except geometry
    filtered_geodata = filtered_geodata[['geometry']]

    # Drop duplicate geometries to get unique polygons
    filtered_geodata = filtered_geodata.drop_duplicates(subset=['geometry']).reset_index(drop=True)

    # Save the unique polygons as a shapefile
    if not filtered_geodata.empty:
        # Get the total number of features for the progress bar
        total_features = len(filtered_geodata)

        # Initialize the progress bar
        progress_bar = tqdm(total=total_features, desc='Converting unique polygons to Shapefile', unit='feature')

        # Prepare the output shapefile schema and CRS
        schema = {
            'geometry': 'Polygon',
            'properties': {}
        }
        crs = filtered_geodata.crs

        # Write the output shapefile in chunks
        with fiona.open(output_shapefile, 'w', driver='ESRI Shapefile', schema=schema, crs=crs) as dst:
            for feature in filtered_geodata.iterfeatures():
                dst.write(feature)
                progress_bar.update(1)

        # Close the progress bar
        progress_bar.close()
    else:
        print("No polygon features found in the input GeoJSON.")

input_geojson = 'output.geojson'
output_shapefile = 'unique_polygons_shapefile.shp'
convert_geojson_to_unique_polygons(input_geojson, output_shapefile)
