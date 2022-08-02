__all__ = ['RegionViewerDev', 'SeriesViewerDev']

import math
import numpy as np
from matplotlib.path import Path as MplPath


from PyQt5.QtCore import Qt, pyqtSignal, QRectF, QEvent, QPointF
from PyQt5.QtWidgets import (QWidget, QPushButton, 
    QHBoxLayout, QVBoxLayout, QToolBar, QAction, QMenu,
    QGraphicsView, QGraphicsScene, QGraphicsObject, QGraphicsItem)
from PyQt5.QtGui import QPixmap, QCursor, QIcon, QColor, QPen, QBrush, qRgb, QImage

from . import icons
from .. import widgets


class RegionViewerDev(QWidget):
    """
    GUI for drawing and editing Regions of Interest
    """

    dataWritten = pyqtSignal()

    def __init__(self, series=None, dimensions=[]): 
        super().__init__()

        self._setWidgets(dimensions=dimensions)
        self._setConnections()
        self._setTool()
        self._setLayout()
        if series is not None:
            self.setData(series)

    def _setWidgets(self, dimensions=[]):

        self.imageSliders = widgets.ImageSliders(dimensions=dimensions)
        self.regionList = widgets.RegionList()
        self.view = MaskView()
        self.toolBox = widgets.ToolBox(
            ImageViewCursor(), 
            ImageViewZoom(),
            MaskViewBrush(),
            MaskViewPenFreehand(),
            MaskViewPenPolygon(),
            MaskViewPenRectangle(),
            MaskViewPenCircle(),
            )
        self.pixelValue = widgets.PixelValueLabel()
        self.colors = widgets.SeriesColors()

        self.view.setToolBox(self.toolBox)

    def _setLayout(self):

        toolBar = QToolBar()
        toolBar.addWidget(self.colors) 
        toolBar.addSeparator()
        toolBar.addWidget(self.regionList)
        toolBar.addSeparator()
        toolBar.addWidget(self.toolBox)
        toolBar.addSeparator()
        toolBar.addWidget(self.pixelValue)
        toolBar.setStyleSheet("background-color: white")  

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(toolBar)
        layout.addWidget(self.view) 
        layout.addWidget(self.imageSliders) 

        self.setLayout(layout)

    def _setConnections(self):

        self.view.mousePositionMoved.connect(self._mouseMoved)
        self.view.newMask.connect(self._newMask)
        self.view.keyPress.connect(self._keyPress)
        self.toolBox.newTool.connect(self._setTool)
        self.regionList.currentRegionChanged.connect(self._currentRegionChanged)
        self.regionList.dataWritten.connect(self.dataWritten.emit)
        self.imageSliders.valueChanged.connect(self._currentImageChanged)
        self.colors.valueChanged.connect(self._currentImageEdited)
        self.view.imageUpdated.connect(self.colors.setValue)

    def setData(self, series):

        self.imageSliders.setData(series, blockSignals=True)
        self.regionList.setData(series)

        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)

        self.colors.setData(series, image)
        self.view.setData(image, mask)
        self.view.fitImage()
        self.pixelValue.setData(image)

    def _currentImageEdited(self):

        self.view.imageItem.setPixMap()
        self.view.imageItem.update()

    def _keyPress(self, event):

        if event.key() == 16777234: # left
            self.imageSliders.move('first', -1)
        elif event.key() == 16777236: # right
            self.imageSliders.move('first', +1)
        elif event.key() == 16777235: # up
            self.imageSliders.move('second', +1)
        elif event.key() == 16777237: # down
            self.imageSliders.move('second', -1)

    def _setTool(self):

        tool = self.toolBox.getTool()
        self.view.setTool(tool)

    def _mouseMoved(self):

        tool = self.toolBox.getTool()
        self.pixelValue.setValue([tool.x, tool.y])
        
    def _currentImageChanged(self):

        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)
        self.colors.setImage(image)
        self.view.setData(image, mask)
        self.pixelValue.setData(image)

    def _currentRegionChanged(self):

        image = self.imageSliders.getImage()
        mask = self.regionList.getMask(image)
        self.view.setMask(mask)

    def _newMask(self):

        mask = self.view.getMask()
        region = self.regionList.getRegion()
        mask = mask.move_to(region)
        self.view.setObject(mask)


class SeriesViewerDev(QWidget):
    """
    GUI for drawing and editing Regions of Interest
    """

    dataWritten = pyqtSignal()

    def __init__(self, series=None, dimensions=[]): 
        super().__init__()

        self._setWidgets(dimensions=dimensions)
        self._setConnections()
        self._setTool()
        self._setLayout()
        if series is not None:
            self.setData(series)

    def _setWidgets(self, dimensions=[]):

        self.imageSliders = widgets.ImageSliders(dimensions=dimensions)
        self.view = ImageView()
        self.toolBox = widgets.ToolBox(
            ImageViewCursor(), 
            ImageViewZoom())
        self.pixelValue = widgets.PixelValueLabel()
        self.colors = widgets.SeriesColors()

        self.view.setToolBox(self.toolBox)

    def _setLayout(self):

        toolBar = QToolBar()
        toolBar.addWidget(self.colors) 
        toolBar.addSeparator()
        toolBar.addWidget(self.toolBox)
        toolBar.addSeparator()
        toolBar.addWidget(self.pixelValue)
        toolBar.setStyleSheet("background-color: white")  

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(toolBar)
        layout.addWidget(self.view) 
        layout.addWidget(self.imageSliders) 

        self.setLayout(layout)

    def _setConnections(self):

        self.view.mousePositionMoved.connect(self._mouseMoved)
        self.view.keyPress.connect(self._keyPress)
        self.toolBox.newTool.connect(self._setTool)
        self.imageSliders.valueChanged.connect(self._currentImageChanged)
        self.colors.valueChanged.connect(self._currentImageEdited)
        self.view.imageUpdated.connect(self.colors.setValue)

    def setData(self, series):

        self.imageSliders.setData(series, blockSignals=True)
        image = self.imageSliders.getImage()
        self.colors.setData(series, image)
        self.view.setData(image)
        self.view.fitImage()
        self.pixelValue.setData(image)

    def _currentImageEdited(self):

        self.view.imageItem.setPixMap()
        self.view.imageItem.update()

    def _keyPress(self, event):

        if event.key() == 16777234: # left
            self.imageSliders.move('first', -1)
        elif event.key() == 16777236: # right
            self.imageSliders.move('first', +1)
        elif event.key() == 16777235: # up
            self.imageSliders.move('second', +1)
        elif event.key() == 16777237: # down
            self.imageSliders.move('second', -1)

    def _setTool(self):

        tool = self.toolBox.getTool()
        self.view.setTool(tool)

    def _mouseMoved(self):

        tool = self.toolBox.getTool()
        self.pixelValue.setValue([tool.x, tool.y])
        
    def _currentImageChanged(self):

        image = self.imageSliders.getImage()
        self.colors.setImage(image)
        self.view.setData(image)
        self.pixelValue.setData(image)

    
class ImageView(QGraphicsView):
    """Wrapper for ImageItem displaying it in a scrollable Widget"""

    imageUpdated = pyqtSignal()
    mousePositionMoved = pyqtSignal()
    keyPress = pyqtSignal(QEvent)

    def __init__(self, image=None): 
        super().__init__()
      
        self.filterItems = []
        self.imageItem = ImageItem(image)

        scene = QGraphicsScene(self)
        scene.addItem(self.imageItem)
        scene.setFocusItem(self.imageItem)

        self.setScene(scene)
        self.setBackgroundBrush(QBrush(Qt.black))
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)

    def setToolBox(self, toolBox):

        self.filterItems = toolBox.allTools()
        for item in self.filterItems:
            self.scene().addItem(item)

    def setTool(self, filterItem):

        self.imageItem.installSceneEventFilter(filterItem)
        
    def setData(self, image):
  
        self.imageItem.setData(image)
        for item in self.filterItems:
            item.boundingRectangle = self.imageItem.boundingRectangle

    def fitImage(self):

        self.fitInView(self.imageItem, Qt.KeepAspectRatio)

    @property
    def image(self):
        return self.imageItem.image
        

class MaskView(ImageView):
    """Extends image view with a MaskItem for drawing masks.
    
    If no mask instance is provided, this creates
    a canvas that can be drawn on
    but the results can't be saved or retrieved."""

    newMask = pyqtSignal()

    def __init__(self, image=None, mask=None): 
        super().__init__(image)
      
        shape = self._shape(mask)
        self.maskItem = MaskItem(mask, shape)
        self.maskItem.newMask.connect(self._newMask)
        self.scene().addItem(self.maskItem)

    @property
    def mask(self):
        return self.maskItem.mask

    def _shape(self, mask): # private

        if mask is None:
            width = self.imageItem.pixMap.width()
            height = self.imageItem.pixMap.height() 
        else:            
            width = mask.Rows
            height = mask.Columns
        return width, height

    def setObject(self, mask): 
        self.maskItem.mask = mask

    def setData(self, image, mask):
        
        self.setImage(image)
        self.setMask(mask)

    def setImage(self, image):
        super().setData(image)
        
    def setMask(self, mask):

        self._updatePixelArray()
        shape = self._shape(mask)
        self.maskItem.mask = mask
        self.maskItem._setMaskImage(shape)

    def getMask(self):

        return self.mask

    def _updatePixelArray(self):
        """Write the current pixel array in the mask image"""

        if self.mask is None: return
        array = self.maskItem._getMaskImage()
        self.mask.set_array(array)

    def eraseMask(self): # not yet in use

        self.maskItem.eraseMaskImage()
        self._updatePixelArray()

    def _newMask(self):

        mask = self.image.copy()
        mask.WindowCenter = 1
        mask.WindowWidth = 2
        self.maskItem.mask = mask
        self._updatePixelArray()
        self.newMask.emit()


class MaskItem(QGraphicsObject):
    """Displays a mask as an overlay on an image.
    """

    newMask = pyqtSignal()

    def __init__(self, mask=None, shape=None): 
        super().__init__()

        self.bin = None
        self.qImage = None
        self.mask = mask
        
        self._setMaskImage(shape=shape)

    def _setMaskImage(self, shape=(128,128)):

        if self.mask is None:
            self.bin = np.zeros(shape, dtype=bool)
        else:
            self.bin = self.mask.array() != 0
        self.qImage = QImage(self.bin.shape[0], self.bin.shape[1], QImage.Format_RGB32)
        self.fillQImage()
        self.update()

    def boundingRect(self): 
        """Abstract method - must be overridden."""

        return QRectF(0, 0, self.bin.shape[0], self.bin.shape[1])

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""

        pixMap = QPixmap.fromImage(self.qImage)
        width = pixMap.width()
        height = pixMap.height()
        painter.setOpacity(0.25)
        painter.drawPixmap(0, 0, width, height, pixMap)

    def _getMaskImage(self):

        return self.bin.astype(float)

    def eraseMaskImage(self):

        self.bin.fill(False)
        self.fillQImage()

    def fillQImage(self):

        for x in range(self.bin.shape[0]):
            for y in range(self.bin.shape[1]):
                self.setPixel(x, y)

    def setPixel(self, x, y, add=None):

        if add is None:
            add = self.bin[x, y]
        else:
            self.bin[x,y] = add
        if add: 
            red = 255
            if self.mask is None:
                self.newMask.emit()
        else:
            red = 0
        color = qRgb(red, 0, 0)
        self.qImage.setPixel(x, y, color)


class ImageItem(QGraphicsObject):
    """Displays an image.
    """

    def __init__(self, image): 
        super().__init__()

        #self.view = view
        self.boundingRectangle = QRectF(0, 0, 128, 128)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable)
        self.setData(image)

    def setData(self, image):

        if image is not None:
            self.boundingRectangle = QRectF(0, 0, image.Columns, image.Rows)
        self.image = image
        self.setPixMap()
        self.update()

    def boundingRect(self): 
        """Abstract method - must be overridden."""

        return self.boundingRectangle

    def paint(self, painter, option, widget):
        """Executed by GraphicsView when calling update()"""

        width = self.pixMap.width()
        height = self.pixMap.height()
        painter.drawPixmap(0, 0, width, height, self.pixMap)

    def setPixMap(self):

        if self.image is None:
            width = int(self.boundingRectangle.width())
            height = int(self.boundingRectangle.height())
            self.pixMap = QPixmap(width, height)
            self.pixMap.fill(Qt.black)
        else:
            self.qImage = self.image.QImage()
            self.pixMap = QPixmap.fromImage(self.qImage)


class ImageViewCursor(QGraphicsObject):
    """Base class for ImageView Cursor Tools.
    """

    def __init__(self): 
        super().__init__()

        self.boundingRectangle = QRectF(0, 0, 128, 128)

        self.contrastCursor = QCursor(QPixmap(icons.contrast), hotX=4, hotY=0)
        self.arrowMoveCursor = QCursor(QPixmap(icons.arrow_move), hotX=4, hotY=0)
        self.cursor = QCursor(QPixmap(icons.hand_point_090), hotX=4, hotY=0)
        self.icon = QIcon(QPixmap(icons.hand_point_090))
        self.toolTip = "Cursor" 
        self.x = None
        self.y = None

    def boundingRect(self): 
        """Abstract method - must be overridden."""
        return self.boundingRectangle

    def paint(self, painter, option, widget):
        """Abstract method - must be overridden."""
        pass

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.KeyPress:

            if event.key() in [16777234, 16777235, 16777236, 16777237]:
                #[left, up, right, down]
                view.keyPress.emit(event)

        elif event.type() == QEvent.GraphicsSceneHoverEnter:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            item.setCursor(self.cursor)
            view.mousePositionMoved.emit()

        elif event.type() == QEvent.GraphicsSceneHoverLeave:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            view.mousePositionMoved.emit()

        elif event.type() == QEvent.GraphicsSceneHoverMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            view.mousePositionMoved.emit()

        elif event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.button()
            if button == Qt.LeftButton:
                item.setCursor(self.arrowMoveCursor)
            elif button == Qt.RightButton:
                item.setCursor(self.contrastCursor)

        elif event.type() == QEvent.GraphicsSceneMouseRelease:

            item.setCursor(self.cursor)

        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.buttons()
            if button == Qt.LeftButton:
                self.pan(item, event)
            elif button == Qt.RightButton:
                self.window(item, event)

        elif event.type() == QEvent.GraphicsSceneWheel:

            if event.delta() < 0:
                zoomFactor = 1.25
            else:
                zoomFactor = 1/1.25
            view.scale(zoomFactor, zoomFactor)
        return True # do not process further

    def pan(self, item, event):
        """Pan the image
        
        Note: this can be implemented more easily as
        self.view.setDragMode(QGraphicsView.ScrollHandDrag)
        but reimplemented here to control the cursor and as a template
        """

        distance = event.screenPos() - event.lastScreenPos()
        self.blockSignals(True)
        view = item.scene().parent()
        hBar = view.horizontalScrollBar()
        vBar = view.verticalScrollBar()
        hBar.setValue(hBar.value() - distance.x())
        vBar.setValue(vBar.value() - distance.y())
        self.blockSignals(False)

    def window(self, item, event):
        """Change intensity and contrast"""

        image = item.image
        if image is None: 
            return
        distance = event.screenPos() - event.lastScreenPos()
        center = image.WindowCenter
        width = image.WindowWidth
        if float(center / image.Columns) > 0.01:
            step_y = float(center / image.Columns)
        else:
            step_y = 0.01
        if float(width / image.Rows) > 0.01:
            step_x = float(width/ image.Rows)
        else:
            step_x = 0.01
        horizontalDiff = step_y * distance.y()
        verticalDiff = step_x * distance.x()
        newCenter = center + horizontalDiff
        newWidth = width + verticalDiff
        image.WindowCenter = newCenter
        image.WindowWidth = newWidth
        item.setPixMap()
        item.update()
        view = item.scene().parent()
        view.imageUpdated.emit()


class ImageViewZoom(ImageViewCursor):
    """Provides zoom/pan/windowing functionality for a MaskOverlay.
    """

    def __init__(self): 
        super().__init__()

        pixMap = QPixmap(icons.magnifier)
        #self.magnifierCursor = QCursor(pixMap, hotX=10, hotY=4)
        self.cursor = QCursor(pixMap, hotX=10, hotY=4)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Zoom tool'
        self.x0 = None
        self.y0 = None

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.button()
            if button == Qt.LeftButton:
                self.x0 = self.x
                self.y0 = self.y

        elif event.type() == QEvent.GraphicsSceneMouseRelease:

            if event.button() == Qt.LeftButton:
                if self.x0 is not None:
                    width = self.x - self.x0
                    height = self.y - self.y0
                    view.fitInView(self.x0, self.y0, width, height, Qt.KeepAspectRatio)
            elif event.button() == Qt.RightButton:
                view.fitInView(item, Qt.KeepAspectRatio)
            self.x0 = None
            self.y0 = None
            item.setCursor(self.cursor)
            item.update() 
            self.update()

        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.buttons()
            if button == Qt.LeftButton:
                item.update()
                self.update()

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further

    def paint(self, painter, option, widget):

        if self.x0 is not None:
            width = self.x - self.x0
            height = self.y - self.y0
            pen = QPen()
            pen.setColor(QColor(Qt.white))
            pen.setWidth(0)
            painter.setPen(pen)
            painter.drawRect(self.x0, self.y0, width, height)


class MaskViewBrush(ImageViewCursor):
    """Painting or erasing tool.
    
    Features
    --------
    >>> Left click and drag to paint or erase.
    >>> Right click to change the brush properties
    (erase or paint, size of the brush).
    >>> Right click and drag to change the windowing.
    """

    def __init__(self, brushSize=1, mode="paint"):
        super().__init__()

        self.setBrushSize(brushSize)
        self.setMode(mode)

    def setBrushSize(self, brushSize):

        self.brushSize = brushSize

    def setMode(self, mode):

        self.mode = mode
        if mode == "paint":
            pixMap = QPixmap(widgets.icons.paint_brush)
            self.cursor = QCursor(pixMap, hotX=0, hotY=16)
            self.toolTip = 'Paint brush'
        elif mode == "erase":
            pixMap = QPixmap(widgets.icons.eraser)
            self.cursor = QCursor(pixMap, hotX=0, hotY=16)
            self.toolTip = 'Eraser'
        self.icon = QIcon(pixMap)

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.button()
            if button == Qt.LeftButton:
                self.paintPixels()
            elif button == Qt.RightButton:
                self.launchContextMenu(event)

        elif event.type() == QEvent.GraphicsSceneMouseRelease:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())

        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            buttons = event.buttons()
            if buttons == Qt.LeftButton:
                self.paintPixels()  
            view.mousePositionMoved.emit()

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further

    def paintPixels(self):

        view = self.scene().parent()
   
        w = int((self.brushSize - 1)/2)
        for x in range(self.x-w, self.x+w+1, 1):
            if 0 <= x < view.maskItem.bin.shape[0]:
                for y in range(self.y-w, self.y+w+1, 1):
                    if 0 <= y < view.maskItem.bin.shape[1]:
                        view.maskItem.setPixel(x, y, self.mode == "paint")
        view.maskItem.update()
       
    def launchContextMenu(self, event):

        view = self.scene().parent()

        pickBrush = QAction(QIcon(widgets.icons.paint_brush), 'Paint', None)
        pickBrush.setCheckable(True)
        pickBrush.setChecked(self.mode == "paint")
        pickBrush.triggered.connect(lambda: self.setMode("paint"))
        
        pickEraser = QAction(QIcon(widgets.icons.eraser), 'Erase', None)
        pickEraser.setCheckable(True)
        pickEraser.setChecked(self.mode == "erase")
        pickEraser.triggered.connect(lambda: self.setMode("erase"))

        clearMask = QAction(QIcon(widgets.icons.arrow_curve_180_left), 'Clear Region', None)
        clearMask.triggered.connect(view.maskItem.eraseMaskImage)

        onePixel = QAction('1 pixel', None)
        onePixel.setCheckable(True)
        onePixel.setChecked(self.brushSize == 1)
        onePixel.triggered.connect(lambda: self.setBrushSize(1))

        threePixels = QAction('3 pixels', None)
        threePixels.setCheckable(True)
        threePixels.setChecked(self.brushSize == 3)
        threePixels.triggered.connect(lambda: self.setBrushSize(3))

        fivePixels = QAction('5 pixels', None)
        fivePixels.setCheckable(True)
        fivePixels.setChecked(self.brushSize == 5)
        fivePixels.triggered.connect(lambda: self.setBrushSize(5))

        sevenPixels = QAction('7 pixels', None)
        sevenPixels.setCheckable(True)
        sevenPixels.setChecked(self.brushSize == 7)
        sevenPixels.triggered.connect(lambda: self.setBrushSize(7))

        ninePixels = QAction('9 pixels', None)
        ninePixels.setCheckable(True)
        ninePixels.setChecked(self.brushSize == 9)
        ninePixels.triggered.connect(lambda: self.setBrushSize(9))

        elevenPixels = QAction('11 pixels', None)
        elevenPixels.setCheckable(True)
        elevenPixels.setChecked(self.brushSize == 11)
        elevenPixels.triggered.connect(lambda: self.setBrushSize(11))

        twentyOnePixels = QAction('21 pixels', None)
        twentyOnePixels.setCheckable(True)
        twentyOnePixels.setChecked(self.brushSize == 21)
        twentyOnePixels.triggered.connect(lambda: self.setBrushSize(21))

        contextMenu = QMenu()
        contextMenu.addAction(pickBrush)
        contextMenu.addAction(pickEraser)
        contextMenu.addAction(clearMask)

        subMenu = contextMenu.addMenu('Brush size')
        subMenu.setEnabled(True)
        # subMenu.clear()
        subMenu.addAction(onePixel)
        subMenu.addAction(threePixels)
        subMenu.addAction(fivePixels)
        subMenu.addAction(sevenPixels)
        subMenu.addAction(ninePixels)
        subMenu.addAction(elevenPixels)
        subMenu.addAction(twentyOnePixels)

        contextMenu.exec_(event.screenPos())


class MaskViewPenFreehand(ImageViewCursor):
    """Freehand region drawing tool.
    
    Features
    --------
    >>> Left click and drag to draw, release to close
    >>> Right click to change the pen properties
    """

    def __init__(self, mode="draw"):
        super().__init__()

        self.icon = QIcon(widgets.icons.layer_shape_curve)
        self.path = None
        self.setMode(mode)
        
    def setMode(self, mode):

        self.mode = mode
        if mode == "draw":
            pixMap = QPixmap(widgets.icons.pencil)
            self.cursor = QCursor(pixMap, hotX=0, hotY=16)
            self.toolTip = 'Draw'
        elif mode == "cut":
            pixMap = QPixmap(widgets.icons.cutter)
            self.cursor = QCursor(pixMap, hotX=0, hotY=16)
            self.toolTip = 'Cut'
        
    def paint(self, painter, option, widget):

        if self.path is None: return

        pen = QPen()
        pen.setColor(QColor(Qt.white))
        pen.setWidth(0)
        painter.setPen(pen)

        position = self.path[0]
        p1 = QPointF(position[0], position[1])
        for position in self.path[1:]:
            p2 = QPointF(position[0], position[1])
            painter.drawLine(p1, p2)
            p1 = p2
        position = self.path[0]
        p2 = QPointF(position[0], position[1])
        painter.drawLine(p1, p2)

    def sceneEventFilter(self, item, event):

        if event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            if event.button() == Qt.LeftButton:
                position = [event.pos().x(), event.pos().y()]
                self.path = [position]
            elif event.button() == Qt.RightButton:
                self.launchContextMenu(event)

        elif event.type() == QEvent.GraphicsSceneMouseRelease:
        
            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.button()
            if button == Qt.LeftButton:
                if self.path is not None:
                    self.fillPath()
                    self.path = None
            
        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            buttons = event.buttons()
            if buttons == Qt.LeftButton:
                position = [event.pos().x(), event.pos().y()]
                #if position not in self.path:
                if position != self.path[-1]:
                    self.path.append(position)
                    item.update()
                    self.update()

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further

    def fillPath(self):

        view = self.scene().parent()

        if len(self.path) == 0: 
            return

        nx, ny = view.maskItem.bin.shape[0], view.maskItem.bin.shape[1]
        x, y = np.meshgrid(np.arange(0.5, 0.5+nx), np.arange(0.5, 0.5+ny), indexing='ij')
        points = list(zip(x.flatten(), y.flatten()))
        #points = np.vstack((x.flatten(), y.flatten())).transpose()

        roiPath = MplPath(self.path, closed=True)
        bin = roiPath.contains_points(points, radius=0.0).reshape((nx, ny))
        #bin = np.transpose(bin != 0)
        #bin = bin != 0
        if self.mode == "draw":
            view.maskItem.bin = np.logical_or(view.maskItem.bin, bin)
        elif self.mode == "cut":
            view.maskItem.bin = np.logical_and(view.maskItem.bin, np.logical_not(bin))
        view.maskItem.fillQImage()
        view.maskItem.update()
        
    def launchContextMenu(self, event):

        view = self.scene().parent()

        pickBrush = QAction(QIcon(widgets.icons.pencil), 'Draw', None)
        pickBrush.setCheckable(True)
        pickBrush.setChecked(self.mode == "draw")
        pickBrush.triggered.connect(lambda: self.setMode("draw"))
        
        pickEraser = QAction(QIcon(widgets.icons.cutter), 'Cut', None)
        pickEraser.setCheckable(True)
        pickEraser.setChecked(self.mode == "cut")
        pickEraser.triggered.connect(lambda: self.setMode("cut"))

        clearMask = QAction(QIcon(widgets.icons.arrow_curve_180_left), 'Clear mask', None)
        clearMask.triggered.connect(view.maskItem.eraseMaskImage)

        contextMenu = QMenu()
        contextMenu.addAction(pickBrush)
        contextMenu.addAction(pickEraser)
        contextMenu.addAction(clearMask)
        contextMenu.exec_(event.screenPos())


class MaskViewPenPolygon(MaskViewPenFreehand):
    """Polygon region drawing tool.
    
    Features
    --------
    >>> Left click and drag to draw, release to close
    >>> Right click to change the pen properties
    """

    def __init__(self, mode="draw"):
        super().__init__(mode=mode)

        self.icon = QIcon(widgets.icons.layer_shape_polygon)

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.GraphicsSceneHoverMove:

            if self.path is not None:
                self.path[-1] = [event.pos().x(), event.pos().y()]
                view.maskItem.update()
            super().sceneEventFilter(item, event)

        elif event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            if event.button() == Qt.LeftButton:
                position = [event.pos().x(), event.pos().y()]
                if self.path is None:
                    self.path = [position, position]
                else:
                    self.path[-1] = position
                    self.path.append(position)
            elif event.button() == Qt.RightButton:
                self.launchContextMenu(event)

        elif event.type() == QEvent.GraphicsSceneMousePress:
            pass

        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            self.path[-1] = [event.pos().x(), event.pos().y()]
            view.maskItem.update()

        elif event.type() == QEvent.GraphicsSceneMouseDoubleClick:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            button = event.button()
            if button == Qt.LeftButton:
                if self.path is not None:
                    self.path[-1] = [event.pos().x(), event.pos().y()]
                    self.fillPath()
                    view.maskItem.update()
                    self.path = None

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further


class MaskViewPenRectangle(MaskViewPenFreehand):
    """Rectangle region drawing tool.
    
    Features
    --------
    >>> Left click and drag to draw, release to close
    >>> Right click to change the pen properties
    """

    def __init__(self, mode="draw"):
        super().__init__(mode=mode)

        self.icon = QIcon(widgets.icons.layer_shape)

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            buttons = event.buttons()
            if buttons == Qt.LeftButton:
                corner1 = self.path[0]
                corner2 = [event.pos().x(), event.pos().y()]
                self.path = [
                    [corner1[0], corner1[1]], 
                    [corner2[0], corner1[1]], 
                    [corner2[0], corner2[1]],
                    [corner1[0], corner2[1]],
                    [corner1[0], corner1[1]]]
                view.maskItem.update()

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further


class MaskViewPenCircle(MaskViewPenFreehand):
    """Rectangle region drawing tool.
    
    Features
    --------
    >>> Left click and drag to draw, release to close
    >>> Right click to change the pen properties
    """

    def __init__(self, mode="draw"):
        super().__init__(mode=mode)

        self.icon = QIcon(widgets.icons.layer_shape_ellipse)
        self.center = None

    def sceneEventFilter(self, item, event):

        view = item.scene().parent()

        if event.type() == QEvent.GraphicsSceneMousePress:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            if event.button() == Qt.LeftButton:
                self.center = [event.pos().x(), event.pos().y()]
            elif event.button() == Qt.RightButton:
                self.launchContextMenu(event)
            
        elif event.type() == QEvent.GraphicsSceneMouseMove:

            self.x = int(event.pos().x())
            self.y = int(event.pos().y())
            buttons = event.buttons()
            if buttons == Qt.LeftButton:
                p = [event.pos().x(), event.pos().y()]
                self.setCirclePath(p)
                view.maskItem.update()

        else:
            super().sceneEventFilter(item, event)
        return True # do not process further

    def setCirclePath(self, p):
        """Return a circle with center in c and going through point p"""

        c = self.center
        pc = [p[0]-c[0], p[1]-c[1]]
        radius = math.sqrt(pc[0]**2 + pc[1]**2)
        if radius == 0: return
        step = 0.5 # pixel - precision of the circle
        if step > radius: step = radius
        angle = math.acos(1-0.5*(step/radius)**2)
        nsteps = round(2*math.pi/angle)
        angle = 2*math.pi/nsteps
        x0 = pc[0]
        y0 = pc[1]
        self.path = [p]
        for _ in range(nsteps):
            x = math.cos(angle)*x0 - math.sin(angle)*y0
            y = math.sin(angle)*x0 + math.cos(angle)*y0
            self.path.append([c[0] + x, c[1] + y])
            x0 = x
            y0 = y