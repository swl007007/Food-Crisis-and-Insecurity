import rasterio
import gzip
import shutil
file = 'GOSIF_GPP_2017.M01_mean'

with gzip.open(f'{file}.tif.gz', 'rb') as f_in:
    with open(f'{file}.tif', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)

def print_crs(file):
    with rasterio.open(f'{file}.tif') as src:
        print(f"The CRS of the raster file is: {src.crs}")


print_crs(file)