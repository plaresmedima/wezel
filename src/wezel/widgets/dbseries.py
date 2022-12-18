import pandas as pd
import random
from matplotlib import cm
import numpy as np

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
    )
from PyQt5.QtGui import QIcon

from wezel import widgets, canvas, icons


class SeriesSliders(QWidget):
    """Widget with sliders to navigate through a DICOM series."""

    valueChanged = pyqtSignal(object)

    def __init__(self, series=None, image=None, dimensions=[]):  
        super().__init__()
        self._blockSignals = False
        if dimensions == []:
            self.sliderTags = ["SliceLocation","AcquisitionTime"]
        else: 
            self.sliderTags = dimensions
        self._setWidgets()
        self._setLayout()
        if series is not None:
            self.setData(series, image)

    def _setWidgets(self):

        self.slidersButton = QPushButton()
        self.slidersButton.setToolTip("Display Multiple Sliders")
        self.slidersButton.setCheckable(True)
        self.slidersButton.setIcon(QIcon(icons.slider_icon))
        self.slidersButton.clicked.connect(self._slidersButtonClicked)  

        self.instanceSlider = widgets.LabelSlider("", range(1))
        self.instanceSlider.valueChanged.connect(self._mainSliderValueChanged)

        self.sliders = [self.instanceSlider]

    def _setLayout(self):

        self.layout = QHBoxLayout()
        self.layout.setAlignment(Qt.AlignLeft  | Qt.AlignVCenter)
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.addWidget(self.slidersButton)
        self.layout.addWidget(self.instanceSlider)

        self.setStyleSheet("background-color: white")
        self.setLayout(self.layout)

    def blockSignals(self, block):
        self._blockSignals = block

    def setData(self, series=None, image=None, blockSignals=False):
        restore = self._blockSignals
        self._blockSignals = blockSignals
        self.series = series
        self._readDataFrame()
        self._setSliderValueLists()
        if image is None:
            if self.series is not None:
                image = self.series.instance()
        self.setImage(image)  
        self._blockSignals = restore          

    def setSeries(self, series): 
        self.series = series
        self._readDataFrame()
        self._setSliderValueLists()
        image = self.series.instance()
        self.setImage(image)

    def setImage(self, image): 
        self.blockSignals(True) 
        self.image = image
        self._setSliderValues()
        self._sliderValueChanged()
        self.blockSignals(False) 


    def _readDataFrame(self):
        """Read the dataframe for the series.
        
        Drop tags that are not present in every instance. 
        Drop tags that appear only once.
        """
        # Add all default tags in the registry and get values
        tags = self.sliderTags.copy()  
        if self.series is None:
            self.dataFrame = pd.DataFrame([], index=[], columns=tags)
            return
        # If all required tags are in the register,
        # then just extract the register for the series;
        # else read the data from disk.
        columns = list(self.series.manager.columns)
        tags = list(set(tags + columns))
        # if set(tags) == set(columns): # integrated in dbdicom read_dataframe
        #     self.dataFrame = self.series.register()
        # else: 
        #     self.dataFrame = self.series.read_dataframe(tags)  
        self.dataFrame = self.series.read_dataframe(tags)  
        self.dataFrame.sort_values("InstanceNumber", inplace=True)
        #self.dataFrame.dropna(axis=1, inplace=True)  
        #self.dataFrame.reset_index()
        # remove tags with one unique value  
        for tag in self.sliderTags:        
            if tag in self.dataFrame: 
                values = self.dataFrame[tag].unique().tolist()
                if len(values) == 1:
                    self.dataFrame.drop(tag, axis=1, inplace=True)
        # update list of slider Tags
        for tag in self.sliderTags.copy():
            if tag not in self.dataFrame:
                self.sliderTags.remove(tag)


    def _setSliderValueLists(self):
        for slider in self._activeSliders:
            values = self.dataFrame[slider.label].unique().tolist()
            values.sort()
            slider.setValues(values)


    def _slidersButtonClicked(self):
        """Show or hide the other sliders that can be added."""

        if self.slidersButton.isChecked(): 
            # Build Checkbox sliders
            #self.slidersButton.setStyleSheet("background-color: red")
            for tag in self.sliderTags:
                tagValues = self.dataFrame[tag].unique().tolist()
                try:
                    tagValues.sort()
                except:
                    pass
                slider = widgets.CheckBoxSlider(tag, tagValues)
                slider.valueChanged.connect(self._sliderValueChanged)
                slider.stateChanged.connect(self._sliderStateChanged)
                self.layout.addWidget(slider)
                self.sliders.append(slider)
        else: 
            # Delete CheckBox sliders
            for slider in self.sliders[1:]:
                slider.deleteLater()
            self.sliders = self.sliders[:1]
            self.sliders[0].show()

    def _sliderStateChanged(self):

        if self.image is None:
            self._sliderValueChanged()
        else:
            self._setActiveSliderValues()
            self._setMainSliderValue()

    def _setSliderValues(self):
        
        if self.image is None: 
            return
        self._setActiveSliderValues()
        self._setMainSliderValue()

    def move(self, slider='first', direction=1, key='up'):
        """
        Move the sliders by one step forwards or backwards.

        Arguments
        ---------
        Specify either slider + direction, or key.

        slider : either first or second slider
        direction : either +1 (forwards) or -1 (backwards)
        key: arrow (left, right, up or down)
        """
        # Translate keyboard arrow hits to slider movement
        self._blockSignals = True
        if key is not None:
            if key == 'left':
                slider = 'first'
                direction = -1
            elif key == 'right':
                slider = 'first'
                direction = 1
            elif key == 'up':
                slider = 'second'
                direction = 1
            elif key == 'down':
                slider = 'second'
                direction = -1
        active = self._activeSliders
        if self.sliders[0].isHidden():
            if slider == 'first':
                sldr = active[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._sliderValueChanged()
            else:
                if len(active) > 1:
                    sldr = active[1]
                else:
                    sldr = active[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._sliderValueChanged()

        else: # main slider is visible

            if slider == 'first':
                sldr = self.sliders[0]
                index = sldr.index() + direction
                if sldr.setIndex(index):
                    self._mainSliderValueChanged()
            else: 
                if len(active) > 0:
                    sldr = active[0]
                    index = sldr.index() + direction
                    if sldr.setIndex(index):
                        self._sliderValueChanged()
                else:
                    sldr = self.sliders[0]
                    index = sldr.index() + direction
                    if sldr.setIndex(index):
                        self._mainSliderValueChanged()
        self._blockSignals = False


    def _setActiveSliderValues(self):

        if self.image is None: 
            return
        find = self.dataFrame.SOPInstanceUID == self.image.uid
        row = self.dataFrame.loc[find]
        for slider in self._activeSliders:
            value = row[slider.label].values[0]
            slider.setValue(value)

    def _setMainSliderValue(self):

        if self.image is None: 
            return
        imageUIDs = self._getAllSelectedImages()
        if len(imageUIDs) <= 1:
            self.sliders[0].hide()
        else:
            index = imageUIDs.index(self.image.uid)
            self.sliders[0].setValue(index)
            self.sliders[0].show()

    def _mainSliderValueChanged(self):  
        """Change the selected image"""

        imageUIDs = self._getAllSelectedImages()
        if imageUIDs == []:
            self.image = None
            self.sliders[0].hide()
        elif len(imageUIDs) == 1:
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            index = self.sliders[0].value()
            self.image = self.series.instance(imageUIDs[index])
        if not self._blockSignals:
            self.valueChanged.emit(self.image)

    def _sliderValueChanged(self):  
        """Change the selected image"""

        imageUIDs = self._getAllSelectedImages()
        if imageUIDs == []: 
            self.image = None
            self.sliders[0].hide()
        elif len(imageUIDs) == 1:
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            self.sliders[0].setValues(range(len(imageUIDs)))
            index = self.sliders[0].value()
            self.image = self.series.instance(imageUIDs[index])
            self.sliders[0].show()
        if not self._blockSignals:
            self.valueChanged.emit(self.image)


    def _getAllSelectedImages(self):
        """Get the list of all image files selected by the optional sliders"""

        selection = pd.Series( 
            index = self.dataFrame.index, 
            data = self.dataFrame.shape[0] * [True]
        )
        for slider in self._activeSliders:
            sliderSelection = self.dataFrame[slider.label] == slider.value()
            selection = selection & sliderSelection
        if not selection.any():
            return []
        else:
            return self.dataFrame.SOPInstanceUID[selection].values.tolist()

    @property
    def _activeSliders(self):
        """Create a list of all active sliders"""

        activeSliders = []
        for slider in self.sliders[1:]:
            if slider.checkBox.isChecked():
                activeSliders.append(slider)
        return activeSliders
    


class SeriesCanvas(QWidget):

    closed = pyqtSignal()
    newRegion = pyqtSignal()
    newImage = pyqtSignal(object)
    mousePositionMoved = pyqtSignal(int, int)
    maskChanged = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.sliders = widgets.SeriesSliders()
        self.sliders.valueChanged.connect(self.changeCanvasImage)
        self.canvas = canvas.Canvas(self)
        self.canvas.arrowKeyPress.connect(lambda arrow: self.arrowKeyPress(arrow))
        self.canvas.mousePositionMoved.connect(lambda x, y: self.mousePositionMoved.emit(x,y))
        self.canvas.maskChanged.connect(self.slotMaskChanged)
        self.setEnabled(False)
        self._model = SeriesCanvasModel()
        self._view = SeriesCanvasView(self)

    def slotMaskChanged(self):
        if self._model._regions == []:
            self._model.addRegion()
            bin = self.canvas.mask()
            clr = self.canvas.maskItem.color()
            self._model.setMask(bin)
            self._model.setColor(clr)
            self.newRegion.emit()
        self.maskChanged.emit()

    def closeEvent(self, event): 
        if self.canvas.toolBar is not None:
            self.canvas.toolBar.setEnabled(False)
        if not self.isEnabled():
            return
        series = self.sliders.series
        if not series.exists():
            return
        images = series.instances()
        for region in self._model._regions:
            roi_series = series.new_sibling(SeriesDescription=region['name'])
            for image in images:
                uid = image.SOPInstanceUID
                if uid in region:
                    array = region[uid].astype(np.float32)
                    mask = image.copy_to(roi_series)
                    mask.set_array(array)
                    mask.WindowCenter = 0.5
                    mask.WindowWidth = 1.0
        #self.destroy(destroyWindow=True)
        #self.deleteLater()
        self.closed.emit()
        
    def setFilter(self, filter):
        self.canvas.setFilter(filter)
        
    def setImageSeries(self, series):
        self._model._series = series
        self.sliders.setData(series)
        self.setCanvasImage()
        self.setEnabled(True)

    def setCanvasImage(self):
        image = self.sliders.image
        if image is not None:
            image.read()
            self._model.setImage(image)
            self.canvas.setImage(            
                image.array(), 
                self.center(), 
                self.width(), 
                self.lut())
            image.clear()

    def changeCanvasImage(self):
#        self.canvas.saveMask()
        bin = self.canvas.mask()
        if bin is not None:
            if self._model._regions == []:
                self.addRegion()
                self.newRegion.emit()
        self._model.setMask(bin)
        image = self.sliders.image
        image.read()
        self._model.setImage(image)
        self.canvas.setImage(            
            image.array(), 
            self.center(), 
            self.width(), 
            self.lut())
        mask = self.mask()
        self.canvas.setMask(mask, color=self._model.color())
        self.newImage.emit(image)
        image.clear()
        
    def arrowKeyPress(self, key):
        self.sliders.move(key=key)
        self.changeCanvasImage()

    def removeCurrentRegion(self):
        currentIndex = self.currentIndex()
        self._model._regions.remove(self._model._currentRegion)
        if self._model._regions == []:
            self._model._currentRegion = None
            self.canvas.setMask(None)
        else:
            if currentIndex >= len(self._model._regions)-1:
                currentIndex = -1
            self._model._currentRegion = self._model._regions[currentIndex]
            self.canvas.setMask(self.mask(), color=self._model.color())
        self.newRegion.emit()

    def addRegion(self):
        if self._model._regions != []:
            self.setMask()
        self._model.addRegion()
        self.canvas.setMask(None, color=self._model.color())
        self.newRegion.emit()

    def setMask(self):
        self._model.setMask(self.canvas.mask())

    def setCurrentRegion(self, index):
        self.setMask()
        self._model._currentRegion = self._model._regions[index]
        self.canvas.setMask(self.mask(), color=self._model.color())
        self.newRegion.emit()

    def setCurrentRegionName(self, name):
        self._model._currentRegion['name'] = name

    def loadRegion(self):
        # Build list of series for all series in the same study
        seriesList = self.sliders.series.parent().children()
        seriesLabels = [series.SeriesDescription for series in seriesList]
        # Ask the user to select series to import as regions
        input = widgets.UserInput(
            {"label":"Series:", "type":"listview", "list": seriesLabels}, 
            title = "Please select regions to load")
        if input.cancel:
            return
        selectedSeries = [seriesList[i] for i in input.values[0]["value"]]
        # Overlay each of the selected series on the displayed series
        for series in selectedSeries:
            # Create overlay
            region = series.map_mask_to(self.sliders.series)
            # Add new region
            newRegion = {'name': region.SeriesDescription, 'color': self._model.newColor()}
            self._model._regions.append(newRegion)
            self._model._currentRegion = newRegion
            # Find masks for each image
            for image in self.sliders.series.instances():
                maskList = region.instances(sort=False, SliceLocation=image.SliceLocation) 
                if maskList != []:
                    newRegion[image.SOPInstanceUID] = maskList[0].array() != 0
        # Show new mask
        self.canvas.setMask(self.mask(), color=self._model.color())
        self.sliders.series.status.hide()

    #
    # Interface for model functions
    #

    def array(self):
        return self.canvas.array()

    def center(self):
        return self._model.center()

    def width(self):
        return self._model.width()

    def lut(self):
        return self._model.lut()

    def colormap(self):
        return self._model.colormap()

    def regionNames(self):
        return self._model.regionNames()

    def currentIndex(self):
        if self._model._regions == []:
            return -1
        current = self._model._currentRegion
        return self._model._regions.index(current)

    def currentRegion(self):
        return self._model._currentRegion

    def mask(self):
        return self._model.mask()

    def setColormap(self, cmap):
        self._model.setColormap(cmap)

    def setWindow(self, center, width):
        self._model.setWindow(center, width)

    def setLUT(self, lut):
        self._model.setLUT(lut)


class SeriesCanvasView():
    def __init__(self, widget):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(widget.canvas)
        layout.addWidget(widget.sliders)
        widget.setLayout(layout)


class SeriesCanvasModel:
    def __init__(self):
        self._series = None
        self._center = {}
        self._width = {}
        self._lut = {}
        self._cmap = {}
        self._regions = []
        self._currentRegion = None # dict
        self._currentImage = None # uid

    def center(self):
        return self._center[self._currentImage]

    def width(self):
        return self._width[self._currentImage]

    def lut(self):
        return self._lut[self._currentImage]

    def colormap(self):
        return self._cmap[self._currentImage]

    def setColormap(self, cmap):
        if cmap == 'Greyscale':
            G = np.linspace(0.0, 1.0, num=256)
            RGB = np.transpose([G, G, G])
        else:
            RGBA = cm.ScalarMappable(cmap=cmap).to_rgba(np.arange(256))
            RGB = RGBA[:,:3]
        self._cmap[self._currentImage] = cmap
        self._lut[self._currentImage] = RGB

    def setWindow(self, center, width):
        self._center[self._currentImage] = center
        self._width[self._currentImage] = width

    def setLUT(self, lut):
        self._lut[self._currentImage] = lut

    def setImage(self, image):
        uid = image.SOPInstanceUID
        self._currentImage = uid
        if uid in self._center.keys():
            return
        self._center[uid] = image.WindowCenter
        self._width[uid] = image.WindowWidth
        self._lut[uid] = image.lut
        self._cmap[uid] = image.colormap

    def color(self):
        if self._currentRegion is None:
            return 0
        return self._currentRegion['color']

    def mask(self):
        if self._currentRegion is None:
            return
        if self._currentImage in self._currentRegion:
            return self._currentRegion[self._currentImage]

    def setMask(self, bin):
        if self._currentRegion is None:
            return
        self._currentRegion[self._currentImage] = bin
        
    def setColor(self, RGB):
        if self._currentRegion is None:
            return
        self._currentRegion['color'] = RGB

    def regionNames(self):
        return [r['name'] for r in self._regions]

    def regionColors(self):
        return [r['color'] for r in self._regions]

    def addRegion(self):
        # Find unique name
        newName = "New Region"
        allNames = self.regionNames()
        count = 0
        while newName in allNames:
            count += 1 
            newName = 'New Region [' + str(count).zfill(3) + ']'
        # Add new region
        newRegion = {'name': newName, 'color': self.newColor()}
        self._regions.append(newRegion)
        self._currentRegion = newRegion

    def newColor(self):
        # Find unique color
        allColors = self.regionColors()
        colorIndex = 0
        color = self.colorFromIndex(colorIndex)
        while color in allColors:
            colorIndex += 1
            color = self.colorFromIndex(colorIndex)
        return color

    def colorFromIndex(self, color):
        # RGB color of the region
        if color == 0:
            return [255, 0, 0]
        if color == 1:
            return [0, 255, 0]
        if color == 2:
            return [0, 0, 255]
        if color == 3:
            return [0, 255, 255]
        if color == 4:
            return [255, 0, 255]
        if color == 5:
            return [255, 255, 0]
        if color == 6:
            return [0, 128, 255]
        if color == 7:
            return [255, 0, 128]
        if color == 8:
            return [128, 255, 0]
        return [
            random.randint(0,255), 
            random.randint(0,255), 
            random.randint(0,255)]


