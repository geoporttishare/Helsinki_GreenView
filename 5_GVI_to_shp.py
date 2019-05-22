# -*- coding: utf-8 -*-
"""
Created on Fri May  3 13:54:03 2019

@author: Administrator
"""

# This script is used to concat the csv files containing GVI infromation and to export them as a shapefile"
# Akseli Toikka and Ville Mäkinen Finnish Geospatial Research Institute FGI. National Land Survey of Finland

import pandas as pd
import geopandas as gpd
import glob
import os
from geopandas import GeoDataFrame
from shapely.geometry import Point
import numpy as np

#the direction of the GVI dataframes to be merged
GVIFrames = os.listdir()

#read and merge the data. Use only wanted columns
PData = pd.concat([pd.read_csv(f, sep = ',', usecols= ['panoID', 'panoDate', 'longitude', 'lattitude', 'GviH_0', 'GviH_60', 'GviH_120', 'GviH_180', 'GviH_240', 'GviH_300', 'Gvi_Mean']) for f in GVIFrames], ignore_index = True,)

#feature foor coordinate reference system
crs = {'init': 'epsg:4326'}

# Create geometry object
geometry = [Point(xy) for xy in zip(PData.longitude, PData.lattitude)]

#create a geodataframe
PGeodata = gpd.GeoDataFrame(PData, crs = crs, geometry = geometry)

#check how it looks
print(PGeodata.head())

#save the result as a shapefile
out_shp= 'Name of the shapefile'
PGeodata.to_file(out_shp, driver='ESRI Shapefile')

