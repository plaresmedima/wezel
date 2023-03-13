

from PySide2.QtCore import  Signal, Qt
from PySide2.QtWidgets import (
    QWidget, 
    #QApplication, 
    QMainWindow, 
    QAction, 
    QMenu, 
    QMenuBar, 
    QDockWidget, 
    QMessageBox) 
from PySide2.QtGui import QIcon

import dbdicom as db
import wezel

#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
#QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


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


class Main(QMainWindow):

    def __init__(self, wzl, project=None): 
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
        title = "  Wezel"
        if project is not None:
            title += ' -- project ' + project
        self.setWindowTitle(title)
        
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

        self.central = wezel.widgets.MainMultipleDocumentInterface()
        self.central.subWindowActivated.connect(lambda subWindow: self.activateSubWindow(subWindow))
        self.setCentralWidget(self.central)

        self.set_menu(wezel.menu.menubar.minimal)

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

    def set_menu(self, menu_func): # -> setMenu()
        self.menubar = MenuBar(self, menu_func)
        self.setMenuBar(self.menubar)

    # def addMenu(self, menu_func):
    #     menuBar = self.menuBar() 
    #     menu_func(menuBar)
    #     menuBar.enable()

    # When menus become objects instead of functions
    # Needs a menu class that can be built before launching QApp
    # def _addMenu(self, menu): 
    #     menuBar = self.menuBar()
    #     menuBar.addMenu(menu)

    def open(self, path):
        folder = db.database(path=path, 
            status = self.status, 
            dialog = self.dialog)
        self.display(folder)
        self.status.hide()

    def close(self):
        """Closes the application."""
        if self.database() is None:
            return True
        accept = self.database().close()
        if accept:
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
        if self.treeView is not None:
            self.treeView.setDatabase()
        self.menuBar().enable()
        self.status.hide()
        
    def display(self, object, view=None):
        if isinstance(object, list):
            for o in object:
                self.display(o)
            return
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
            if view == 'Surface':
                viewer = wezel.widgets.SurfaceDisplay(object)
            else:
                viewer = wezel.widgets.SeriesDisplay(object)
            self.addWidget(viewer, title=object.label())
        elif object.type() == 'Instance':
            pass

    # THIS WILL BE DEPRECATED!! 
    # Included for backwards compatibility only.
    @property
    def folder(self):
        return self.database()

    # THIS WILL BE DEPRECATED!!
    # Use selected()
    def get_selected(self, generation):  
        if self.treeView is None: 
            return []
        return self.treeView.get_selected(generation)

    # Retrieve the selected database
    def database(self):
        databases = self.selected('Databases')
        if databases == []:
            return 
        else:
            return databases[0]   

    def top_level_selected(self):
        patients = self.selected('Patients')
        studies = self.selected('Studies')
        series = self.selected('Series')
        sel = patients + studies + series
        if sel == []:     
            return
        tl_patients = []
        tl_studies = []
        tl_series = []
        for patient in self.database().patients():
            if patient in patients:
                tl_patients.append(patient)
            else:
                for study in patient.studies():
                    if study in studies:
                        tl_studies.append(study)
                    else:
                        for sery in study.series():
                            if sery in series:
                                tl_series.append(sery)
        return tl_patients, tl_studies, tl_series
             

    def selected(self, generation='Series'):
        """Returns a list of selected objects of the requested generation"""

        # Check if any databases are open
        if self.treeView is None: 
            return []

        # If an object is selected in the treeView, use that.
        if generation == 'Databases':
            return [self.treeView.database()]
        sel = self.treeView.selected(generation)
        if sel != []:
            return sel

        # If none are selected in the database, check the display.
        activeWindow = self.central.activeWindow
        if activeWindow is None:
            return []
        widget = activeWindow.widget()
        if generation=='Instances':
            if hasattr(widget, 'instance'):
                return [widget.instance()]
        elif generation=='Series':
            if hasattr(widget, 'series'):
                return [widget.series()]
        elif generation=='Studies':
            if hasattr(widget, 'study'):
                return [widget.study()]
        elif generation=='Patients':
            if hasattr(widget, 'patient'):
                return [widget.patient()]
        elif generation=='Databases':
            if hasattr(widget, 'database'):
                return [widget.database()]
        return []
        
 
    def nr_selected(self, generation):
        if self.treeView is None: 
            return 0
        nr = self.treeView.nr_selected(generation)
        if nr != 0:
            return nr
        activeWindow = self.central.activeWindow
        if activeWindow is None:
            return 0
        widget = activeWindow.widget()
        if generation=='Instances':
            if hasattr(widget, 'instance'):
                return 1
        elif generation=='Series':
            if hasattr(widget, 'series'):
                return 1
        elif generation=='Studies':
            if hasattr(widget, 'study'):
                return 1
        elif generation=='Patients':
            if hasattr(widget, 'patient'):
                return 1
        elif generation=='Databases':
            if hasattr(widget, 'database'):
                return 1
        return 0
        

    def closeSubWindow(self, subWindow):
        self.central.removeSubWindow(subWindow)
        self.central.tileSubWindows()
        # The widget continues to exist - memory issues?
        # Delete widget when subwindow closes
        widget = subWindow.widget().__class__.__name__
        # Hack
        # The widget is sometimes destroyed by removeSubWindow but not always - not sure why
        if widget == 'QWidget':
            return
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

    databaseUpdated = Signal() 

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

    def __init__(self, main, menu=None):
        super().__init__()

        self._menus = []
        self.main = main
        if menu is not None:
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

    def add(self, menu):
        menu._QMenu(self)
        #self.addMenu(menu)


class Menu(QMenu):

    def __init__(self, parent=None, title='Menu'):
        super().__init__()

        self._parent = parent
        self._actions = []
        self._menus = []
        self.setTitle(title)
        if parent is not None:
            self.main = parent.main
            parent.addMenu(self)

    def addMenu(self, menu):
        super().addMenu(menu)
        self._menus.append(menu)
        self.enable()

    def menu(self, title='Submenu'):
        return Menu(self, title)

    def action(self, action, **kwargs):
        act = action(self, **kwargs)
        super().addAction(act)
        self._actions.append(act)
        
    def addAction(self, 
        text = 'Action',
        shortcut = None,
        tooltip = None, 
        icon = None, 
        on_clicked = None,
        is_clickable = None):

        action = Action(self, 
            text = text,
            shortcut = shortcut,
            tooltip = tooltip,
            icon = icon,
            on_clicked = on_clicked,
            is_clickable = is_clickable)
        super().addAction(action)
        self._actions.append(action)

    def add(self, action):
        super().addAction(action)
        self._actions.append(action)
        
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
        on_clicked = None,
        is_clickable = None,
        **kwargs):
        
        super().__init__()

        self.main = parent.main
        self._on_clicked = on_clicked
        self._is_clickable = is_clickable

        if text is None:
            text = self.__class__.__name__
        self.setText(text)
        #self.triggered.connect(lambda: self.run(self.main))
        self.triggered.connect(self.__run)
    
        if icon is not None: 
            self.setIcon(QIcon(icon))
        if shortcut is not None: 
            self.setShortcut(shortcut)
        if tooltip is not None: 
            self.setToolTip(tooltip)

        # Dictionary with optional settings
        for option in kwargs:
            self.__dict__[option] = kwargs[option]

    def __run(self):
        try:
            self.run(self.main)
        except:
            self.main.dialog.error()
            self.main.refresh()
        self.main.status.hide()
        self.main.status.message('Ready for your next move.. Give it to me!')

    def enable(self, app):
        if self._is_clickable is not None:
            return self._is_clickable(app)
        else:
            return True

    def run(self, app):
        if self._on_clicked is not None:
            self._on_clicked(app)
        else:
            pass