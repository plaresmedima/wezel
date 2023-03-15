# This is the code run to create an executable

# to build an executable:
# -----------------------
# distribution mode: splash screen, single file and no console
# pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. --noconfirm --splash wezel.jpg exec.py

# debug mode: not single file & no splash screen
# pyinstaller --name wezel --clean --noconsole --additional-hooks-dir=. --noconfirm exec.py

# After this, you should see a dist folder which contains a link to the executable wezel.exe
# Troubleshoot: if pyinstaller throws an error, try deleting "build" and "dist" folders before running this command.


import wezel
from wezel.plugins import (
    hello_world, 
    surface_display,
)

if __name__ == "__main__":

    app = wezel.app()
    app.add_menu(hello_world.menu, position=-1)
    app.add_action(hello_world.hello_japan, 'Hello')
    app.add_action(hello_world.hello_china, 'Hello')
    app.add_action(surface_display.action, 'View', 5)
    app.show()