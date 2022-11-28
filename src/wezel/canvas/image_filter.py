import numpy as np

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QAction, QMenu, QPushButton, QActionGroup
from PyQt5.QtGui import QPixmap, QCursor, QIcon

from wezel import canvas, icons


class ImageWindow(canvas.FilterItem):
    """Change contrast
    """
    def __init__(self): 
        super().__init__()
        pixMap = QPixmap(icons.color)
        self.cursor = QCursor(pixMap, hotX=4, hotY=0)
        self.icon = QIcon(pixMap)
        self.toolTip = 'Select color scale window..'
        self.text = 'Window' 
        self.setActionPick()

    def window(self, dx, dy):
        """Change intensity and contrast"""

        cnvs = self.scene().parent()
        image = cnvs.imageItem.image
        image.mute()
        min = image.SmallestImagePixelValue
        max = image.LargestImagePixelValue
        if (min is None) or (max is None):
            array = image.get_pixel_array()
            min = np.amin(array)
            max = np.amax(array)
            image.SmallestImagePixelValue = min
            image.LargestImagePixelValue = max
       
        # Move 1024 to change the center over the full range
        # Speed is faster further away from the center of the range
        center = image.WindowCenter 
        v0 = (max-min)/1024
        a0 = 1.0/256
        vy = v0 + a0*abs((center - (min+(max-min)/2.0)))
        center = center + vy * dy
        image.WindowCenter = center

        # Changing the width is faster at larger widths
        width = image.WindowWidth
        v0 = (max-min)/512
        a0 = 1.0/64
        vx = v0 + a0*width
        width = width - vx * dx
        image.WindowWidth = width if width>1 else 1

        cnvs.imageItem.setQImage()
        cnvs.imageItem.update()
#        cnvs.imageUpdated.emit(image)
        if cnvs.toolBar is not None:
            cnvs.toolBar.window.setData(image, set=True)
        image.unmute()

    def mouseMoveEvent(self, event):
        self.x = int(event.pos().x())
        self.y = int(event.pos().y())
        button = event.buttons()
        if button == Qt.LeftButton:
            d = event.screenPos() - event.lastScreenPos()
            self.window(d.x(), d.y())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.x0 = None
            self.y0 = None 

    def contextMenu(self):
        return self.actionPick.menu()

    def menuOptions(self):
        menu = QMenu()
        menu.setIcon(QIcon(icons.spectrum))
        menu.setTitle('Set colormap..')
        menu.triggered.connect(lambda action: self.setColorMap(action.cmap))
        actionGroup = QActionGroup(menu)
        default = None
        self.addActionSetColormap(menu, actionGroup, None, default)
        self.addSeparator(menu)
        COLORMAPS = canvas.COLORMAPS
        for group in range(5):
            for cmap in COLORMAPS[group][1]:
                self.addActionSetColormap(menu, actionGroup, cmap, default)
            self.addSeparator(menu)
        for cmap in COLORMAPS[5][1]:
            self.addActionSetColormap(menu, actionGroup, cmap, default)
        return menu

    def setData(self, image, set=None):
        pass

    def setColorMap(self, cmap):
        self.pick()
        self.scene().parent().imageItem.setColormap(cmap)

    def getColorMap(self):
        menu = self.actionPick.menu()
        for action in menu.actions():
            if not action.isSeparator():
                if action.isChecked():
                    return action.cmap

    def setData(self, image, set=True):
        if image is None:
            return
        if set:  # adjust selection value to image cmap
            self.updateAction(image)
        else:    # adjust image cmap to selection 
            image.colormap = self.getColorMap()       

    def updateAction(self, image, cmap=None):
        menu = self.actionPick.menu()
        if cmap is None:
            cmap = image.colormap
        for action in menu.actions():
            if not action.isSeparator():
                checked = action.cmap == cmap
                action.setChecked(checked)
    
    def addActionSetColormap(self, menu, actionGroup, cmap, current):
        text = cmap
        if text is None:
            text = 'Greyscale'
        action = QAction(text)
        action.setCheckable(True)
        action.setChecked(cmap == current)
        action.cmap = cmap
        actionGroup.addAction(action)
        menu.addAction(action)
