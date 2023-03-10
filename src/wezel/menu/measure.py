"""
A collection of methods for measuring numbers from images.
"""


from wezel.menu.skimage import VolumeFeatures
from wezel.menu.scipy import ROIstatistics, ROIcurve



def all(parent):   

    parent.action(VolumeFeatures, text="3D volume features")
    parent.action(ROIstatistics, text="ROI statistics")
    parent.action(ROIcurve, text="ROI curve")
    




