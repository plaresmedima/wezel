import numpy as np

from PyQt5.QtCore import Qt, pyqtSignal, QRectF
from PyQt5.QtWidgets import (QGraphicsObject, QGraphicsItem,
    QAction, QMenu, QGraphicsView, QGraphicsScene, QActionGroup)
from PyQt5.QtGui import QPixmap, QBrush, QIcon, qRgb, QTransform, QCursor, QImage

import dbdicom
from wezel import canvas, icons


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
        self.image = None

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
            image.read()
        self.image = image
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
            if image[shape] != self.image[shape]:
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
        image = self.image
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
            image = self.image
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
        image = self.image
        if image is None: # image is corrupted
            return
        image.mute()
        image.save()
        image.unmute()
        self.maskItem.save()

    def restore(self):
        image = self.image
        if image is None: # image is corrupted
            return
        image.restore()
        self.imageItem.setData(image)
        #self.imageItem.update()
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
    def __init__(self, image): 
        super().__init__()
        #self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setOpacity(1.0)
        self.setData(image)
        self.setDisplay()

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""
        if self._qImage is None: # image is corrupted
            return
        painter.drawImage(0, 0, self._qImage)

    def setData(self, image):
        try:
            self.setArray(image.array())
            self.setWindow(image.WindowCenter, image.WindowWidth)
            self.setLUT(image.lut)
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
        # Alpha channel - set transparent by default
        self._BGRA[:,:,3] = 255 
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
        #self.setQImage()

    def setDisplay(self):
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
            array = self.image.array()
            self.mask = array != 0
        else:
            rect = self.boundingRect()
            dx, dy = rect.width(), rect.height()
            self.mask = np.zeros((int(dx), int(dy)), dtype=bool)
        shape = (self.mask.shape[1], self.mask.shape[0], 4)
        self.BGRA = np.zeros(shape, dtype=np.ubyte)
        self.BGRA[:,:,3] = 255 # Alpha channel - required by QImage
        self.setQImage()
        self._hasChanged = False

    def setQImage(self):
        #QImage expects transpose
        mask = self.mask.astype(np.ubyte).T
        for c in range(3):
            if self._RGB[2-c] != 0:
                LUT = np.array([0,self._RGB[2-c]], dtype=np.ubyte)
                self.BGRA[:,:,c] = LUT[mask]
        #self.qImage = canvas.makeQImage(self.BGRA)
        self.qImage = QImage(self.BGRA, self.BGRA.shape[1], self.BGRA.shape[0], QImage.Format_RGB32)

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


