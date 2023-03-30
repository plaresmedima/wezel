from wezel.gui import Menu
from wezel.plugins import numpy, scipy


menu = Menu('Transform')
menu.add(scipy.action_function_of_one_series)
menu.add(scipy.action_function_of_two_series)
menu.add(scipy.action_function_of_n_series)
menu.add_separator()
menu.add(scipy.action_distance_transform_edit_3d)
menu.add_separator()
menu.add(numpy.menu_project)
menu.add_separator()
menu.add(scipy.action_zoom)
menu.add(scipy.action_resample_3d_isotropic)
menu.add(scipy.action_resample_3d)
menu.add_separator()
menu.add(scipy.action_reslice_axial)
menu.add(scipy.action_reslice_coronal)
menu.add(scipy.action_reslice_sagittal)
