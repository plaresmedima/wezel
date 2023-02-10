"""
A collection of methods for image segmentation.

Requirements:

dipy
"""


from wezel.menu.numpy import (
    ThresholdAbsolute,
    ThresholdRelative,
)
from wezel.menu.scipy import (
    DistanceTransformEdt,
    BinaryFillHoles, 
    Label2D, Label3D,
)
from wezel.menu.dipy import (
    MedianOtsu,
)
from wezel.menu.skimage import (
    CannyFilter,
    Watershed2D, 
    Watershed3D,
    ConvexHullImage,
    Skeletonize,
    Skeletonize_3D,
    PeakLocalMax3D,
)
from wezel.menu.sklearn import (
    KMeans,
)


def all(parent):   
    parent.action(ThresholdAbsolute, text="Threshold (absolute values)")
    parent.action(ThresholdRelative, text="Threshold (relative values)")
    parent.action(MedianOtsu, text="Median Otsu segmentation")
    parent.action(KMeans, text='K-Means clustering')
    parent.separator()
    parent.action(CannyFilter, text="Canny Edge Detection")
    parent.separator()
    parent.action(BinaryFillHoles, text="Fill holes")
    parent.action(Label2D, text="Label structures (2D)")
    parent.action(Label3D, text="Label structures (3D)")
    parent.action(ConvexHullImage, text="Convex hull (2D)")
    parent.action(Skeletonize, text="Skeletonize (2D)")
    parent.action(Skeletonize_3D, text="Skeletonize (3D)")
    parent.action(DistanceTransformEdt, text="Euclidian distance transform (3D)")
    parent.action(PeakLocalMax3D, text="Local maxima (3D)")
    parent.action(Watershed2D, text="Watershed (2D)")
    parent.action(Watershed3D, text="Watershed (3D)")


