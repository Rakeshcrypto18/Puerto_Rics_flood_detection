"""
Still work in progress, trying different methods of getting slope from the dem
"""
import rasterio
import numpy as np
import pandas as pd
import rioxarray as rxr 

def calculate_slope(dem_path, output_path):
    """
    Calculates slope from a DEM using numpy and rasterio.

    Args:
        dem_path (str): Path to the input DEM raster file.
        output_path (str): Path to save the output slope raster file.
    """
    with rasterio.open(dem_path) as src:
        elevation = src.read(1)
        rows, cols = elevation.shape
        x, y = np.meshgrid(np.arange(cols), np.arange(rows))
        
        # Calculate the gradient in the x and y directions
        dx = np.diff(elevation, axis=1)
        dy = np.diff(elevation, axis=0)
        
        # Pad the arrays to match the original shape
        dx = np.pad(dx, ((0, 0), (0, 1)), mode='edge')
        dy = np.pad(dy, ((0, 1), (0, 0)), mode='edge')
        
        # Calculate slope in degrees
        slope = np.arctan(np.sqrt(dx**2 + dy**2)) * (180 / np.pi)

        # Update metadata for output raster
        profile = src.profile
        profile.update({
            'dtype': rasterio.float32,
            'count': 1
        })

        # Write the slope array to a new raster file
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(slope.astype(np.float32), 1)


if __name__ == '__main__':
    dem_file = 'dem_tifs/dem_01.tiff'  # Replace with your DEM file path
    slope_file = 'slope_test.tiff' # Replace with desired output path
    calculate_slope(dem_file, slope_file)
    print(f"Slope calculation complete. Output saved to {slope_file}")

dem = 'slope_test.tiff'


#different bands to pandas VH example
da = rxr.open_rasterio(dem, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfdem = da[0].to_pandas()
dfdem
dfdem['y'] = dfdem.index
dfdem = pd.melt(dfdem, id_vars='y')
dfdem=dfdem.rename(columns={'value':'dem'})
dfdem

dfdem.to_csv('slope_test.csv')



import numpy as np
import rasterio
from rasterio.enums import Resampling

def calculate_slope(dem_path, output_path):
    """
    Calculates slope from a DEM using numpy and rasterio.

    Args:
        dem_path (str): Path to the input DEM raster file.
        output_path (str): Path to save the output slope raster file.
    """

    with rasterio.open(dem_path) as src:
        # Read the DEM data into a NumPy array
        dem = src.read(1)

        # Calculate the horizontal and vertical resolution of the DEM
        xres, yres = src.res
        
        # Calculate the slopes in the x and y directions
        slope_x, slope_y = np.gradient(dem, xres, yres)

        # Calculate the overall slope in degrees
        slope = np.degrees(np.arctan(np.sqrt(slope_x**2 + slope_y**2)))

        # Update metadata for the output raster
        profile = src.profile
        profile.update({
            'dtype': rasterio.float32,
            'count': 1
        })

        # Write the slope data to a new raster file
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(slope.astype(rasterio.float32), 1)

if __name__ == '__main__':
    dem_file = 'dem_tifs/dem_01.tiff'  # Replace with your DEM file path
    output_file = 'slope_test2.tiff' # Replace with your desired output path
    calculate_slope(dem_file, output_file)
    print(f"Slope calculation complete. Output saved to {output_file}")


dem = 'slope_test2.tiff'
#different bands to pandas VH example
da = rxr.open_rasterio(dem, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfdem = da[0].to_pandas()
dfdem
dfdem['y'] = dfdem.index
dfdem = pd.melt(dfdem, id_vars='y')
dfdem=dfdem.rename(columns={'value':'dem'})
dfdem

dfdem.to_csv('slope_test2.csv')


dem = 'dem_tifs/dem_01.tiff'
#different bands to pandas VH example
da = rxr.open_rasterio(dem, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfdem = da[0].to_pandas()
dfdem
dfdem['y'] = dfdem.index
dfdem = pd.melt(dfdem, id_vars='y')
dfdem=dfdem.rename(columns={'value':'dem'})
dfdem

dfdem.to_csv('dem_csv_1.csv')


