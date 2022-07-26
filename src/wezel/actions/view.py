import numpy as np
import wezel

#Named constants
SERIES_VIEWER = 3
IMAGE_VIEWER = 4

def all(parent):
   
    parent.action(Image)
    parent.action(Series)
    parent.action(Region)
    parent.action(Array4D, text = '4D Array')
    parent.action(HeaderDICOM, text='DICOM Header')
    parent.separator()
    parent.action(CloseWindows, text='Close windows')
    parent.action(TileWindows, text='Tile windows')


class Image(wezel.Action):

    def enable(self, app):
        
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(IMAGE_VIEWER) != 0

    def run(self, app):

        for image in app.get_selected(IMAGE_VIEWER):
            app.display(image)


class Series(wezel.Action):

    def enable(self, app):
        
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):

        for series in app.get_selected(SERIES_VIEWER):
            app.display(series)


class Region(wezel.Action):

    def enable(self, app):
        
        if app.__class__.__name__ != 'Windows':
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):

        for series in app.get_selected(SERIES_VIEWER):

            viewer = wezel.widgets.SeriesViewerROI(series)
            viewer.dataWritten.connect(app.treeView.setFolder)
            app.addAsSubWindow(viewer, title=series.label())


class Array4D(wezel.Action):

    def enable(self, app):
        
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(3) != 0

    def run(self, app):

        series = app.get_selected(3)[0]
        array, _ = series.array(['SliceLocation', 'AcquisitionTime'], pixels_first=True)
        array = np.squeeze(array[...,0])
        if array.ndim < 4:
            app.dialog.information('Please select a series with >1 slice location and acquisition time.')
        else:
            viewer = wezel.widgets.FourDimViewer(app.status, array)
            app.addAsSubWindow(viewer, title=series.label())

            
class HeaderDICOM(wezel.Action):

    def enable(self, app):
        if not hasattr(app, 'folder'):
            return False
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):
       for series in app.get_selected(SERIES_VIEWER):
            viewer = wezel.widgets.SeriesViewerMetaData(series)
            app.addAsSubWindow(viewer, title=series.label())


class CloseWindows(wezel.Action):

    def enable(self, app):
        return app.__class__.__name__ == 'Windows'

    def run(self, app):
        app.central.closeAllSubWindows()


class TileWindows(wezel.Action):

    def enable(self, app):
        return app.__class__.__name__ == 'Windows'

    def run(self, app):
        app.central.tileSubWindows()
