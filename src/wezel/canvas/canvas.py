import random
import numpy as np
import copy

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtWidgets import (QGraphicsObject, QGraphicsItem,
    QAction, QMenu, QGraphicsView, QGraphicsScene, QActionGroup)
from PyQt5.QtGui import QPixmap, QBrush, QIcon, qRgb, QTransform, QCursor, QImage

from wezel import canvas, icons


class Canvas(QGraphicsView):
    """Wrapper for ImageItem displaying it in a scrollable Widget"""

    #imageUpdated = pyqtSignal(object)
    newMaskSeries = pyqtSignal(object)
    mousePositionMoved = pyqtSignal(int, int)
    arrowKeyPress = pyqtSignal(str)
    maskChanged = pyqtSignal()

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

    def array(self):
        return self.imageItem._array
    def center(self):
        return self.imageItem._center
    def width(self):
        return self.imageItem._width
    
    def setImage(self, array, center, width, lut):
        self.removeItem(self.imageItem)
        item = canvas.ImageItem(array, center, width, lut)
        self.scene().addItem(item)
        item.setZValue(0)
        filter = self.filterItem
        if filter is not None:
            filter.prepareGeometryChange()
            filter.boundingRectangle = self.scene().sceneRect()
        # mask = self.findMask()
        # if self.toolBar is None:
        #     opacity=0.5
        # else:
        #     opacity=self.toolBar.opacity()
        self.setMask(None)
        return item

    def setMask(self, mask, color=0, opacity=0.5):
        self.removeItem(self.maskItem)
        # if image is not None:
        #     image = image.array() != 0
        item = canvas.MaskItem(self.imageItem, mask, opacity=opacity, color=color)
        item.setZValue(1)
        item.maskChanged.connect(self.maskChanged.emit)
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

    def mask(self):
        return self.maskItem.bin()
     
    def zoomTo(self, factor):
        self.setTransform(QTransform())
        self.scale(factor, factor)

    def fitItem(self):
        item = self.imageItem
        if item is None:
            item = self.maskItem
        if item is not None:
            self.fitInView(item, Qt.KeepAspectRatio)

    def array(self):
        return self.imageItem.array()


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
    def __init__(self, array, center, width, lut): 
        super().__init__()
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setOpacity(1.0)
        self.setData(array, center, width, lut)
        self.setDisplay()

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""
        if self._qImage is None: # image is corrupted
            return
        painter.drawImage(0, 0, self._qImage)

    def setData(self, array, center, width, lut):
        try:
            self.setArray(array)
            self.setWindow(center, width)
            self.setLUT(lut)
        except: # image is corrupted
            self._array = None
            self._width = None
            self._center = None  
            self._lut = None 
            self._array_scaled = None
            self._BGRA = None
            self._qImage = None 
        
    def setArray(self, array):
        self._array = array
        nx, ny = array.shape[0], array.shape[1]
        if nx is None: # image is corrupted
            nx, ny = 0, 0
        self.boundingRectangle = QRectF(0, 0, nx, ny)
        # QImage requires transpose
        self._BGRA = np.empty((ny, nx, 4), dtype=np.ubyte)
        # Alpha channel - required but not used
        self._BGRA[:,:,3] = 0 
        # QImage points to self._BGRA in memory - does not need to be updated
        self._qImage = QImage(self._BGRA, self._BGRA.shape[1], self._BGRA.shape[0], QImage.Format_RGB32)

    def setWindow(self, center, width):
        self._width = width
        self._center = center
        max = center + width/2
        min = center - width/2
        # Scale pixel array into byte range
        array = np.clip(self._array, min, max)
        array -= min
        if max > min:
            scale = 255/(max-min)
            array *= scale
        # QImage expects the array transposed
        self._array_scaled = array.astype(np.ubyte)
        self._array_scaled = np.transpose(self._array_scaled)

    def setLUT(self, lut):
        #LUT is lookup table with values in range [0,1]
        if lut is None:
            self._lut = None
        else:
            # Create RGB array by indexing LUT with pixel array
            lut = 255*lut 
            self._lut = lut.astype(np.ubyte)     

    def setDisplay(self):
        if self._BGRA is None: # image is corrupted
            return
        if self._lut is None:
            # Greyscale image
            for c in range(3):
                self._BGRA[:,:,c] = self._array_scaled
        else:
            # Create RGB array by indexing LUT with pixel array 
            for c in range(3):
                self._BGRA[:,:,c] = self._lut[self._array_scaled, 2-c]
        self.update()

    def array(self):
        return self._array    


class MaskItem(AnyItem):
    """Displays a mask as an overlay on an image.
    """
    maskChanged = pyqtSignal()

    def __init__(self, imageItem, mask, opacity=0.75, color=0): 
        super().__init__(imageItem)
        self._bin = []
        self._current = None
        self._BGRA = None
        self._qImage = None
        self._BGR = list(reversed(self.RGB(color)))
        self.boundingRectangle = None
        self.setData(mask)
        self.setOpacity(opacity)

    def color(self):
        return list(reversed(self._BGR))

    def boundingRect(self): 
        """Abstract method - must be overridden."""
        if self.boundingRectangle is None:
            self.boundingRectangle = self.parentItem().boundingRect()
        return self.boundingRectangle

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""
        if self._qImage is not None:
            painter.drawImage(0, 0, self._qImage)

    def setBin(self, bin):
        self._bin[self._current] = bin

    def bin(self):
        if self._current == None:
            return
        return self._bin[self._current]

    def setData(self, mask):
        #array = mask.array()
        #self._bin = array != 0
        if mask is None:
            return
        self._bin = [mask != 0]
        self._current = 0
        shape = (self.bin().shape[1], self.bin().shape[0], 4)
        self._BGRA = np.zeros(shape, dtype=np.ubyte)
        self._qImage = QImage(self._BGRA, self._BGRA.shape[1], self._BGRA.shape[0], QImage.Format_ARGB32)
        self.setDisplay()
        self.maskChanged.emit()

    def initMask(self):
        rect = self.boundingRect()
        dx, dy = rect.width(), rect.height()
        self._bin = [np.zeros((int(dx), int(dy)), dtype=bool)]
        self._current = 0
        shape = (self.bin().shape[1], self.bin().shape[0], 4)
        self._BGRA = np.zeros(shape, dtype=np.ubyte)
        self._qImage = QImage(self._BGRA, self._BGRA.shape[1], self._BGRA.shape[0], QImage.Format_ARGB32)

    def setDisplay(self):
        if self._bin == []:
            return
        LUT = np.array([0,1], dtype=np.ubyte)
        mask = self.bin().astype(np.ubyte)
        mask = np.transpose(mask)
        mask = LUT[mask]
        for c in range(3):
            if self._BGR[c] != 0:
                self._BGRA[:,:,c] = mask*self._BGR[c]
        self._BGRA[:,:,3] = mask*255
        self.update()
        self.maskChanged.emit()

    def setPixel(self, x, y, value):
        # if self._bin == []:
        #     self.initMask()
        self.bin()[x,y] = value
        if value: 
            self._BGRA[y,x,:3] = self._BGR
            self._BGRA[y,x,3] = 255
        else:
            self._BGRA[y,x,:] = 0

    def extend(self):
        if self._bin == []:
            self.initMask()
        bin = copy.deepcopy(self.bin())
        self._bin = self._bin[:self._current+1]
        self._bin.append(bin)
        self._current += 1
        self.maskChanged.emit()

    def undo(self):
        if self._current == None:
            return
        if self._current != 0:
            self._current -= 1
            self.setDisplay()
    
    def redo(self):
        if self._current == None:
            return
        if self._current != len(self._bin)-1:
            self._current += 1
            self.setDisplay()
         
    def erase(self):
        self.extend()
        self.bin().fill(False)
        self.setDisplay()

    def RGB(self, color):
        if isinstance(color, list):
            return color
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



