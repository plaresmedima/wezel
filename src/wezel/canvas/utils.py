import numpy as np
from PyQt5.QtGui import QImage

from skimage import feature
import cv2 as cv2


def region_grow_add(img, selected, to_select, min, max):
    width, height = img.shape
    checked = np.copy(selected)
    neighbours = [
        [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], 
        [0, 1], [-1, 1], [-1, 0]
    ]
    while to_select != []:
        p = to_select.pop()
        selected[p[0], p[1]] = True
        for next in neighbours:
            x = p[0] + next[0]
            y = p[1] + next[1]
            if x < 0 or y < 0 or x >= width or y >= height:
                continue
            if not checked[x,y]:
                checked[x,y] = True
                if min <= img[x,y] <= max:
                    to_select.append([x,y])
    return selected

def region_grow_remove(img, selected, to_select, min, max):
    width, height = img.shape
    checked = np.copy(np.logical_not(selected))
    neighbours = [
        [-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], 
        [0, 1], [-1, 1], [-1, 0]
    ]
    while to_select != []:
        p = to_select.pop()
        selected[p[0], p[1]] = False
        for next in neighbours:
            x = p[0] + next[0]
            y = p[1] + next[1]
            if x < 0 or y < 0 or x >= width or y >= height:
                continue
            if not checked[x,y]:
                checked[x,y] = True
                if min <= img[x,y] <= max:
                    to_select.append([x,y])
    return selected


COLORMAPS = [ # This needs to move to dbdicom - list of supported colormaps
    ('Perceptually Uniform Sequential',[
        'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
    ('Sequential', [
        'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
        'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
        'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
    ('Miscellaneous', [
        'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
        'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
        'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
        'gist_ncar']),
    ('Sequential (2)', [
        'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
        'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
        'hot', 'afmhot', 'gist_heat', 'copper']),
    ('Diverging', [
        'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
        'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
    ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
    ('Qualitative', [
        'Pastel1', 'Pastel2', 'Paired', 'Accent',
        'Dark2', 'Set1', 'Set2', 'Set3',
        'tab10', 'tab20', 'tab20b', 'tab20c']),
]

  

# HELPER FUNCTION ADAPTED FROM pyQtGraph


def makeQImage(imgData, copy=True):
    """
    Turn an ARGB array into QImage. 'd
    By default, the data is copied; changes to the array will not
    be reflected in the image. The image will be given aata' attribute
    pointing to the array which shares its data to prevent python
    freeing that memory while the image is in use.
    
    ============== ===================================================================
    **Arguments:**
    imgData        Array of data to convert. Must have shape (width, height, 3 or 4) 
                   and dtype=ubyte. The order of values in the 3rd axis must be 
                   (b, g, r, a).
    copy           If True, the data is copied before converting to QImage.
                   If False, the new QImage points directly to the data in the array.
                   Note that the array must be contiguous for this to work
                   (see numpy.ascontiguousarray).
    ============== ===================================================================    
    """

    copied = False

    imgData = imgData.transpose((1, 0, 2))  ## QImage expects the row/column order to be opposite

    if not imgData.flags['C_CONTIGUOUS']:
        imgData = np.ascontiguousarray(imgData)
        copied = True
        
    if copy is True and copied is False:
        imgData = imgData.copy()       
    try:
        img = QImage(imgData.ctypes.data, imgData.shape[1], imgData.shape[0], QImage.Format_RGB32)
    except:
        img = QImage(memoryview(imgData), imgData.shape[1], imgData.shape[0], QImage.Format_RGB32)
                
    img.data = imgData
    
    return img 


def kidneySegmentation(img_array,pixelY,pixelX,pixelSize,side=None):

        img_array_Blurred = cv2.GaussianBlur(img_array, (31,31),cv2.BORDER_DEFAULT)

        KidneyBlurred = np.zeros(np.shape(img_array_Blurred))
        if pixelX>img_array.shape[0]/2:
            KidneyBlurred[int(np.shape(img_array_Blurred)[0]/2):np.shape(img_array_Blurred)[0],:] = img_array_Blurred[int(np.shape(img_array_Blurred)[0]/2):np.shape(img_array_Blurred)[0],:]
        if pixelX<img_array.shape[0]/2:
            KidneyBlurred[0:int(np.shape(img_array_Blurred)[0]/2),:] = img_array_Blurred[0:int(np.shape(img_array_Blurred)[0]/2),:]

        sigmaCanny = 0
        edges = feature.canny(KidneyBlurred, sigma =sigmaCanny)
        edges= edges.astype(np.uint8)
        #plt.imshow(edges)

        maxIteration = 10
        maxIteration_2 =5

        Kidney=[]
        #dilate edges until you find a potential renal contour 
        for j in range(maxIteration):

            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1+j,1+j))
            dilated = cv2.dilate(edges, kernel)
            #plt.imshow(dilated)
            cnts_Kidney,hierarchy_Kidney = cv2.findContours(dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cnts_Kidney = sorted(cnts_Kidney, key=cv2.contourArea, reverse=True)

            #loop through the different contours until you find a potential renal contour 
            for i in range(len(cnts_Kidney)):
                cntTemp = cnts_Kidney[i]
                #print(i)
                #print(cv2.contourArea(cntTemp))
                #print(cv2.pointPolygonTest(cntTemp,(pixelY,pixelX),True))

                #Kidney = cntTemp
                #mask_Kidney = np.ones(np.shape(img_array))
                #cv2.drawContours(mask_Kidney,[Kidney],0,(0,255,0),thickness=cv2.FILLED)
                #mask_Kidney = np.abs(mask_Kidney + 1 - 2)
                #plt.imshow(mask_Kidney)
                #Kidney = []

                if cv2.contourArea(cntTemp)*pixelSize[0]*pixelSize[1]>1500: #check if the area of the contour is suitable with the kidneys

                    dist = cv2.pointPolygonTest(cntTemp,(pixelY,pixelX),True)
                    
                    if dist > 0:
                        #print('Dilation iteration: ' +str(j))
                        #print('Contour Number: ' +str(i))
                        #print('Distance: ' +str(dist))
                        #print('ROI Area: ' +str(cv2.contourArea(cntTemp)) +' pixels')
                        #print('Son: '+str(hierarchy_Kidney[0,i][2]))
                        #print('Grandfather: '+str(hierarchy_Kidney[0,i][3]))

                        Kidney = cntTemp
                        mask_Kidney = np.ones(np.shape(img_array))
                        cv2.drawContours(mask_Kidney,[Kidney],0,(0,255,0),thickness=cv2.FILLED)
                        mask_Kidney = np.abs(mask_Kidney + 1 - 2)
                        
                        kernel_mask = np.ones((j+3,j+3)).astype(np.uint8)
                        edges_Kidney_new = (cv2.erode(mask_Kidney,kernel_mask)*edges).astype(np.uint8)
                        
                        kernel_new = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(1,1))
                        edges_Kidney_new = cv2.erode(edges_Kidney_new,kernel_new).astype(np.uint8)
                        edges_Kidney_new = cv2.dilate(edges_Kidney_new,kernel_new).astype(np.uint8)

                        edges_Kidney_new_dilated = cv2.dilate(edges_Kidney_new, kernel_new)
                        cnts_Kidney_new,hierarchy_Kidney_new = cv2.findContours(edges_Kidney_new_dilated.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
                        cnts_Kidney_new_Sorted = sorted(cnts_Kidney_new, key=cv2.contourArea, reverse=True)

                        #check if contours needed to be removed from the main mask (nasty pelvis pixels)
                        for i_2 in range(len(cnts_Kidney_new_Sorted)):
                            cntTemp_new = cnts_Kidney_new_Sorted[i_2]
                            if cv2.contourArea(cntTemp_new)==0:
                                break

                            cntHull = cv2.convexHull(cntTemp_new, returnPoints=True)
                            #mask_Kidney_son = np.ones(np.shape(img_array))
                            #cv2.drawContours(mask_Kidney_son,[cntHull],0,(0,255,0),thickness=cv2.FILLED)
                            #plt.imshow(mask_Kidney_son)


                            if (cv2.contourArea(cntHull) < 0.5*cv2.contourArea(cntTemp) and cv2.contourArea(cntHull) > 0.03*cv2.contourArea(cntTemp)):
                                
                                Kidney_son = cntHull

                                mask_Kidney_son = np.ones(np.shape(img_array))
                                cv2.drawContours(mask_Kidney_son,[Kidney_son],0,(0,255,0),thickness=cv2.FILLED)
                                mask_Kidney_son = np.abs(mask_Kidney_son + 1 - 2)
                                mask_Kidney = mask_Kidney - mask_Kidney_son
                                mask_Kidney[mask_Kidney<0]=0

                if Kidney!=[]:
                    #print(' Kindey Found')
                    return mask_Kidney