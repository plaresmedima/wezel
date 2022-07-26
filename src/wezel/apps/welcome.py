__all__ = ['About']

import wezel

class About(wezel.App):
    """Entry wezel application"""

    def __init__(self, app):
        super().__init__(app)

        self.set_central(wezel.widgets.ImageLabel())
        self.set_menu(wezel.menus.about)
        self.set_status("Welcome to Wezel!")