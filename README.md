# Hydrowatchers_Repository
Repository for Hydrowatchers DAEN 690 Term Project

First need to pick location of interest and identify boundaries for "cells" or shape to load in API data
- for our first iteration, cells 1-5, we created a grid on QGIS 
- need to ensure each area of interest, or cell, is small enough to allow image download resolution to be 10m per pixel
- a guide for possible grid values and the corresponding boundary points can be found in the puertorico_grid excel sheet


After boundaries for cells or areas of interest are defined, we use the process_api_connection.py script and dem_process_api.py to pull the data. The process api file will pull the VV and VH values of the pixels in defined cells. The DEM process api file will pull the DEM vlaues for the specified cell to be used in slope calculation
- ensure copernicus credentials are valid
- pull 3 pre flood images and 2 post flood images 
- the current process will pull both VH and VV (VH in band 0 and VV in band 1)
- NOTE these tiffs are not optimized for visual use since we dont have RGB bands only used for data (ie it wont create the black and white images)
- this will create all tiffs for analysis in different folders that currently need to be manually renamed and moved to appropriate folders
- see more notes in the python script for usage


Currently all tiffs used in our analysis are in the geo_tiffs folder with the naming convention pre/postfloodimagenumber_cellnumber (ex: postflood1_01.tiff) where the 1 after postflood indicates it is the first pre flood image and 01 represents the cell.

After all tiffs have been downloaded we use the geotiff_to_csv.py script to generate a csv of all points, their coordinates, and he corresponding VH/VV value. band [0] will grab the VH values and band [1] will grab the VV values. see more notation in the geotiff_to_csv.py for detailed info.
The script currently creates a csv per cell. the csvs are located in the geotiff_csvs folder and are labeled by cell and value they contain (either vh or vv)

Similar to the VV/VH GeoTiffs, we aldo convert the slope GeoTiffs to csvs. After running the geotiff_to_csv.py for the dem tiffs, we use the slope.py file to calculate the slope values using the dem values in our csv. The resulting slope values are saved in a csv for later use.

The initial_flood_extent.py is 1 of the 2 key scripts used to run our model.
It first merges all csvs of the areas of interest together and calculates needed metrics such as mean change. After initial calculations the thresholding method is applied. Once the thresholding method is applied the only pixels remaining in the dataframe are pixels that might indicate possible flooding. We take these pixles and turn them into shape files where overlapping/neighboring points represent a flooded polygon. We can map this shape file to QGIS to get current flood extent.

To prepare for the locical conditioning,  we use a loop to assign points to each flood extent polygon. We do this to get the values of the points within the flooded polygon. EX. polygon 1 contains points 1,2,3,4,5 and these are the decible values we have/change values we have for those points. 

After we finish running the initial_flood_extent.py, we have all the needed information to refine out flood extent. We then move to the 2nd key script, flood_extent_filtering.py. We gather the information on our initial flood extent and for each polygon calculate the area, mean change, and mean slope. We then apply our conditional filtering where all three conditions (area greater or equal to 2 acres, mean chnage of at least -5dB, and mean slope value below 5 degrees) must be satisfied.

Finally we filter out polygons that do not satisfy the thre logical conditions and generate the final flood extent shape file to be mapped using any GIS software.
