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
        self._setLayout()
        self._setConnections()
        if series is not None:
            self.setData(series)
        self._setMaskViewTool()

    def _setWidgets(self, dimensions=[]):

        self.imageSliders = widgets.ImageSliders(dimensions=dimensions)
        self.regionList = widgets.RegionList()
        self.maskView = widgets.MaskView()
        self.maskViewToolBox = widgets.MaskViewToolBox()
        self.pixelValue = widgets.PixelValueLabel()
        self.colors = widgets.SeriesColors()

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

    def refresh(self):
        if not self.imageSliders.series.in_database():
            self.close()
            return
        self.regionList.refresh()


    def setData(self, series=None):

        series.message('Setting data: Setting up sliders..')
        self.imageSliders.setData(series, blockSignals=True)
        series.message('Setting data: Setting up region list..')
        self.regionList.setData(series)
        series.message('Setting data: Getting image..')
        image = self.imageSliders.getImage()
        image.read()
        series.message('Setting data: Getting mask..')
        mask = self.regionList.getMask(image)
        series.message('Setting data: Setting colors..')
        self.colors.setData(series, image)
        series.message('Setting data: Setting mask View..')
        self.maskView.setData(image, mask)
        series.message('Setting data: Setting pixel value..')
        self.pixelValue.setData(image)
        series.message('Setting data: Finished..')

        #series.status.hide()

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


    def _setMaskViewTool(self):

        #self.imageSliders.series.message('setMaskViewTool: getting tool..')
        tool = self.maskViewToolBox.getTool()
        #self.imageSliders.series.message('setMaskViewTool: setting tool..')
        self.maskView.setEventHandler(tool)
        #self.imageSliders.series.message('setMaskViewTool: Finished..')

    def _mouseMoved(self):

        self.imageSliders.series.message('mouseMoved: getting tool..')
        tool = self.maskViewToolBox.getTool()
        self.imageSliders.series.message('mouseMoved: setting pixel value..')
        self.pixelValue.setValue([tool.x, tool.y])
        self.imageSliders.series.message('mouseMoved: Finished..')
        
    def _currentImageChanged(self):

        #if self.image is not None:
        #    self.image.write()
        self.imageSliders.series.message('currentImageChanged: Getting image..')
        image = self.imageSliders.getImage()
        image.read()
        self.imageSliders.series.message('currentImageChanged: Getting mask..')
        mask = self.regionList.getMask(image)
        self.imageSliders.series.message('currentImageChanged: Setting colors..')
        self.colors.setImage(image)
        self.imageSliders.series.message('currentImageChanged: Setting maskView..')
        self.maskView.setData(image, mask)
        self.imageSliders.series.message('currentImageChanged: Setting value label..')
        self.pixelValue.setData(image)
        self.imageSliders.series.message('currentImageChanged: Finished..')
        #image.read()
        #self.image = image

    def _currentImageEdited(self):

        self.imageSliders.series.message('currentImageEdited: setting image..')
        self.maskView.imageItem.setPixMap()
        self.maskView.imageItem.update()
        self.imageSliders.series.message('currentImageEdited: finished..')
        
    def _currentRegionChanged(self):

        self.imageSliders.series.message('currentRegionChanged: Getting image..')
        image = self.imageSliders.getImage()
        self.imageSliders.series.message('currentRegionChanged: Getting mask..')
        mask = self.regionList.getMask(image)
        self.imageSliders.series.message('currentRegionChanged: Setting mask..')
        self.maskView.setMask(mask)
        self.imageSliders.series.message('currentRegionChanged: Finished..')

    def _newMask(self):

        self.imageSliders.series.message('newMask: Getting mask..')
        mask = self.maskView.getMask()
        self.imageSliders.series.message('newMask: Getting region..')
        region = self.regionList.getRegion()
        self.imageSliders.series.message('newMask: Moving mask..')
        mask = mask.move_to(region) 
        self.imageSliders.series.message('newMask: Setting Maskview..')
        self.maskView.setObject(mask)
        self.imageSliders.series.message('newMask: Finished..')

