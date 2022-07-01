import webbrowser
from wezel.core import Action

from wezel.widgets.icons import question_mark


def menu(parent):

    #menu = parent.menu('About')
    parent.action(About, text='Wezel', icon=question_mark) 


class About(Action):

    def run(self, app):
        webbrowser.open("wezel.pro")
        #webbrowser.get('chrome').open("Wezel.pro")
