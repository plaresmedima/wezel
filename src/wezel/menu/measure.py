"""
A collection of methods for measuring numbers from images.
"""


from wezel.menu.skimage import VolumeFeatures
from wezel.menu.scipy import ROIstatistics



def all(parent):   

    parent.action(ROIstatistics, text="ROI statistics")
    parent.action(VolumeFeatures, text="3D Volume Features")
    




