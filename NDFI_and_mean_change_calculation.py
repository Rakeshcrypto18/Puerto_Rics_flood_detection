""""
this notebook reads all geotif csv information and first calculates necessary inputs such as the mean dB values pre
and post flood, NDFI, and mean change. Once values have been claulated we filter the data based on threshold values.
after the data filter, for each method either NDFI or mean change, we creat a "base" flood extent shape file with no further
filtering and save the shape, after the shape and flood polygons are created we merge all existing point data with the 
created shape file in a csv. This resulting csv will have eaach point information including what polygon it belongs to 
and pre and post cell values. this csv is then used in the fuzzy logic python script for refining the flood model.
"""

""""
Import all necessary packages
"""
import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 
import pandas as pd
import geopandas as gpd

""""
load in csv data
"""
# df1 = pd.read_csv('geotiff_csvs/vh_06.csv')
# df2 = pd.read_csv('geotiff_csvs/vh_07.csv')
# df3 = pd.read_csv('geotiff_csvs/vh_08.csv')
# df4 = pd.read_csv('geotiff_csvs/vh_09.csv')
# df5 = pd.read_csv('geotiff_csvs/vh_10.csv')
# df6 = pd.read_csv('geotiff_csvs/vh_11.csv')
# df7 = pd.read_csv('geotiff_csvs/vh_12.csv')
# df8 = pd.read_csv('geotiff_csvs/vh_13.csv')
# df9 = pd.read_csv('geotiff_csvs/vh_14.csv')
# df10 = pd.read_csv('geotiff_csvs/vh_15.csv')

df1 = pd.read_csv('geotiff_csvs/vh_01.csv')
df2 = pd.read_csv('geotiff_csvs/vh_02.csv')
df3 = pd.read_csv('geotiff_csvs/vh_03.csv')
df4 = pd.read_csv('geotiff_csvs/vh_04.csv')
df5 = pd.read_csv('geotiff_csvs/vh_05.csv')

# df1 = pd.read_csv('geotiff_csvs/vv_01.csv')
# df2 = pd.read_csv('geotiff_csvs/vv_02.csv')
# df3 = pd.read_csv('geotiff_csvs/vv_03.csv')
# df4 = pd.read_csv('geotiff_csvs/vv_04.csv')
# df5 = pd.read_csv('geotiff_csvs/vv_05.csv')

""""
concat all csv data into one csv to analyse
"""
#df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9,df10])

df = pd.concat([df1, df2, df3, df4, df5])
df


""""
create min, mean, and max values for preflood and post flood images

example: this will create a mean VH value for all preflood/postflood images we have 
"""

df['mean_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].mean(axis=1)
df['mean_post'] = df[['postflood_vh1', 'postflood_vh2']].mean(axis=1)
df['min_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].min(axis=1)
df['min_post'] = df[['postflood_vh1', 'postflood_vh2']].min(axis=1)
df['max_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].max(axis=1)
df['max_post'] = df[['postflood_vh1', 'postflood_vh2']].max(axis=1)

# df['mean_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].mean(axis=1)
# df['mean_post'] = df[['postflood_vv1', 'postflood_vv2']].mean(axis=1)
# df['min_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].min(axis=1)
# df['min_post'] = df[['postflood_vv1', 'postflood_vv2']].min(axis=1)
# df['max_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].max(axis=1)
# df['max_post'] = df[['postflood_vv1', 'postflood_vv2']].max(axis=1)

""""
calculate mean change
"""
df['change'] = df['min_post'] - df['mean_pre']
#df['change'] = df['mean_post'] - df['mean_pre']
df

"""
calculate NDFI if we want to use later
"""
df['DFI'] = df['min_post'] - df['mean_pre']
df['DFVI'] = df['max_post'] - df['mean_pre']
df

df['NDFI'] = (df['DFI'] - df['DFI'].min())/(df['DFI'].max()-df['DFI'].min())
df['NDFVI'] = (df['DFVI'] - df['DFVI'].min())/(df['DFVI'].max()-df['DFVI'].min())
df

""""
Classic chnage detection using mean vh values
postflood-preflood

returns change value, if change is less than 0 then the VH value decreased, the more negative, 
the greater the change
"""

#filter to only have data points that have decreased vh values
df_decrease = df[df['change']<0]
df_decrease

# df_decrease = df[df['DFI']<0]
# df_decrease

# filter for values that are less than 20 pre flood
# we can change this value depending on threshold
# this removes values that have a negative change but we already previously classified as water, only want values not classified as a flood in pre flood
# keep in mind this is a flitering step
df_low_preflood = df_decrease[df_decrease['mean_pre'] >= -16]
df_low_preflood




# filter for post flood vlaues that are now less than 20
# we can change this value depending on threshold
# this removes values that have a negative change but still have vh values above -20
df_low_postflood = df_low_preflood[df_low_preflood['mean_post'] <= -16]
df_low_postflood

# df_low_postflood = df_low_preflood[df_low_preflood['mean_post'] <= -20]
# df_low_postflood

""""
Save mean change values to a csv
"""

# df_change = df_low_postflood#[['x','y',"change"]]
# df_change

# df_low_preflood.to_csv('change_vh_20db_test2.csv')

""""
SHAPE FILE CREATION
"""


gdf = gpd.GeoDataFrame(
    df_low_postflood, geometry=gpd.points_from_xy(df_low_postflood.x, df_low_postflood.y), crs="EPSG:4326"
)
gdf


#filter points within puertorico boundary (this eliminated ocean water from the model)
# pr_map = gpd.read_file('puertoricoshape/pri_admbnda_adm0_2019.shp')
# pr_map

# pr_map = pr_map.explode()
# pr_map

# pr_map = pr_map.reset_index(drop=True)
# pr_map = pr_map.reset_index()
# pr_map

#pr_map.to_file('puertoricoshape/pr_map.shp')

pr_map = gpd.read_file('puertoricoshape/pr_map.shp')
pr_map_main = pr_map[pr_map['index']==58]
pr_map_main

polygon = pr_map_main.iloc[0].geometry
polygon

#gdf= gdf.rename(columns ={'geometry':'point'})

pip = gdf[gdf.geometry.within(polygon)]
pip


#chnage crs so we can buffer in meters
gdf = pip.to_crs(epsg=3857)
gdf

#create buffer so points will overlap
buffer_distance = 11
gdf['buffer_polygon'] = gdf.geometry.buffer(buffer_distance, cap_style=3)
gdf

gdf = gdf.reset_index()
gdf.rename(columns={'index': 'id'}, inplace=True)

gdf= gdf.rename(columns ={'geometry':'point'})
gdf=gdf.rename(columns ={'buffer_polygon':'geometry'})
gdf

""""
merge overlapping polygons
""" 
single_multi_polygon = gdf.unary_union

single_multi_polygon

from shapely.geometry import MultiPolygon

gdf = gpd.GeoDataFrame(geometry=[single_multi_polygon], crs="EPSG:3857")
gdf

gdf = gdf.explode()
gdf = gdf.to_crs(epsg=4326)
gdf

#save current flood extent as shape file before fuzzy logic
gdf.to_file('mean_change_16db.shp')


""""
asssign points to thier polygon
"""

gdf2 = gdf.reset_index(drop=True)
gdf2 = gdf2.reset_index()
gdf2

#for each point in df check if it is in the listed polygon if yes, add the polygon index
#to a column in df
# df_change_points = gpd.GeoDataFrame(
#     df_low_postflood, geometry=gpd.points_from_xy(df_low_postflood.x, df_low_postflood.y), crs="EPSG:4326"
# )

# pick first polygon, filter df_change_points for only points within that polygon, assign those points polygon as the index number
#df_change_points['polygon_id'] = ''
pip['polygon_id'] = ''
mean_change_gdf=pip
mean_change_gdf
for index, row in gdf2.iterrows():
    polygon = row['geometry']
    polygon_id = row['index']
    gdf_filtered = mean_change_gdf[mean_change_gdf['geometry'].within(polygon)]
    for i, r in gdf_filtered.iterrows():
        #if point in df chnage points is in gdf filtered then add polygon id
        point = r['geometry']
        pip = point.within(polygon) 
        if pip == True:
            mean_change_gdf.at[i,'polygon_id']=polygon_id

mean_change_gdf

#left merge 
join= pd.merge(mean_change_gdf, gdf2, left_on='polygon_id', right_on='index', how='left')
join


mean_change_gdf.to_csv('floodpoints_and_polygons_mean_change_aoi116db.csv')



#df_save[df_save["NDFI"]<=0.3]


""""
calculate NDFI and NDVFI using values we just created
*** not sure if NDVFI is working
"""
#old not working/not correct calculation
# df['NDFI'] = (df['mean_pre']-(df['min_post']+df['min_pre']))/(df['mean_pre']+(df['min_post']+df['min_pre']))
# df['NDFVI'] = ((df['max_post']+df['max_pre'])-df['mean_pre'])/((df['max_post']+df['max_pre'])+df['mean_pre'])

# values that became brighter reference flooded vegitation
# they use the mean reference image for "normal" values and then take the min or max of the post flood to get the largest 
# difference in the time series (most drastic change)
df['DFI'] = df['min_post'] - df['mean_pre']
df['DFVI'] = df['max_post'] - df['mean_pre']
df

df['NDFI'] = (df['DFI'] - df['DFI'].min())/(df['DFI'].max()-df['DFI'].min())
df['NDFVI'] = (df['DFVI'] - df['DFVI'].min())/(df['DFVI'].max()-df['DFVI'].min())
df



df
# #svae to csv?
# #saving for exploration
# df_save = df [['y', 'x','NDFI', 'DFI', 'NDFVI', 'DFVI', 'mean_post', 'mean_pre', 'change']]
# df_save 
# df_save.to_csv('df_NDF_NDFVI_explore.csv')

# """"
# NDFI and NDVFI thresholding and shape file creation
# """
# df_NDFI_NDVFI = df#[['x','y',"NDFI", "NDFVI"]]
# df_NDFI_NDVFI

# threshold = df_NDFI_NDVFI[df_NDFI_NDVFI['NDFI']<=-0.40]
# threshold


# threshold = threshold[threshold['mean_pre'] >= -18]
# threshold

# #save df to inspect
# threshold.to_csv('NDFI_NDFVI_values_vh.csv')

# """"
# code below changes neighboring points to a shape file for NDFI
# """

# gdf = gpd.GeoDataFrame(
#     threshold, geometry=gpd.points_from_xy(threshold.x, threshold.y), crs="EPSG:4326"
# )
# gdf

# gdf = gdf.to_crs(epsg=3857)
# gdf

# buffer_distance = 11
# gdf['buffer_polygon'] = gdf.geometry.buffer(buffer_distance, cap_style=3)
# gdf

# gdf = gdf.reset_index()
# gdf.rename(columns={'index': 'id'}, inplace=True)

# gdf= gdf.rename(columns ={'geometry':'point'})
# gdf=gdf.rename(columns ={'buffer_polygon':'geometry'})
# gdf

# #testing merge
# single_multi_polygon = gdf.unary_union

# single_multi_polygon

# from shapely.geometry import MultiPolygon

# gdf = gpd.GeoDataFrame(geometry=[single_multi_polygon], crs="EPSG:3857")
# gdf

# gdf = gdf.explode()
# gdf = gdf.to_crs(epsg=4326)
# gdf

# gdf.to_file('NDFI_filter_40.shp')

# """"
# asssign points to thier polygon
# """

# gdf2 = gdf.reset_index(drop=True)
# gdf2 = gdf2.reset_index()
# gdf2

# #for each point in df check if it is in the listed polygon if yes, add the polygon index
# #to a column in df
# df_NDFI_points = gpd.GeoDataFrame(
#     threshold, geometry=gpd.points_from_xy(threshold.x, threshold.y), crs="EPSG:4326"
# )

# # pick first polygon, filter df_change_points for only points within that polygon, assign those points polygon as the index number
# df_NDFI_points['polygon_id'] = ''


# for index, row in gdf2.iterrows():
#     polygon = row['geometry']
#     polygon_id = row['index']
#     gdf_filtered = df_NDFI_points[df_NDFI_points['geometry'].within(polygon)]
#     for i, r in gdf_filtered.iterrows():
#         #if point in df chnage points is in gdf filtered then add polygon id
#         point = r['geometry']
#         pip = point.within(polygon) 
#         if pip == True:
#             df_NDFI_points.at[i,'polygon_id']=polygon_id

# df_NDFI_points

# #left merge 
# join= pd.merge(df_NDFI_points, gdf2, left_on='polygon_id', right_on='index', how='left')
# join


# join.to_csv('floodpoints_and_polygons_NDFI.csv')















