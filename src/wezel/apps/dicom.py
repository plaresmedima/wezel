__all__ = ['Windows', 'Series', 'Entry']

from PyQt5.QtWidgets import QDockWidget
from PyQt5.QtCore import Qt

import dbdicom as db
import wezel


class Entry(wezel.App):
    """Entry wezel application"""

    def __init__(self, wezel):
        super().__init__(wezel)

        central = wezel.widgets.ImageLabel()
        self.main.setCentralWidget(central)
        self.set_menu(dicom_entry_menu)
        self.status.message("Welcome to Wezel!")

def dicom_entry_menu(parent): 

    view = parent.menu('Open')
    view.action(DicomEntry, text='DICOM folder')

    about = parent.menu('About')
    wezel.actions.about.all(about)

class DicomEntry(wezel.Action):

    def enable(self, app):
        return app.__class__.__name__ in ['Entry']

    def run(self, app):

        app.status.message("Opening DICOM folder..")
        path = app.dialog.directory("Select a DICOM folder")
        if path == '': return

        app.status.cursorToHourglass()
        folder = db.database(status=app.status, dialog=app.dialog)
        folder.open(path)
        
        app = app.set_app(app.DicomWindows)
        app.set_data(folder)
        app.status.cursorToNormal()


class Windows(wezel.App):

    def __init__(self, wzl): 
        """Creates the default main window."""

        super().__init__(wzl)

        self.treeView = None
        self.folder = None
        self.central = wezel.widgets.MainMultipleDocumentInterface()
        self.main.setCentralWidget(self.central)
        self.set_menu(wezel.menus.dicom)

    def set_data(self, folder):

        if self.folder is not None:
            if self.folder.close():
                self.central.closeAllSubWindows()
            else:
                return
        self.folder = folder
        if self.treeView is None:
            self.display(folder)
        else:
            self.treeView.setFolder(folder)
        self.menubar.enable()

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
            self.central.closeAllSubWindows()
            for dockwidget in self.main.findChildren(QDockWidget):
                self.main.removeDockWidget(dockwidget)
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
        self.status.message()

    def addAsDockWidget(self, widget, title=''):

        dockwidget = QDockWidget(title, self.main, Qt.SubWindow)
        dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockwidget.setWindowTitle('DICOM database')
        dockwidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        #dockwidget.setObjectName(widget.__class__.__name__)
        dockwidget.setWidget(widget)

        self.main.addDockWidget(Qt.LeftDockWidgetArea, dockwidget)

    def addAsSubWindow(self, widget, title=None, icon=None):
        """
        displays a widget as a subwindow in the MDI. 
        
        Returns the subwindow
        """ 
        return self.central.addWidget(widget, title=title, icon=icon)

    def addSubWindow(self, subWindow):

        self.central.addSubWindow(subWindow) 

    def closeAllSubWindows(self):
        """
        Closes all open windows.
        """
        self.central.closeAllSubWindows()

    def closeSubWindow(self, subWindowName):
        """
        Closes all subwindows with a given name
        """   
        self.central.closeSubWindow(subWindowName)  

    def tileSubWindows(self):
        """
        Tiles all open windows.
        """
        self.central.tileSubWindows()

    def display(self, object):

        if object.type() == 'Database':
            self.treeView = wezel.widgets.DICOMFolderTree(object)
            self.treeView.itemSelectionChanged.connect(self.menubar.enable)
            self.addAsDockWidget(self.treeView)
            self.menubar.enable()
        elif object.type() == 'Patient': # No Patient Viewer yet
            pass
        elif object.type() == 'Study': # No Study Viewer yet
            pass
        elif object.type() == 'Series':
            viewer = wezel.widgets.SeriesViewer(object)
            self.addAsSubWindow(viewer, title=object.label())
        elif object.type() == 'Instance':
            viewer = wezel.widgets.ImageViewer(object)
            self.addAsSubWindow(viewer, title=object.label())

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


class Series(wezel.App):
    """WORK IN PROGRESS"""

    def __init__(self, wzl): 
        """Creates a central window showing series only."""

        super().__init__(wzl)

        self.treeView = None
        self.folder = None
        self.central = wezel.widgets.SeriesViewer()
        self.main.setCentralWidget(self.central)
        self.set_menu(wezel.menus.dicom) 

    def open(self, path, message='Opening folder..', attributes=None):

        self.folder = db.database(path=path, attributes=attributes, message=message, status=self.status, dialog=self.dialog)
        self.display(self.folder)

    def close(self):
        """Closes the Wezel display"""

        if self.folder is None:
            return True
        accept = self.folder.close()
        if accept:
            for dockwidget in self.main.findChildren(QDockWidget):
                self.main.removeDockWidget(dockwidget)
            self.main.menuBar().enable()
        return accept

    def refresh(self):
        """
        Refreshes the Wezel display.
        """
        self.status.message('Refreshing display..')
        self.treeView.setFolder()
        self.menubar.enable()
        self.status.message()

    def addAsDockWidget(self, widget, title=''):

        dockwidget = QDockWidget(title, self.main, Qt.SubWindow)
        dockwidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        dockwidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        dockwidget.setObjectName(widget.__class__.__name__)
        dockwidget.setWidget(widget)

        self.main.addDockWidget(Qt.LeftDockWidgetArea, dockwidget)

    def display(self, object=None):

        if object is None:
            self.treeView = wezel.widgets.DICOMFolderTree(object, self.status)
            self.treeView.itemSelectionChanged.connect(self.menubar.enable)
            self.addAsDockWidget(self.treeView, title=object.path)
            self.menubar.enable()
        elif object.generation == 1: # No Patient Viewer yet
            pass
        elif object.generation == 2: # No Study Viewer yet
            pass
        elif object.generation == 3:
            self.central.setData(object)
        elif object.generation == 4:
            pass

    def get_selected(self, generation):
        
        if self.treeView is None: return []
        if generation == 4: return []
        selected = self.treeView.get_selected(generation)
        return [self.folder.object(row, generation) for row in selected]
                  
    def nr_selected(self, generation):

        if self.treeView is None: return 0
        if generation == 4: return 0
        selected = self.treeView.get_selected(generation)
        return len(selected)