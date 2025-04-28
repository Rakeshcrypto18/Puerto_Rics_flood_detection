"""
The process API script collects both VH and VV values for the area of interest
the values returned in each band are the decible values
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
connecto to sentinel 1 processing API and create configuration
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
eval script below defines that the VV and VH values will be pulled
when the tiff is downloaded the VH values will be in band 1 and the VV values in band 2
"""

evalscriptVHVV_decible = """
//VERSION=3
function setup() {
  return {
    input: [{
      bands: ["VV", "VH", "dataMask"]
    }],
    output: {
      bands: 3, 
      sampleType: "FLOAT32" 
    }
  }
}
function evaluatePixel(samples){
   let decibelsvh = [10 * Math.log(samples.VH) / Math.LN10]
   let decibelsvv = [10 * Math.log(samples.VV) / Math.LN10]
   return [decibelsvh, decibelsvv, samples.dataMask]
}

"""

"""
send request
need to identify a box and grab coordinates for the box of data being pulled as well as the size
"""

# change coordinates by grid request
# copy and pase from excel sheet be sure to include commas between values

#this is changing depending on grid being pulled 
bbox1 = BBox(bbox=[-66.4386081, 18.46376767,	-66.3886081,	18.41876767], crs=CRS.WGS84)
bbox2 = BBox(bbox=[-66.3886081,	18.46376767,	-66.3386081,	18.41876767], crs=CRS.WGS84)
bbox3 = BBox(bbox=[-66.3386081,	18.46376767,	-66.2886081,	18.41876767], crs=CRS.WGS84)
bbox4 = BBox(bbox=[-66.2886081,	18.46376767,	-66.2386081,	18.41876767], crs=CRS.WGS84)
bbox5 = BBox(bbox=[-66.2386081,	18.46376767,	-66.1886081,	18.41876767], crs=CRS.WGS84)

bbox6 = BBox(bbox=[-66.71300914, 18.50403898,	-66.66300914,	18.45903898], crs=CRS.WGS84)
bbox7 = BBox(bbox=[-66.66300914, 18.50403898, -66.61300914, 18.45903898], crs=CRS.WGS84)


#sizes currently getting this from process builder but need to automate i think above commented out code is a way to do this
size1 = [528.0843937854222, 500.93770856969985]
size2 = [528.0843937852881, 500.93770856969985]
size3 = [528.0843937852881, 500.93770856969985]
size4 = [528.0843937854222, 500.93770856969985]
size5 = [528.0843937852881, 500.93770856969985]

size6 = [527.9606554502335, 500.9377085697706]
size7 = [527.9606554502335, 500.9377085697706]


#naming convention new
#postflood1_01
#post or preflood followed by image number 1,2,3 and cell number

"""
identify time frames of when to pull image data
"""
#current image timeframes per image number 1,2,3
preflood1 = ('2017-09-01', '2017-09-06')
preflood2 = ('2017-09-06', '2017-09-12')
preflood3 = ('2017-09-13', '2017-09-16')

postflood1 = ('2017-09-20', '2017-09-24')
postflood2 = ('2017-09-25', '2017-09-28')

"""
send request, to send request ensure that all inputs are set noted with "MODIFY ME"
"""
#request
request = SentinelHubRequest(
    data_folder="preflood3_07", #this is changing every pull <---- MODIFY ME  
    evalscript=evalscriptVHVV_decible,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL1_IW.define_from(
                    "s1iw", service_url=config.sh_base_url
                ),          
            time_interval=preflood3, #this is changing depending on image pulled  <---- MODIFY ME       
            other_args={"dataFilter": {"mosaickingOrder": "mostRecent"},"processing": {"backCoeff": "GAMMA0_TERRAIN","orthorectify": True,"demInstance": "COPERNICUS","speckleFilter": {"type": "LEE","windowSizeX": 3,"windowSizeY": 3}}}
        ),
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
    ],
    bbox=bbox7, #changing depending on cell <---- MODIFY ME 
    size=size7, #changing depending on cell <---- MODIFY ME 
    config=config
)
"""
save geotiff to folder
"""
# save data to a tiff
layer = request.get_data(save_data=True)
for folder, _, filenames in os.walk(request.data_folder):
    for filename in filenames:
        print(os.path.join(folder, filename))
layer
#another way to see data pulled
request.get_data()



