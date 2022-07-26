__all__ = [
    'SelectImageColorTable',
    'RestoreImageButton', 
    'SaveImageButton', 
    'ExportImageButton', 
    'DeleteImageButton', 
    'PixelValueLabel', 
]

from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QComboBox, QPushButton, QLabel
from PyQt5.QtGui import QIcon

from . import icons

listColors =  ['gray', 'cividis',  'magma', 'plasma', 'viridis', 
    'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
    'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
    'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn',
    'binary', 'gist_yarg', 'gist_gray', 'bone', 'pink',
    'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
    'hot', 'afmhot', 'gist_heat', 'copper',
    'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
    'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic',
    'twilight', 'twilight_shifted', 'hsv',
    'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
    'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg', 'turbo',
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar', 'custom']

QComboBoxStyleSheet = """

QComboBox::drop-down 
{
    border: 0px; /* This seems to replace the whole arrow of the combo box */
}
QComboBox:down-arrow 
{
    image: url("wezel/widgets/icons/fugue-icons-3.5.6/spectrum.png");
}
"""


class SelectImageColorTable(QComboBox):  

    newColorTable = pyqtSignal(str)

    def __init__(self, image=None):
        super().__init__() 
                                         
        self.blockSignals(True)
        self.addItems(listColors)
        self.blockSignals(False)
        self.setToolTip('Change colors')
        #self.setFixedHeight(28)
        self.setMaximumWidth(120)
        self.setStyleSheet(QComboBoxStyleSheet)
        self.currentIndexChanged.connect(self.colorTableChanged)

        self.setData(image)
#        if image is None:
#            colorTable = 'gray'
#        else:
#            colorTable, _ = image.get_colormap()
#        self.image = image

    def setData(self, image):

        self.image = image
        self.setValue()
    
    def setValue(self):

        if self.image is None:
            colorTable = 'gray'
        else:
            colorTable, _ = self.image.get_colormap()
        self.blockSignals(True)
        self.setCurrentText(colorTable)
        self.blockSignals(False)
        
    def colorTableChanged(self):

        if self.image is None: return
        
        colorTable = self.currentText()
        if colorTable.lower() == 'custom':
            colorTable = 'gray'             
            self.blockSignals(True)
            self.setCurrentText(colorTable)
            self.blockSignals(False) 
        self.image.set_colormap(colormap=colorTable)
        self.newColorTable.emit(colorTable)


class DeleteImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()

    #    self.image = image
        
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.bin_metal))
        self.setToolTip('Delete image')
        self.clicked.connect(self.delete) 

        self.setData(image)

    def delete(self):
 
        if self.image is None:
            return
        self.image.remove()
        self.buttonClicked.emit()

    def setData(self, image):
        self.image = image


class ExportImageButton(QPushButton):

    def __init__(self, image=None):
        super().__init__()
 
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.blue_document_export))
        self.setToolTip('Export as .png')
        self.clicked.connect(self.export)
        self.setData(image)

    def setData(self, image):
        self.image = image

    def export(self):
        """Export as png."""

        if self.image is None: 
            return
        fileName = self.image.dialog.file_to_save(filter = "*.png")
        if fileName is None: 
            return
        self.image.export_as_png(fileName[:-4])


class RestoreImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()
         
        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.arrow_curve_180_left))
        self.setToolTip('Undo changes')
        self.clicked.connect(self.restore) 

        self.setData(image)

    def setData(self, image):
        self.image = image

    def restore(self):

        if self.image is None: return
        self.image.restore()
        self.buttonClicked.emit()


class SaveImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()

        self.setFixedSize(24, 24)
        self.setIcon(QIcon(icons.disk))
        self.setToolTip('Save changes')
        self.clicked.connect(self.save) 

        self.setData(image)

    def save(self):
 
        if self.image is None:
            return
        self.image.save()
        self.buttonClicked.emit()

    def setData(self, image):
        self.image = image


class PixelValueLabel(QLabel):
    """
    Label showing the pixel value.
    """

    def __init__(self, image=None):
        super().__init__()

        self.image = image
        self.setMargin(0)
        self.setTextFormat(Qt.PlainText)

    def setData(self, image):
        self.image = image

    def setValue(self, coordinates):
        
        text = ""
        if self.image is not None:
            if len(coordinates) == 2:
                x = coordinates[0]
                y = coordinates[1]
                if 0 <= x < self.image.Columns:
                    if 0 <= y < self.image.Rows:
                        pixelArray = self.image.array()
                        pixelValue = pixelArray[x,y]
                        text = "Signal ({}, {}) = {}".format(x, y, pixelValue)
        self.setText(text)


