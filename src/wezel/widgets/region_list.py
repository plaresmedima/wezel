from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QAction,
    QWidget, 
    QComboBox, QToolBar, 
    QHBoxLayout, QVBoxLayout,
    QPushButton)

from wezel import icons, widgets

class RegionList(QWidget):
    """Manages a list of regions on the same underlay series"""
    currentRegionChanged = pyqtSignal()

    def __init__(self, layout='Horizontal'):
        super().__init__()
        self.regions = []
        self.series = None
        self._defineWidgets()
        self._defineConnections()
        if layout=='Vertical':
            self._defineLayoutVertical()
        elif layout == 'Horizontal':
            self._defineLayout()

    def _defineWidgets(self):
        self.comboBox = QComboBox()
        self.comboBox.setDuplicatesEnabled(False)
        self.comboBox.setSizeAdjustPolicy(QComboBox.AdjustToContents)
        self.comboBox.setToolTip("List of regions")
        self.comboBox.setEditable(True)
        self.comboBox.setInsertPolicy(QComboBox.InsertAtCurrent)
        self.comboBox.setDuplicatesEnabled(True)
        self.comboBox.setEnabled(False)
        self.comboBox.setFixedWidth(115)
        #self.btnLoad = QPushButton()
        self.btnLoad = QAction()
        self.btnLoad.setToolTip('Load new ROIs')
        self.btnLoad.setIcon(QIcon(icons.application_import))
        #self.btnNew = QPushButton() 
        self.btnNew = QAction() 
        self.btnNew.setToolTip('Create a new ROI')
        self.btnNew.setIcon(QIcon(icons.plus))
        #self.btnDelete = QPushButton() 
        self.btnDelete = QAction() 
        self.btnDelete.setToolTip('Delete the current ROI')
        self.btnDelete.setIcon(QIcon(icons.minus))
        self.btnDelete.setEnabled(False)

    def _defineLayoutVertical(self):
        column = QVBoxLayout()
        column.setContentsMargins(0, 0, 0, 0)
        column.setSpacing(0)
        column.addWidget(self.comboBox, alignment=Qt.AlignLeft)
        #row = QHBoxLayout()
        #row.setContentsMargins(0, 0, 0, 0)
        #row.setSpacing(0)
        row = QToolBar()
        row.addAction(self.btnLoad)
        row.addAction(self.btnNew)
        row.addAction(self.btnDelete)
        column.addWidget(row)
        self.setLayout(column)

    def _defineLayout(self):
        btns = QToolBar()
        btns.addWidget(self.btnLoad)
        btns.addWidget(self.btnNew)
        btns.addWidget(self.btnDelete)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(btns, alignment=Qt.AlignLeft)
        # layout.addWidget(self.btnLoad, alignment=Qt.AlignLeft)
        # layout.addWidget(self.btnNew, alignment=Qt.AlignLeft)
        # layout.addWidget(self.btnDelete, alignment=Qt.AlignLeft)
        layout.addWidget(self.comboBox, alignment=Qt.AlignLeft)
        self.setLayout(layout)

    def _defineConnections(self):
        self.comboBox.currentIndexChanged.connect(self.currentRegionChanged.emit)
        self.btnLoad.triggered.connect(self._loadRegion)
        self.btnNew.triggered.connect(self._newRegion)
        self.btnDelete.triggered.connect(self._deleteRegion)
        # self.btnLoad.clicked.connect(self._loadRegion)
        # self.btnNew.clicked.connect(self._newRegion)
        # self.btnDelete.clicked.connect(self._deleteRegion)

    def setRegions(self, regions):
        if regions is None:
            return
        self.regions = [region.read() for region in regions]
        self.comboBox.blockSignals(True)
        self.comboBox.clear()
        self.comboBox.addItems(self._items())
        self.comboBox.setCurrentIndex(0)
        self.comboBox.setEnabled(self.regions!=[])
        self.comboBox.blockSignals(False)
        self.btnDelete.setEnabled(self.regions!=[])

    def getMask(self, image):
        """Get the mask corresponding to a given image"""
        if image is None: 
            return
        if self.region() is None: 
            return
        # make it an option to specify attributes here
        maskList = self.region().instances(sort=False, SliceLocation=image.SliceLocation) 
        if maskList != []: 
            return maskList[0]

    def refresh(self):
        regions = [r for r in self.regions if r.exists()]
        if len(regions) != len(self.regions):
            currentRegion = self.region()
            self.setRegions(regions)
            try:
                i=regions.index(currentRegion)
                changed = False
            except:
                i=0
                changed = True
            self.comboBox.setCurrentIndex(i)
            if changed:
                self.currentRegionChanged.emit()
  
    def region(self):
        if self.regions == []:
            return None
        return self.regions[self.comboBox.currentIndex()]

    def _items(self):
        items = []
        for region in self.regions:
            if region.empty():
                item = 'New Region'
            else:
                item = region.SeriesDescription
                if isinstance(item, list):
                    item = item[0]
            items.append(item)
        return items

    def saveRegions(self):
        for i, region in enumerate(self.regions):
            text = self.comboBox.itemText(i)
            region.SeriesDescription = text
        return self.regions != []

    def addRegion(self, region):
        if region is None:
            return
        region.read()
        self.regions.append(region) # add to the list
        description = region.SeriesDescription
        self.comboBox.blockSignals(True) #update the widget
        self.comboBox.addItem(description)
        self.comboBox.setCurrentIndex(len(self.regions)-1)
        self.comboBox.blockSignals(False)
        self.comboBox.setEnabled(True)
        self.btnDelete.setEnabled(True)
        
    def _newRegion(self):
        region = self.series.new_sibling()
        region.read()
        self.regions.append(region) # add to the list
        description = "New Region"
        count = 2
        while -1 != self.comboBox.findText(description, flags=Qt.MatchContains):
            description = "New Region" + ' [' + str(count).zfill(2) + ']'
            count += 1
        self.comboBox.blockSignals(True) #update the widget
        self.comboBox.addItem(description)
        self.comboBox.setCurrentIndex(len(self.regions)-1)
        self.comboBox.blockSignals(False)
        self.comboBox.setEnabled(True)
        self.btnDelete.setEnabled(True)
        self.currentRegionChanged.emit()
        
    def _deleteRegion(self): # deletes it from the list 
        currentIndex = self.comboBox.currentIndex()
        region = self.region()
        # Drop from the list and delete from database
        self.regions.remove(region) 
        region.remove()
        # Update the widget
        self.comboBox.blockSignals(True) 
        self.comboBox.removeItem(currentIndex)
        self.comboBox.setEnabled(self.regions != [])
        self.btnDelete.setEnabled(self.regions != [])
        if self.regions == []:
            self.comboBox.setCurrentIndex(0)
        else:
            if currentIndex >= len(self.regions)-1:
                newIndex = len(self.regions)-1
            else:
                newIndex = currentIndex+1
            self.comboBox.setCurrentIndex(newIndex)
        self.comboBox.blockSignals(False)
        self.currentRegionChanged.emit()

    def _loadRegion(self):
        # Build list of series for all series in the same study
        seriesList = self.series.parent().children()
        seriesLabels = [series.SeriesDescription for series in seriesList]
        # Ask the user to select series to import as regions
        input = widgets.UserInput(
            {"label":"Series:", "type":"listview", "list": seriesLabels}, 
            title = "Please select regions to load")
        if input.cancel:
            return
        selectedSeries = [seriesList[i] for i in input.values[0]["value"]]
        # Overlay each of the selected series on the displayed series
        self.comboBox.blockSignals(True)
        for series in selectedSeries:
            #series.read()
            region = series.map_mask_to(self.series)
            self.regions.append(region)
            self.comboBox.addItem(region.SeriesDescription)
        series.status.hide()
        self.comboBox.setCurrentIndex(len(self.regions)-1)
        self.comboBox.blockSignals(False)
        self.comboBox.setEnabled(True)
        self.currentRegionChanged.emit()