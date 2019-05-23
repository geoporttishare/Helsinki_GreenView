# -*- coding: utf-8 -*-

#Created on Tue Nov 20 12:40:09 2018

# The program downloads one GSV panorama in 6 images for the wanted locations. 
# The GSV images are organized by alpabetical order based on the panoID of the panorama.
# Folder named by the panoID contains all the 6 images downloaded from that location.
# The 6 images are named by the panoID and the heading direction.
# For running the script you will need Google API key and a URL signing secret.

# The original script can be seen at https://github.com/mittrees/Treepedia_Public/blob/master/Treepedia/GreenView_Calculate.py
# Copyright(C) Xiaojiang Li, Ian Seiferling, Marwa Abdulhai, Senseable City Lab, MIT. First version June 18, 2014
# # Modified by Akseli Toikka and Ville Mäkinen Finnish Geospatial Research Institute FGI. National Land Survey of Finland 


# Each time the function will read a panoID list and save the results as jpg.images in to files named by the panoID
def GVS_image_downloader(GSVinfoFolder, outputImageFile, greenmonth):
    
    """
    This function is used to download the GSV from the information provide
    by the gsv info txt, and save the result to a shapefile
    
    Required modules: StringIO, numpy, requests, and PIL
    
        GSVinfoTxt: the input folder name of GSV info txt
        outTXTRoot: the output folder to store result green result in txt files
        greenmonth: a list of the green season, for example in Boston, greenmonth = ['05','06','07','08','09']
    
    """
    
    import time
    from PIL import Image
    import numpy as np
    import requests
    from io import StringIO
    import base64
    import hashlib
    import hmac
    import base64
    from urllib.parse import urlparse
    
    
    #This Function to decode the singning code for google API url request
    def sign_url(input_url=None, secret=None):
 
        if not input_url or not secret:
          raise Exception("Both input_url and secret are required")

        url = urlparse(input_url)

        # We only need to sign the path+query part of the string
        url_to_sign = url.path + "?" + url.query

         # Decode the private key into its binary format
         # We need to decode the URL-encoded private key
        decoded_key = base64.urlsafe_b64decode(secret)

         # Create a signature using the private key and the URL-encoded
         # string using HMAC SHA1. This signature will be binary.
        signature = hmac.new(decoded_key, url_to_sign.encode('utf-8'), hashlib.sha1)

        # Encode the binary signature into base64 for use within a URL
        encoded_signature = base64.urlsafe_b64encode(signature.digest())

        original_url = url.scheme + "://" + url.netloc + url.path + "?" + url.query

        # Return signed URL
        return original_url + "&signature=" + encoded_signature.decode('utf-8')

    
    
    
    # set a series of heading angle
    headingArr = 360/6*np.array([0,1,2,3,4,5])
    
    # number of GSV images = 6 horizontal images
    numGSVImg = len(headingArr)*1.0
    pitch = 0
    
    # create a folder for GSV images and greenView Info
    if not os.path.exists(outputImageFile):
        os.makedirs(outputImageFile)
    
    # the input GSV info should be in a folder
    if not os.path.isdir(GSVinfoFolder):
        print ('You should input a folder for GSV metadata')
        return
    else:
        allTxtFiles = os.listdir(GSVinfoFolder)
        for txtfile in allTxtFiles:
            if not txtfile.endswith('.txt'):
                continue
            
            txtfilename = os.path.join(GSVinfoFolder,txtfile)
            lines = open(txtfilename,"r")
            
            # create empty lists, to store the information of panos,and remove duplicates
            panoIDLst = []
            panoDateLst = []
            panoLonLst = []
            panoLatLst = []
            
            
            # loop all lines in the txt files
            for line in lines:
                metadata = line.split(" ")
                panoID = metadata[1]
                panoDate = metadata[3]
                month = panoDate[-2:]
                lon = metadata[5]
                lat = metadata[7][:-1]
                
                
                # in case, the longitude and latitude are invalide
                if len(lon)<3:
                    continue
                
               # drop double id.s
                if panoID in panoIDLst:
                    continue
                
                # only use the months of green seasons
                if month not in greenmonth:
                    continue
                else:
                    panoIDLst.append(panoID)
                    panoDateLst.append(panoDate)
                    panoLonLst.append(lon)
                    panoLatLst.append(lat)
            
            
            for i in range(len(panoIDLst)):
                panoDate = panoDateLst[i]
                panoID = panoIDLst[i]
                lat = panoLatLst[i]
                lon = panoLonLst[i]
                    
                #check if the panoID looks right
                if len(panoID) != 22:
                    raise Exception('strange panoID')
                    
                    #different levels for the GSV image storage based on the panoID letters
                level1 = os.path.join(outputImageFile,panoID[0:1])
                level2 = os.path.join(level1,panoID[0:2])
                level3 = os.path.join(level2,panoID)
                    
                    # Create directions if they dont exist
                if not os.path.exists(level1):
                    os.mkdir(level1)
                if not os.path.exists(level2):
                    os.mkdir(level2)
                if not os.path.exists(level3):
                    os.mkdir(level3)
                    
                    
                for heading in headingArr:
                    print ("Heading is: ",heading)
                        
                    # construct the orginal URL
                    URL = "http://maps.googleapis.com/maps/api/streetview?size=400x400&pano=%s&fov=60&heading=%s&pitch=%d&sensor=false&key="your API key here"%(panoID,heading,pitch)
                    #add the decoded google security key into the URL
                    URL = sign_url(URL, 'put your signing signature here')
                    
                    # let the code to pause by 1s, in order to not go over data limitation of Google quota
                    #time.sleep(1)
                        
                        
                        
                    # Download and save the GSV images
                    try:        
                        name = os.path.join(level3,'GSV_Image_{}_{}.jpg'.format(panoID,heading))
                        if not os.path.exists(name):
                            response = requests.get(URL)
                            with open(name,'wb') as f:
                                f.write(response.content)
                    except:
                        print('downloading '+ name + ' failed ')
                               


# ------------------------------Main function-------------------------------
if __name__ == "__main__":
    
    import os,os.path
    import itertools
    

    GSVinfoRoot = "root of the working directory"
    outputImageFile = "name of the output image file"
    greenmonth = ['05','06','07','08','09'] #months used
    
    GVS_image_downloader(GSVinfoRoot,outputImageFile, greenmonth)



