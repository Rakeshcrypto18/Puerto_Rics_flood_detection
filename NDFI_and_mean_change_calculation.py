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
df1 = pd.read_csv('geotiff_csvs/vh_01.csv')
df2 = pd.read_csv('geotiff_csvs/vh_02.csv')
df3 = pd.read_csv('geotiff_csvs/vh_03.csv')
df4 = pd.read_csv('geotiff_csvs/vh_04.csv')
df5 = pd.read_csv('geotiff_csvs/vh_05.csv')

df1 = pd.read_csv('geotiff_csvs/vv_01.csv')
df2 = pd.read_csv('geotiff_csvs/vv_02.csv')
df3 = pd.read_csv('geotiff_csvs/vv_03.csv')
df4 = pd.read_csv('geotiff_csvs/vv_04.csv')
df5 = pd.read_csv('geotiff_csvs/vv_05.csv')

""""
concat all csv data into one csv to analyse
"""
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

df['mean_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].mean(axis=1)
df['mean_post'] = df[['postflood_vv1', 'postflood_vv2']].mean(axis=1)
df['min_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].min(axis=1)
df['min_post'] = df[['postflood_vv1', 'postflood_vv2']].min(axis=1)
df['max_pre'] = df[['preflood_vv1', 'preflood_vv2', 'preflood_vv3']].max(axis=1)
df['max_post'] = df[['postflood_vv1', 'postflood_vv2']].max(axis=1)

""""
calculate mean change
"""

df['change'] = df['mean_post'] - df['mean_pre']
df

""""
calculate NDFI and NDVFI using values we just created
*** not sure if NDVFI is working
"""
df['NDFI'] = (df['mean_pre']-(df['min_post']+df['min_pre']))/(df['mean_pre']+(df['min_post']+df['min_pre']))
df['NDFVI'] = ((df['max_post']+df['max_pre'])-df['mean_pre'])/((df['max_post']+df['max_pre'])+df['mean_pre'])

#svae to csv?
#saving for VV exploration
#df.to_csv('vv_explore.csv')

""""
NDFI and NDVFI thresholding and shape file creation
"""
df_NDFI_NDVFI = df#[['x','y',"NDFI", "NDFVI"]]
df_NDFI_NDVFI

threshold = df_NDFI_NDVFI[df_NDFI_NDVFI['NDFI']<=-0.40]
threshold


threshold = threshold[threshold['mean_pre'] >= -18]
threshold

#save df to inspect
threshold.to_csv('NDFI_NDFVI_values_vh.csv')

""""
code below changes neighboring points to a shape file for NDFI
"""

gdf = gpd.GeoDataFrame(
    threshold, geometry=gpd.points_from_xy(threshold.x, threshold.y), crs="EPSG:4326"
)
gdf

gdf = gdf.to_crs(epsg=3857)
gdf

buffer_distance = 11
gdf['buffer_polygon'] = gdf.geometry.buffer(buffer_distance, cap_style=3)
gdf

gdf = gdf.reset_index()
gdf.rename(columns={'index': 'id'}, inplace=True)

gdf= gdf.rename(columns ={'geometry':'point'})
gdf=gdf.rename(columns ={'buffer_polygon':'geometry'})
gdf

#testing merge
single_multi_polygon = gdf.unary_union

single_multi_polygon

from shapely.geometry import MultiPolygon

gdf = gpd.GeoDataFrame(geometry=[single_multi_polygon], crs="EPSG:3857")
gdf

gdf = gdf.explode()
gdf = gdf.to_crs(epsg=4326)
gdf

gdf.to_file('NDFI_filter_40.shp')

""""
asssign points to thier polygon
"""

gdf2 = gdf.reset_index(drop=True)
gdf2 = gdf2.reset_index()
gdf2

#for each point in df check if it is in the listed polygon if yes, add the polygon index
#to a column in df
df_NDFI_points = gpd.GeoDataFrame(
    threshold, geometry=gpd.points_from_xy(threshold.x, threshold.y), crs="EPSG:4326"
)

# pick first polygon, filter df_change_points for only points within that polygon, assign those points polygon as the index number
df_NDFI_points['polygon_id'] = ''


for index, row in gdf2.iterrows():
    polygon = row['geometry']
    polygon_id = row['index']
    gdf_filtered = df_NDFI_points[df_NDFI_points['geometry'].within(polygon)]
    for i, r in gdf_filtered.iterrows():
        #if point in df chnage points is in gdf filtered then add polygon id
        point = r['geometry']
        pip = point.within(polygon) 
        if pip == True:
            df_NDFI_points.at[i,'polygon_id']=polygon_id

df_NDFI_points

#left merge 
join= pd.merge(df_NDFI_points, gdf2, left_on='polygon_id', right_on='index', how='left')
join


join.to_csv('floodpoints_and_polygons_NDFI.csv')



""""
Classic chnage detection using mean vh values
postflood-preflood

returns change value, if change is less than 0 then the VH value decreased, the more negative, 
the greater the change
"""
#last method we used with mean values
df['change'] = df['mean_post'] - df['mean_pre']
df

#filter to only have data points that have decreased vh values
df_decrease = df[df['change']<0]
df_decrease

# filter for values that are less than 20 pre flood
# we can change this value depending on threshold
# this removes values that have a negative change but we already previously classified as water, only want values not classified as a flood in pree flood
# keep in mind this is a flitering step
df_low_preflood = df_decrease[df_decrease['mean_pre'] >= -20]
df_low_preflood


# filter for post flood vlaues that are now less than 20
# we can change this value depending on threshold
# this removes values that have a negative change but still have vh values above -20
df_low_postflood = df_low_preflood[df_low_preflood['mean_post'] <= -20]
df_low_postflood

""""
Save mean change values to a csv
"""

df_change = df_low_postflood#[['x','y',"change"]]
df_change

df_change.to_csv('change_mean_vh_20db.csv')

""""
SHAPE FILE CREATION
"""


gdf = gpd.GeoDataFrame(
    df_low_postflood, geometry=gpd.points_from_xy(df_low_postflood.x, df_low_postflood.y), crs="EPSG:4326"
)
gdf

#chnage crs so we can buffer in meters
gdf = gdf.to_crs(epsg=3857)
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
gdf.to_file('mean_change.shp')


""""
asssign points to thier polygon
"""

gdf2 = gdf.reset_index(drop=True)
gdf2 = gdf2.reset_index()
gdf2

#for each point in df check if it is in the listed polygon if yes, add the polygon index
#to a column in df
df_change_points = gpd.GeoDataFrame(
    df_low_postflood, geometry=gpd.points_from_xy(df_low_postflood.x, df_low_postflood.y), crs="EPSG:4326"
)

# pick first polygon, filter df_change_points for only points within that polygon, assign those points polygon as the index number
df_change_points['polygon_id'] = ''

for index, row in gdf2.iterrows():
    polygon = row['geometry']
    polygon_id = row['index']
    gdf_filtered = df_change_points[df_change_points['geometry'].within(polygon)]
    for i, r in gdf_filtered.iterrows():
        #if point in df chnage points is in gdf filtered then add polygon id
        point = r['geometry']
        pip = point.within(polygon) 
        if pip == True:
            df_change_points.at[i,'polygon_id']=polygon_id

df_change_points

#left merge 
join= pd.merge(df_change_points, gdf2, left_on='polygon_id', right_on='index', how='left')
join


df_change_points.to_csv('floodpoints_and_polygons_mean_change.csv')





















