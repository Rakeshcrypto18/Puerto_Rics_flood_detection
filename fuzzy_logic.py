"""
Fuzzy logic script reads in the original flood extent polygon shape file and the 
csv information assigned to each shape file (mean change or NDFI) and re assigns each point in the
dataframe to each corresponding polygon
"""
import pandas as pd
import geopandas as gpd
import numpy as np

""""
well start with the mean change flood extent 

read df change points and mean chnage shape file
"""
#need to run 18 again in ndfi
df_change_points = pd.read_csv('flood_extent_shape_files/floodpoints_and_polygons_mean_change_aoi216db.csv')
df_change_points

#small size fuzzy logic
df_small_size = df_change_points.groupby('polygon_id').size().reset_index(name='point_counts')


#minimal change fuzzy logic
df_change_points['mean_polygon_change'] = df_change_points.groupby('polygon_id')['change'].transform(lambda x: x.mean())
df_change_points

#slope fuzzy logic
df_change_points.columns
slope1 = pd.read_csv('DEM_1_5_slope/DEM_multi_slope_output.csv')
slope2 = pd.read_csv('DEM_1_5_slope/DEM_single_slope_output.csv')
slope = pd.concat([slope2,slope1])
    #merge slope with df_change_points (left merge)
df_change_points = pd.merge(df_change_points, slope, left_on=['y', 'x'], right_on=['Latitude', 'Longitude'], how = 'left')

df_change_points['mean_polygon_slope'] = df_change_points.groupby('polygon_id')['Slope_Degree'].transform(lambda x: x.mean())
df_change_points

#to_gdf = df_change_points[df_change_points['mean_polygon_change'] <= -3]

# Specify the path to the shapefile
shapefile_path = "flood_extent_shape_files/mean_change_new16db.shp"

# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

to_gdf= pd.merge(df_change_points,df_small_size, on='polygon_id', how = 'left')
to_gdf = to_gdf.drop_duplicates(subset=['polygon_id'], keep='first')
to_gdf.columns
# to_gdf

gdf2= to_gdf[['mean_polygon_change', 'polygon_id', 'point_counts']] #, 'mean_polygon_slope'
gdf2

gdf_info= pd.merge(gdf2,gdf, left_on='polygon_id', right_on='FID', how = 'left')
gdf_info

#convert to geopandas dataframe and calculate area of flood
gdf_info = gpd.GeoDataFrame(gdf_info, geometry='geometry', crs="EPSG:4326")
gdf_info = gdf_info.to_crs("EPSG:3857")

gdf_info["area"] = gdf_info['geometry'].area

gdf_info = gdf_info.to_crs("EPSG:4326")
gdf_info.columns

gdf_info

gdf_info['large_enough2'] = np.where(gdf_info['point_counts']>=100, 1, 0)
gdf_info['large_enough'] = np.where(gdf_info['area']>=8093.71, 1, 0)
gdf_info['change_enough'] = np.where(gdf_info['mean_polygon_change']<=-3, 1, 0)
#gdf_info['slope_enough'] = np.where(gdf_info['mean_polygon_slope']<=5, 1, 0)
gdf_info['combine'] = gdf_info['large_enough'] + gdf_info['change_enough']+gdf_info['large_enough2'] #+gdf_info['slope_enough']
gdf_info_filter = gdf_info[gdf_info['combine']==3]
gdf_info_filter

# gdf_info = gdf_info[['point_counts', 'large_enough2', 'area', 'large_enough', 'polygon_id']]
# gdf_info[gdf_info['polygon_id']==220]
# gdf_info.columns


gdf = gpd.GeoDataFrame(gdf_info_filter, geometry='geometry', crs="EPSG:4326")
gdf.to_file('filtered_mean_change_on_fuzzy_logic_new16db_2acre.shp')



""""
look at the same but with ndfi
"""
# df_change_points = pd.read_csv('floodpoints_and_polygons_NDFI.csv')
# df_change_points.columns


# df_small_size = df_change_points.groupby('polygon_id').size().reset_index(name='point_counts')
# df_small_size

# df_change_points['mean_polygon_change'] = df_change_points.groupby('polygon_id')['NDFI'].transform(lambda x: x.mean())
# df_change_points

# #to_gdf = df_change_points[df_change_points['mean_polygon_change'] <= -3]

# # Specify the path to the shapefile
# shapefile_path = "flood_extent_shape_files/NDFI_filter_40.shp"

# # Read the shapefile into a GeoDataFrame
# gdf = gpd.read_file(shapefile_path)

# to_gdf= pd.merge(df_change_points,df_small_size, on='polygon_id', how = 'left')
# to_gdf = to_gdf.drop_duplicates(subset=['polygon_id'], keep='first')
# to_gdf.columns

# gdf2= to_gdf[['mean_polygon_change', 'point_counts', 'polygon_id']]
# gdf2

# gdf_info= pd.merge(gdf2,gdf, left_on='polygon_id', right_on='FID', how = 'left')
# gdf_info

# gdf_info['large_enough'] = np.where(gdf_info['point_counts']>=10, 1, 0)
# gdf_info['change_enough'] = np.where(gdf_info['mean_polygon_change']<=-0.45, 1, 0)
# gdf_info['combine'] = gdf_info['large_enough'] + gdf_info['change_enough'] 
# gdf_info_filter = gdf_info[gdf_info['combine']>=1]
# gdf_info_filter

# gdf = gpd.GeoDataFrame(gdf_info_filter, geometry='geometry', crs="EPSG:4326")
# gdf.to_file('filtered_NDFI_on_fuzzy_logic.shp')


# gdf = gpd.GeoDataFrame(gdf, crs="EPSG:4326", geometry='geometry_y')
# gdf = gdf[['mean_polygon_change', 'point_counts', 'polygon_id', 'geometry_y']]
# gdf.to_file('flood_polygon_info.shp')

# gdf2