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
    Label2D, 
    Label3D,
    ExtractLargestCluster3D,
)
from wezel.menu.dipy import (
    MedianOtsu,
)
from wezel.menu.skimage import (
    CannyFilter,
    Watershed2D, 
    Watershed3D,
    ConvexHullImage,
    ConvexHullImage3D,
    Skeletonize,
    Skeletonize_3D,
    PeakLocalMax3D,
    AreaOpening2D,
    AreaOpening3D,
    AreaClosing2D,
    AreaClosing3D,
    Opening2D,
    Opening3D,
    Closing2D,
    Closing3D,
    RemoveSmallHoles2D,
    RemoveSmallHoles3D,
)
from wezel.menu.sklearn import (
    KMeans,
    SequentialKMeans,
)


def all(parent):   
    parent.action(ThresholdAbsolute, text="Threshold (absolute values)")
    parent.action(ThresholdRelative, text="Threshold (relative values)")
    parent.action(MedianOtsu, text="Median Otsu segmentation")
    parent.action(KMeans, text='K-Means clustering')
    parent.action(SequentialKMeans, text='Sequential K-Means clustering')
    parent.action(Watershed2D, text="Watershed (2D)")
    parent.action(Watershed3D, text="Watershed (3D)")
    parent.separator()
    parent.action(CannyFilter, text="Canny Edge Detection")
    parent.action(DistanceTransformEdt, text="Euclidian distance transform (3D)")
    parent.action(PeakLocalMax3D, text="Local maxima (3D)")
    parent.separator()
    parent.action(Label2D, text="Label structures (2D)")
    parent.action(Label3D, text="Label structures (3D)")
    parent.action(ExtractLargestCluster3D, text="Extract largest cluster (3D)")
    parent.action(ConvexHullImage, text="Convex hull (2D)")
    parent.action(ConvexHullImage3D, text="Convex hull (3D)")
    parent.action(Skeletonize, text="Skeletonize (2D)")
    parent.action(Skeletonize_3D, text="Skeletonize (3D)")
    parent.separator()
    parent.action(Opening2D, text="Remove bright spots (2D)")
    parent.action(Opening3D, text="Remove bright spots (3D)")
    parent.action(Closing2D, text="Remove dark spots (2D)")
    parent.action(Closing3D, text="Remove dark spots (3D)")
    parent.separator()
    parent.action(AreaOpening2D, text="Remove bright spots smaller than.. (2D)")
    parent.action(AreaOpening3D, text="Remove bright spots smaller than.. (3D)")
    parent.action(AreaClosing2D, text="Remove dark spots smaller than.. (2D)")
    parent.action(AreaClosing3D, text="Remove dark spots smaller than.. (3D)")
    parent.separator()
    parent.action(BinaryFillHoles, text="Fill holes in labels")
    parent.action(RemoveSmallHoles2D, text="Fill holes in labels smaller than.. (2D)")
    parent.action(RemoveSmallHoles3D, text="Fill holes in labels smaller than.. (3D)")





