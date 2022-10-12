from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QPushButton

from .. import widgets as widgets



class ToolBox(QWidget):
    """General purpose toolbox for cursor tools"""

    newTool = pyqtSignal()
    
    def __init__(self, *tools):
        super().__init__()

        self.buttons = {}
        self.current = tools[0].__class__.__name__
        self._defineWidgets(*tools)
        self._defineLayout()
        self.setTool(self.current)

    def _defineWidgets(self, *tools):

        for tool in tools:
            self._defineButton(tool)

    def _defineButton(self, tool):

        key = tool.__class__.__name__
        self.buttons[key] = QPushButton()
        self.buttons[key].setToolTip(tool.toolTip)
        self.buttons[key].setCheckable(True)
        self.buttons[key].setIcon(tool.icon)
        self.buttons[key].tool = tool
        self.buttons[key].clicked.connect(lambda: self._buttonClicked(key))     

    def _defineLayout(self):

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for button in self.buttons.values():
            layout.addWidget(button, alignment=Qt.AlignLeft)
        self.setLayout(layout)

    def _buttonClicked(self, key):

        self.setTool(key)
        self.newTool.emit()

    def setTool(self, key):
        
        #self.buttons[self.current].blockSignals(True)
        self.buttons[self.current].setChecked(False)
        #self.buttons[self.current].blockSignals(False)
        self.current = key
        #self.buttons[self.current].blockSignals(True)
        self.buttons[self.current].setChecked(True)
        #self.buttons[self.current].blockSignals(False)

    def getTool(self):

        return self.buttons[self.current].tool

    def allTools(self):

        return [button.tool for button in self.buttons.values()]


class MaskViewToolBox(QWidget):

    newTool = pyqtSignal()
    
    def __init__(self):
        super().__init__()

        self.button = {}
        self.current = "ImageViewCursor"
        self.defineWidgets()
        self.defineLayout()
        self.setTool(self.current) 
        
    def defineWidgets(self):

        self.defineButton(widgets.ImageViewCursor())
        self.defineButton(widgets.ImageViewZoom())
        self.defineButton(widgets.MaskViewBrush())
        self.defineButton(widgets.MaskViewPenFreehand())
        self.defineButton(widgets.MaskViewPenPolygon())
        self.defineButton(widgets.MaskViewPenRectangle())
        self.defineButton(widgets.MaskViewPenCircle())
        self.defineButton(widgets.MaskViewRegionGrowing())
        self.defineButton(widgets.MaskViewDeleteROI())
        self.defineButton(widgets.MaskViewEdgeDetection())
        self.defineButton(widgets.MaskViewErode())
        self.defineButton(widgets.MaskViewDilate())


    def defineButton(self, tool):

        key = tool.__class__.__name__
        self.button[key] = QPushButton()
        self.button[key].setToolTip(tool.toolTip)
        self.button[key].setCheckable(True)
        self.button[key].setIcon(tool.icon)
        self.button[key].tool = tool
        self.button[key].clicked.connect(lambda: self.buttonClicked(key))     
        
    def defineLayout(self):

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        for button in self.button.values():
            layout.addWidget(button, alignment=Qt.AlignLeft)
        self.setLayout(layout)

    def buttonClicked(self, key):

        self.setTool(key)
        self.newTool.emit()

    def setTool(self, key):

        self.button[self.current].setChecked(False)
        self.current = key
        self.button[self.current].setChecked(True)

    def getTool(self):

        return self.button[self.current].tool