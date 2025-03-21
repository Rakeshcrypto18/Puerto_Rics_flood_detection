# Hydrowatchers_Repository
Repository for Hydrowatchers DAEN 690 Term Project

First need to pick location of interest and identify boundaries for "cells" or shape to load in API data
- for our first iteration, cells 1-30, we created a grid on QGIS 
- need to ensure each area of interest, or cell, is small enough to allow image download resolution to be 10m per pixel
- we can go back and look at the dimensions of our old grid as well to help with this

After boundaries for cells or areas of interest are defined, we use the process_api_connection.py script to pull down data
- ensure credentials are valid
- pull 3 pre flood images and 2 post flood images 
- the current process will pull both VH and VV (VH in band 0 and VV in band 1)
- NOTE these tiffs are not optimized for visual use since we dont have RGB bands only used for data (ie it wont create the black and white images we've been using)
- see more notes in the python script for usage
- this will create all tiffs for analysis in different folders that currently need to be manually renamed and moved to appropriate folders

Currently all tiffs are in the NDFI_NDVFI_tiffs folder with the naming convention pre/postfloodimagenumber_cellnumber (ex: postflood1_01.tiff) where the 1 after postflood indicates it is the first pre flood image and 01 represents the cell.

After all tiffs have been downloaded we use the geotiff_to_csv.py script to generate a csv of all points, their coordinates, and he corresponding VH/VV value. band [0] will grab the VH values and band [1] will grab the VV values. see more notation in the geotiff_to_csv.py for detailed info.
The script currently creates a csv per cell. the csvs are located in the geotiff_csvs folder and are labeled by cell and value they contain (either vh or vv)

algorithm_exploration.py
Current script exploring NDFI, NDVFI, and mean chnage detection. This script reads in csv files of the geotiffs creates mean, min, and max columns for vh/vv values for both post and preflood. using these columns we can calculate NDFI, NDVFI, and mean change. More details in script.

After calculateing the NDFI, NDVFI, and mean change there may be some filtering steps depending on the method being used. Currently no extra filtering for NDFI or NDVFI because not sure what threshold should be. Extra filtering applied to men change and described deeper in script.

After creating the mean chnage and filtering for "flooded areas" there is code to create a shape file. We can map this shape file to QGIS to get current flood extent.

For further fuzzy logic, we use a loop to assign points to each flood extent polygon. We do this to get the values of the points within the flooded polygon. EX. polygon 1 contains points 1,2,3,4,5 and these are the decible values we have/change values we have for those points. 

Current cell 1-5 polygon and point values are in floodpoints_and_polygons.csv

Now grouping by polygon id we can get means for specific values like postflood vh and change by polygon and eliminate if the polygon does not meet specific thresholds form our fuzzy logic

EXLPORING:
we also have DEM tiffs to explore using slope as a filter for fuzzy logic. the tiffs for dem values are in the dem_tifs folder and were pulled using the copernicus API. (dem_process_API.py currently in allisons branch will move later). code to change the dem values to slope currently being explored will be placed in dem_to_sple.py. we can later add these slope vlaues to our floodpoints_and_polygons.csv by joining on latitude and longitude
