"""
`widgets` is a collection of PyQt widgets that can be used as components 
in `wezel` applications.

"""

#from .log_to_GUI import *

from .dbimage import (
    ImageWindow,
)
from .series_sliders import (
    SeriesSliders,
)
from .series_display_4d import (
    SeriesDisplay4D,
)
from .series_display import (
    SeriesDisplay,
)
from .surface_display import (
    SurfaceDisplay,
)
from .plot_display import (
    PlotDisplay,
)
from .table_display import (
    TableDisplay,
)
from .plot_curve import (
    PlotCurve,
)
from .qrangeslider import (
    QRangeSlider,
)
from .sliders import (
    IndexSlider, 
    LabelSlider, 
    CheckBoxSlider,
)
from .main_mdi import (
    MainMultipleDocumentInterface, 
)
from .message import (
    Dialog, 
    StatusBar,
)
from .user_input import (
    UserInput,
)
from .dbdatabase import (
    DICOMFolderTree,
)
from .region_list import (
    RegionList,
)
from .file_display import (
    ImageLabel,
)
from .dicom_header import (
    SeriesViewerMetaData,
)