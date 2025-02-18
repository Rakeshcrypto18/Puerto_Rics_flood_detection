
import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 

file = 'test_tiff.tiff'
tiff = rasterio.open(file)



rasterio.plot.show(tiff)

print(tiff.shape)
#band 1 = red
#band 2= green
#band 3 = blue
num_bands = tiff.count
print(f"Number of bands: {num_bands}")

band_indexes = tiff.indexes
print(f"Band indexes: {band_indexes}")

band_dtypes = tiff.dtypes
print(f"Band data types: {band_dtypes}")


# Open the GeoTIFF file
with rasterio.open(file) as src:
    # Read a specific band (e.g., band 1)
    band_number = 1
    band_data = src.read(band_number)

band_data

with rasterio.open(file) as src:
    # Read a specific band (e.g., band 1)
    band_number = 2
    band_data2 = src.read(band_number)

band_data2

with rasterio.open(file) as src:
    # Read a specific band (e.g., band 1)
    band_number = 3
    band_data3 = src.read(band_number)

band_data3

tiff

for i in range(1, num_bands + 1):
            band_metadata = tiff.tags(i)
            print(f"Band {i} metadata: {band_metadata}")

file2 = 'dorado_09222017/2017-09-22-00:00_2017-09-22-23:59_Sentinel-1_IW_VV+VH_VH_-_decibel_gamma0.tiff'
tiff2 = rasterio.open(file2)

rasterio.plot.show(tiff2)

print(tiff2.shape)

num_bands = tiff2.count
print(f"Number of bands: {num_bands}")

band_indexes = tiff2.indexes
print(f"Band indexes: {band_indexes}")

band_dtypes = tiff2.dtypes
print(f"Band data types: {band_dtypes}")

with rasterio.open(file2) as src:
    # Read a specific band (e.g., band 1)
    band_number = 1
    band_data = src.read(band_number)

band_data


# file2='dorado_09222017/2017-09-22-00:00_2017-09-22-23:59_Sentinel-1_IW_VV+VH_VH_-_decibel_gamma0.tiff'
# df2 = rxr.open_rasterio(file2,
#                                  masked=True)
# df2.rio.bounds()

# #3 bands in decible gamma
# print("Number of bands", df2.rio.count)

#different bands to pandas
import pandas as pd
da = rxr.open_rasterio(file, masked=True)
#da = da.rio.reproject("EPSG:4326")
df = da[0].to_pandas()
df['y'] = df.index
df = pd.melt(df, id_vars='y')
df

filtered_df = df[df['x'] >= -66.05833]
filtered_df

da

df2 = da[1].to_pandas()
df2['y'] = df2.index
df2 = pd.melt(df2, id_vars='y')
df2

df3 = da[0].to_pandas()
df3['y'] = df3.index
df3 = pd.melt(df3, id_vars='y')
df3



da = rxr.open_rasterio(file2, masked=True)
#da = da.rio.reproject("EPSG:4326")
df22 = da[0].to_pandas()
df22['y'] = df22.index
df22 = pd.melt(df22, id_vars='y')
df22

df23 = da[1].to_pandas()
df23['y'] = df23.index
df23 = pd.melt(df23, id_vars='y')
df23

df24 = da[2].to_pandas()
df24['y'] = df24.index
df24 = pd.melt(df24, id_vars='y')
df24

# import rasterio
# import pandas as pd
# import numpy as np


#     """
#     Converts a specific band from a GeoTIFF to a Pandas DataFrame.

#     Args:
#         geotiff_path (str): Path to the GeoTIFF file.
#         band_num (int): Band number to extract (1-based index).

#     Returns:
#         pandas.DataFrame: DataFrame with columns 'x', 'y', and 'value'.
#                         Returns None if an error occurs.
#     """


# band_data = tiff.read(1)
            
#             # Create coordinate arrays
# rows, cols = band_data.shape
# x, y = np.meshgrid(np.arange(cols), np.arange(rows))
            
#             # Flatten arrays and create DataFrame
# df_test = pd.DataFrame({'x': x.flatten(),'y': y.flatten(),'value': band_data.flatten()})
# df_test

