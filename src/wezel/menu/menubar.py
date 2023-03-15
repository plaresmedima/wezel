import wezel

def minimal(menubar):
    wezel.menu.folder.all(menubar.menu('File'))
    wezel.menu.edit.all(menubar.menu('Edit'))
    wezel.menu.view.all(menubar.menu('View'))
    wezel.menu.about.all(menubar.menu('About'))

def default(parent): 
    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))
    wezel.menu.view.all(parent.menu('View'))
    wezel.menu.filter.all(parent.menu('Filter'))
    wezel.menu.segment.all(parent.menu('Segment'))
    wezel.menu.transform.all(parent.menu('Transform'))
    wezel.menu.measure.all(parent.menu('Measure'))
    wezel.menu.about.all(parent.menu('About'))

def test(parent):
    wezel.menu.folder.all(parent.menu('File'))
    wezel.menu.edit.all(parent.menu('Edit'))
    wezel.menu.view.all(parent.menu('View'))
    wezel.menu.about.all(parent.menu('About'))
    wezel.menu.test.all(parent.menu('Test'))


