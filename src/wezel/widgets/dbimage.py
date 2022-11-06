from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QComboBox, QPushButton, QLabel, QWidget, QDoubleSpinBox, QHBoxLayout
from PyQt5.QtGui import QIcon, QPixmap

import wezel.icons as icons

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
    'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

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



class ImageContrast(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, image=None):
        super().__init__()

        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.contrast))
        self.label.setFixedSize(24, 24)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Contrast")
        self.spinBox.setMinimum(-1000000000.00)
        self.spinBox.setMaximum(1000000000.00)
        self.spinBox.setWrapping(True)
        self.spinBox.setFixedWidth(75)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(2)
        self.layout.addWidget(self.spinBox)
        self.layout.addWidget(self.label)

        self.setMaximumWidth(120)
        self.setLayout(self.layout)

        self.setData(image)

    def setData(self, image, set=True):

        self.image = image
        if image is None: 
            self.setValue(1)  
        else:
            if set:  # adjust spinbox value to image contrast
                value = self.image.WindowWidth 
                self.setValue(value) 
            else:               # adjust image contrast to spinbox value    
                value = self.spinBox.value()
                self.image.WindowWidth = value
                #self.valueChanged.emit(value)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, width=None):

        if width is None:
            width = self.image.WindowWidth
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(width)
        self.spinBox.blockSignals(False)
        self.setSpinBoxStepSize()

    def setSpinBoxStepSize(self):

        if self.image is None: return

        centre, width = self.image.window # should be the actual value range, not the window
        minimumValue = centre - width/2
        maximumValue = centre + width/2
        if (minimumValue < 1 and minimumValue > -1) and (maximumValue < 1 and maximumValue > -1):
            spinBoxStep = float(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        else:
            spinBoxStep = int(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        self.spinBox.setSingleStep(spinBoxStep)

    def spinBoxValueChanged(self):
        """Update Window Width of the image."""
        
        if self.image is None:
            return
        self.image.message('Contrast changed!!!')
        width = self.spinBox.value()
        self.image.WindowWidth = width
        self.valueChanged.emit(width)


class ImageBrightness(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, image=None):

        super().__init__() 

        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.brightness))
        self.label.setFixedSize(24, 24)

        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Brightness")
        self.spinBox.setMinimum(-100000.00)
        self.spinBox.setMaximum(1000000000.00)
        self.spinBox.setWrapping(True)
        self.spinBox.setFixedWidth(75)

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(2)
        self.layout.addWidget(self.spinBox)
        self.layout.addWidget(self.label)

        self.setMaximumWidth(120)
        self.setLayout(self.layout)

        self.setData(image)

    def setData(self, image, set=True):

        self.image = image
        if image is None: 
            self.setValue(1)  
        else:
            if set:  # adjust spinbox value to image contrast
                value = self.image.WindowCenter
                self.setValue(value) 
            else:               # adjust image contrast to spinbox value    
                value = self.spinBox.value()
                self.image.WindowCenter = value
                # self.valueChanged.emit(value)

    def spinBoxValueChanged(self):
        """Update Window Width of the image."""
        
        if self.image is None:
            return

        self.image.message('Brightness changed!!!')

        center = self.spinBox.value()
        self.image.WindowCenter = center
        self.valueChanged.emit(center)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, center=None):

        if center is None: 
            center = self.image.WindowCenter
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(center)
        self.spinBox.blockSignals(False)
        self.setSpinBoxStepSize()        
    
    def setSpinBoxStepSize(self):

        if self.image is None: return

        centre, width = self.image.window
        minimumValue = centre - width/2
        maximumValue = centre + width/2
        if (minimumValue < 1 and minimumValue > -1) and (maximumValue < 1 and maximumValue > -1):
            spinBoxStep = float(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        else:
            spinBoxStep = int(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        self.spinBox.setSingleStep(spinBoxStep)



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
            colorTable = self.image.colormap
        self.blockSignals(True)
        self.setCurrentText(colorTable)
        self.blockSignals(False)
        
    def colorTableChanged(self):

        if self.image is None: 
            return

        self.image.message('Color table changed!!!')
        
        colorTable = self.currentText()
        if colorTable == 'gray':
            colorTable = None            
        self.image.colormap = colorTable
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
        path = self.image.dialog.directory("Where do you want to export the data?")
        self.image.export_as_png(path)


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
        self.array = self.image.array()

    def setValue(self, coordinates):
        
        text = ""
        if self.image is not None:
            if len(coordinates) == 2:
                x = coordinates[0]
                y = coordinates[1]
                #
                # THIS IS VERY SLOW FOR DATA IN MEMORY DUE TO LOOKUPS FOR UID
                #
                if 0 <= x < self.image.Columns:
                     if 0 <= y < self.image.Rows:
                #if 0 <= x < self.array.shape[0]:
                #    if 0 <= y < self.array.shape[1]:
                        pixelValue = self.array[x,y]
                        text = "Signal ({}, {}) = {}".format(x, y, pixelValue)
        self.setText(text)


