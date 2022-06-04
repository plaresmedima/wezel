__all__ = ['WeaselWelcome', 'WeaselAbout']

import weasel.wewidgets as widgets
import weasel.actions as actions
import weasel.apps as apps
from weasel.core import App, Action
from weasel import dbdicom

class WeaselAbout(App):
    """Entry weasel application"""

    def __init__(self, weasel):
        super().__init__(weasel)

        self.set_central(widgets.ImageLabel())
        self.set_menu(actions.about.menu)
        self.set_status("Welcome to Weasel!")

class WeaselWelcome(App):
    """Entry weasel application"""

    def __init__(self, weasel):
        super().__init__(weasel)

        central = widgets.ImageLabel()
        self.main.setCentralWidget(central)
        self.set_menu(menu)
        self.status.message("Welcome to Weasel!")


def menu(parent): 

    view = parent.menu('Open')
    view.action(DICOM, text='DICOM folder')

    about = parent.menu('About')
    actions.about.menu(about)

class DICOM(Action):

    def enable(self, app):
        return app.__class__.__name__ in ['WeaselWelcome']

    def run(self, app):

        app.status.message("Opening DICOM folder..")
        path = app.dialog.directory("Select a DICOM folder")
        if path == '': return

        app.status.cursorToHourglass()
        folder = dbdicom.Folder(status=app.status, dialog=app.dialog)
        folder.open(path)
        
        app = app.set_app(apps.DicomWindows)
        app.set_data(folder)
        app.status.cursorToNormal()