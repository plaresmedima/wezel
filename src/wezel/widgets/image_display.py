from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout, 
    QLabel, 
    QToolBar,
)
from .. import widgets as widget
import wezel.icons as icons

class ImageLabel(QLabel):

    def __init__(self):
        super().__init__()
        self.setScaledContents(True)
        self.setData(icons.wezel)
        
    def setData(self, file):
        self.im = QPixmap(file).scaledToWidth(512)
        self.setPixmap(self.im)


