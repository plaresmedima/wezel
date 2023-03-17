from wezel.gui import Menu
from wezel.plugins import (
    numpy,
    scipy,
    dipy,
    skimage,
    sklearn,
)


menu = Menu('Segment')
menu.add(numpy.action_absolute_threshold)
menu.add(numpy.action_relative_threshold)
menu.add(dipy.action_median_otsu)
menu.add(sklearn.action_k_means)
menu.add(sklearn.action_sequential_k_means)
menu.add(skimage.action_watershed_2d)
menu.add(skimage.action_watershed_3d)
menu.add_separator()
menu.add(skimage.action_canny)
menu.add(scipy.action_distance_transform_edit_3d)
menu.add(skimage.action_peak_local_max_3d)
menu.add_separator()
menu.add(scipy.action_label_2d)
menu.add(scipy.action_label_3d)
menu.add(scipy.action_extract_largest_cluster_3d)
menu.add(skimage.action_convex_hull_image_2d)
menu.add(skimage.action_convex_hull_image_3d)
menu.add(skimage.action_skeletonize_2d)
menu.add(skimage.action_skeletonize_3d)
menu.add_separator()
menu.add(skimage.action_opening_2d)
menu.add(skimage.action_opening_3d)
menu.add(skimage.action_closing_2d)
menu.add(skimage.action_closing_3d)
menu.add_separator()
menu.add(skimage.action_area_opening_2d)
menu.add(skimage.action_area_opening_3d)
menu.add(skimage.action_area_closing_2d)
menu.add(skimage.action_area_closing_3d)
menu.add_separator()
menu.add(scipy.action_binary_fill_holes)
menu.add(skimage.action_remove_small_holes_2d)
menu.add(skimage.action_remove_small_holes_3d)