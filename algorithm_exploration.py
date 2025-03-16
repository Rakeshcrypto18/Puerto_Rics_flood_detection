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

df = pd.read_csv('01_05_decible_vh.csv')
df

df['change']= df['postflood_vh']-df['preflood_vh']
df

#decrease in vh
df_decrease = df[df['change']<0]
df_decrease

#filter for values that are less than 20 pre flood
df_low_preflood = df_decrease[df_decrease['preflood_vh'] >= -20]
df_low_preflood

#filter for post flood vlaues that are now less than 20
df_low_postflood = df_low_preflood[df_low_preflood['postflood_vh'] <= -20]
df_low_postflood

df_low_postflood.to_csv('change_test2.csv')


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

gdf.to_file('test_file.shp')














