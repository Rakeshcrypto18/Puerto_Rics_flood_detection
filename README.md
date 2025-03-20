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


