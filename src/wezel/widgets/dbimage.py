import timeit
import numpy as np
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import (QToolBar,
    QAction, QComboBox, QPushButton, QLabel, 
    QWidget, QDoubleSpinBox, QHBoxLayout, QVBoxLayout)
from PyQt5.QtGui import QIcon, QPixmap

from wezel import widgets, icons

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
    image: url("icons/fugue_icons/spectrum.png");
    width: 14px;
    height: 14px;
}
"""

# class ImageColors(QWidget):
#     """Widget to set and manage color and window settings of a Series"""

#     valueChanged = pyqtSignal(list)  # emitted when the color settings are changed by the widget

#     def __init__(self, image=None):
#         super().__init__()
#         self._setWidgets()
#         self._setConnections()
#         self._setLayout()
#         self.setData(image)

#     def _setWidgets(self):
#         self.mode = widgets.LockUnlockButton(toolTip = 'Lock image settings')
#         self.colors = SelectImageColorMap()
#         self.brightness = ImageBrightness()
#         self.contrast = ImageContrast()

#     def _setConnections(self):
#         self.colors.newColorMap.connect(self._valueChanged)
#         self.brightness.valueChanged.connect(self._valueChanged)
#         self.contrast.valueChanged.connect(self._valueChanged)

#     def _setLayout(self):
#         layout = QHBoxLayout()
#         layout.setContentsMargins(0,0,0,0)
#         layout.setSpacing(0)
#         layout.addWidget(self.mode)
#         layout.addWidget(self.colors)
#         layout.addWidget(self.brightness)
#         layout.addWidget(self.contrast)
#         #self.setStyleSheet("background-color: white")
#         self.setLayout(layout)

#     def _valueChanged(self):
#         self.valueChanged.emit(self.getValue())

#     def setData(self, image):
#         if image is None:
#             return
#         if self.colors.image is None:
#             set = True
#         else:
#             set = not self.mode.isLocked
#         self.colors.setData(image, set)
#         self.brightness.setData(image, set)
#         self.contrast.setData(image, set)

#     def getValue(self):
#         return [
#             self.colors.getValue(), 
#             self.brightness.getValue(),
#             self.contrast.getValue(),
#         ]

#     def setValue(self, colormap=None, WindowCenter=None, WindowWidth=None):
#         self.colors.setValue(colormap)
#         self.brightness.setValue(WindowCenter)
#         self.contrast.setValue(WindowWidth)


class ImageWindow(QWidget):
    """Widget to set and manage color and window settings of a Series"""

    valueChanged = pyqtSignal(list)  # emitted when the color settings are changed by the widget

    def __init__(self, image=None, layout=True):
        super().__init__()
        self._setWidgets(layout)
        self._setConnections()
        if layout:
            self._setLayout()
        self.setData(image)

    def _setWidgets(self, layout):
        self.mode = LockUnlockWidget(toolTip = 'Lock image settings')
        self.brightness = ImageBrightness(layout=layout)
        self.contrast = ImageContrast(layout=layout)

    def _setConnections(self):
        self.brightness.valueChanged.connect(self._valueChanged)
        self.contrast.valueChanged.connect(self._valueChanged)

    def _setLayout(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        #layout.addWidget(self.mode)
        layout.addWidget(self.brightness)
        layout.addWidget(self.contrast)
        #self.setStyleSheet("background-color: white")
        self.setLayout(layout)

    def _valueChanged(self):
        self.valueChanged.emit(self.getValue())

    def setData(self, image, set=None):
        if image is None:
            return
        if set is None:
            set = not self.mode.isLocked
        self.brightness.setData(image, set)
        self.contrast.setData(image, set)

    def getValue(self):
        return [
            self.brightness.getValue(),
            self.contrast.getValue(),
        ]

    def setValue(self, WindowCenter=None, WindowWidth=None):
        self.brightness.setValue(WindowCenter)
        self.contrast.setValue(WindowWidth)


class ImageContrast(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, image=None, layout=True):
        super().__init__()
        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.contrast))
        #self.label.setFixedSize(24, 24)
        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Contrast")
        self.spinBox.setMinimum(0)
        self.spinBox.setMaximum(1000000000.00)
        self.spinBox.setWrapping(False)
        self.spinBox.setFixedWidth(115)
        if layout:
            self.layout = QHBoxLayout()
            self.layout.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(2)
            self.layout.addWidget(self.spinBox)
            self.layout.addWidget(self.label)
            #self.setMaximumWidth(120)
            self.setLayout(self.layout)
        self.setData(image)

    def setData(self, image, set=True):
        self.spinBox.blockSignals(True)
        self.image = image
        if image is None: 
            self.spinBox.setValue(1)  
            self.spinBox.setSingleStep(0.1)
        else:
            if set:  # adjust spinbox value to image contrast
                value = self.image.WindowWidth
                self.spinBox.setValue(value)
                self.setSpinBoxStepSize()
            else:    # adjust image contrast to spinbox value 
                value = self.spinBox.value()
                self.image.WindowWidth = value
        self.spinBox.blockSignals(False)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, value):
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(value)
        self.spinBox.blockSignals(False)
        if self.image is not None:
            self.image.WindowWidth = value
        self.setSpinBoxStepSize()

    def setSpinBoxStepSize(self):
        if self.image is None: 
            return
        min = self.image.SmallestImagePixelValue
        max = self.image.LargestImagePixelValue
        if (min is None) or (max is None):
            array = self.image.get_pixel_array()
            min = np.amin(array)
            max = np.amax(array)
            self.image.SmallestImagePixelValue = min
            self.image.LargestImagePixelValue = max
        width = max-min
        spinBoxStep = float(width / 10)
        self.spinBox.setSingleStep(spinBoxStep)
        #centre, width = self.image.window # should be the actual value range, not the window
        #minimumValue = centre - width/2
        #maximumValue = centre + width/2
        # if (minimumValue < 1 and minimumValue > -1) and (maximumValue < 1 and maximumValue > -1):
        #     spinBoxStep = float(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        # else:
        #     spinBoxStep = int(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
        # self.spinBox.setSingleStep(spinBoxStep)

    def spinBoxValueChanged(self):
        """Update Window Width of the image."""
        
        if self.image is None:
            return
        width = self.spinBox.value()   
        self.image.WindowWidth = width
        self.valueChanged.emit(width)


class ImageBrightness(QWidget):

    valueChanged = pyqtSignal(float)

    def __init__(self, image=None, layout=True):
        super().__init__() 
        self.label = QLabel()
        self.label.setPixmap(QPixmap(icons.brightness))
        #self.label.setFixedSize(24, 24)
        self.spinBox = QDoubleSpinBox()
        self.spinBox.valueChanged.connect(self.spinBoxValueChanged)
        self.spinBox.setToolTip("Adjust Brightness")
        self.spinBox.setMinimum(-1000000000.00)
        self.spinBox.setMaximum(+1000000000.00)
        self.spinBox.setWrapping(False)
        self.spinBox.setFixedWidth(115)
        if layout:
            self.layout = QHBoxLayout()
            self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
            self.layout.setContentsMargins(0,0,0,0)
            self.layout.setSpacing(2)
            self.layout.addWidget(self.spinBox)
            self.layout.addWidget(self.label)
            #self.setMaximumWidth(120)
            self.setLayout(self.layout)
        self.setData(image)

    def setData(self, image, set=True):
        self.spinBox.blockSignals(True)
        self.image = image
        if image is None: 
            self.spinBox.setValue(1)  
            self.spinBox.setSingleStep(0.1)
        else:
            if set:  # adjust spinbox value to image contrast
                value = self.image.WindowCenter
                self.spinBox.setValue(value)
                self.setSpinBoxStepSize()
            else:    # adjust image contrast to spinbox value 
                value = self.spinBox.value()
                self.image.WindowCenter = value
        self.spinBox.blockSignals(False)

    def getValue(self):
        return self.spinBox.value()

    def setValue(self, center):
        self.spinBox.blockSignals(True)
        self.spinBox.setValue(center)
        self.spinBox.blockSignals(False)
        if self.image is not None: 
            self.image.WindowCenter = center
        self.setSpinBoxStepSize()

    def setSpinBoxStepSize(self):
        if self.image is None: 
            return
        min = self.image.SmallestImagePixelValue
        max = self.image.LargestImagePixelValue
        if (min is None) or (max is None):
            array = self.image.get_pixel_array()
            min = np.amin(array)
            max = np.amax(array)
            self.image.SmallestImagePixelValue = min
            self.image.LargestImagePixelValue = max
        center = (max+min)/2
        spinBoxStep = float(center / 10)
        self.spinBox.setSingleStep(spinBoxStep)

    # def setSpinBoxStepSize(self):
    #     if self.image is None: 
    #         return
    #     centre, width = self.image.window
    #     minimumValue = centre - width/2
    #     maximumValue = centre + width/2
    #     if (minimumValue < 1 and minimumValue > -1) and (maximumValue < 1 and maximumValue > -1):
    #         spinBoxStep = float(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
    #     else:
    #         spinBoxStep = int(width / 10) # It takes 100 clicks to walk through the middle 50% of the signal range
    #     self.spinBox.setSingleStep(spinBoxStep)

    def spinBoxValueChanged(self):
        if self.image is None:
            return
        center = self.spinBox.value()
        self.image.WindowCenter = center
        self.valueChanged.emit(center)

# class SelectImageColorMap(QComboBox):  

#     newColorMap = pyqtSignal(str)

#     def __init__(self, image=None):
#         super().__init__()                              
#         self.blockSignals(True)
#         self.addItems(listColors)
#         self.blockSignals(False)
#         self.setToolTip('Change colors')
#         self.setMaximumWidth(120)
#         #self.setStyleSheet(QComboBoxStyleSheet)
#         self.currentIndexChanged.connect(self.colorMapChanged)
#         self.setData(image)

#     def setData(self, image, set=True):
#         self.blockSignals(True)
#         self.image = image
#         if image is None:
#             self.setCurrentText('gray')
#         else:
#             if set: # set list to image colormap
#                 colormap = self.image.colormap
#                 self.setCurrentText(colormap)
#             else:   # set image colormap to current value
#                 colormap = self.getValue()
#                 self.image.colormap = colormap
#         self.blockSignals(False)

#     def setValue(self, colormap):
#         self.blockSignals(True)
#         self.setCurrentText(colormap)
#         self.blockSignals(False)
#         if self.image is not None:
#             self.image.colormap = colormap

#     def getValue(self):
#         return str(self.currentText())
        
#     def colorMapChanged(self):
#         if self.image is None: 
#             return
#         colormap = self.currentText()
#         # if colormap.lower() == 'custom':
#         #     colormap = 'gray'             
#         #     self.blockSignals(True)
#         #     self.setCurrentText(colormap)
#         #     self.blockSignals(False) 
#         self.image.colormap = colormap
#         self.newColorMap.emit(colormap)

class LockUnlockWidget(QToolBar):

    toggled = pyqtSignal()

    def __init__(self, toolTip = 'Lock state'):
        super().__init__()
        self.isLocked = True
        self.icon_lock = QIcon(icons.lock) 
        self.icon_lock_unlock = QIcon(icons.lock_unlock) 
        self.mode = QAction()
        self.mode.setIcon(self.icon_lock)
        self.mode.setToolTip(toolTip)
        self.mode.triggered.connect(self.toggle) 
        self.addAction(self.mode)

    def toggle(self):
        if self.isLocked == True:
            self.mode.setIcon(self.icon_lock_unlock)
            self.isLocked = False
        elif self.isLocked == False:
            self.mode.setIcon(self.icon_lock)
            self.isLocked = True  
        self.toggled.emit()

# class LockUnlockButton(QPushButton):

#     toggled = pyqtSignal()

#     def __init__(self, toolTip = 'Lock state'):
#         super().__init__()
#         self.isLocked = True
#         self.icon_lock = QIcon(icons.lock) 
#         self.icon_lock_unlock = QIcon(icons.lock_unlock) 
#         self.setFixedSize(24, 24)
#         self.setIcon(self.icon_lock)
#         self.setToolTip(toolTip)
#         self.clicked.connect(self.toggle) 

#     def toggle(self):
#         if self.isLocked == True:
#             self.setIcon(self.icon_lock_unlock)
#             self.isLocked = False
#         elif self.isLocked == False:
#             self.setIcon(self.icon_lock)
#             self.isLocked = True  
#         self.toggled.emit()


class DeleteImageButton(QPushButton):

    buttonClicked = pyqtSignal()

    def __init__(self, image=None):
        super().__init__()
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
        if self.image is None: 
            return
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

