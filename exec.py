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
    pyvista,
    scipy,
    measure,
    transform,
    segment,
    align,
)


if __name__ == "__main__":

    app = wezel.app()
    
    app.add_menu(scipy.menu_filter)
    app.add_menu(segment.menu)
    app.add_menu(align.menu)
    app.add_menu(transform.menu)
    app.add_menu(measure.menu)
    app.add_menu(wezel.menubar.about.menu)

    app.add_action(pyvista.action_show_mask_surface, menu='View', position=5)

    app.show()