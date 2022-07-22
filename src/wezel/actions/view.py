from wezel.core import Action
from wezel.widgets import SeriesViewerROI
from wezel.widgets import SeriesViewerMetaData

#Named constants
SERIES_VIEWER = 3
IMAGE_VIEWER = 4


def menu(parent):
   
    parent.action(Image)
    parent.action(Series)
    parent.separator()
    parent.action(Region)
    parent.action(HeaderDICOM, text='DICOM Header')
    parent.separator()
    parent.action(CloseWindows, text='Close windows')
    parent.action(TileWindows, text='Tile windows')

class HeaderDICOM(Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):
       for series in app.get_selected(SERIES_VIEWER):
            viewer = SeriesViewerMetaData(series)
            app.addAsSubWindow(viewer, title=series.label())


class Series(Action):

    def enable(self, app):
        
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):

        for series in app.get_selected(SERIES_VIEWER):
            app.display(series)
      

class Image(Action):

    def enable(self, app):
        
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(IMAGE_VIEWER) != 0

    def run(self, app):

        for image in app.get_selected(IMAGE_VIEWER):
            app.display(image)


class Region(Action):

    def enable(self, app):
        
        if app.__class__.__name__ != 'DicomWindows':
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):

        for series in app.get_selected(SERIES_VIEWER):

            viewer = SeriesViewerROI(series)
            viewer.dataWritten.connect(app.treeView.setFolder)
            app.addAsSubWindow(viewer, title=series.label())

class CloseWindows(Action):

    def enable(self, app):
        
        return app.__class__.__name__ != 'DicomWindows'

    def run(self, app):

        app.central.closeAllSubWindows()

class TileWindows(Action):

    def enable(self, app):
        
        return app.__class__.__name__ != 'DicomWindows'

    def run(self, app):

        app.central.tileSubWindows()

