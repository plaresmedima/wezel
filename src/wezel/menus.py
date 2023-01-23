import wezel

def dicom(parent): 

    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))
    wezel.menu.view.all(parent.menu('View'))
    wezel.menu.filter.all(parent.menu('Filter'))
    wezel.menu.segment.all(parent.menu('Segment'))
    wezel.menu.transform.all(parent.menu('Transform'))
    wezel.menu.about.all(parent.menu('About'))

def test(parent):

    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))
    wezel.menu.view.all(parent.menu('View'))
    wezel.menu.about.all(parent.menu('About'))
    wezel.menu.test.all(parent.menu('Test'))

def about(parent): 

    wezel.menu.about.all(parent.menu('About'))

def hello_world(parent):

    subMenu = parent.menu('Hello')
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World")
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (again)")

    subSubMenu = subMenu.menu('Submenu')
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again)")
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again!)")

    wezel.menu.about.all(parent.menu('About'))

def tricks(parent): 

    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))

    view = parent.menu('View')
    view.action(wezel.menu.demo.ToggleApp, text='Toggle application')
    view.action(wezel.menu.view.Image, text='Display image')
    view.action(wezel.menu.view.Series, text='Display series')
    view.action(wezel.menu.view.Region, text='Draw region')
    view.separator()
    view.action(wezel.menu.view.CloseWindows, text='Close windows')
    view.action(wezel.menu.view.TileWindows, text='Tile windows')

    tutorial = parent.menu('Tutorial')
    tutorial.action(wezel.menu.demo.HelloWorld, text="Hello World")

    subMenu = tutorial.menu('Submenus')
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (Again)")
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again)")

    subSubMenu = subMenu.menu('Subsubmenus')
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again again)")
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again again again)")

    wezel.menu.about.all(parent.menu('About'))
