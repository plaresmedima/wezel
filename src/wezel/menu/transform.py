from wezel.menu.package_dipy import (
    CoregisterToDiPy,
)
from wezel.menu.package_elastix import (
    CoregisterToElastix,
)
from wezel.menu.package_skimage import (
    CoregisterToSkImage, 
    CoregisterSeries, 
    MDRegConstant2D, 
    MDRegConstant3D,
)
from wezel.menu.package_scipy import (
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