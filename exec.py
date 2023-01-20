# This is the code run to create an executable

# to build an executable:
# pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. exec.py
# with splash screen
# pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. --splash wezel.jpg exec.py


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