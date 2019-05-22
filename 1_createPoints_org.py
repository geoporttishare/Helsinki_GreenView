
# This script was  used to create sample points between every 20m along the street network of Helsinki.
# The sample point locations are later used for downloading the GSV metadata from Google API 

# Copyright(C) Ian Seiferling, Xiaojiang Li, Marwa Abdulhai, Senseable City Lab, MIT First version July 21 2017

# Modified by Akseli Toikka and Ville Mäkinen Finnish Geospatial Research Institute FGI. National Land Survey of Finland 

# now run the python file: createPoints.py, the input shapefile has to be in projection of WGS84, 4326

def createPoints(inshp, outshp, mini_dist):
    
    '''
    This function will parse throigh the street network of provided city and
    clean all highways and create points every mini_dist meters (or as specified) along
    the linestrings
    Required modules: Fiona and Shapely
    parameters:
        inshp: the input linear shapefile, must be in WGS84 projection, ESPG: 4326
        output: the result point feature class
        mini_dist: the minimum distance between two created point
    
    '''
    
    import fiona
    import os,os.path
    from shapely.geometry import shape,mapping
    from shapely.ops import transform
    from functools import partial
    import pyproj
    from fiona.crs import from_epsg
    
    
    count = 0
    
    #name the road types NOT to be used.  
    s = {'trunk_link','motorway','motorway_link','steps', None,'pedestrian','trunk','bridleway','service'}
    
    # the temporaray file of the cleaned data
    root = os.path.dirname(inshp)
    basename = 'clean_' + os.path.basename(inshp)
    temp_cleanedStreetmap = os.path.join(root,basename)
    
    # if the tempfile exist then delete it
    if os.path.exists(temp_cleanedStreetmap):
        fiona.remove(temp_cleanedStreetmap, 'ESRI Shapefile')
    
    # clean the original street maps by removing highways, if it the street map not from Open street data, users'd better to clean the data themselve
    with fiona.open(inshp) as source, fiona.open(temp_cleanedStreetmap, 'w', driver=source.driver, crs=source.crs,schema=source.schema) as dest:
        
        for feat in source:
            try:
                i = feat['properties']['fclass'] # for the OSM street data
                if i in s:
                    continue
            except:
               # if the street map is not osm, do nothing. You'd better to clean the street map, if you don't want to map the GVI for highways
               # key = dest.schema['properties'].keys()[0] # get the field of the input shapefile and duplicate the input feature
               # i = feat['properties'][key]
               # if i in s:
               continue
            
            dest.write(feat)

    schema = {
        'geometry': 'Point',
        'properties': {'id': 'int'},
    }

    # Create pointS along the streets
    with fiona.drivers():
        #with fiona.open(outshp, 'w', 'ESRI Shapefile', crs=source.crs, schema) as output:
        with fiona.open(outshp, 'w', crs = from_epsg(4326), driver = 'ESRI Shapefile', schema = schema) as output:
            for line in fiona.open(temp_cleanedStreetmap):
                first = shape(line['geometry'])
                if first.geom_type != 'LineString': continue
                
                length = first.length
                
                try:
                    # convert degree to meter, in order to split by distance in meter
                    project = partial(pyproj.transform,pyproj.Proj(init='EPSG:4326'),pyproj.Proj(init='EPSG:3067')) #3857 is psudo WGS84 the unit is meter
                    
                    line2 = transform(project, first)
                    linestr = list(line2.coords)
                    dist = mini_dist #set
                    for distance in range(0,int(line2.length), dist):
                        point = line2.interpolate(distance)
                        
                        # convert the local projection back the the WGS84 and write to the output shp
                        project2 = partial(pyproj.transform,pyproj.Proj(init='EPSG:3067'),pyproj.Proj(init='EPSG:4326'))
                        point = transform(project2, point)
                        output.write({'geometry':mapping(point),'properties': {'id':1}})
                except Exception as e:
                    print(e)
                    print ("You should make sure the input shapefile is WGS84")
                    return
                    
    print("Process Complete")
    
    # delete the temprary cleaned shapefile
   # fiona.remove(temp_cleanedStreetmap, 'ESRI Shapefile')


# Example to use the code, 
# Note: make sure the input linear featureclass (shapefile) is in WGS 84 or ESPG: 4326
# ------------main ----------
if __name__ == "__main__":
    import os,os.path
    import sys
    
    root = "root of the working directory"
    inshp = os.path.join(root,'hki_osm_roads.shp') #the input shapefile of road network
    outshp = os.path.join(root,'Helsinki20m.shp') #the output shapefile of the points
    mini_dist = 20 #the minimum distance between two generated points in meters
    createPoints(inshp, outshp, mini_dist)
