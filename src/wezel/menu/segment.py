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
    BinaryFillHoles, 
    Label,
)
from wezel.menu.dipy import (
    MedianOtsu,
)
from wezel.menu.skimage import (
    CannyFilter, 
    Watershed2DLabels, 
    Watershed2D, 
    Watershed3D,
    ConvexHullImage,
    Skeletonize,
    Skeletonize_3D,
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
    parent.action(Label, text="Label structures")
    parent.action(ConvexHullImage, text="Determine convex Hull")
    parent.action(Skeletonize, text="Skeletonize (2D)")
    parent.action(Skeletonize_3D, text="Skeletonize (3D)")
    parent.separator()
    parent.action(Watershed2DLabels, text="Watershed 2D (from labels)")
    # Check on github - accidentally deleted?
    #parent.action(Watershed3DLabels, text="Watershed 3D (from labels)")
    parent.action(Watershed2D, text="Watershed 2D (no labels)")
    parent.action(Watershed3D, text="Watershed 3D (no labels)")


