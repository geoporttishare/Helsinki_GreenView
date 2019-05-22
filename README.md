<img src="https://github.com/geoportti/Logos/blob/master/geoportti_logo_300px.png">

# Helsinki_GreenView

This repository contains scripts and instructions for calculating the Green View Index (GVI) for Google Street View (GSV) images in Helsinki. The scripts were used in Master's thesis of Akseli Toikka from the Finnish Geospatial Research Institute (FGI), Department of Geoinformatics and Cartography. Thesis available at LINKKI

The modified scripts are based on the Treepedia_Public repository by @mittrees and are originally created by Ian Seiferling, Xiaojiang Li, Marwa Abdulhai, Senseable City Lab, MIT. For further information on GVI and Treepedia, visit: [https://github.com/mittrees/Treepedia_Public]

## Workflow
### 1. Create sample points along the street network of Helsinki
Data in: OpenStreetMap road network of Helsinki

Data out: Sample points between every 20m along the street network of wanted road segments.

Use script: createPoints.py

### 2. Download the metadata based on the sample point locations
Data in: Sample points

Data out: Metadata text file of the panoramas located at the sample point locations

Use script: metadataCollector.py

You also need: Google API key

### 3. Download and save the GSV images
Data in: downloaded metadata

Data out: GSV images of sample point locations. Every panorama is downloaded in 6 images 

Use script: GSV_image_downloader.py, GSV_image_download_batch

You also need: Google API key, Google signing signature

### 4. Calculate the GVI for the sample sites

Data in: GSV images

Data out: GVI values for sample site locations.

Use script: GVI_local_calculator.py, GVI_local_calculator_batch

### 5. Save as shapefile

Data in: GVI values.csv

Data out: GVI_Helsinki.shp

Use script: GVI_to_shp.py


