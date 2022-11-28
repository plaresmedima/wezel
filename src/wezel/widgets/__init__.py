"""
`widgets` is a collection of PyQt widgets that can be used as components 
in `wezel` applications.

"""

#from .log_to_GUI import *

from .dbimage import (
    ImageWindow,
    ImageBrightness, 
    ImageContrast,
)
from .dbseries import (
    SeriesSliders,
    SeriesCanvas,
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