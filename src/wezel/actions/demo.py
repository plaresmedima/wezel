from wezel.core import Action
import wezel.apps as apps
import wezel.actions as actions

def hello_world(parent):

    subMenu = parent.menu('Hello')
    subMenu.action(HelloWorld, text="Hello World")
    subMenu.action(HelloWorld, text="Hello World (again)")

    subSubMenu = subMenu.menu('Submenu')
    subSubMenu.action(HelloWorld, text="Hello World (And again)")
    subSubMenu.action(HelloWorld, text="Hello World (And again!)")


def menu_hello(parent):

    subMenu = parent.menu('Submenus')
    subMenu.action(HelloWorld, text="Hello World (Again)")
    subMenu.action(HelloWorld, text="Hello World (And again)")
    subMenu.action(ToggleApp, text='Toggle application')

    subSubMenu = subMenu.menu('Subsubmenus')
    subSubMenu.action(HelloWorld, text="Hello World (And again again)")
    subSubMenu.action(HelloWorld, text="Hello World (And again again again)")
    
    actions.about.menu(parent.menu('About'))

def menu(parent): 

    actions.folder.menu(parent.menu('File'))
    actions.edit.menu(parent.menu('Edit'))

    view = parent.menu('View')
    view.action(ToggleApp, text='Toggle application')
    view.action(actions.view.Image, text='Display image')
    view.action(actions.view.Series, text='Display series')
    view.action(actions.view.Region, text='Draw region')
    view.action(actions.view.HeaderDICOM, text='DICOM Header')
    view.separator()
    view.action(actions.view.CloseWindows, text='Close windows')
    view.action(actions.view.TileWindows, text='Tile windows')

    tutorial = parent.menu('Tutorial')
    tutorial.action(HelloWorld, text="Hello World")

    subMenu = tutorial.menu('Submenus')
    subMenu.action(HelloWorld, text="Hello World (Again)")
    subMenu.action(HelloWorld, text="Hello World (And again)")

    subSubMenu = subMenu.menu('Subsubmenus')
    subSubMenu.action(HelloWorld, text="Hello World (And again again)")
    subSubMenu.action(HelloWorld, text="Hello World (And again again again)")

    actions.about.menu(parent.menu('About'))


class HelloWorld(Action):

    def run(self, app):
        app.dialog.information("Hello World!", title = 'My first pipeline!')


class ToggleApp(Action):

    def enable(self, app):
        return app.__class__.__name__ in ['WezelWelcome', 'DicomSeries', 'DicomWindows']

    def run(self, app):
        
        wezel = app.wezel
        if app.__class__.__name__ == 'WezelWelcome':
            wezel.app = apps.DicomSeries(wezel)
        elif app.__class__.__name__ == 'DicomSeries':
            wezel.app = apps.DicomWindows(wezel)
        elif app.__class__.__name__ == 'DicomWindows':
            wezel.app = apps.WezelWelcome(wezel)