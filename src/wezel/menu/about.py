import webbrowser
import wezel


def all(parent):

    parent.action(About, text='Wezel', icon=wezel.icons.animal_dog) 
    parent.action(Fugue, text='Fugue icons')


class About(wezel.gui.Action):
    def run(self, app):
        webbrowser.open("https://github.com/QIB-Sheffield/wezel")

class Fugue(wezel.gui.Action):
    def run(self, app):
        webbrowser.open("https://p.yusukekamiyamane.com/")
