import sys
import os
import shutil
import timeit
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget
import dbdicom as db
import wezel
from wezel import widgets


datapath = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
twofiles = os.path.join(datapath, 'TWOFILES')
onefile = os.path.join(datapath, 'ONEFILE')
rider = os.path.join(datapath, 'RIDER')
rider_full = os.path.join(datapath, 'RIDER Neuro MRI-3369019796')
zipped = os.path.join(datapath, 'ZIP')
multiframe = os.path.join(datapath, 'MULTIFRAME')
skull_ct = os.path.join(datapath, '2_skull_ct')
tristan = 'C:\\Users\\steve\\Dropbox\\Data\\TRISTAN_patient_examples_2\\v1_1'

# Helper functions

def create_tmp_database(path=None, name='tmp'):
    tmp = os.path.join(os.path.dirname(__file__), name)
    if os.path.isdir(tmp):
        shutil.rmtree(tmp)
    if path is not None:
        shutil.copytree(path, tmp)
    else:
        os.makedirs(tmp)
    return tmp

def remove_tmp_database(tmp):
    shutil.rmtree(tmp)


##
## Tests
##


def test_build():
    pass
    # To build an executable of the application
    # -----------------------------------------
    # place any required hooks in the directory of the main script.
    # pip install pyinstaller
    # pyinstaller --name dev_app --clean --onefile --noconsole --additional-hooks-dir=. dev.py

def test_launch():

    #tmp = create_tmp_database(onefile)
    tmp = tristan

    app = wezel.app()
    app.set_app(wezel.apps.dicom.Windows)
    app.open(tmp)
    #app.set_menu(wezel.menus.test)
    app.show()



if __name__ == "__main__":

    test_launch()


    print('-----------------------')
    print('wezel passed all tests!')
    print('-----------------------')