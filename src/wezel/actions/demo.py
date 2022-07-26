import wezel


def all(parent): 

    parent.action(HelloWorld, text="Hello World")
    parent.action(ToggleApp, text="Toggle application")


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