from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (QWidget, 
                            QVBoxLayout, 
                            QToolBar)

from .. import widgets

class SeriesViewerROI(QWidget):
    """
    GUI for drawing and editing Regions of Interest
    """

    dataWritten = pyqtSignal()

    def __init__(self, series=None, dimensions=[]): 
        super().__init__()

        #Faster access but loading times are prohibitive for large series
        #series.read()

        self._setWidgets(dimensions=dimensions)
        self._setConnections()
        self._setMaskViewTool()
        self._setLayout()
        if series is not None:
            self.setData(series)

    def _setWidgets(self, dimensions=[]):

        self.imageSliders = widgets.ImageSliders(dimensions=dimensions)
        self.regionList = widgets.RegionList()
        self.maskView = widgets.MaskView()
        self.maskViewToolBox = widgets.MaskViewToolBox()
        self.pixelValue = widgets.PixelValueLabel()
        self.colors = widgets.SeriesColors()

    def setData(self, series):

        self.imageSliders.setData(series, blockSignals=True)
        self.regionList.setData(series)

        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)
        self.colors.setData(series, image)
        self.maskView.setData(image, mask)
        self.pixelValue.setData(image)

        #self.maskView.fitInView(self.maskView.imageItem, Qt.KeepAspectRatio)
        #self.maskView.imageItem.update()
        
        # changes are made in memory only until a new image is displayed
        #image.read() 
        #self.image = image

    def _setConnections(self):

        self.maskView.mousePositionMoved.connect(self._mouseMoved)
        self.maskView.newMask.connect(self._newMask)
        self.maskViewToolBox.newTool.connect(self._setMaskViewTool)
        self.regionList.currentRegionChanged.connect(self._currentRegionChanged)
        self.regionList.dataWritten.connect(self.dataWritten.emit)
        self.imageSliders.valueChanged.connect(self._currentImageChanged)
        self.colors.valueChanged.connect(self._currentImageEdited)
        self.maskView.imageUpdated.connect(self.colors.setValue)

    def _currentImageEdited(self):

        self.maskView.imageItem.setPixMap()
        self.maskView.imageItem.update()

    def _setMaskViewTool(self):

        tool = self.maskViewToolBox.getTool()
        self.maskView.setEventHandler(tool)

    def _mouseMoved(self):

        tool = self.maskViewToolBox.getTool()
        self.pixelValue.setValue([tool.x, tool.y])
        
    def _currentImageChanged(self):

        #if self.image is not None:
        #    self.image.write()
        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)
        self.colors.setImage(image)
        self.maskView.setData(image, mask)
        self.pixelValue.setData(image)
        #image.read()
        #self.image = image
        
    def _currentRegionChanged(self):

        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)
        self.maskView.setMask(mask)

    def _newMask(self):

        mask = self.maskView.getMask()
        region = self.regionList.getRegion()
        mask = mask.move_to(region)
        self.maskView.setObject(mask)

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