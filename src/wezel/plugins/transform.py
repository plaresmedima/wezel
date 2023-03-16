from wezel.gui import Menu
from wezel.plugins import (
    numpy, 
    dipy,
    elastix,
    skimage,
    scipy,
)

menu = Menu('Transform')
menu.add(scipy.action_function_of_one_series)
menu.add(scipy.action_function_of_two_series)
menu.add_separator()
menu.add(scipy.action_zoom)
menu.add(scipy.action_resample_3d_isotropic)
menu.add(scipy.action_resample_3d)
menu.add_separator()
menu.add(scipy.action_reslice_axial)
menu.add(scipy.action_reslice_coronal)
menu.add(scipy.action_reslice_sagittal)
menu.add_separator()
menu.add(scipy.action_overlay_on)
menu.add_separator()
menu.add(skimage.action_coregistration, text='Coregister to (skimage)')
menu.add(elastix.action_coregistration, text='Coregister to (elastix)')
menu.add(dipy.action_coregister, text='Coregister to (dipy)')
menu.add_separator()
menu.add(skimage.action_coregister_series)
menu.add(skimage.action_mdr_constant_2d)
menu.add(skimage.action_mdr_constant_3d)
menu.add_separator()
menu.add(numpy.action_mean_intensity_projection)
menu.add(numpy.action_maximum_intensity_projection)