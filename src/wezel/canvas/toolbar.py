import numpy as np

from PyQt5.QtWidgets import (
    QWidget, QGridLayout, 
    QToolBar, QAction, QMenu,
    QActionGroup, QFrame)
from PyQt5.QtGui import QIcon

from wezel import canvas, icons, widgets


class ToolBar(QWidget):

    def __init__(self, parent=None, filters=None):
        super().__init__(parent)

        self.seriesCanvas = None
        self.canvas = None

        if filters is not None:
            self.filters = filters
        else:
            self.filters = self.defaultFilters()

        # Not displayed - context menu only
        # move to appropriate filters
        self.setActionFitItem()
        self.setActionZoomTo()

        # displayed in toolbar
        self.regionList = widgets.RegionList(layout=None)
        self.setImageWindow()
        self.setActionFitItemAndZoom()
        self.setActionZoomIn()
        self.setActionZoomOut()
        self.setActionOpacity()
        self.setActionSetDefaultColor()
        self.setActionUndo()
        self.setActionRedo()
        self.setActionErase()

        # Add to toolbar
        self.group = QActionGroup(self)
        self.group.triggered.connect(
            lambda action: self.canvas.setFilter(action.filter))
        for filter in self.filters:
            self.group.addAction(filter.actionPick)

        # Set default filter
        self.filters[0].actionPick.setChecked(True)
        self.setEnabled(False)

        self._setLayout()

        
    def _setLayout(self):

        grid = QGridLayout()
        grid.setHorizontalSpacing(0)
        grid.setVerticalSpacing(4)

        row = 0
        nrows = 2
        frame = self._getWidgetDisplay()
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 3
        frame = self._getWidgetColor()
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 3
        frame = self._getWidgetRegion()
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 4
        frame = self._getWidgetDraw()
        grid.addWidget(frame,row,0,nrows,3)

        row += nrows
        nrows = 1
        frame = self._getWidgetDrawCustom()
        grid.addWidget(frame,row,0,nrows,3)

        self.setLayout(grid)

    def _getWidgetRegion(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        framegrid.addWidget(self.regionList.comboBox,0,0,1,3)
        w = QToolBar()
        w.addAction(self.regionList.btnLoad)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(self.regionList.btnNew)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(self.regionList.btnDelete)
        framegrid.addWidget(w,1,2)
        w = QToolBar()
        w.addAction(self.actionUndo)
        framegrid.addWidget(w,2,0)
        w = QToolBar()
        w.addAction(self.actionRedo)
        framegrid.addWidget(w,2,1)
        w = QToolBar()
        w.addAction(self.actionErase)
        framegrid.addWidget(w,2,2) 
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetColor(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addWidget(self.window.mode)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(self.actionSetDefaultColor)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(self.filters[2].actionPick)
        framegrid.addWidget(w,0,2)
        framegrid.addWidget(self.window.brightness.spinBox, 1, 0, 1, 3)
        framegrid.addWidget(self.window.contrast.spinBox, 2, 0, 1, 3)
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetDisplay(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addAction(self.actionZoomIn)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(self.actionZoomOut)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(self.actionFitItemAndZoom)
        framegrid.addWidget(w,0,2)
        w = QToolBar()
        w.addAction(self.filters[1].actionPick)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(self.filters[0].actionPick)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(self.actionOpacity)
        framegrid.addWidget(w,1,2)    
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetDraw(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addAction(self.filters[10].actionPick)
        framegrid.addWidget(w,0,0)
        w = QToolBar()
        w.addAction(self.filters[11].actionPick)
        framegrid.addWidget(w,0,1)
        w = QToolBar()
        w.addAction(self.filters[12].actionPick)
        framegrid.addWidget(w,0,2)
        w = QToolBar()
        w.addAction(self.filters[4].actionPick)
        framegrid.addWidget(w,1,0)
        w = QToolBar()
        w.addAction(self.filters[5].actionPick)
        framegrid.addWidget(w,1,1)
        w = QToolBar()
        w.addAction(self.filters[6].actionPick)
        framegrid.addWidget(w,1,2)
        w = QToolBar()
        w.addAction(self.filters[7].actionPick)
        framegrid.addWidget(w,2,0)
        w = QToolBar()
        w.addAction(self.filters[8].actionPick)
        framegrid.addWidget(w,2,1)
        w = QToolBar()
        w.addAction(self.filters[9].actionPick)
        framegrid.addWidget(w,2,2)               
        w = QToolBar()
        w.addAction(self.filters[3].actionPick)
        framegrid.addWidget(w,3,0)
        w = QToolBar()
        w.addAction(self.filters[13].actionPick)
        framegrid.addWidget(w,3,1)
        w = QToolBar()
        w.addAction(self.filters[14].actionPick)
        framegrid.addWidget(w,3,2)
        frame.setLayout(framegrid)
        return frame
    
    def _getWidgetDrawCustom(self):
        frame = QFrame()
        frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        framegrid = QGridLayout()
        framegrid.setHorizontalSpacing(0)
        framegrid.setVerticalSpacing(0)
        w = QToolBar()
        w.addAction(self.filters[15].actionPick)
        framegrid.addWidget(w,0,0)
        frame.setLayout(framegrid)
        return frame

    def setImageWindow(self):
        self.window = widgets.ImageWindow(layout=False)
        self.window.valueChanged.connect(lambda v: self.imageWindowValueChanged(v))

    def imageWindowValueChanged(self, v):
        self.seriesCanvas.setWindow(v[0], v[1])
        self.canvas.imageItem.setWindow(v[0], v[1])
        self.canvas.imageItem.setDisplay()
        
    def defaultFilters(self):
        return [
            canvas.PanFilter(),
            canvas.ZoomFilter(),
            canvas.ImageWindow(),
            canvas.MaskThreshold(),
            canvas.MaskBrush(mode='paint'),
            canvas.MaskPaintByNumbers(mode='paint'),
            canvas.MaskRegionGrowing(mode='paint'),
            canvas.MaskBrush(mode='erase'),
            canvas.MaskPaintByNumbers(mode='erase'),
            canvas.MaskRegionGrowing(mode='erase'),
            canvas.MaskPenSet(mode='draw'),
            canvas.MaskPenSet(mode='cut'),
            canvas.MaskPenSet(mode='catch'),
            canvas.MaskDilate(),
            canvas.MaskShrink(),
            canvas.MaskKidneyEdgeDetection(),
        ]

    def setSeriesCanvas(self, seriesCanvas):
        if seriesCanvas == self.seriesCanvas:
            return
        self.seriesCanvas = seriesCanvas
        self.regionList.setSeriesCanvas(seriesCanvas)
        self.setCanvas(seriesCanvas.canvas)
        seriesCanvas.newImage.connect(lambda image: self.newImage(image))
        seriesCanvas.newRegion.connect(self.newRegion)
        seriesCanvas.maskChanged.connect(self.setRedoUndoEnabled)
        mask = seriesCanvas.mask()
        if mask is not None:
            opacity = self.opacity()
            seriesCanvas.canvas.setMask(mask, color=1, opacity=opacity)

    def setCanvas(self, canvas):
        if canvas == self.canvas:
            return
        self.canvas = canvas
        self.canvas.toolBar = self
        self.setEnabled(True)
        self.canvas.setFilter(self.group.checkedAction().filter)
        self.window.setData(canvas.array(), canvas.center(), canvas.width(), set=True)
    
    def newRegion(self):
        self.setRedoUndoEnabled()
        self.regionList.setView()

    def newImage(self, image):
        self.setRedoUndoEnabled()
        if self.window.mode.isLocked:
            v = self.window.getValue()
            cmap = self.filters[2].getColorMap()
            self.seriesCanvas.setWindow(v[0], v[1])
            self.seriesCanvas.setColormap(cmap)
        else:
            self.window.setData(
                image.array(), 
                self.seriesCanvas.center(), 
                self.seriesCanvas.width())
            self.filters[2].setChecked(self.seriesCanvas.colormap())

    def opacity(self):
        menu = self.actionOpacity.menu()
        for action in menu.actions():
            if action.isChecked():
                return action.opacity

    def setOpacity(self, opacity):
        menu = self.actionOpacity.menu()
        for action in menu.actions():
            checked = action.opacity == opacity
            action.setChecked(checked)

    def setActionFitItem(self):
        icon = QIcon(icons.magnifier_zoom_fit)
        self.actionFitItem = QAction(icon, 'Fit in view', self)
        self.actionFitItem.triggered.connect(lambda: self.canvas.fitItem())

    def setActionZoomTo(self):
        icon = QIcon(icons.magnifier_zoom_actual)
        self.actionZoomTo = QAction(icon, 'Zoom to..', self)
        self.actionZoomTo.setMenu(self.menuZoomTo())

    def setActionZoomIn(self):
        self.actionZoomIn = QAction(QIcon(icons.magnifier_zoom_in), 'Zoom in..', self)
        self.actionZoomIn.triggered.connect(lambda: self.canvas.scale(2.0, 2.0))
        
    def setActionZoomOut(self):
        self.actionZoomOut = QAction(QIcon(icons.magnifier_zoom_out), 'Zoom out..', self)
        self.actionZoomOut.triggered.connect(lambda: self.canvas.scale(0.5, 0.5))

    def setActionFitItemAndZoom(self):
        icon = QIcon(icons.magnifier_zoom_fit)
        self.actionFitItemAndZoom = QAction(icon, 'Fit in view', self)
        self.actionFitItemAndZoom.triggered.connect(lambda: self.canvas.fitItem())
        self.actionFitItemAndZoom.setMenu(self.menuZoomTo())

    def setActionUndo(self):
        self.actionUndo = QAction(QIcon(icons.arrow_curve_180_left), 'Undo..', self)
        self.actionUndo.triggered.connect(self.undo)
        self.actionUndo.setEnabled(False)

    def setActionRedo(self):
        self.actionRedo = QAction(QIcon(icons.arrow_curve), 'Redo..', self)
        self.actionRedo.triggered.connect(self.redo)
        self.actionRedo.setEnabled(False)

    def setRedoUndoEnabled(self):
        item = self.canvas.maskItem
        enable = item._current!=0 and item._current is not None
        self.actionUndo.setEnabled(enable)
        enable = item._current!=len(item._bin)-1 and item._current is not None
        self.actionRedo.setEnabled(enable)

    def undo(self):
        item = self.canvas.maskItem
        item.undo()
        self.setRedoUndoEnabled()

    def redo(self):
        item = self.canvas.maskItem
        item.redo()
        self.setRedoUndoEnabled()


    def setActionErase(self):
        self.actionErase = QAction(QIcon(icons.cross_script), 'Erase..', self)
        self.actionErase.triggered.connect(lambda: self.canvas.maskItem.erase())

    def setActionOpacity(self):
        menu = QMenu()
        menu.setIcon(QIcon(icons.layer_transparent))
        menu.setTitle('Transparency..')
        menu.triggered.connect(lambda action: self.canvas.maskItem.setOpacity(action.opacity))
        actionGroup = QActionGroup(menu)
        settings = {
            '100%': 0.0,
            '90%': 0.10,
            '75%': 0.25,
            '50%': 0.50,
            '25%': 0.75,
            '10%': 0.90,
            '0%': 1.0,
        }
        for text, value in settings.items():
            action = QAction(text)
            action.opacity = value
            action.setCheckable(True) 
            #action.setChecked(action.opacity == self.canvas.maskItem.opacity())
            action.setChecked(action.opacity == 0.75) # default opacity
            actionGroup.addAction(action)
            menu.addAction(action)
        icon = QIcon(icons.layer_transparent)
        self.actionOpacity = QAction(icon, 'Transparency', self)
        self.actionOpacity.setMenu(menu)
        self.actionOpacity.triggered.connect(lambda: self.toggleOpacity())
        #self.actionOpacity.triggered.connect(lambda: self.canvas.maskItem.toggleOpacity())

    def toggleOpacity(self):
        if self.canvas.maskItem is None:
            return
        if self.canvas.maskItem.opacity() <= 0.25:
            opacity = 0.75
        else: 
            opacity = 0.25
        self.canvas.maskItem.setOpacity(opacity)
        self.setOpacity(opacity)

    def setActionSetDefaultColor(self):
        self.actionSetDefaultColor = QAction(QIcon(icons.contrast_low), 'Greyscale', self)
        self.actionSetDefaultColor.setToolTip('Set to default greyscale')
        self.actionSetDefaultColor.triggered.connect(lambda: self.setDefaultColor())

    def setDefaultColor(self):
        array = self.canvas.array()
        min = np.min(array)
        max = np.max(array)
        center = (max+min)/2
        width = 0.9*(max-min)
        self.seriesCanvas.setWindow(center, width)
        self.seriesCanvas.setColormap('Greyscale')
        self.canvas.imageItem.setWindow(center, width)
        self.canvas.imageItem.setLUT(self.seriesCanvas.lut())
        self.canvas.imageItem.setDisplay()
        self.window.setData(array, center, width, set=True)
        self.filters[2].setChecked('Greyscale')

    def menuZoomTo(self, parent=None):
        menu = QMenu(parent)
        menu.setIcon(QIcon(icons.magnifier_zoom_actual))
        menu.setTitle('Zoom to..')
        zoomTo010 = QAction('10%', menu)
        zoomTo025 = QAction('25%', menu)
        zoomTo050 = QAction('50%', menu)
        zoomTo100 = QAction('100%', menu)
        zoomTo200 = QAction('200%', menu)
        zoomTo400 = QAction('400%', menu)
        zoomTo1000 = QAction('1000%', menu)
        zoomTo010.triggered.connect(lambda: self.canvas.zoomTo(0.10)) 
        zoomTo025.triggered.connect(lambda: self.canvas.zoomTo(0.25))
        zoomTo050.triggered.connect(lambda: self.canvas.zoomTo(0.5))
        zoomTo100.triggered.connect(lambda: self.canvas.zoomTo(1))
        zoomTo200.triggered.connect(lambda: self.canvas.zoomTo(2))
        zoomTo400.triggered.connect(lambda: self.canvas.zoomTo(4))
        zoomTo1000.triggered.connect(lambda: self.canvas.zoomTo(10))
        menu.addAction(zoomTo010)
        menu.addAction(zoomTo025)
        menu.addAction(zoomTo050)
        menu.addAction(zoomTo100)
        menu.addAction(zoomTo200)
        menu.addAction(zoomTo400)
        menu.addAction(zoomTo1000)
        return menu
    