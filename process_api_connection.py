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
config.sh_client_id = '<client id>'
config.sh_client_secret = 'client secret id'
config.sh_base_url = 'https://sh.dataspace.copernicus.eu'
config.sh_token_url = 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token'
config.save("cdse")

config = SHConfig("cdse")

"""
define bounding box coordinates of interest
"""

# coords_wgs84 = (-66.07507,18.41733,-66.058282,18.428126)


resolution = 10
# pr_bbox = BBox(bbox=coords_wgs84, crs=CRS.WGS84)
# pr_size = bbox_to_dimensions(pr_bbox, resolution=resolution)

print(f"Image shape at {resolution} m resolution: {pr_size} pixels")

"""
create eval script to downolad and grab images of interest

current eval script is the VH decible 0 Gamma
"""

evalscript = """
//VERSION=3
function setup() {
  return {
    input: ["VH", "dataMask"],
    output: [
      { id: "default", bands: 4 },
      { id: "eobrowserStats", bands: 1 },
      { id: "dataMask", bands: 1 },
    ],
  };
}

function evaluatePixel(samples) {
  const value = Math.max(0, Math.log(samples.VH) * 0.21714724095 + 1);
  return {
    default: [value, value, samples.dataMask],
    eobrowserStats: [Math.max(-30, (10 * Math.log10(samples.VH)))],
    dataMask: [samples.dataMask],
  };
}
// ---
/*
// displays VH in decibels from -20 to 0
// the following is simplified below
// var log = 10 * Math.log(VH) / Math.LN10;
// var val = Math.max(0, (log + 20) / 20);

return [Math.max(0, Math.log(VH) * 0.21714724095 + 1)];
*/

"""

"""
send request
"""
bbox = BBox(bbox=[-7377043.971, 2092185.762, -7372043.971, 2087185.762], crs=CRS.POP_WEB)

request = SentinelHubRequest(
    data_folder="preflood_VV_01",
    evalscript=evalscript,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL1_IW.define_from(
                    "s1iw", service_url=config.sh_base_url
                ),          
            time_interval=('2017-09-01', '2017-09-16'),          
            other_args={"dataFilter": {"mosaickingOrder": "mostRecent"},"processing": {"orthorectify": True,"demInstance": "COPERNICUS","speckleFilter": {"type": "LEE","windowSizeX": 3,"windowSizeY": 3}}}
        ),
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.TIFF),
    ],
    bbox=bbox,
    size=[474.37555468171587, 474.3100863719954],
    config=config
)

request.get_data()

# request = SentinelHubRequest(
#     data_folder="test",
#     evalscript=evalscript,
#     input_data=[
#         SentinelHubRequest.input_data(
#             data_collection=DataCollection.SENTINEL1_IW.define_from(
#                     "s1iw", service_url=config.sh_base_url
#                 ),          
#             time_interval=('2017-09-01', '2017-09-16'),          
#             other_args={"dataFilter": {"mosaickingOrder": "mostRecent","resolution": "HIGH"},"processing": {"orthorectify": True,"demInstance": "COPERNICUS","speckleFilter": {"type": "LEE","windowSizeX": 3,"windowSizeY": 3}}}
#         ),
#     ],
#     responses=[
#         SentinelHubRequest.output_response('default', MimeType.TIFF),
#     ],
#     bbox=pr_bbox,
#     size=pr_size,
#     config=config
# )


#response = request.get_data()
"""
save geotiff to folder
"""

#%%time
vh_layer = request.get_data(save_data=True)
for folder, _, filenames in os.walk(request.data_folder):
    for filename in filenames:
        print(os.path.join(folder, filename))

"""
plot image
"""

imgs = request.get_data()

image = imgs[0]
print(f"Image type: {image.dtype}")

# plot function
# factor 1/255 to scale between 0-1
# factor 3.5 to increase brightness
#plot_image(image, factor=3.5 / 255, clip_range=(0, 1))

"""
read geotiff as a dataframe
"""

import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 

file = 'test/85d04f52ed4133d55e72d84a476ef5a6/response.tiff'
tiff = rasterio.open(file)

import pandas as pd
da = rxr.open_rasterio(file, masked=True)
#da = da.rio.reproject("EPSG:4326")
df = da[0].to_pandas()
df['y'] = df.index
df = pd.melt(df, id_vars='y')
df