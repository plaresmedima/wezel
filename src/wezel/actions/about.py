import webbrowser
import wezel

#from wezel.widgets.icons import question_mark

def menu(parent):

    menu = parent.menu('About')
    menu.action(About, text='Wezel', icon=wezel.widgets.icons.question_mark) 


class About(wezel.Action):

    def run(self, app):
        webbrowser.open("weasel.pro")
        #webbrowser.get('chrome').open("Wezel.pro")
