import numpy as np

from PyQt5.QtCore import Qt, pyqtSignal, QEvent, QRectF
from PyQt5.QtWidgets import (QWidget, QGraphicsObject, QGraphicsItem,
    QVBoxLayout, QHBoxLayout, QGridLayout, QToolBar, QAction, QMenu,
    QGraphicsView, QGraphicsScene, QActionGroup, QFrame)
from PyQt5.QtGui import QPixmap, QBrush, QIcon, qRgb, QTransform, QCursor

from wezel import canvas, icons, widgets


class Canvas(QGraphicsView):
    """Wrapper for ImageItem displaying it in a scrollable Widget"""

    #imageUpdated = pyqtSignal(object)
    newMaskSeries = pyqtSignal(object)
    mousePositionMoved = pyqtSignal(int, int)
    arrowKeyPress = pyqtSignal(str)

    def __init__(self, parent=None): 
        super().__init__(parent)
        self.setScene(QGraphicsScene(self))
        self.setBackgroundBrush(QBrush(Qt.black))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

        #self.defaultImage = dbdicom.zeros((128, 128)).instances()[0]
        # would like to do: dbdicom.zeros((128, 128))[0,:,:]
        self.maskSeries = None
        self.toolBar = None

    def item(self, n):
        for item in self.scene().items():
            if item.zValue() == n:
                return item
    def removeItem(self, item):
        if item is not None:
            self.scene().removeItem(item)
    @property
    def imageItem(self):
        return self.item(0)
    @property
    def maskItem(self):
        return self.item(1)
    @property
    def filterItem(self):
        return self.item(2)
    
    def setImage(self, image, **kwargs):
        self.removeItem(self.imageItem)
        if image is not None:
            #image = self.defaultImage
            image.read()
        item = canvas.ImageItem(image, **kwargs)
        self.scene().addItem(item)
        item.setZValue(0)
        filter = self.filterItem
        if filter is not None:
            filter.prepareGeometryChange()
            filter.boundingRectangle = self.scene().sceneRect()
        mask = self.findMask()
        if self.toolBar is None:
            opacity=0.5
        else:
            opacity=self.toolBar.opacity()
        self.setMask(mask, color=1, opacity=opacity)
        return item

    def setMask(self, image=None, color=0, opacity=0.5):
        if self.imageItem is None:
            error_msg = 'Create an imageItem before creating a maskItem'
            raise ValueError(error_msg)
        if image is not None:
            shape = ['Columns', 'Rows']
            if image[shape] != self.imageItem.image[shape]:
                image.clear()
                error_msg = 'The mask must have the same dimensions as the image'
                raise ValueError(error_msg)
        self.removeItem(self.maskItem)
        item = canvas.MaskItem(self.imageItem, image, opacity=opacity, color=color)
        #self.scene().addItem(item)
        item.setZValue(1)
        return item

    def setFilter(self, filter=None):
        self.removeItem(self.filterItem)
        if filter is None:
            return
        if filter == 'Default':
            filter = canvas.PanFilter()
        self.scene().addItem(filter)
        self.scene().setFocusItem(filter)
        filter.setZValue(2)
        filter.prepareGeometryChange()
        filter.boundingRectangle = self.scene().sceneRect()
        filter.initialize()

    def findMask(self):
        image = self.imageItem.image
        if image is None:
            return None
        if self.maskSeries is None:
            return None
        maskList = self.maskSeries.instances(sort=False, SliceLocation=image.SliceLocation) 
        if maskList != []: 
            return maskList[0]
        else:
            return None        

    def getMask(self):
        # called by maskItem when mask needs to be saved but none exists
        mask = self.findMask()
        if mask is None:
            image = self.imageItem.image
            if image is not None:
                if self.maskSeries is None:
                    self.maskSeries = image.new_pibling()
                    self.newMaskSeries.emit(self.maskSeries)
                mask = image.copy_to_series(self.maskSeries)
                mask.read()
                mask.WindowCenter = 1
                mask.WindowWidth = 2
        return mask

    def saveMask(self):
        self.maskItem.save()

    def save(self):
        self.imageItem.save()
        self.maskItem.save()

    def restore(self):
        self.imageItem.restore()
        self.maskItem.restore()

    def zoomTo(self, factor):
        self.setTransform(QTransform())
        self.scale(factor, factor)

    def fitItem(self):
        item = self.imageItem
        if item is None:
            item = self.maskItem
        if item is not None:
            self.fitInView(item, Qt.KeepAspectRatio)


class AnyItem(QGraphicsObject):
    """Displays an image.
    """

    def __init__(self, parent=None): 
        super().__init__(parent)
        self.boundingRectangle = QRectF(0, 0, 0, 0) 

    def addSeparator(self, menu):
        separator = QAction(menu)
        separator.setSeparator(True)
        menu.addAction(separator)

    def boundingRect(self): 
        """Abstract method - must be overridden."""
        return self.boundingRectangle

    def paint(self, painter, option, widget):
        """Abstract method - must be overridden."""
        pass


class ImageItem(AnyItem):
    """Displays an image.
    """
    def __init__(self, image): 
        super().__init__()
        self.image = image
        self.qImage = None
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setOpacity(1.0)
        nx, ny = image.Columns, image.Rows
        if nx is None: # image is corrupted
            self.image = None
            nx, ny = 0, 0
        self.boundingRectangle = QRectF(0, 0, nx, ny)
        self.setQImage()
        # self.setMenuColormap()

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""
        if self.image is None: # image is corrupted
            return
        painter.drawImage(0, 0, self.qImage)

    def setQImage(self):
        if self.image is None: # image is corrupted
            return
        try:
            self.qImage = canvas.makeQImage(self.image.BGRA_array())
        except:
            self.image = None # image is corrupted

    def save(self):
        if self.image is None: # image is corrupted
            return
        self.image.mute()
        self.image.save()
        self.image.unmute()

    def restore(self):
        if self.image is None: # image is corrupted
            return
        self.image.restore()
        self.setQImage()
        self.update()
        #cnvs = self.scene().parent()
        #cnvs.imageUpdated.emit(self.image)

    def setColormap(self, cmap):
        if self.image is None: # image is corrupted
            return
        self.image.mute()
        if cmap == 'Greyscale':
            self.image.colormap = None
        else:
            self.image.colormap = cmap
        self.image.unmute()
        self.setQImage()
        self.update()

    def array(self):
        if self.image is None:
            return
        return self.image.array()



class MaskItem(AnyItem):
    """Displays a mask as an overlay on an image.
    """
    def __init__(self, imageItem, image=None, opacity=0.75, color=0): 
        super().__init__(imageItem)
        self.image = image
        self.mask = None
        self.qImage = None
        self._RGB = self.RGB(color)
        #self.boundingRectangle = QRectF(0, 0, image.Columns, image.Rows) 
        self.boundingRectangle = None
        self._hasChanged = False
        self.setMask()
        self.setOpacity(opacity)
  
    def boundingRect(self): 
        """Abstract method - must be overridden."""
        if self.boundingRectangle is None:
            self.boundingRectangle = self.parentItem().boundingRect()
        return self.boundingRectangle

    def toggleOpacity(self):
        if self.opacity() <= 0.25:
            opacity = 0.75
        else: 
            opacity = 0.25
        self.setOpacity(opacity)
        toolBar = self.scene().parent().toolBar
        if toolBar is not None:
            toolBar.setOpacity(opacity)

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""
        painter.drawImage(0, 0, self.qImage)

    def RGB(self, color):
        if color == 0:
            return (255, 0, 0)
        if color == 1:
            return (0, 255, 0)
        if color == 2:
            return (0, 0, 255)
        if color == 3:
            return (0, 255, 255)
        if color == 4:
            return (255, 0, 255)
        if color == 5:
            return (255, 255, 0)
        if color == 6:
            return (0, 128, 255)
        if color == 7:
            return (255, 0, 128)
        if color == 8:
            return (128, 255, 0)
        return (color[0], color[1], color[2])

    def setMask(self):
        if self.image is not None:
            array = self.image.get_pixel_array()
            self.mask = array != 0
        else:
            rect = self.boundingRect()
            dx, dy = rect.width(), rect.height()
            self.mask = np.zeros((int(dx), int(dy)), dtype=bool)
        self.BGRA = np.zeros(self.mask.shape[:2]+(4,), dtype=np.ubyte)
        self.BGRA[:,:,3] = 255 # Alpha channel - required by QImage
        self.setQImage()
        self._hasChanged = False

    def setQImage(self):
        mask = self.mask.astype(np.ubyte)
        for c in range(3):
            if self._RGB[2-c] != 0:
                LUT = np.array([0,self._RGB[2-c]], dtype=np.ubyte)
                self.BGRA[:,:,c] = LUT[mask]
        self.qImage = canvas.makeQImage(self.BGRA)

    def save(self):
        if not self._hasChanged:
            return
        if self.image is None: 
            self.image = self.scene().parent().getMask()
        array = self.mask.astype(np.float32)
        self.image.mute()
        self.image.set_pixel_array(array)
        self.image.unmute()
        self._hasChanged = False

    def restore(self):
        self.setMask()
        self.update()

    def erase(self):
        self.mask.fill(False)
        self.setQImage()
        self.update()
        self._hasChanged = True

    # def setActionErase(self):
    #     self.actionErase = QAction(QIcon(icons.cross_script), 'Erase..', self)
    #     self.actionErase.triggered.connect(self.erase)

    def setPixel(self, x, y, value=None):
        if value is None:
            value = self.mask[x, y]
        else:
            self.mask[x,y] = value
        if value: 
            color = qRgb(self._RGB[0], self._RGB[1], self._RGB[2])
        else:
            color = qRgb(0, 0, 0)
        self.qImage.setPixel(x, y, color)
        self._hasChanged = True


class FilterItem(AnyItem):
    """Base class for View events.
    """

    def __init__(self): 
        super().__init__()
        pixMap = QPixmap(icons.hand)
        self.cursor = QCursor(pixMap, hotX=4, hotY=0)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Filter'
        self.text = 'Filter'
        self.boundingRectangle = QRectF(0, 0, 0, 0) 
        self.x = None
        self.y = None
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)

    def setActionPick(self):
        self.actionPick = QAction(self.icon, self.text)
        self.actionPick.setCheckable(True)
        #self.actionPick.setEnabled(False)
        self.actionPick.filter = self
        menu = self.menuOptions()
        if menu is not None:
            self.actionPick.setMenu(menu)

    def menuOptions(self):
        return

    def updateAction(self, image):
        return

    def initialize(self):
        pass

    # def pan(self, distance):
    #     cnvs = self.scene().parent()
    #     hBar = cnvs.horizontalScrollBar()
    #     vBar = cnvs.verticalScrollBar()
    #     hBar.setValue(hBar.value() - distance.x())
    #     vBar.setValue(vBar.value() - distance.y())

    def keyPressEvent(self, event):
        cnvs = self.scene().parent()
        if event.key() == 16777234:
            cnvs.arrowKeyPress.emit('left') 
        elif event.key() == 16777235:
            cnvs.arrowKeyPress.emit('up')
        elif event.key() == 16777236:
            cnvs.arrowKeyPress.emit('right')
        elif event.key() == 16777237:
            cnvs.arrowKeyPress.emit('down')

    def hoverEnterEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        self.setCursor(self.cursor)
        self.setFocus()
        cnvs = self.scene().parent()
        cnvs.mousePositionMoved.emit(self.x, self.y)

    def hoverLeaveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        cnvs = self.scene().parent()
        cnvs.mousePositionMoved.emit(self.x, self.y)  

    def hoverMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        self.setFocus()
        cnvs = self.scene().parent()
        cnvs.mousePositionMoved.emit(self.x, self.y)    

    def wheelEvent(self, event):
        if event.delta() < 0:
            factor = 1.25
        else:
            factor = 1/1.25
        cnvs = self.scene().parent()
        cnvs.scale(factor, factor)

    def mousePressEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())

    def mouseMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        # Do not pan in FilterItem
        # button = event.buttons()
        # if button == Qt.LeftButton:
        #     distance = event.screenPos() - event.lastScreenPos()
        #     self.pan(distance)

    def mouseReleaseEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
    
    def contextMenu(self):
        menu = QMenu()
        canvas = self.scene().parent()
        toolBar = canvas.toolBar
        if toolBar is None:
            return menu
        menu.addAction(toolBar.actionFitItem)
        menu.addAction(toolBar.actionZoomTo)
        menu.addAction(toolBar.actionZoomIn)
        menu.addAction(toolBar.actionZoomOut)
        if canvas.maskItem is not None:
            self.addSeparator(menu)
            menu.addAction(toolBar.actionOpacity)
        return menu

    def contextMenuEvent(self, event):
        menu = self.contextMenu()
        menu.exec_(event.screenPos())

    def pick(self):
        self.actionPick.setChecked(True)
        self.actionPick.triggered.emit(True)
        self.update()


class FilterSet():
    def __init__(self):
        self.filters = None
        self.icon = None
        self.text = None
        self.current = None

    def pick(self, filter):
        self.current = filter
        self.actionPick.filter = filter
        self.actionPick.setChecked(True)
        self.actionPick.triggered.emit(True)
        #self.update()

    def setActionPick(self):
        self.actionPick = QAction(self.icon, self.text)
        self.actionPick.setCheckable(True)
        #self.actionPick.setEnabled(False)
        self.actionPick.filter = self.current
        self.actionPick.setMenu(self.menu())
        for filter in self.filters:
            filter.contextMenu = self.menu

    def menu(self):
        menu = QMenu()
        menu.triggered.connect(lambda action: self.pick(action.filter))
        actionGroup = QActionGroup(menu)
        for filter in self.filters:
            action = QAction(filter.iconInSet, filter.textInSet)
            action.filter = filter
            action.setCheckable(True)
            action.setChecked(action.filter == self.current)
            actionGroup.addAction(action)
            menu.addAction(action)
        return menu

    def updateAction(self, image):
        return


class ToolBar(QWidget):

    def __init__(self, parent=None, filters=None):
        super().__init__(parent)

        if filters is not None:
            self.filters = filters
        else:
            self.filters = self.defaultFilters()

        # Not displayed - context menu only
        # move to appropriate filters
        self.setActionFitItem()
        self.setActionZoomTo()

        # displayed in toolbar
        self.setRegionList()
        self.setImageWindow()
        self.setActionFitItemAndZoom()
        self.setActionZoomIn()
        self.setActionZoomOut()
        self.setActionOpacity()
        self.setActionSetDefaultColor()
        self.setActionSave()
        self.setActionRestore()
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
        w.addAction(self.actionSave)
        framegrid.addWidget(w,2,0)
        w = QToolBar()
        w.addAction(self.actionRestore)
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

    def setRegionList(self):
        self.regionList = widgets.RegionList(layout=None)
        self.regionList.currentRegionChanged.connect(self.currentRegionChanged)
        
    def currentRegionChanged(self):
        self.seriesCanvas.canvas.saveMask()
        self.seriesCanvas.setMaskSeries(self.regionList.region())
        self.seriesCanvas.setCanvasImage()

    def setImageWindow(self):
        self.window = widgets.ImageWindow(layout=False)
        self.window.valueChanged.connect(lambda v: self.imageWindowValueChanged(v))

    def imageWindowValueChanged(self, v):
        self.canvas.imageItem.setQImage()
        self.canvas.imageItem.update()
        
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
        self.seriesCanvas = seriesCanvas
        self.regionList.series = seriesCanvas.sliders.series
    #    self.regionList.setRegions(seriesCanvas.regions)
        self.setCanvas(seriesCanvas.canvas)
        seriesCanvas.newImage.connect(lambda image: self.newImage(image))

    def setCanvas(self, canvas):
        self.canvas = canvas
        self.canvas.toolBar = self
        self.setEnabled(True)
        self.canvas.setFilter(self.group.checkedAction().filter)
        self.canvas.newMaskSeries.connect(lambda series: self.regionList.addRegion(series))
        self.window.setData(canvas.imageItem.image, set=True)
        self.regionList.addRegion(canvas.maskSeries)

    def newImage(self, image):
        self.window.setData(image)
        self.filters[2].setData(image, set=not self.window.mode.isLocked)
        for filter in self.filters:
            filter.updateAction(image)

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

    def setActionSave(self):
        self.actionSave = QAction(QIcon(icons.disk), 'Save..', self)
        self.actionSave.triggered.connect(lambda: self.canvas.save())

    def setActionRestore(self):
        self.actionRestore = QAction(QIcon(icons.arrow_curve_180_left), 'Restore..', self)
        self.actionRestore.triggered.connect(lambda: self.canvas.restore())

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
        self.actionOpacity.triggered.connect(lambda: self.canvas.maskItem.toggleOpacity())
        
    def setActionSetDefaultColor(self):
        self.actionSetDefaultColor = QAction(QIcon(icons.contrast_low), 'Default', self)
        self.actionSetDefaultColor.setToolTip('Set to default greyscale')
        self.actionSetDefaultColor.triggered.connect(lambda: self.setDefaultColor())

    def setDefaultColor(self):
        image = self.canvas.imageItem.image
        if image is None: # image is corrupted
            return
        image.mute()
        array = image.get_pixel_array()
        min = np.min(array)
        max = np.max(array)
        center = (max+min)/2
        width = 0.9*(max-min)
        image.WindowCenter = center
        image.WindowWidth = width
        image.colormap = None
        self.canvas.imageItem.setQImage()
        self.canvas.imageItem.update()
        #cnvs = self.scene().parent()
        #cnvs.imageUpdated.emit(image)
        image.unmute()
        self.window.setData(image, set=True)


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
    