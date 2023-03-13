import wezel

def all(parent):
   
    parent.action(DataBase, text = 'Database')
    parent.separator()
    parent.action(Series, text = 'Series (2D)')
    parent.action(Array4D, text = 'Series (2D + 1D)')
    parent.action(HeaderDICOM, text = 'Series (Header)')
    parent.action(MaskSurface, text = '3D surface (mask)')
    parent.separator()
    parent.action(ToolBar, text='Toolbar')
    parent.action(CloseWindows, text='Close windows')
    parent.action(TileWindows, text='Tile windows')


class ToolBar(wezel.gui.Action):

    def enable(self, app):
        return True
        # Closer sensitivity control requires enable to be called
        # whenever the user closes the toolbar dockwidget
        # if app.toolBarDockWidget.widget() is None:
        #     return False
        # return app.toolBarDockWidget.isHidden()
        
    def run(self, app):
        if app.toolBarDockWidget.widget() is None:
            msg = 'There are currently no toolbars available.'
            msg += '\n Please open a display first.'
            app.dialog.information(msg, title='No toolbars available')
            return
        app.toolBarDockWidget.show()
        #self.setEnabled(False)


class DataBase(wezel.gui.Action):

    def enable(self, app):
        if app.treeViewDockWidget is None:
            return False
        #return not app.treeViewDockWidget.isVisible()
        return True

    def run(self, app):
        app.treeViewDockWidget.show()
        app.menubar.enable()

        
class Series(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            app.display(series)      
        #app.central.tileSubWindows()      


class Array4D(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            viewer = wezel.displays.SeriesDisplay4D()
            viewer.setSeries(series)
            app.addWidget(viewer, series.label())


class MaskSurface(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
        for series in app.selected('Series'):
            app.display(series, view='Surface')

            
class HeaderDICOM(wezel.gui.Action):

    def enable(self, app):
        return app.nr_selected('Series') != 0

    def run(self, app):
       for series in app.selected('Series'):
            viewer = wezel.displays.SeriesViewerMetaData(series)
            app.addWidget(viewer, series.label())


class CloseWindows(wezel.gui.Action):
    def run(self, app):
        app.central.closeAllSubWindows()


class TileWindows(wezel.gui.Action):
    def run(self, app):
        app.central.tileSubWindows()
