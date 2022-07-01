__all__ = ['WezelWelcome', 'WezelAbout']

import wezel.widgets as widgets
import wezel.actions as actions
from wezel.core import App, Action
import dbdicom as db

class About(App):
    """Entry wezel application"""

    def __init__(self, wezel):
        super().__init__(wezel)

        self.set_central(widgets.ImageLabel())
        self.set_menu(actions.about.menu)
        self.set_status("Welcome to Wezel!")

class Wezel(App):
    """Entry wezel application"""

    def __init__(self, wezel):
        super().__init__(wezel)

        central = widgets.ImageLabel()
        self.main.setCentralWidget(central)
        self.set_menu(menu)
        self.status.message("Welcome to Wezel!")


def menu(parent): 

    view = parent.menu('Open')
    view.action(DICOM, text='DICOM folder')

    about = parent.menu('About')
    actions.about.menu(about)

class DICOM(Action):

    def enable(self, app):
        return app.__class__.__name__ in ['WezelWelcome']

    def run(self, app):

        app.status.message("Opening DICOM folder..")
        path = app.dialog.directory("Select a DICOM folder")
        if path == '': return

        app.status.cursorToHourglass()
        folder = db.Folder(status=app.status, dialog=app.dialog)
        folder.open(path)
        
        app = app.set_app(apps.DicomWindows)
        app.set_data(folder)
        app.status.cursorToNormal()