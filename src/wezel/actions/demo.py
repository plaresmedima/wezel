import wezel

def menu(parent): 

    wezel.actions.folder.menu(parent.menu('File'))
    wezel.actions.edit.menu(parent.menu('Edit'))

    view = parent.menu('View')
    view.action(wezel.actions.view.Image, text='Display image')
    view.action(wezel.actions.view.Series, text='Display series')
    view.action(wezel.actions.view.Region, text='Draw region')
    view.separator()
    view.action(wezel.actions.view.CloseWindows, text='Close windows')
    view.action(wezel.actions.view.TileWindows, text='Tile windows')

    wezel.actions.about.menu(parent.menu('About'))

def menu_hello_world(parent):

    subMenu = parent.menu('Hello')
    subMenu.action(HelloWorld, text="Hello World")
    subMenu.action(HelloWorld, text="Hello World (again)")

    subSubMenu = subMenu.menu('Submenu')
    subSubMenu.action(HelloWorld, text="Hello World (And again)")
    subSubMenu.action(HelloWorld, text="Hello World (And again!)")

def menu_tricks(parent): 

    wezel.actions.folder.menu(parent.menu('File'))
    wezel.actions.edit.menu(parent.menu('Edit'))

    view = parent.menu('View')
    view.action(ToggleApp, text='Toggle application')
    view.action(wezel.actions.view.Image, text='Display image')
    view.action(wezel.actions.view.Series, text='Display series')
    view.action(wezel.actions.view.Region, text='Draw region')
    view.separator()
    view.action(wezel.actions.view.CloseWindows, text='Close windows')
    view.action(wezel.actions.view.TileWindows, text='Tile windows')

    tutorial = parent.menu('Tutorial')
    tutorial.action(HelloWorld, text="Hello World")

    subMenu = tutorial.menu('Submenus')
    subMenu.action(HelloWorld, text="Hello World (Again)")
    subMenu.action(HelloWorld, text="Hello World (And again)")

    subSubMenu = subMenu.menu('Subsubmenus')
    subSubMenu.action(HelloWorld, text="Hello World (And again again)")
    subSubMenu.action(HelloWorld, text="Hello World (And again again again)")

    wezel.actions.about.menu(parent.menu('About'))


class HelloWorld(wezel.Action):

    def run(self, app):
        app.dialog.information("Hello World!", title = 'My first pipeline!')


class ToggleApp(wezel.Action):

    def enable(self, app):
        return app.__class__.__name__ in ['Series', 'Windows', 'About']

    def run(self, app):
        
        wzl = app.wezel
        if app.__class__.__name__ == 'About':
            wzl.app = wezel.apps.dicom.Series(wzl)
        elif app.__class__.__name__ == 'Series':
            wzl.app = wezel.apps.dicom.Windows(wzl)
        elif app.__class__.__name__ == 'Windows':
            wzl.app = wezel.apps.welcome.About(wzl)