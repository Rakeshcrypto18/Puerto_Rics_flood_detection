""""
This Script takes all collected geotiffs and transformes them in the workable csvs in pandas format
"""
""""
Import all necessary packages
"""
import rasterio
import rasterio.plot
import matplotlib
import rioxarray as rxr 
import pandas as pd

""""
read pre and post flood images
"""
#MODIFY ME
preflood1_tiff = 'NDFI_NDFVI_tiffs/preflood1_13.tiff'
preflood2_tiff = 'NDFI_NDFVI_tiffs/preflood2_13.tiff'
preflood3_tiff = 'NDFI_NDFVI_tiffs/preflood3_13.tiff'
postflood1_tiff = 'NDFI_NDFVI_tiffs/postflood1_13.tiff'
postflood2_tiff = 'NDFI_NDFVI_tiffs/postflood2_13.tiff'


""""
bands to pandas each section is for a different band 
band 0 grabs VH values, band 1 will grab VV values
"""
#band 0 VH values 
#band 1 VV values 

#different bands to pandas VH example
da = rxr.open_rasterio(preflood1_tiff, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfpreflood1 = da[0].to_pandas() #da[x] this is where the band specification occurs
dfpreflood1['y'] = dfpreflood1.index
dfpreflood1 = pd.melt(dfpreflood1, id_vars='y')
dfpreflood1=dfpreflood1.rename(columns={'value':'preflood_vh1'})
dfpreflood1

da = rxr.open_rasterio(preflood2_tiff, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfpreflood2 = da[0].to_pandas()
dfpreflood2['y'] = dfpreflood2.index
dfpreflood2 = pd.melt(dfpreflood2, id_vars='y')
dfpreflood2=dfpreflood2.rename(columns={'value':'preflood_vh2'})
dfpreflood2

da = rxr.open_rasterio(preflood3_tiff, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfpreflood3 = da[0].to_pandas()
dfpreflood3['y'] = dfpreflood3.index
dfpreflood3 = pd.melt(dfpreflood3, id_vars='y')
dfpreflood3=dfpreflood3.rename(columns={'value':'preflood_vh3'})
dfpreflood3

da = rxr.open_rasterio(postflood1_tiff, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfpostflood1 = da[0].to_pandas()
dfpostflood1['y'] = dfpostflood1.index
dfpostflood1 = pd.melt(dfpostflood1, id_vars='y')
dfpostflood1=dfpostflood1.rename(columns={'value':'postflood_vh1'})
dfpostflood1

da = rxr.open_rasterio(postflood2_tiff, masked=True)
#da = da.rio.reproject("EPSG:4326")
dfpostflood2 = da[0].to_pandas()
dfpostflood2['y'] = dfpostflood2.index
dfpostflood2 = pd.melt(dfpostflood2, id_vars='y')
dfpostflood2=dfpostflood2.rename(columns={'value':'postflood_vh2'})
dfpostflood2

""""
merge data into one single pandas dataframe
"""
join1= pd.merge(dfpreflood1, dfpreflood2, on=['y', 'x'], how='inner')
join2= pd.merge(join1, dfpreflood3, on=['y', 'x'], how='inner')
join3= pd.merge(dfpostflood1, dfpostflood2, on=['y', 'x'], how='inner')
df = pd.merge(join2,join3, on=['y', 'x'], how='inner')
df

""""
save to csv
"""
#MODIFY ME
df.to_csv('vh_13.csv')


# """
# VV to csv
# """
# #different bands to pandas VH example
# da = rxr.open_rasterio(preflood1_tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# dfpreflood1 = da[1].to_pandas()
# dfpreflood1['y'] = dfpreflood1.index
# dfpreflood1 = pd.melt(dfpreflood1, id_vars='y')
# dfpreflood1=dfpreflood1.rename(columns={'value':'preflood_vv1'})
# dfpreflood1

# da = rxr.open_rasterio(preflood2_tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# dfpreflood2 = da[1].to_pandas()
# dfpreflood2['y'] = dfpreflood2.index
# dfpreflood2 = pd.melt(dfpreflood2, id_vars='y')
# dfpreflood2=dfpreflood2.rename(columns={'value':'preflood_vv2'})
# dfpreflood2

# da = rxr.open_rasterio(preflood3_tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# dfpreflood3 = da[1].to_pandas()
# dfpreflood3['y'] = dfpreflood3.index
# dfpreflood3 = pd.melt(dfpreflood3, id_vars='y')
# dfpreflood3=dfpreflood3.rename(columns={'value':'preflood_vv3'})
# dfpreflood3

# da = rxr.open_rasterio(postflood1_tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# dfpostflood1 = da[1].to_pandas()
# dfpostflood1['y'] = dfpostflood1.index
# dfpostflood1 = pd.melt(dfpostflood1, id_vars='y')
# dfpostflood1=dfpostflood1.rename(columns={'value':'postflood_vv1'})
# dfpostflood1

# da = rxr.open_rasterio(postflood2_tiff, masked=True)
# #da = da.rio.reproject("EPSG:4326")
# dfpostflood2 = da[1].to_pandas()
# dfpostflood2['y'] = dfpostflood2.index
# dfpostflood2 = pd.melt(dfpostflood2, id_vars='y')
# dfpostflood2=dfpostflood2.rename(columns={'value':'postflood_vv2'})
# dfpostflood2





