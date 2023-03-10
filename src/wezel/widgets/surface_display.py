import numpy as np
import scipy.ndimage as ndi
import pyvista as pv

from PyQt5.QtWidgets import (
    QVBoxLayout,
)

from pyvistaqt import QtInteractor
import wezel


class SurfaceDisplay(wezel.gui.MainWidget):

    def __init__(self, series=None):
        super().__init__()
        self.initUI()
        self.setSeries(series)

    def initUI(self):

        # Widgets
        self.plotter = QtInteractor(self)

        # Layout
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.plotter)
        self.setLayout(layout)


    def setSeries(self, series):

        if series is None:
            return

        series.status.message('Getting array dimensions...')

        affine = series.affine_matrix()
        if isinstance(affine, list):
            msg = 'Cannot display this as a single volume \n'
            msg += 'This series contains multiple slice groups.'
            series.dialog.information(msg)
            return
        else:
            affine = affine[0]
        column_spacing = np.linalg.norm(affine[:3, 0])
        row_spacing = np.linalg.norm(affine[:3, 1])
        slice_spacing = np.linalg.norm(affine[:3, 2])
        spacing = (column_spacing, row_spacing, slice_spacing)  # mm

        # Get array sorted by slice location
        arr, _ = series.array('SliceLocation', pixels_first=True)

        # If there are multiple volumes, show only the first one
        arr = arr[...,0]

        series.status.message('Preprocessing mask...')

        # Scale in the range [0,1] so it can be treated as mask
        max = np.amax(arr)
        min = np.amin(arr)
        arr -= min
        arr /= max-min

        # add zeropadding at the boundary slices
        shape = list(arr.shape)
        npad = 4
        shape[-1] = shape[-1] + 2*npad
        array = np.zeros(shape)
        array[:,:,npad:-npad] = arr

        # Smooth surface
        array = ndi.gaussian_filter(array, 1.0)

        series.status.message('Displaying surface...')

        # Extracting surface
        grid = pv.UniformGrid(dimensions=array.shape, spacing=spacing)
        surf = grid.contour([0.5], array.flatten(order="F"), method='marching_cubes')
        # This works but does not help with the visualisation
        # surf = surf.reconstruct_surface()

        try:
            self.plotter.add_mesh(surf, 
                scalars = np.linalg.norm(surf.points, axis=1), 
                show_edges = False, 
                smooth_shading = True, 
                specular = 0, 
                cmap = "plasma", 
                show_scalar_bar = False,
                opacity = 1.0)
        except Exception as msg:
            series.dialog.information(str(msg))

        ## Note: In script, plotting can also be done as:
        # surf.plot(scalars=dist, show_edges=False, smooth_shading=True, specular=5, cmap="plasma", show_scalar_bar=False)

        # Extracting surfaces with skimage causes erratic crashes of PolyData
        # verts, faces, _, _ = skimage.measure.marching_cubes(array, level=0.5, spacing=spacing, step_size=1.0)
        # cloud = pv.PolyData(verts, faces, n_faces=faces.shape[0])
        # surf = cloud.reconstruct_surface()

