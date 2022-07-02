__all__ = ['app', 'build', 'install']

import os
import sys
import venv
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon

import wezel.widgets as widgets
from wezel.core import Main
from wezel.apps.welcome import Wezel as WezelWelcome

QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

class Wezel:

    def __init__(self):
        self.app = None
        self.log = logger()
        self.QApp = QApplication([])
        self.QApp.setWindowIcon(QIcon(widgets.icons.favicon))
        self.status = widgets.StatusBar()
        self.main = Main(self)
        self.main.setStatusBar(self.status)
        self.dialog = widgets.Dialog(self.main)
        self.app = WezelWelcome(self)


def app(application=None):

    wsl = Wezel().app
    if application is not None:
        wsl.set_app(application)
    return wsl



def post_installation_build_cleanup():
    print("Cleaning up building and compilation files...")
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        os.system('move dist\* .')
        os.system('rmdir build /S /Q')
        os.system('rmdir dist /S /Q')
        os.system('del myproject.spec')
        print("Deleting the created Python Virtual Environment for the process...")
        os.system('rmdir .venv /S /Q')
    else:
        os.system('mv dist/* .')
        os.system('rm -rf build/ dist/')
        os.system('rm myproject.spec')
        print("Deleting the created Python Virtual Environment for the process...")
        os.system('rm -r .venv/')

def activate():
    """Active virtual environment"""

    venv_dir = os.path.join(os.getcwd(), ".venv")
    os.makedirs(venv_dir, exist_ok=True)
    venv.create(venv_dir, with_pip=True)
    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')
    if windows:
        return os.path.join(venv_dir, "Scripts", "activate")
    else: # MacOS and Linux
        return '. "' + os.path.join(venv_dir, "bin", "activate")

def install():
    """Install requirements to a virtual environment"""

    print('Creating virtual environment..')
    os.system('py -3 -m venv .venv')

    print('Installing requirements..')
    os.system(activate() + ' && ' + 'py -m pip install -r requirements.txt')  

def build(project, onefile=True, terminal=False, data_folders=[], hidden_modules=[]):
    """Generate project executable"""

    # COMMENT
    # subprocess.run() is recommended to call commands in python
    # but only works for creating the virtual environment.
    # For some reason pip install does not work with subprocess.
    # Using os.system() until this can be resolved.

    # EXAMPLE OF hidden_modules
    # pyinstaller tells the user which packages failed to detect and import during the build and it recommends to add the package to the hidden imports flag
    # hidden = ['xnat', 'dipy', 'dipy.data', 'matplotlib', 'lmfit', 'fpdf', 
    #           'reportlab', 'reportlab.platypus', 'joblib', 'cv2', 'SimpleITK ', 'itk',
    #           'ukat', 'mdreg', 'mdreg.models', 'sklearn.utils._typedefs', 'sklearn.utils._cython_blas',
    #           'sklearn.neighbors.typedefs', 'sklearn.neighbors.quad_tree', 'sklearn.tree._utils',
    #           'sklearn.neighbors._partition_nodes']

    install()

#    hidden_modules = ['matplotlib']
#    hidden_imports = ' '.join(['--hidden-import '+ mod + ' ' for mod in hidden_modules])

    windows = (sys.platform == "win32") or (sys.platform == "win64") or (os.name == 'nt')

    if 'itk' in hidden_modules:
        # Pyinstaller doesn't have hooks for the itk package
        itk_path_win = '.venv\\lib\\site-packages\\itk'
        intermediate_python_folder = [fldr.name for fldr in os.scandir('venv/lib') if fldr.is_dir()][0] # It's known there's a Python subfolder between 'lib' and 'site-packages' for Unix systems
        itk_path_unix = '.venv/lib/' + intermediate_python_folder + '/site-packages/itk'
    
    if windows:
        all_data = [
            'wezel\\widgets\\icons\\my_icons;.\\wezel\\widgets\\icons\\my_icons',
            'wezel\\widgets\\icons\\fugue-icons-3.5.6;.\\wezel\\wwidgets\\icons\\fugue-icons-3.5.6',
            'wezel;.\\wezel'
            ]
        if 'itk' in hidden_modules: all_data.append(itk_path_win+';.\\itk')
        for name in data_folders:
            all_data.append(name+";./"+name) 
    else:
        all_data = [
            'wezel/widgets/icons/my_icons:./wezel/widgets/icons/my_icons',
            'wezel/widgets/icons/fugue-icons-3.5.6:./wezel/widgets/icons/fugue-icons-3.5.6',
            'wezel:./wezel'
            ]
        if 'itk' in hidden_modules: all_data.append(itk_path_unix+':./itk')
        for name in data_folders:
            all_data.append(name+":./"+name) 

    add_data = ' '.join(['--add-data='+ mod + ' ' for mod in all_data])
    hidden_imports = ' '.join(['--hidden-import '+ mod + ' ' for mod in hidden_modules])
    # The following is a special situation for dbdicom and dipy
    collect_data = ''
    if 'dbdicom' in hidden_modules:
        collect_data += ' --collect-datas dbdicom'
    if 'dipy' in hidden_modules:
        collect_data += ' --collect-datas dipy'
    # wezel and widgets might be needed at --collect-datas in the future. It's a matter of trying to build with those 2 and see what happens

    print('Creating executable..')
    cmd = activate() + ' && ' + 'pyinstaller --name "myproject" --clean'
    if onefile: 
        cmd += ' --onefile'
    if not terminal: 
        cmd += ' --noconsole'
    cmd += ' ' + hidden_imports
    cmd += ' ' + add_data
    cmd += ' ' + collect_data
    if os.path.exists(os.path.join(os.getcwd(), project + '.py')):
        cmd += ' ' + project + '.py'
    else:
        # Default option
        cmd += ' ' + "wezel\\main.py" # This command (and path!) may be different when wezel becomes a pip install package
    os.system(cmd)

    post_installation_build_cleanup()


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


if __name__ == '__main__':
    wsl = app()
    wsl.show()