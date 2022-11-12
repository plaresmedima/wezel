"""
`widgets` is a collection of PyQt widgets that can be used as components 
in `wezel` applications.

"""

#from .series_display_dev import *
#from .folder import *
#from .log_to_GUI import *

from .dbimage import (
    LockUnlockButton,
    ImageColors, 
    SelectImageColorMap,
    RestoreImageButton, 
    SaveImageButton, 
    ExportImageButton, 
    DeleteImageButton, 
    PixelValueLabel, 
    ImageBrightness, 
    ImageContrast,
)
from .dbseries import (
    SeriesSliders,
)
from .array_display import (
    FourDimViewer,
)
from .array_view import (
    ArrayViewToolBox, 
    ArrayView,
)
from .curve_plotters import (
    PlotCurve,
)
from .image_view import (
    ImageView, 
    ImageViewCursor, 
    ImageViewZoom,
)
from .mask_view import (
    MaskView, 
    MaskViewBrush, 
    MaskViewPenFreehand,
    MaskViewPenRectangle, 
    MaskViewPenPolygon, 
    MaskViewPenCircle,
    MaskViewRegionGrowing,
    MaskViewDeleteROI,
    MaskViewEdgeDetection,
    MaskViewErode,
    MaskViewDilate,
)
from .sliders import (
    IndexSlider, 
    LabelSlider, 
    CheckBoxSlider,
)
from .main_mdi import (
    MainMultipleDocumentInterface, 
    Message,
)
from .drawing_tools import (
    ToolBox, 
    MaskViewToolBox,
)
from .message import (
    Dialog, 
    StatusBar,
)
from .folder_fast import (
    DICOMFolderTree,
)
from .region_list import (
    RegionList,
)
from .region_draw import (
    SeriesViewerROI,
)
from .series_display import (
    SeriesViewer,
)
from .image_display import (
    ImageViewer, 
    ImageLabel,
)
from .user_input import (
    ParameterInputDialog,
)
from .view_meta_data import (
    SeriesViewerMetaData,
)