import numpy as np
import scipy.ndimage as ndi
import skimage
import pyvista as pv

from PyQt5.QtWidgets import (
    QVBoxLayout,
)

from pyvistaqt import QtInteractor
import wezel


class SurfaceDisplay(wezel.gui.MainWidget):

    def __init__(self):
        super().__init__()

        # Widgets
        self.plotter = QtInteractor(self)

        # Display
        self._view = SurfaceDisplayView(self)

    def setSeries(self, series):

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
        shape[-1] = shape[-1] + 2*4
        array = np.zeros(shape)
        array[:,:,4:-4] = arr

        # Smooth surface
        array = ndi.gaussian_filter(array, 1.5)

    
        series.status.message('Extracting surface...')
        verts, faces, _, _ = skimage.measure.marching_cubes(array, level=0.5, step_size=1.0)
        cloud = pv.PolyData(verts, faces)
        surf = cloud.reconstruct_surface()

    
        series.status.message('Displaying surface...')
        self.plotter.add_mesh(surf, 
            scalars = np.linalg.norm(surf.points, axis=1), 
            show_edges = False, 
            smooth_shading = True, 
            specular = 0, 
            cmap = "plasma", 
            show_scalar_bar = False,
        )

        ## Note: In script, plotting can also be done as:
        # surf.plot(scalars=dist, show_edges=False, smooth_shading=True, specular=5, cmap="plasma", show_scalar_bar=False)


        ## Note: Extracting surface using pyVista does not work for some reason:
        # grid = pv.UniformGrid(
        #     dimensions=array.shape,
        #     spacing=(1, 1, 1),
        #     origin=(0, 0, 0),
        # )
        # cloud = grid.contour([0.5], array.flatten(), method='marching_cubes')
        # surf = cloud.reconstruct_surface()


class SurfaceDisplayView():
    def __init__(self, controller):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(controller.plotter)
        controller.setLayout(layout)