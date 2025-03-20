""""
Import all necessary packages
"""
import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 
import pandas as pd

""""
load in csv data
"""
df1 = pd.read_csv('mean_change_NDFI/vh_NDFI_calc_01.csv')
df2 = pd.read_csv('mean_change_NDFI/vh_NDFI_calc_02.csv')
df3 = pd.read_csv('mean_change_NDFI/vh_NDFI_calc_03.csv')
df4 = pd.read_csv('mean_change_NDFI/vh_NDFI_calc_04.csv')
df5 = pd.read_csv('mean_change_NDFI/vh_NDFI_calc_05.csv')

df = pd.concat([df1, df2, df3, df4, df5])
df


df.columns.values

df['mean_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].mean(axis=1)
df['mean_post'] = df[['postflood_vh1', 'postflood_vh2']].mean(axis=1)
df['min_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].min(axis=1)
df['min_post'] = df[['postflood_vh1', 'postflood_vh2']].min(axis=1)
df['max_pre'] = df[['preflood_vh1', 'preflood_vh2', 'preflood_vh3']].max(axis=1)
df['max_post'] = df[['postflood_vh1', 'postflood_vh2']].max(axis=1)

df


df['NDFI'] = (df['mean_pre']-(df['min_post']+df['min_pre']))/(df['mean_pre']+(df['min_post']+df['min_pre']))
df['NDFVI'] = ((df['max_post']+df['max_pre'])-df['mean_pre'])/((df['max_post']+df['max_pre'])+df['mean_pre'])

df2 = df[['x','y',"NDFI", "NDFVI"]]
df2

#save df to inspect
df2.to_csv('NDFI_NDFVI_values_vh.csv')


#last method we used with mean values
df['change'] = df['mean_post'] - df['mean_pre']
df

#decrease in vh
df_decrease = df[df['change']<0]
df_decrease

#filter for values that are less than 20 pre flood
df_low_preflood = df_decrease[df_decrease['mean_pre'] >= -20]
df_low_preflood

#filter for post flood vlaues that are now less than 20
df_low_postflood = df_low_preflood[df_low_preflood['mean_post'] <= -20]
df_low_postflood

df_change = df_low_postflood[['x','y',"change"]]
df_change

df_change.to_csv('change_mean_vh_20db.csv')

""""
code below changes neighboring points to a shape file
"""

import geopandas as gpd


gdf = gpd.GeoDataFrame(
    df_low_postflood, geometry=gpd.points_from_xy(df_low_postflood.x, df_low_postflood.y), crs="EPSG:4326"
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

gdf.to_file('mean_change.shp')

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





""""
code below changes neighboring points to a shape file for NDFI
"""

import geopandas as gpd

df2
threshold = df2[df2['NDFI']<=-0.40]
threshold

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

gdf.to_file('NDFI_test3.shp')



"""
chnage detection old
"""
# df = pd.read_csv('01_05_decible_vh.csv')
# df

# df['change']= df['postflood_vh']-df['preflood_vh']
# df

# #decrease in vh
# df_decrease = df[df['change']<0]
# df_decrease

# #filter for values that are less than 20 pre flood
# df_low_preflood = df_decrease[df_decrease['preflood_vh'] >= -20]
# df_low_preflood

# #filter for post flood vlaues that are now less than 20
# df_low_postflood = df_low_preflood[df_low_preflood['postflood_vh'] <= -20]
# df_low_postflood

# df_low_postflood.to_csv('change_test2.csv')










