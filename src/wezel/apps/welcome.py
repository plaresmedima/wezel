__all__ = ['About']

import wezel
# import wezel.widgets as widgets
# import wezel.actions as actions
# from wezel.core import App

class About(wezel.App):
    """Entry wezel application"""

    def __init__(self, app):
        super().__init__(app)

        self.set_central(wezel.widgets.ImageLabel())
        self.set_menu(wezel.actions.about.menu)
        self.set_status("Welcome to Wezel!")