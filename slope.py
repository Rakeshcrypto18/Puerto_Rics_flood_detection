import os
import rasterio
import numpy as np
import pandas as pd
from tqdm import tqdm

# Input folder containing TIFFs
#input_dir = "/Users/rakesh/Desktop/DEM_tiff_1_5"
input_dir = "dem_tifs"
# Output CSV path
output_csv = "slope_output.csv"

def calculate_slope(dem_array, transform):
    # Approximate pixel resolution in meters
    x_res_m = transform[0] * 111320
    y_res_m = abs(transform[4]) * 110540 

    # Calculate gradient
    dx, dy = np.gradient(dem_array, x_res_m, y_res_m)

    # Calculate slope in radians then convert to degrees
    slope_rad = np.arctan(np.sqrt(dx**2 + dy**2))
    slope_deg = np.degrees(slope_rad)

    return slope_deg


# Collect all slope data
all_data = []

# Loop through files
for file in tqdm(os.listdir(input_dir), desc="Processing TIFF files"):
    if file.lower().endswith((".tif", ".tiff")):
        filepath = os.path.join(input_dir, file)

        with rasterio.open(filepath) as src:
            dem_array = src.read(1).astype(float)
            transform = src.transform

            # Handle no-data
            if src.nodata is not None:
                dem_array[dem_array == src.nodata] = np.nan

            # Compute slope
            slope_array = calculate_slope(dem_array, transform)

            # Get pixel coordinates
            rows, cols = np.indices(dem_array.shape)
            xs, ys = rasterio.transform.xy(transform, rows, cols)
            lons = np.array(xs).flatten()
            lats = np.array(ys).flatten()
            slopes = slope_array.flatten()

            # Create DataFrame
            df = pd.DataFrame({
                "File_Name": file,
                "Longitude": lons,
                "Latitude": lats,
                "Slope_Degree": slopes
            })

            # Drop NaNs
            df = df.dropna(subset=["Slope_Degree"])
            all_data.append(df)

# Save to CSV
if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    final_df.to_csv(output_csv, index=False)
    print(f" Slope data saved at: {output_csv}")
else:
    print(" No TIFFs were processed.")
