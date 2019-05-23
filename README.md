<img src="https://github.com/geoportti/Logos/blob/master/geoportti_logo_300px.png">

# Helsinki_GreenView

This repository contains scripts and instructions for downloading Google Street View (GSV) images of Helsinki and calculating the Green View Index (GVI) . The scripts were used in Master's thesis of Akseli Toikka from the Finnish Geospatial Research Institute (FGI), Department of Geoinformatics and Cartography. Thesis available at LINKKI

The modified scripts are based on the Treepedia_Public repository by @mittrees and are originally created by Ian Seiferling, Xiaojiang Li, Marwa Abdulhai, Senseable City Lab, MIT. For further information on GVI and Treepedia, visit: [https://github.com/mittrees/Treepedia_Public]

## Workflow
## 1. Create sample points along the street network of Helsinki
The first task is to download the OpenStreetMap data of Finland and cut the road network with Helsinki city boarders. You can do this manually for example in QGis. Also other road data sources are ok, but the script is made to work with OpenStreetMap road data. Before creating the sample points, the road data is cleaned by removing motorways and some other types of roads. You can also skip this and create sample points for all roads available. 

**Data in:** OpenStreetMap (or other) road network of Helsinki

**Data out:** Sample points between every 20m along the street network of wanted road segments.

**Use script:** [1_createPoints.py](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/1_createPoints_org.py)


## 2. Download the metadata based on the sample point locations
Based on the sample point locations, the metadataCollector will make a set of URL requests for the Google API. If API holds a street view panorama within 50m of the sample point location, the function downloads the metadata of that panorama. Example of metadata:
```
panoID: g_asC6f050C67UYQoCXxAg panoDate: 2009-06 longitude: 24.894128 latitude: 60.211182
panoID: iZNpqcbGu0z2Ho6buYjoWg panoDate: 2009-06 longitude: 24.894292 latitude: 60.211143
panoID: PNaAU8oy5rn0emzbWmlK7g panoDate: 2011-08 longitude: 24.897470 latitude: 60.212611
panoID: -TuQHCfniQn3hbpDFVCsRw panoDate: 2011-08 longitude: 24.897409 latitude: 60.212507
```
**Data in:** Sample points

**Data out:** Metadata text file of the panoramas located at the sample point locations

**Use script:** [2_metadataCollector.py](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/2_metadataCollector.py)

**You also need:** Google API key



## 3. Download and save the GSV images
Based on the metadata information you now know when are the images taken. You can download the Google imagery of Helsinki using only summermonths when the leaves are usually green (May- September). Every panorama will be downloaded in 6 images and saved alpabetically based on the panoID first letters. The download will take some time and the images will require about 20 gigabytes of space on your hard drive. You can run this script in CSC Taito computing environment by using the provided batch script.

**Data in:** downloaded metadata text file

**Data out:** GSV images of sample point locations.

**Use script:** [3_GSV_image_downloader.py](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/3_GSV_image_downloader.py), [GSV_image_download_batch](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/GSV_Image_download_batch.py)

**You also need**: Google API key, Google signing signature



## 4. Calculate the GVI for the sample sites
GVI is calclulated for every GSV image separately. Sample site GVI is a mean GVI value of six images from that location. You can run this script in CSC Taito computing environment by using the provided batch script. For running time efficiency the script is run as an array job. Array jobs are separated by the first letter of the panoID.s. Beware that this process might take some time.

Example of the GVI data:
```
panoID: d78rmtRxyB4EdrYnEeEryg panoDate: 2009-07 longitude: 25.00531 latitude: 60.262958, headingGVI: [16.858124999999998, 27.173125, 34.4375, 28.515625, 30.320000000000004, 16.455624999999998] MeanGVI: 25.6266666667
panoID: drMyW3WBdd-0ZyCCKCoDHA panoDate: 2009-07 longitude: 25.004901 latitude: 60.263337, headingGVI: [13.020000000000001, 9.936250000000001, 8.425, 20.366875, 21.4725, 44.618125] MeanGVI: 19.6397916667
panoID: p0G9MEiHR9zXmuMMatfiKw panoDate: 2009-07 longitude: 25.001899 latitude: 60.263875, headingGVI: [25.66625, 13.10375, 19.998125, 74.8325, 14.299999999999999, 29.485] MeanGVI: 29.5642708333
```

**Data in:** GSV images

**Data out:** GVI values for sample site locations.

**Use script:** [4_GVI_local_calculator.py](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/4_GVI_local_calculator.py), GVI_local_calculator_batch



## 5. Save as shapefile

To be able to make some geospatial analyses or visualisations with the data it is good to save it as a georeferenced shapefile. 

**Data in:** GVI values.csv

**Data out:** Point shapefile of with the GVI values for every sample site.

**Use script:** [5_GVI_to_shp.py](https://github.com/geoporttishare/Helsinki_GreenView/blob/master/5_GVI_to_shp.py)


