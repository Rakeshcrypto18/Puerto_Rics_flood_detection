"""
Flood extent filtering script reads in the original flood extent polygon shape file and the 
csv information assigned to each point and uses simple filtering logic to remove polygons that dont meet the selected criteria
"""
import pandas as pd
import geopandas as gpd
import numpy as np

""""
well start with the mean change flood extent 
read df change points and mean chnage shape file
"""
#load in polygon and point information
df_change_points = pd.read_csv('final_flood_extent/floodpoints_and_polygons_mean_change_aoi1_16db.csv')
df_change_points

#minimal change 
df_change_points['mean_polygon_change'] = df_change_points.groupby('poly_id')['change'].transform(lambda x: x.mean())
df_change_points

#slope fuzzy logic
df_change_points.columns
slope = pd.read_csv('dem_slope_csvs/slope_output_aoi1.csv')
#merge slope with df_change_points (left merge)
df_change_points = pd.merge(df_change_points, slope, left_on=['y', 'x'], right_on=['Latitude', 'Longitude'], how = 'left')
df_change_points['mean_polygon_slope'] = df_change_points.groupby('poly_id')['Slope_Degree'].transform(lambda x: x.mean())
    # if no slope computed assume 0
df_change_points['mean_polygon_slope'] = df_change_points['mean_polygon_slope'].fillna(0)


# Specify the path to the shapefile
shapefile_path = "final_flood_extent/mean_change_aoi1_16db.shp"
# Read the shapefile into a GeoDataFrame
gdf = gpd.read_file(shapefile_path)

to_gdf = df_change_points.drop_duplicates(subset=['poly_id'], keep='first')

gdf2= to_gdf[['mean_polygon_change', 'poly_id' , 'mean_polygon_slope']] 

gdf_info= pd.merge(gdf2,gdf, left_on='poly_id', right_on='poly_id', how = 'left')


#convert to geopandas dataframe and calculate area of flood
gdf_info = gpd.GeoDataFrame(gdf_info, geometry='geometry', crs="EPSG:4326")
gdf_info = gdf_info.to_crs("EPSG:3857")

gdf_info["area"] = gdf_info['geometry'].area

gdf_info = gdf_info.to_crs("EPSG:4326")
gdf_info

# caculate weather polygon meet criteria
gdf_info['large_enough'] = np.where(gdf_info['area']>=8093.71, 1, 0) #areas less than 2 acres are removed
gdf_info['change_enough'] = np.where(gdf_info['mean_polygon_change']<=-5, 1, 0) #areas less tha 5 decible average chnage are removed
gdf_info['slope_enough'] = np.where(gdf_info['mean_polygon_slope']<=5, 1, 0) #areas with slope greater then 5 are removed
gdf_info['combine'] = gdf_info['large_enough'] + gdf_info['change_enough'] + gdf_info['slope_enough']
gdf_info_filter = gdf_info[gdf_info['combine']==3]
gdf_info

gdf = gpd.GeoDataFrame(gdf_info, geometry='geometry', crs="EPSG:4326")
gdf2 = gpd.GeoDataFrame(gdf_info_filter, geometry='geometry', crs="EPSG:4326")

gdf.to_file('final_flood_extent/mean_change_fuzzy_logic_aoi1_16db.shp')
gdf2.to_file('final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_16db.shp')


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