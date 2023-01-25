import wezel

def minimal(parent):
    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))
    wezel.menu.view.all(parent.menu('View'))
    wezel.menu.about.all(parent.menu('About'))

def default(parent): 
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


def hello_world(parent):

    subMenu = parent.menu('Hello')
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World")
    subMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (again)")

    subSubMenu = subMenu.menu('Submenu')
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again)")
    subSubMenu.action(wezel.menu.demo.HelloWorld, text="Hello World (And again!)")

    wezel.menu.about.all(parent.menu('About'))