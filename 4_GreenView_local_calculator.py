# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#This program is used to calculate the GVI for the saved GSV images.
# The Object based images classification algorithm is used to classify the greenery from the GSV images.
# Meanshift algorithm implemented by pymeanshift was used to segment the image.
# Based on the segmented image, we further use the Otsu's method to find threshold from
# ExG image to extract the greenery pixels.

# For more details about the object based image classification algorithm
# check: Li et al., 2016, Who lives in greener neighborhoods? the distribution of street greenery and it association with residents' socioeconomic conditions in Hartford, Connectictu, USA

# This program implementing OTSU algorithm to chose the threshold automatically
# For more details about the OTSU algorithm and python implmentation
# cite: http://docs.opencv.org/trunk/doc/py_tutorials/py_imgproc/py_thresholding/py_thresholding.html

# For running time efficiency the script is run as an array job.
# Array job order is based on the first letter of the panoID

# The original script can be seen at https://github.com/mittrees/Treepedia_Public/blob/master/Treepedia/GreenView_Calculate.py
# Copyright(C) Xiaojiang Li, Ian Seiferling, Marwa Abdulhai, Senseable City Lab, MIT. First version June 18, 2014
# Modified by Akseli Toikka and Ville Mäkinen Finnish Geospatial Research Institute FGI. National Land Survey of Finland 

def graythresh(array,level):
    '''array: is the numpy array waiting for processing
    return thresh: is the result got by OTSU algorithm
    if the threshold is less than level, then set the level as the threshold
    by Xiaojiang Li
    '''
    
    import numpy as np
    
    maxVal = np.max(array)
    minVal = np.min(array)
    
#   if the inputImage is a float of double dataset then we transform the data 
#   in to byte and range from [0 255]
    if maxVal <= 1:
        array = array*255
        # print "New max value is %s" %(np.max(array))
    elif maxVal >= 256:
        array = np.int((array - minVal)/(maxVal - minVal))
        # print "New min value is %s" %(np.min(array))
    
    # turn the negative to natural number
    negIdx = np.where(array < 0)
    array[negIdx] = 0
    
    # calculate the hist of 'array'
    dims = np.shape(array)
    hist = np.histogram(array,range(257))
    P_hist = hist[0]*1.0/np.sum(hist[0])
    
    omega = P_hist.cumsum()
    
    temp = np.arange(256)
    mu = P_hist*(temp+1)
    mu = mu.cumsum()
    
    n = len(mu)
    mu_t = mu[n-1]
    
    sigma_b_squared = (mu_t*omega - mu)**2/(omega*(1-omega))
    
    # try to found if all sigma_b squrered are NaN or Infinity
    indInf = np.where(sigma_b_squared == np.inf)
    
    CIN = 0
    if len(indInf[0])>0:
        CIN = len(indInf[0])
    
    maxval = np.max(sigma_b_squared)
    
    IsAllInf = CIN == 256
    if IsAllInf !=1:
        index = np.where(sigma_b_squared==maxval)
        idx = np.mean(index)
        threshold = (idx - 1)/255.0
    else:
        threshold = level
    
    if np.isnan(threshold):
        threshold = level
    
    return threshold



def VegetationClassification(Img):
    '''
    This function is used to classify the green vegetation from GSV image,
    This is based on object based and otsu automatically thresholding method
    The season of GSV images were also considered in this function
        Img: the numpy array image, eg. Img = np.array(Image.open(StringIO(response.content)))
        return the percentage of the green vegetation pixels in the GSV image
    
    '''
    
    import pymeanshift as pms
    import numpy as np
    
    # use the meanshift segmentation algorithm to segment the original GSV image
    (segmented_image, labels_image, number_regions) = pms.segment(Img,spatial_radius=6,
                                                     range_radius=7, min_density=40)
    
    I = segmented_image/255.0
    
    red = I[:,:,0]
    green = I[:,:,1]
    blue = I[:,:,2]
    
    # calculate the difference between green band with other two bands
    green_red_Diff = green - red
    green_blue_Diff = green - blue
    
    ExG = green_red_Diff + green_blue_Diff
    diffImg = green_red_Diff*green_blue_Diff
    
    redThreImgU = red < 0.6
    greenThreImgU = green < 0.9
    blueThreImgU = blue < 0.6
    
    shadowRedU = red < 0.3
    shadowGreenU = green < 0.3
    shadowBlueU = blue < 0.3
    del red, blue, green, I
    
    greenImg1 = redThreImgU * blueThreImgU*greenThreImgU
    greenImgShadow1 = shadowRedU*shadowGreenU*shadowBlueU
    del redThreImgU, greenThreImgU, blueThreImgU
    del shadowRedU, shadowGreenU, shadowBlueU
    
    greenImg3 = diffImg > 0.0
    greenImg4 = green_red_Diff > 0
    threshold = graythresh(ExG, 0.1)
    
    if threshold > 0.1:
        threshold = 0.1
    elif threshold < 0.05:
        threshold = 0.05
    
    greenImg2 = ExG > threshold
    greenImgShadow2 = ExG > 0.05
    greenImg = greenImg1*greenImg2 + greenImgShadow2*greenImgShadow1
    del ExG,green_blue_Diff,green_red_Diff
    del greenImgShadow1,greenImgShadow2
    
    # calculate the percentage of the green vegetation
    greenPxlNum = len(np.where(greenImg != 0)[0])
    greenPercent = greenPxlNum/(400.0*400)*100
    del greenImg1,greenImg2
    del greenImg3,greenImg4
    
    return greenPercent



# using 18 directions is too time consuming, therefore, here I only use 6 horizontal directions
# Each time the function will read a text, with 1000 records, and save the result as a single TXT
def GreenViewComputing_ogr_6Horizon(GSVinfoFolder, outTXTRoot, greenmonth, GSVimagesRoot, myLetter):
    
    """
    This function is used to download the GSV from the information provide
    by the gsv info txt, and save the result to a shapefile
    
    Required modules: StringIO, numpy, requests, and PIL
    
        GSVinfoTxt: the input folder name of GSV info txt
        outTXTRoot: the output folder to store result green result in txt files
        greenmonth: a list of the green seasons in Helsinki = ['05','06','07','08','09']
    
    """
    
    import time
    from PIL import Image
    import numpy as np
    from StringIO import StringIO
    
    

    # set a series of heading angle
    headingArr = 360.0/6*np.array([0,1,2,3,4,5])
    
    # number of GSV images = 6 horizontal images
    numGSVImg = len(headingArr)*1.0

    
    # create a folder for GSV images and grenView Info
    if not os.path.exists(outTXTRoot):
        os.makedirs(outTXTRoot)
    
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
            
            gvTxt = 'GV_'+ myLetter+'_' +os.path.basename(txtfile)
            GreenViewTxtFile = os.path.join(outTXTRoot,gvTxt)
            CalculatedPanoId = set()
            
            if os.path.exists(GreenViewTxtFile):
                with open(GreenViewTxtFile, 'r') as f:
                    for line in f:
                        sline = line.split(' ')
                        CalculatedPanoId.add(sline[1])
            
            # loop all lines in the txt files
            for line in lines:
                metadata = line.split(" ")
                panoID = metadata[1]
                if not panoID[0] == myLetter:
                    continue
                panoDate = metadata[3]
                month = panoDate[-2:]
                lon = metadata[5]
                lat = metadata[7][:-1].strip()
                
                # print (lon, lat, month, panoID, panoDate)
                
                # in case, the longitude and latitude are invalide
                if len(lon)<3:
                    continue
                
                # check if GVI is calculated earlier
                if panoID in CalculatedPanoId:
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
            

            
            # check whether the file already generated, if yes, skip. Therefore, you can run several process at same time using this code.
            print (GreenViewTxtFile)
            if os.path.exists(GreenViewTxtFile):
                continue
            
            # write the green view and pano info to txt            
            with open(GreenViewTxtFile,"a") as gvResTxt:
                for i in range(len(panoIDLst)):
                    panoDate = panoDateLst[i]
                    panoID = panoIDLst[i]
                    lat = panoLatLst[i]
                    lon = panoLonLst[i]
                    
                    #check if the panoID looks right
                    if len(panoID) != 22:
                        raise Exception('vieras panoID')
                    
                    #different levels for the GSV image storage
                    level1 = os.path.join(GSVimagesRoot,panoID[0:1])
                    level2 = os.path.join(level1,panoID[0:2])
                    level3 = os.path.join(level2,panoID)
                    
                    # Create directions if they dont exist
                    #if not os.path.exists(level1):
                        #os.mkdir(level1)
                    #if not os.path.exists(level2):
                        #os.mkdir(level2)
                    #if not os.path.exists(level3):
                        #os.mkdir(level3)
                    
                    # calculate the green view index
                    #0 value for new panoID GVI
                    greenPercent = 0.0
                    #list to collect the GVI.s for different headings of panoID
                    headingGVI = []
                    
                    for heading in headingArr:
                        print ("Heading is: ",heading)
   
                        #  save the GSV images, classify the GSV images, calcuate the GVI for each heading  
                        try:        
                            name = os.path.join(level3,'GSV_Image_{}_{}.jpg'.format(panoID,heading))
                            
                            print(name)
                            
                            if os.path.exists(name):
                                image = Image.open(name)
                            else:
                                print('GSV Image not found')
                            
                            im = np.array(image)
                            percent = VegetationClassification(im)
                            headingGVI.append(percent)
                            greenPercent = greenPercent + percent

                        #if the GSV images are not download successfully or failed to run, then return a null value
                        except:
                            greenPercent = -1000
                            break

                    # calculate the green view index by averaging six percents from six images
                    greenViewVal = greenPercent/numGSVImg
                    print ('The MeanGVI: %s, headingGVI: %s, pano: %s, (%s, %s)'%(greenViewVal, headingGVI, panoID, lat, lon))

                    # write the result and the pano info to the result txt file
                    lineTxt = 'panoID: %s panoDate: %s longitude: %s latitude: %s, headingGVI: %s MeanGVI: %s\n'%(panoID, panoDate, lon, lat,headingGVI, greenViewVal)
                    gvResTxt.write(lineTxt)
                    gvResTxt.flush()


# ------------------------------Main function-------------------------------
if __name__ == "__main__":
    import sys
    import os,os.path
    import itertools
    
    ArrayList = 'aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ1234567890-_' # pano ID starting letters for separating the array jobs
    GSVimagesRoot = 'root of the GSV images'
    GSVinfoRoot = 'root of the metadata file'
    outputTextPath = 'root/ file of the output'
    greenmonth = ['05','06','07','08','09'] # months used
    myLetter = ArrayList[int(sys.argv[1])] 
    
    
    GreenViewComputing_ogr_6Horizon(GSVinfoRoot,outputTextPath, greenmonth, GSVimagesRoot, myLetter)


