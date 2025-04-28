"""
The DEM process API script collects DEM values for the area of interest which can bes used to calculate slope
"""

"""
first install necessary imports
may need to run a pip install on machine or create virtual environment
"""
import datetime
import os
import getpass

import matplotlib.pyplot as plt
import numpy as np

from sentinelhub import (
    SHConfig,
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions
)

"""
connect to to sentinel 1 processing API and create configuration
need client ID and client secret from copernicus dashboard to connect
"""

from sentinelhub import SHConfig


config = SHConfig()
config.sh_client_id = '<client id>' # key is given to user by copernicus
config.sh_client_secret = '<client secret>' # key is given to user by copernicus
config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
config.save("cdse")

config = SHConfig("cdse")


"""
This eval script is specific for DEM values
"""
evalscriptdem = """
//VERSION=3

function setup() {
  return {
    input: [
      {
        bands: ["DEM","dataMask"],                  
      }
    ],
    output: [
      {
        id: "default",
        bands: 2,
        sampleType: "FLOAT32",        
      },    
    ],
    mosaicking: "SIMPLE",
  };
}

function evaluatePixel(sample) {
  return [sample.DEM]
}

"""

#this is changing depending on grid being pulled
bbox1 = BBox(bbox=[-66.4386081, 18.46376767,	-66.3886081,	18.41876767], crs=CRS.WGS84)
bbox2 = BBox(bbox=[-66.3886081,	18.46376767,	-66.3386081,	18.41876767], crs=CRS.WGS84)
bbox3 = BBox(bbox=[-66.3386081,	18.46376767,	-66.2886081,	18.41876767], crs=CRS.WGS84)
bbox4 = BBox(bbox=[-66.2886081,	18.46376767,	-66.2386081,	18.41876767], crs=CRS.WGS84)
bbox5 = BBox(bbox=[-66.2386081,	18.46376767,	-66.1886081,	18.41876767], crs=CRS.WGS84)


bbox6 = BBox(bbox=[-66.71300914,	18.50403898,	-66.66300914,	18.45903898], crs=CRS.WGS84)
bbox7 = BBox(bbox=[-66.71300914,	18.45903898,	-66.66300914,	18.41403898], crs=CRS.WGS84)
bbox8 = BBox(bbox=[-66.71300914,	18.41403898,	-66.66300914,	18.36903898], crs=CRS.WGS84)
bbox9 = BBox(bbox=[-66.66300914,	18.50403898,	-66.61300914,	18.45903898], crs=CRS.WGS84)
bbox10 = BBox(bbox=[-66.66300914,	18.45903898,	-66.61300914,	18.41403898], crs=CRS.WGS84)
bbox11 = BBox(bbox=[-66.66300914,	18.41403898,	-66.61300914,	18.36903898], crs=CRS.WGS84)
bbox12 = BBox(bbox=[-66.61300914,	18.50403898,	-66.56300914,	18.45903898], crs=CRS.WGS84)
bbox13 = BBox(bbox=[-66.61300914,	18.45903898,	-66.56300914,	18.41403898], crs=CRS.WGS84)
bbox14 = BBox(bbox=[-66.61300914,	18.41403898,	-66.56300914,	18.36903898], crs=CRS.WGS84)
bbox15 = BBox(bbox=[-66.56300914,	18.50403898,	-66.51300914,	18.45903898], crs=CRS.WGS84)


size1 = [528.0843937854222, 500.93770856969985]
size2 = [528.0843937852881, 500.93770856969985]
size3 = [528.0843937852881, 500.93770856969985]
size4 = [528.0843937854222, 500.93770856969985]
size5 = [528.0843937852881, 500.93770856969985]

size6 = [527.9606554502335, 500.9377085697706]
size7 = [528.0989061273101, 500.93770856969985]
size8 = [528.2368310464356, 500.9377085697706]
size9 = [527.9606554502335, 500.9377085697706]
size10 = [528.0989061273101, 500.93770856969985]
size11 = [528.2368310464356, 500.9377085697706]
size12 = [527.9606554502335, 500.9377085697706]
size13 = [528.0989061273101, 500.93770856969985]
size14 = [528.2368310464356, 500.9377085697706]
size15 = [527.9606554503678, 500.9377085697706]

"""
The below request pulls the DEM values for the specified area of interest and will save the TIFF and jason file
to the folder name assigned by the user
"""

request = SentinelHubRequest(
    data_folder="dem_15", #folder name
    evalscript=evalscriptdem,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.DEM.define_from(
                    "dem", service_url=config.sh_base_url
                ),          
            time_interval=('2017-09-20', '2017-09-28'), #define time of data pull         
            other_args={"dataFilter": {"demInstance": "COPERNICUS_30"},"processing": {"upsampling": "NEAREST","downsampling": "NEAREST"}}
        ),
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
    ],
    bbox=bbox15,
    size=size15,
    config=config
)

"""
save geotiff to folder
"""

#%%time
layer = request.get_data(save_data=True)
for folder, _, filenames in os.walk(request.data_folder):
    for filename in filenames:
        print(os.path.join(folder, filename))

layer


