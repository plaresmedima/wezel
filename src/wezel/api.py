import sys
import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import wezel


QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)


class Wezel:

    def __init__(self):
        self.log = logger()
        self.QApp = QApplication(sys.argv)
        self.QApp.setWindowIcon(QIcon(wezel.icons.favicon))
        self.main = wezel.gui.Main(self)

    def show(self):    
        self.log.info('Launching Wezel!')
        try:
            self.main.show()
            self.QApp.exec()
            #sys.exit(self.QApp.exec())
        except Exception as e:
            # Use QMessage
            print('Wezel Error: ' + str(e))
            self.log.exception('Wezel Error: ' + str(e))

    def open(self, path):
        self.main.open(path)

    def set_menu(self, menu):
        self.main.set_menu(menu)

    # def add_menu(self, menu):
    #     self.main.addMenu(menu)

    def set_menubar(self, mbar):
        qmbar = mbar._QMenuBar(self.main)
        self.main.setMenuBar(qmbar)
        self.main.menubar = qmbar

    @property
    def menubar(self):
        return self.main.menuBar()


class Action():
    def __init__(self, 
        text = 'Action',
        shortcut = None,
        tooltip = None, 
        icon = None, 
        on_clicked = None,
        is_clickable = None
    ):
        self._text = text
        self._shortcut = shortcut
        self._tooltip = tooltip
        self._icon = icon
        self._on_clicked = on_clicked
        self._is_clickable = is_clickable
        self._qaction = None

    def _QAction(self, parent):
        action = wezel.gui.Action(parent,
            text = self._text,
            shortcut = self._shortcut,
            tooltip = self._tooltip, 
            icon = self._icon,  
            on_clicked = self._on_clicked,
            is_clickable = self._is_clickable)
        self._qaction = action
        return action


class Separator:
    pass


class Menu():

    def __init__(self, title='Menu'):
        self._title = title
        self._items = []

    def add(self, item):
        self._items.append(item)
        self._qmenu = None

    def add_action(self, *args, **kwargs):
        action = Action(*args, **kwargs)
        self._items.append(action)
        return action

    def add_menu(self, *args, **kwargs):
        menu = Menu(*args, **kwargs)
        self._items.append(menu)
        return menu

    def add_separator(self):
        self._items.append(Separator())

    def _QMenu(self, parent):
        menu = wezel.gui.Menu(parent, self._title)
        for item in self._items:
            if isinstance(item, Action):
                action = item._QAction(menu)
                menu.add(action)
            elif isinstance(item, Menu):
                submenu = item._QMenu(menu)
                menu.addMenu(submenu)
            elif isinstance(item, Separator):
                menu.addSeparator()
        self._qmenu = menu
        return menu



class MenuBar():
    def __init__(self):
        self._menus = []
        self._qmenubar = None

    def add(self, menu):
        self._menus.append(menu)

    def add_menu(self, title='Menu'):
        menu = Menu(title)
        self.add(menu)
        return menu

    def _QMenuBar(self, parent):
        mbar = wezel.gui.MenuBar(parent)
        for menu in self._menus:
            menu._QMenu(mbar)
        self._qmenubar = mbar
        return mbar
    

def app():

    # Otional
    # This closes the splash screen
    # pyi_splash is part of pyinstaller
    try:
        import pyi_splash
        pyi_splash.update_text('Loaded wezel..')
        pyi_splash.close()
    except:
        pass

    return Wezel()


def logger():
    
    LOG_FILE_NAME = "wezel_log.log"
    # creates some sort of conflict with mdreg - commenting out for now
#    if os.path.exists(LOG_FILE_NAME):
#        os.remove(LOG_FILE_NAME)
    LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
    logging.basicConfig(
        filename = LOG_FILE_NAME, 
        level = logging.INFO, 
        format = LOG_FORMAT)
    return logging.getLogger(__name__)


