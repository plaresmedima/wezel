

import sys
import logging

#from PyQt5.QtCore import *
from PyQt5.QtCore import  pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QWidget, 
    QApplication, 
    QMainWindow, 
    QAction, 
    QMenu, 
    QMenuBar, 
    QDockWidget, 
    QMessageBox) 
from PyQt5.QtGui import QIcon

import dbdicom as db
import wezel

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


# Examples of style sheets
# https://doc.qt.io/qtforpython/overviews/stylesheet-examples.html
# 



STYLESHEET = """
    QWidget {
        background-color: #1E1E1E;
        color: #DCDCDC;
    }

    QMenuBar {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenuBar::item {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenu {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenu::item {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QTabWidget {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QTabWidget::pane {
        border: 1px solid #3F3F3F;
        background-color: #2C2C2C;
    }

    QTabWidget::tab-bar {
        left: 5px; /* move to the right by 5px */
    }

    QTabBar::tab {
        background-color: #2C2C2C;
        color: #DCDCDC;
        padding: 5px;
        border: 1px solid #3F3F3F;
        border-bottom-color: #2C2C2C; /* same as pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background-color: #3F3F3F;
    }

    """


SMALLSTYLESHEET = """

    QMenuBar {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenuBar::item {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenu {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QMenu::item {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QTabWidget {
        background-color: #2C2C2C;
        color: #DCDCDC;
    }

    QTabWidget::pane {
        border: 1px solid #3F3F3F;
        background-color: #2C2C2C;
    }

    QTabWidget::tab-bar {
        left: 5px; /* move to the right by 5px */
    }

    QTabBar::tab {
        background-color: #2C2C2C;
        color: #DCDCDC;
        padding: 5px;
        border: 1px solid #3F3F3F;
        border-bottom-color: #2C2C2C; /* same as pane color */
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
    }

    QTabBar::tab:selected {
        background-color: #3F3F3F;
    }

    """


class Wezel:

    def __init__(self):
        self.log = logger()
        self.QApp = QApplication(sys.argv)
        self.QApp.setWindowIcon(QIcon(wezel.icons.favicon))
        self.main = Main(self)

    def open(self, path):
        self.main.open(path)

    def show(self):    
        self.log.info('Launching Wezel!')
        try:
            self.main.show()
            self.QApp.exec()
            #sys.exit(self.QApp.exec())
        except Exception as e:
            # Use QMessage
            print('Wezel Error: ' + str(e))
            self.log.exception('Wezel Error: ' + str(e))


class Main(QMainWindow):

    def __init__(self, wzl): 
        """
        Initialize the Wezel class and its attributes.
        
        Parameters:
            wzl (object): An instance of the wezel class.
        
        Attributes:
            wezel (object): An instance of the wezel class, passed as an argument.
            dialog (object): An instance of the Dialog class from the wezel.widgets module.
            status (object): An instance of the StatusBar class from the wezel.widgets module.
            toolBar (dict): A dictionary to store the toolbar widgets.
            toolBarDockWidget (QDockWidget): A QDockWidget instance to hold the toolbar.
            treeView (None): Placeholder for the treeview widget.
            treeViewDockWidget (QDockWidget): A QDockWidget instance to hold the treeview.
            folder (None): Placeholder for the folder widget.
            central (object): An instance of the MainMultipleDocumentInterface class from the wezel.widgets module.
        """

        super().__init__()
        self.wezel = wzl
        #self.setStyleSheet(SMALLSTYLESHEET)
        self.setWindowTitle("Wezel")
        
        # self.offset = None
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowMinMaxButtonsHint)
        # self.setMouseTracking(True)

        self.dialog = wezel.widgets.Dialog(self)
        self.status = wezel.widgets.StatusBar()
        self.setStatusBar(self.status)

        self.toolBar = {}
        self.toolBarDockWidget = QDockWidget()
        self.addDockWidget(Qt.RightDockWidgetArea, self.toolBarDockWidget)
        self.toolBarDockWidget.hide()

        self.treeView = None
        self.treeViewDockWidget = QDockWidget()
        self.addDockWidget(Qt.LeftDockWidgetArea, self.treeViewDockWidget)
        self.treeViewDockWidget.hide()

        self.folder = None # should be in TreeView
        self.central = wezel.widgets.MainMultipleDocumentInterface()
        self.central.subWindowActivated.connect(lambda subWindow: self.activateSubWindow(subWindow))
        self.setCentralWidget(self.central)

        self.set_menu(wezel.menus.dicom)

    # def mousePressEvent(self, event):
    #     self.offset = event.pos()

    # def mouseMoveEvent(self, event):
    #     if self.offset is not None:
    #         x=event.globalX()
    #         y=event.globalY()
    #         x_w = self.offset.x()
    #         y_w = self.offset.y()
    #         self.move(x-x_w, y-y_w)

    # def mouseReleaseEvent(self, event):
    #     self.offset is None
        
    # def resizeEvent(self, event):
    #     # add 8px padding on each side
    #     self.setContentsMargins(8, 8, 8, 8)
    #     super().resizeEvent(event)

    def closeEvent(self, event): #main
        accept = self.close()
        if accept:
            event.accept()
        else:
            event.ignore()

    def set_menu(self, menu):
        self.menubar = MenuBar(self, menu)
        self.setMenuBar(self.menubar)

    def open(self, path):
        self.folder = db.database(path=path, 
            status = self.status, 
            dialog = self.dialog)
        self.display(self.folder)
        self.status.hide()

    def close(self):
        """Closes the application."""
        if self.folder is None:
            return True
        accept = self.folder.close()
        if accept:
            self.folder = None
            self.toolBarDockWidget.hide()
            self.treeViewDockWidget.hide()
            for subWindow in self.central.subWindowList():
                self.central.removeSubWindow(subWindow)
            self.menuBar().enable()
        return accept

    def refresh(self):
        """
        Refreshes the Wezel display.
        """
        self.status.message('Refreshing display..')
        self.treeView.setFolder()
        self.menuBar().enable()
        self.status.hide()
        
    def display(self, object):
        if object is None:
            self.dialog.information('There are no data to show here')
            return
        if object.type() == 'Database':
            self.treeView = wezel.widgets.DICOMFolderTree(object)
            self.treeView.itemSelectionChanged.connect(self.menuBar().enable)
            self.treeViewDockWidget.setWidget(self.treeView)
            self.treeViewDockWidget.show()
            self.menuBar().enable()
        elif object.type() == 'Patient': # No Patient Viewer yet
            pass
        elif object.type() == 'Study': # No Study Viewer yet
            pass
        elif object.type() == 'Series':
            seriesDisplay = wezel.widgets.SeriesDisplay()
            seriesDisplay.setSeries(object)
            self.addWidget(seriesDisplay, title=object.label())
        elif object.type() == 'Instance':
            pass

    def get_selected(self, generation):   
        if self.treeView is None: 
            return []
        return self.treeView.get_selected(generation)

    def selected(self, generation):
        if self.treeView is None: 
            return []
        return self.treeView.selected(generation)
 
    def nr_selected(self, generation):
        if self.treeView is None: 
            return 0
        return self.treeView.nr_selected(generation)

    def closeSubWindow(self, subWindow):
        self.central.removeSubWindow(subWindow)
        self.central.tileSubWindows()
        # The widget continues to exist - memory issues?
        # Delete widget when subwindow closes
        widget = subWindow.widget().__class__.__name__
        if 0 == self.central.countSubWindow(widget):
            toolBar = subWindow.widget().toolBar
            if toolBar is not None:
                toolBar.setEnabled(False)
            #self.toolBarDockWidget.hide()
        #self.refresh()

    def activateSubWindow(self, subWindow):
        if self.central.activeWindow == subWindow:
            return
        activeWindow = self.central.activeWindow
        if activeWindow is not None:
            activeWindow.widget().setActive(False)
        self.central.activeWindow = subWindow
        if subWindow is not None:
            subWindow.widget().setActive(True)
            # If the main widget has a toolbar, set its state
            # add it as a dockwidget.
            toolBar = subWindow.widget().toolBar
            if toolBar is not None:
                subWindow.widget().setToolBarState()
                self.toolBarDockWidget.setWidget(toolBar)

    def addWidget(self, widget, title):
        # rename to addSubWindow()
        # widget needs to be subclassed from MainWidget
        if widget.error:
            return
        subWindow = self.central.addWidget(widget, title)
        subWindow.closed.connect(lambda: self.closeSubWindow(subWindow))
        self.central.tileSubWindows()
        widget.databaseUpdated.connect(self.refresh)
        # If the right kind of toolbar does not exist yet, create it and show it
        # If it does exist juts set it as current.
        if widget.toolBarClass is not None:
            toolBarName =  widget.toolBarClass.__name__
            if toolBarName in self.toolBar:
                toolBar = self.toolBar[toolBarName]
                self.toolBarDockWidget.setWidget(toolBar)
                widget.setToolBar(toolBar)
            else:
                toolBar =  widget.toolBarClass()
                self.toolBar[toolBarName] = toolBar
                self.toolBarDockWidget.setWidget(toolBar)
                widget.setToolBar(toolBar)
                self.toolBarDockWidget.show()
        self.menuBar().enable() # added


class MainWidget(QWidget):
    """Base class for widgets that are set as subWindow widgets"""

    databaseUpdated = pyqtSignal() 

    def __init__(self):
        super().__init__()
        self.toolBarClass = None
        self.toolBar = None
        self.error = False

    def setError(self, message='Error displaying data!!'):
        self.error = True
        QMessageBox.information(self, 'Information', message)

    def setToolBar(self, toolBar):
        self.toolBar = toolBar
        self.setToolBarState()

    def setToolBarState(self):
        self.toolBar.setWidget(self)
        self.toolBar.setEnabled(True)
        
    def setActive(self, active):
        pass
        # If the window is activated, set its toolbar
        # to the toolbar dockwidget
        # if active:
        #     if self.toolBar is not None:
        #         self.setToolBarState()
        #         subWindow = self.parentWidget()
        #         mdiArea = subWindow.mdiArea()
        #         mainWindow = mdiArea.parentWidget()
        #         mainWindow.toolBarDockWidget.setWidget(self.toolBar)
                
    def closeEvent(self, event):
        pass



class MenuBar(QMenuBar):
    """
    Programming interfaces for the Wezel menus. 
    """

    def __init__(self, main, menu):
        super().__init__()

        self._menus = []
        self.main = main
        menu(self)
        self.enable()

    def addMenu(self, menu):
        super().addMenu(menu)
        self._menus.append(menu)
        
    def menu(self, label = "Menu"):
        """
        Creates a top level menu in the menuBar.
        """
        return Menu(self, label)

    def enable(self):
        """
        Refreshes the enabled status of each menu item.
        """
        for menu in self._menus:
            menu.enable()


class Menu(QMenu):

    def __init__(self, parent, title='Menu'):
        super().__init__()

        self._actions = []
        self._menus = []
        self.setTitle(title)
        self.main = parent.main
        if parent is not None:
            parent.addMenu(self)

    def addMenu(self, menu):
        super().addMenu(menu)
        self._menus.append(menu)

    def menu(self, title='Submenu'):
        return Menu(self, title)

    def action(self, action, **kwargs):
        #return action(self, **kwargs)
        action = action(self, **kwargs)
        self.addAction(action)
        self._actions.append(action)
        return action
        
    def separator(self):
        self.addSeparator() 

    def enable(self):
        """
        Refreshes the enabled status of each menu item.
        """
        for submenu in self._menus:
            submenu.enable()
        for action in self._actions:
            enable = action.enable(action.main)
            action.setEnabled(enable)


class Action(QAction):
    """Base class for all wezel actions"""

    def __init__(self, parent,
        text = None,
        shortcut = None,
        tooltip = None, 
        icon = None,  
        **kwargs):
        """parent: App, Menu or MenuBar"""
        super().__init__()

        self.main = parent.main
        # parent.addAction(self)
        # parent._actions.append(self)

        # if hasattr(parent, 'main'):
        #     self.main = parent.main
        #     parent.addAction(self)
        #     parent._actions.append(self)
        # else:
        #     self.main = parent
        if text is None:
            text = self.__class__.__name__
        self.setText(text)
        self.triggered.connect(lambda: self.run(self.main))
    
        if icon is not None: 
            self.setIcon(QIcon(icon))
        if shortcut is not None: 
            self.setShortcut(shortcut)
        if tooltip is not None: 
            self.setToolTip(tooltip)

        # Dictionary with optional settings
        for option in kwargs:
            self.__dict__[option] = kwargs[option]

    def enable(self, app):
        return True

    def run(self, app):
        pass






def logger():
    
    LOG_FILE_NAME = "wezel_log.log"
    # creates some sort of conflict with mdreg - commenting out for now
#    if os.path.exists(LOG_FILE_NAME):
#        os.remove(LOG_FILE_NAME)
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename = LOG_FILE_NAME, 
        level = logging.INFO, 
        format = LOG_FORMAT)
    return logging.getLogger(__name__)


