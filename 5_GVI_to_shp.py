# -*- coding: utf-8 -*-
"""
Created on Thu May 23 08:13:20 2019

@author: Administrator
"""
import pandas as pd
import geopandas as gpd
import glob
import os
from geopandas import GeoDataFrame
from shapely.geometry import Point
import numpy as np

# This script is used to concat the csv files containing GVI infromation and to export them as a shapefile"
# Akseli Toikka and Ville Mäkinen Finnish Geospatial Research Institute FGI. National Land Survey of Finland.

#Make sure you are working in the directory where the GVI files are saved at. 

#os.listdir returns list of the files in direction
GVI_files = os.listdir()

#create empty dataframe with the wanted names for columns
DF = pd.DataFrame(columns = ['panoID','panoDate','longitude','lattitude','GviH_0','GviH_60','GviH_120','GviH_180','GviH_240','GviH_300','Gvi_Mean'])

#Loop through the files in file direction, separate lines (s) in files, separate items (si) in lines
for textfile in GVI_files:
    with open(textfile) as f:
        s = ''
        for line in f:
            s += line.strip()
    s = s.split('panoID: ')
    for item in s:
        if len(item)<2:
            continue
        si = item.replace('[', '').replace(']','').replace(',','')
        si = si.split(' ')
        if len(si)<15:
            print('invalid GVI value')
            continue
       
        data = {'panoID':[si[0]],'panoDate':[si[2]],'longitude':[si[4]],'lattitude':[si[6]],'GviH_0':[si[8]],'GviH_60':[si[9]],'GviH_120':[si[10]],'GviH_180':[si[11]],'GviH_240':[si[12]],'GviH_300':[si[13]],'Gvi_Mean':[si[15]]}
        DF = DF.append(pd.DataFrame.from_dict(data))
    

#shape of the DF
DF.shape

#remove rows with panoID doubles
Data = DF.drop_duplicates(subset=['panoID'], keep='first', inplace=False)

#check how many rows, should have 94455 with the Helsinki dataset
Data.shape

#check that there is only summer months included
Data.groupby('panoDate').nunique()

#wanted objects to float
Data['longitude'] = Data['longitude'].astype(float)
Data['lattitude']= Data['lattitude'].astype(float)
Data['GviH_0'] = Data['GviH_0'].astype(float)
Data['GviH_60'] = Data['GviH_60'].astype(float)
Data['GviH_120'] = Data['GviH_120'].astype(float)
Data['GviH_180'] = Data['GviH_180'].astype(float)
Data['GviH_240'] = Data['GviH_240'].astype(float)
Data['GviH_300'] = Data['GviH_300'].astype(float)
Data['Gvi_Mean'] = Data['Gvi_Mean'].astype(float)

# set the wanted crs
crs = {'init': 'epsg:4326'}

#create coordinate object for the geodataframe
geometry = [Point(xy) for xy in zip(Data.longitude, Data.lattitude)]

#create a geodataframe
Geodata = gpd.GeoDataFrame(Data, crs = crs, geometry = geometry)

#check how it looks
print(Geodata.head())

#save the result as a shapefile
out_shp= 'Name of the file.shp'
Geodata.to_file(out_shp, driver='ESRI Shapefile')
