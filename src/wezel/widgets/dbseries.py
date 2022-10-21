import pandas as pd

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton,
    )
from PyQt5.QtGui import QIcon

from .. import widgets as widgets

class SeriesColors(QWidget):
    """Widget to set and manage color and window settings of a Series"""

    valueChanged = pyqtSignal()  # emitted when the color settings are changed by the widget

    def __init__(self):
        super().__init__()

        self._setWidgets()
        self._setConnections()
        self._setLayout()

    def _setWidgets(self):

        self.mode = widgets.LockUnlockButton(toolTip = 'Lock image settings')
        self.colors = widgets.SelectImageColorTable()
        self.brightness = widgets.ImageBrightness()
        self.contrast = widgets.ImageContrast()
        self.save = widgets.SaveImageButton()

    def setData(self, series, image):

        self.series = series
        self.colors.setData(image)
        self.brightness.setData(image)
        self.contrast.setData(image)
        self.save.setData(image)

    def setValue(self):

        # self.colors.setValue()
        self.brightness.setValue()
        self.contrast.setValue()

    def setImage(self, image):
        """Assigns a new image to the color tools
        
        If the settings are locked, the color settings
        of the image are updated based on the current values 
        and a signal is emitted that the image properties have changed.

        If the settings are not locked then they are set to 
        the values of the new image.
        """

        self.colors.setData(image)
        self.brightness.setData(image, set=not self.mode.isLocked)
        self.contrast.setData(image, set=not self.mode.isLocked)
        self.save.setData(image)
#        if self.mode.isLocked: # image has been updated based on color settings
#            self.valueChanged.emit()

    def _setConnections(self):

        self.brightness.valueChanged.connect(self.valueChanged.emit)
        self.contrast.valueChanged.connect(self.valueChanged.emit)
        self.colors.newColorTable.connect(self.valueChanged.emit)

    def _setLayout(self):

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)
        layout.addWidget(self.mode)
    #    layout.addWidget(self.colors)
        layout.addWidget(self.brightness)
        layout.addWidget(self.contrast)
    #    layout.addWidget(self.save)
        
        #self.setStyleSheet("background-color: white")
        self.setLayout(layout)


class ImageSliders(QWidget):
    """Widget with sliders to navigate through a DICOM series."""

    valueChanged = pyqtSignal()

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
        self.slidersButton.setIcon(QIcon(widgets.icons.slider_icon))
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
        self.image = image
        if image is None:
            if self.series is not None:
                self.image = self.series.instance()
                #images = self.series.children()
                # images = self.series.instances()
                # if images != []:
                #     self.image = images[0]
        #self.series.message('setSliderValues')
        self._setSliderValues()
        #self.series.message('sliderValueChanged')
        self._sliderValueChanged()  
        self._blockSignals = restore          

    def setSeries(self, series): # Obsolete?

        self.series = series
        self._readDataFrame()
        self._setSliderValueLists()
        self.image = self.series.children()[0]
        self.setImage(self.image)

    def setImage(self, image):  # Obsolete?

        self.image = image
        self._setSliderValues()
        self._sliderValueChanged()

    def getSeries(self):

        return self.series

    def getImage(self):

        return self.image

    def _setSliderValueLists(self):

        for slider in self._activeSliders:
            values = self.dataFrame[slider.label].unique().tolist()
            values.sort()
            slider.setValues(values)

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
        self.dataFrame.dropna(axis=1, inplace=True)  
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


    def _slidersButtonClicked(self):
        """Show or hide the other sliders that can be added."""

        if self.slidersButton.isChecked(): 
            # Build Checkbox sliders
            self.slidersButton.setStyleSheet("background-color: red")
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
            self.slidersButton.setStyleSheet(
                "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #CCCCBB, stop: 1 #FFFFFF)"
            )
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

    def move(self, slider, direction):
        """
        Move the sliders by one step forwards or backwards.

        Arguments
        ---------
        slider : either first or second slider
        direction : either +1 (forwards) or -1 (backwards)
        """
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
            #self._set_image(imageUIDs[0])
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            index = self.sliders[0].value()
            #self._set_image(imageUIDs[index])
            self.image = self.series.instance(imageUIDs[index])
        if not self._blockSignals:
            self.valueChanged.emit()

    def _sliderValueChanged(self):  
        """Change the selected image"""

        imageUIDs = self._getAllSelectedImages()
        if imageUIDs == []: 
            self.image = None
            self.sliders[0].hide()
        elif len(imageUIDs) == 1:
            #self.image = self.series.children(SOPInstanceUID = imageUIDs[0])[0]
            #self._set_image(imageUIDs[0])
            self.image = self.series.instance(imageUIDs[0])
            self.sliders[0].hide()
        else:
            self.sliders[0].setValues(range(len(imageUIDs)))
            index = self.sliders[0].value()
            # self.image = self.series.children(SOPInstanceUID = imageUIDs[index])[0]
            # self._set_image(imageUIDs[index])
            self.image = self.series.instance(imageUIDs[index])
            self.sliders[0].show()
        if not self._blockSignals:
            self.valueChanged.emit()

#     def _set_image(self, SOPInstanceUID):
#         """
#         Set image based on its UID
#         """
#         df = self.dataFrame[self.dataFrame.SOPInstanceUID == SOPInstanceUID]
#         self.image = self.series.dicm.object(self.series.folder, df.iloc[0], 4)
# #        self.image = self.series.children(SOPInstanceUID = imageUIDs[index])[0]

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