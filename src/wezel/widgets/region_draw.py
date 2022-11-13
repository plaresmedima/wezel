import timeit

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, 
                            QVBoxLayout, 
                            QToolBar)

from wezel import widgets

class SeriesViewerROI(QWidget):
    """
    GUI for drawing and editing Regions of Interest
    """

    newRegions = pyqtSignal()

    def __init__(self, series=None, dimensions=[]): 
        super().__init__()
        #Faster access but loading times are prohibitive for large series
        #series.read()
        self._setWidgets(dimensions=dimensions)
        self._setLayout()
        self._setConnections()
        if series is not None:
            self.setData(series)
        self._setMaskViewTool()

    def _setWidgets(self, dimensions=[]):
        self.imageSliders = widgets.SeriesSliders(dimensions=dimensions)
        self.regionList = widgets.RegionList()
        self.maskView = widgets.MaskView()
        self.maskViewToolBox = widgets.MaskViewToolBox()
        self.pixelValue = widgets.PixelValueLabel()
        self.colors = widgets.ImageColors()

    def _setLayout(self):
        toolBar = QToolBar()
        toolBar.addWidget(self.maskViewToolBox)
        toolBar.addWidget(self.regionList)
        toolBar.addSeparator()
        toolBar.addWidget(self.colors) 
        toolBar.addSeparator()
        toolBar.addWidget(self.pixelValue)
        toolBar.setStyleSheet("background-color: white")  
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(toolBar)
        layout.addWidget(self.maskView) 
        layout.addWidget(self.imageSliders) 
        self.setLayout(layout)

    def _setConnections(self):
        self.maskView.mousePositionMoved.connect(self._mouseMoved)
        self.maskView.newMask.connect(self._newMask)
        self.maskViewToolBox.newTool.connect(self._setMaskViewTool)
        self.regionList.currentRegionChanged.connect(self._currentRegionChanged)
        self.imageSliders.valueChanged.connect(self._currentImageChanged)
        self.colors.valueChanged.connect(self._currentImageEdited)
        self.maskView.imageUpdated.connect(self.colors.setValue)

    def closeEvent(self, event): 
        if not self.imageSliders.series.exists():
            return
        self.maskView.setMaskArray()
        newRegions = self.regionList.saveRegions()
        if newRegions:
            self.newRegions.emit()

    def refresh(self):
        if self.imageSliders.series is None:
            self.close()
            return
        if not self.imageSliders.series.exists():
            self.close()
            return
        self.regionList.refresh()

    def setData(self, series=None):
        self.imageSliders.setData(series, blockSignals=True)
        self.regionList.series = series
        image = self.imageSliders.image
        if image is None:
            msg = series.label() + ' is an empty series.' 
            msg += ' \n Nothing to see here..'
            series.dialog.information(msg)
            self.setEnabled(False)
            return
        image.read()
        mask = self.regionList.getMask(image)
        self.colors.setData(image)
        self.maskView.setData(image, mask)
        self.pixelValue.setData(image)

    def _setMaskViewTool(self):
        tool = self.maskViewToolBox.getTool()
        self.maskView.setEventHandler(tool)

    def _mouseMoved(self):
        tool = self.maskViewToolBox.getTool()
        self.pixelValue.setValue([tool.x, tool.y])
        
    def _currentImageChanged(self):
        self.maskView.setMaskArray()
        image = self.imageSliders.image
        if image is not None:
            image.read()
        self.colors.setData(image)
        mask = self.regionList.getMask(image)
        self.maskView.setData(image, mask)
        self.pixelValue.setData(image)

    def _currentImageEdited(self):
        self.maskView.imageItem.setPixMap()
        self.maskView.imageItem.update()
        
    def _currentRegionChanged(self):
        image = self.imageSliders.image
        mask = self.regionList.getMask(image)
        self.maskView.setMask(mask)
        self.maskViewToolBox.setEnabled(self.regionList.regions!=[])

    def _newMask(self):
        region = self.regionList.region()
        image = self.maskView.image
        mask = image.copy_to_series(region)
        mask.read()
        self.maskView.maskItem.mask = mask
        mask.WindowCenter = 1
        mask.WindowWidth = 2