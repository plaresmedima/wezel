__all__ = ['Windows']

from PyQt5.QtWidgets import QDockWidget, QSplitter
from PyQt5.QtCore import Qt

import dbdicom as db
import wezel


class Windows(wezel.App):

    def __init__(self, wzl): 
        """Creates the default main window."""

        super().__init__(wzl)

        self.toolBar = wezel.canvas.ToolBar()
        self.toolBarDockWidget = QDockWidget()
        self.toolBarDockWidget.setWidget(self.toolBar)
        self.main.addDockWidget(Qt.RightDockWidgetArea, self.toolBarDockWidget)
        self.toolBarDockWidget.hide()

        self.treeView = None
        self.treeViewDockWidget = QDockWidget()
        self.main.addDockWidget(Qt.LeftDockWidgetArea, self.treeViewDockWidget)
        self.treeViewDockWidget.hide()

        self.folder = None
        #self.central = QSplitter()
        self.central = wezel.widgets.MainMultipleDocumentInterface()
        self.central.subWindowActivated.connect(lambda subWindow: self.setSubWindow(subWindow))
        self.main.setCentralWidget(self.central)

        self.set_menu(wezel.menus.dicom)

    def setSubWindow(self, subWindow):
        # activeWindow = self.central.activeWindow
        # if activeWindow is not None:
        #     activeWidget = activeWindow.widget()
        #     if activeWidget.__class__.__name__ == 'SeriesCanvas':
        #         activeWidget.regions = self.toolBar.regionList.regions
        self.central.activeWindow = subWindow
        if self.folder is None:
            return
        widget = subWindow.widget()
        if widget.__class__.__name__ == 'SeriesCanvas':
            self.toolBar.setSeriesCanvas(widget)

    def open(self, path):
        self.folder = db.database(path=path, 
            status = self.status, 
            dialog = self.dialog)
        self.display(self.folder)

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
            #self.central.closeAllSubWindows()
            self.menubar.enable()
        #    self.set_app(apps.WezelWelcome)
        return accept

    def refresh(self):
        """
        Refreshes the Wezel display.
        """
        self.status.message('Refreshing display..')
        self.treeView.setFolder()
        self.menubar.enable()
        self.status.hide()
        #self.status.message()

    def addAsSubWindow(self, widget, title=None, icon=None):
        """
        displays a widget as a subwindow in the MDI. 
        
        Returns the subwindow
        """ 
        self.central.addWidget(widget, title=title, icon=icon)
        
    def display(self, object):

        if object.type() == 'Database':
            self.treeView = wezel.widgets.DICOMFolderTree(object)
            self.treeView.itemSelectionChanged.connect(self.menubar.enable)
            self.treeViewDockWidget.setWidget(self.treeView)
            self.treeViewDockWidget.show()
            self.menubar.enable()
        elif object.type() == 'Patient': # No Patient Viewer yet
            pass
        elif object.type() == 'Study': # No Study Viewer yet
            pass
        elif object.type() == 'Series':
            seriesCanvas = wezel.widgets.SeriesCanvas()
            seriesCanvas.setImageSeries(object)
            seriesCanvas.mousePositionMoved.connect(
                lambda x, y: self.status.pixelValue(x,y,seriesCanvas.canvas.imageItem.array())
            )
            self.addAsSubWindow(seriesCanvas, title=object.label())
            self.central.tileSubWindows()
            self.toolBar.setSeriesCanvas(seriesCanvas)
            self.toolBarDockWidget.show()
        elif object.type() == 'Instance':
            pass

        
    def get_selected(self, generation):   
        if self.treeView is None: 
            return []
        if generation == 4: 
            return []
        return self.treeView.get_selected(generation)

    
    def selected(self, generation):
        if isinstance(generation, str):
            if generation == 'Patients':
                generation=1
            elif generation == 'Studies':
                generation=2
            elif generation == 'Series':
                generation=3
            elif generation == 'Instances':
                generation=4
        if self.treeView is None: 
            return []
        if generation == 4: 
            return []
        return self.treeView.get_selected(generation)

    
    def nr_selected(self, generation):
        if isinstance(generation, str):
            if generation == 'Patients':
                generation=1
            elif generation == 'Studies':
                generation=2
            elif generation == 'Series':
                generation=3
            elif generation == 'Instances':
                generation=4
        if self.treeView is None: 
            return 0
        selected = self.treeView.get_selected(generation)
        return len(selected)
    
    
    # def set_data(self, folder):
    #     if self.folder is not None:
    #         if self.folder.close():
    #             self.central.closeAllSubWindows()
    #         else:
    #             return
    #     self.folder = folder
    #     if self.treeView is None:
    #         self.display(folder)
    #     else:
    #         self.treeView.setFolder(folder)
    #     self.menubar.enable()

    # def addSubWindow(self, subWindow):

    #     self.central.addSubWindow(subWindow) 

    # def closeAllSubWindows(self):
    #     """
    #     Closes all open windows.
    #     """
    #     self.central.closeAllSubWindows()

    # def closeSubWindow(self, subWindowName):
    #     """
    #     Closes all subwindows with a given name
    #     """   
    #     self.central.closeSubWindow(subWindowName)

    # def tileSubWindows(self):
    #     """
    #     Tiles all open windows.
    #     """
    #     self.central.tileSubWindows()

    # def addAsDockWidget(self, widget):

    #     #dockwidget = QDockWidget(self.main, Qt.SubWindow)
    #     dockwidget = QDockWidget()
    #     #dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
    #     #dockwidget.setWindowTitle('DICOM database')
    #     #dockwidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
    #     #dockwidget.setObjectName(widget.__class__.__name__)
    #     dockwidget.setWidget(widget)
    #     self.main.addDockWidget(Qt.LeftDockWidgetArea, dockwidget)


