"""
A collection of methods for transforming image geometry, 
including resampling, reslicing, coregistration.

Requires optional dependencies:

dipy
SimpleITK
itk-elastix
"""


from wezel.menu.dipy import (
    CoregisterToDiPy,
)
from wezel.menu.elastix import (
    CoregisterToElastix,
)
from wezel.menu.skimage import (
    CoregisterToSkImage, 
    CoregisterSeries, 
    MDRegConstant2D, 
    MDRegConstant3D,
)
from wezel.menu.scipy import (
    Zoom,
    Resample3Disotropic,
    Resample3D,
    ResliceAxial,
    ResliceCoronal,
    ResliceSagittal,
    OverlayOn,
    FunctionOfTwoSeries,
)



def all(parent): 
    parent.action(FunctionOfTwoSeries, text="Image calculator")
    parent.separator()
    parent.action(Zoom, text="Resample images")
    parent.action(Resample3Disotropic, text="Resample 3D volume (isotropic)")
    parent.action(Resample3D, text="Resample 3D volume")
    parent.separator()
    parent.action(ResliceAxial, text='Reslice (axial)')
    parent.action(ResliceCoronal, text='Reslice (coronal)')
    parent.action(ResliceSagittal, text='Reslice (sagittal)')
    parent.separator()
    parent.action(OverlayOn, text='Overlay on..')
    parent.separator()
    parent.action(CoregisterToSkImage, text='Coregister to (skimage)')
    parent.action(CoregisterToElastix, text='Coregister to (elastix)')
    parent.action(CoregisterToDiPy, text='Coregister to (dipy)')
    parent.separator()
    parent.action(CoregisterSeries, text='Align time series')
    parent.action(MDRegConstant2D, text='Align time series (mdreg 2D - constant)')
    parent.action(MDRegConstant3D, text='Align time series (mdreg 3D - constant)')