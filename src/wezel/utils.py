import numpy as np
from PyQt5.QtGui import QImage



def makeQImage(imgData, copy=True):
    # HELPER FUNCTION ADAPTED FROM pyQtGraph
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


