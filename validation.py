"""
imports
"""

import geopandas as gpd
import pandas as pd
import numpy as np

"""
load shapes
"""
#aerial shape boundary
aerial1 =  gpd.read_file("testing_shapes/test_area_1.shp")
aerial1
#aerial flood extent
aerial_flood = gpd.read_file("testing_shapes/aoi1_final_test_flood.shp")
aerial_flood = aerial_flood.explode()
aerial_flood
aerial_flood = aerial_flood.to_crs("EPSG:3857")


aerial_flood["area"] = aerial_flood['geometry'].area
aerial_flood = aerial_flood[aerial_flood['area']>=8093.71]

#aerial_flood.to_file('flood_1acre_test.shp')

#our flood extent
flood16 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_16db.shp")
flood16 = flood16.to_crs("EPSG:3857")
flood18 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_18db.shp")
flood18 = flood18.to_crs("EPSG:3857")
flood20 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_20db.shp")
flood20 = flood20.to_crs("EPSG:3857")


"""
percent overlap
"""

intersection16 = gpd.overlay(aerial_flood, flood16, how='intersection')
intersection18 = gpd.overlay(aerial_flood, flood18, how='intersection')
intersection20 = gpd.overlay(aerial_flood, flood20, how='intersection')

# Calculate the area of the intersection
intersection_area16 = intersection16.geometry.area.sum()
intersection_area18 = intersection18.geometry.area.sum()
intersection_area20 = intersection20.geometry.area.sum()

# Calculate the area of the target polygon (polygon_a)
test_area = aerial_flood.geometry.area.sum()
test_area

pct_16 = (intersection_area16 / test_area) * 100
pct_18 = (intersection_area18 / test_area) * 100
pct_20 = (intersection_area20 / test_area) * 100

pct_16
pct_18
pct_20

"""
calculate area of our flood extent
"""
flood_area16 = flood16.geometry.area.sum()
flood_area18 = flood18.geometry.area.sum()
flood_area20 = flood20.geometry.area.sum()

flood_area16 #covers 62% of 6648736.131199692
flood_area18 #covers 56% of 6648736.131199692
flood_area20 #covers 37% of 6648736.131199692 

"""
extra remaining flood false negatives?
"""
error16 = ((flood_area16-intersection_area16)/(flood_area16))*100
error18 = ((flood_area18-intersection_area18)/(flood_area18))*100
error20 = ((flood_area20-intersection_area20)/(flood_area20))*100

error16 #29%
error18 #31%
error20 #40%

"""
test area 2
"""

"""
load shapes
"""
#aerial shape boundary
aerial2 =  gpd.read_file("testing_shapes/test_area_2.shp")
aerial2
aerial2 = aerial2.to_crs("EPSG:3857")
#aerial flood extent
aerial_flood = gpd.read_file("testing_shapes/aoi2_final_test_flood.shp")
aerial_flood = aerial_flood.to_crs("EPSG:3857")

aerial_flood["area"] = aerial_flood['geometry'].area
aerial_flood = aerial_flood[aerial_flood['area']>=8093.71]
#aerial_flood.to_file('flood_1acre_test2.shp')

#our flood extent
flood16 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_16db.shp")
flood16 = flood16.to_crs("EPSG:3857")
flood18 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_18db.shp")
flood18 = flood18.to_crs("EPSG:3857")
flood20 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_20db.shp")
flood20 = flood20.to_crs("EPSG:3857")


"""
Only use flood polygons that are in the same area we have aerial photos
"""
flood16 = gpd.sjoin(flood16, aerial2[['geometry']], how='left')
flood16 = flood16.dropna()

flood18 = gpd.sjoin(flood18, aerial2[['geometry']], how='left')
flood18 = flood18.dropna()

flood20 = gpd.sjoin(flood20, aerial2[['geometry']], how='left')
flood20 = flood20.dropna()

"""
percent overlap
"""
intersection16 = gpd.overlay(aerial_flood, flood16, how='intersection')
intersection18 = gpd.overlay(aerial_flood, flood18, how='intersection')
intersection20 = gpd.overlay(aerial_flood, flood20, how='intersection')

# Calculate the area of the intersection
intersection_area16 = intersection16.geometry.area.sum()
intersection_area18 = intersection18.geometry.area.sum()
intersection_area20 = intersection20.geometry.area.sum()

# Calculate the area of the target polygon (polygon_a)
test_area = aerial_flood.geometry.area.sum()
test_area

pct_16 = (intersection_area16 / test_area) * 100
pct_18 = (intersection_area18 / test_area) * 100
pct_20 = (intersection_area20 / test_area) * 100

pct_16
pct_18
pct_20

"""
calculate area of our flood extent
"""
flood_area16 = flood16.geometry.area.sum()
flood_area18 = flood18.geometry.area.sum()
flood_area20 = flood20.geometry.area.sum()

flood_area16 #covers 71% of 2013462.7799295655
flood_area18 #covers 55% of 2013462.7799295655 
flood_area20 #covers 33% of 2013462.7799295655

"""
extra remaining flood false negatives?
"""
error16 = ((flood_area16-intersection_area16)/(flood_area16))*100
error18 = ((flood_area18-intersection_area18)/(flood_area18))*100
error20 = ((flood_area20-intersection_area20)/(flood_area20))*100

error16 #75%
error18 #79%
error20 #84%


"""
GFM test with both shapes
"""

"""
load shapes
"""
gfm = gpd.read_file("testing_shapes/GFM_data/flood_polygons.shp")
gfm = gfm.to_crs("EPSG:3857")

gfm["area"] = gfm['geometry'].area
gfm = gfm[gfm['area']>=8093.71]
gfm

#our flood extent
flood16_1 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_16db.shp")
flood16_1 = flood16_1.to_crs("EPSG:3857")
flood18_1 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_18db.shp")
flood18_1 = flood18_1.to_crs("EPSG:3857")
flood20_1 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi1_20db.shp")
flood20_1 = flood20_1.to_crs("EPSG:3857")
flood16_2 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_16db.shp")
flood16_2 = flood16_2.to_crs("EPSG:3857")
flood18_2 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_18db.shp")
flood18_2 = flood18_2.to_crs("EPSG:3857")
flood20_2 = gpd.read_file("final_flood_extent/filtered_mean_change_on_fuzzy_logic_aoi2_20db.shp")
flood20_2 = flood20_2.to_crs("EPSG:3857")

flood16 = pd.concat([flood16_1, flood16_2])
flood18 = pd.concat([flood18_1, flood18_2])
flood20 = pd.concat([flood20_1, flood20_2])


"""
percent overlap
"""
intersection16 = gpd.overlay(gfm, flood16, how='intersection')
intersection18 = gpd.overlay(gfm, flood18, how='intersection')
intersection20 = gpd.overlay(gfm, flood20, how='intersection')

# Calculate the area of the intersection
intersection_area16 = intersection16.geometry.area.sum()
intersection_area18 = intersection18.geometry.area.sum()
intersection_area20 = intersection20.geometry.area.sum()

# Calculate the area of the target polygon (polygon_a)
test_area = gfm.geometry.area.sum()
test_area

pct_16 = (intersection_area16 / test_area) * 100
pct_18 = (intersection_area18 / test_area) * 100
pct_20 = (intersection_area20 / test_area) * 100

pct_16
pct_18
pct_20

"""
calculate area of our flood extent
"""
flood_area16 = flood16.geometry.area.sum()
flood_area18 = flood18.geometry.area.sum()
flood_area20 = flood20.geometry.area.sum()

flood_area16 #covers 30% of 7661540.297199166
flood_area18 #covers 40% of 7661540.297199166 
flood_area20 #covers 41% of 7661540.297199166

"""
extra remaining flood false negatives?
"""
error16 = ((flood_area16-intersection_area16)/(flood_area16))*100
error18 = ((flood_area18-intersection_area18)/(flood_area18))*100
error20 = ((flood_area20-intersection_area20)/(flood_area20))*100

error16 #82%
error18 #68%
error20 #53%

"""
overlap of our aerial images to GFM model
"""
gfm = gpd.read_file("testing_shapes/GFM_data/flood_polygons.shp")
gfm = gfm.to_crs("EPSG:3857")

gfm["area"] = gfm['geometry'].area
gfm = gfm[gfm['area']>=8093.71]

#aerial flood extent 1
aerial_flood1 = gpd.read_file("testing_shapes/aoi1_final_test_flood.shp")
aerial_flood1 = aerial_flood1.to_crs("EPSG:3857")

aerial_flood1["area"] = aerial_flood1['geometry'].area
aerial_flood1 = aerial_flood1[aerial_flood1['area']>=8093.71]

#aerial flood extent 2
aerial_flood2 = gpd.read_file("testing_shapes/aoi2_final_test_flood.shp")
aerial_flood2 = aerial_flood2.to_crs("EPSG:3857")

aerial_flood2["area"] = aerial_flood2['geometry'].area
aerial_flood2 = aerial_flood2[aerial_flood2['area']>=8093.71]

aerial_flood = pd.concat([aerial_flood1, aerial_flood2])

merged_flood_area = gpd.read_file("testing_shapes/merged_flood_area.shp")
merged_flood_area = merged_flood_area.explode()
merged_flood_area = merged_flood_area.to_crs("EPSG:3857")

merged_flood_area["area"] = merged_flood_area['geometry'].area
merged_flood_area = merged_flood_area[merged_flood_area['area']>=8093.71]

"""
percent overlap
"""
intersection_floods = gpd.overlay(gfm, aerial_flood, how='intersection')

# Calculate the area of the intersection
intersection_area_flood = intersection_floods.geometry.area.sum()
intersection_area_flood
# Calculate the area of the target polygon (polygon_a)
test_area = merged_flood_area.geometry.area.sum()
test_area

gfm_area = gfm.geometry.area.sum()
gfm_area

aerial_flood_area = aerial_flood.geometry.area.sum()
aerial_flood_area

pct_flood = (intersection_area_flood / test_area) * 100
pct_flood #14%


#percent overap / total area

