from PyQt5.QtCore import Qt
import numpy as np

import wezel

#Named constants
SERIES_VIEWER = 3
IMAGE_VIEWER = 4

def all(parent):
   
    parent.action(DataBase, text = 'Database')
    parent.action(Series, text = 'Series')
    parent.action(Array4D, text = '4D Array')
    parent.action(HeaderDICOM, text='DICOM Header')
    parent.separator()
    parent.action(ToolBar, text='Tool bar')
    parent.action(CloseWindows, text='Close windows')
    parent.action(TileWindows, text='Tile windows')


class ToolBar(wezel.Action):
    def enable(self, app):
        return True
    def run(self, app):
        app.toolBarDockWidget.show()

class DataBase(wezel.Action):

    def enable(self, app):
        if app.treeViewDockWidget is None:
            return False
        #return not app.treeViewDockWidget.isVisible()
        return True

    def run(self, app):
        app.treeViewDockWidget.show()
        app.menubar.enable()

        
class Series(wezel.Action):

    def enable(self, app):
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):
        for series in app.get_selected(SERIES_VIEWER):
            app.display(series)      
        app.central.tileSubWindows()      


class Array4D(wezel.Action):

    def enable(self, app):
        return app.nr_selected(3) != 0

    def run(self, app):

        series = app.get_selected(3)[0]
        array, _ = series.array(['SliceLocation', 'AcquisitionTime'], pixels_first=True)
        array = np.squeeze(array[...,0])
        app.status.hide()
        if array.ndim < 4:
            app.dialog.information('Please select a series with >1 slice location and acquisition time.')
        else:
            viewer = wezel.widgets.FourDimViewer(app.status, array)
            app.central.addWidget(viewer, title=series.label())

            
class HeaderDICOM(wezel.Action):

    def enable(self, app):
        return app.nr_selected(SERIES_VIEWER) != 0

    def run(self, app):
       for series in app.get_selected(SERIES_VIEWER):
            viewer = wezel.widgets.SeriesViewerMetaData(series)
            app.central.addWidget(viewer, title=series.label())


class CloseWindows(wezel.Action):
    def run(self, app):
        app.central.closeAllSubWindows()


class TileWindows(wezel.Action):
    def run(self, app):
        app.central.tileSubWindows()
