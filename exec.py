# This is the code run to create an executable

# to build an executable:
# -----------------------
# distribution mode: splash screen, single file and no console
# pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. --splash wezel.jpg exec.py
# debugging mode: not single file & no splash & console included
# pyinstaller --name wezel --clean --additional-hooks-dir=. exec.py


import wezel
import numpy as np


if __name__ == "__main__":

    # This closes the splash screen
    # pyi_splash is part of pyinstaller
    try:
        import pyi_splash
        pyi_splash.update_text('Loaded wezel..')
        pyi_splash.close()
    except:
        pass

    app = wezel.app()
    app.show()