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
tristan = 'C:\\Users\\steve\\Dropbox\\Data\\wezel_dev_tristan'

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
    # Turn off dropbox
    # place any required hooks in the directory of the main script.
    # pip install pyinstaller
    # pyinstaller --name wezel --clean --onefile --noconsole --additional-hooks-dir=. exec.py

def test_launch():

    #tmp = create_tmp_database(onefile)
    #tmp = create_tmp_database(rider)
    tmp = tristan

    app = wezel.app()
    app.set_app(wezel.apps.dicom.Windows)
    app.open(tmp)
    #app.set_menu(wezel.menus.test)
    app.show()
    

def test_DICOMFolderTree():

    interactive = True

    tmp = create_tmp_database(rider)
    #tmp = tristan
    database = db.database(tmp)

    app = QApplication(sys.argv)
    start = timeit.default_timer()
    window = widgets.DICOMFolderTree(database)
    stop = timeit.default_timer()
    window.selectRecords(database.patients()[0].studies()[0].uid)
    window.selectRecords(database.patients()[-1].uid)
    window.itemSelectionChanged.connect(lambda record: print('Selection changed for ' + record['label']))
    window.itemDoubleClicked.connect(lambda record: print('Double click on ' + record['label']))
    window.show()
    if interactive:
        app.exec_()

    print('Time for buiding display (sec)', stop-start)

    remove_tmp_database(tmp)


def test_SeriesSliders():

    interactive = True

    tmp = create_tmp_database(rider)
    #tmp = tristan
    database = db.database(tmp)
    #series = database.series()[5]
    series = db.merge(database.series())

    app = QApplication(sys.argv)
    window = widgets.SeriesSliders(series)
    window.valueChanged.connect(lambda image: 
        print('No image') if image is None else print('Image ' + str(image.InstanceNumber))
    )
    window.show()
    if interactive:
        app.exec_()

    remove_tmp_database(tmp)



if __name__ == "__main__":

    test_launch()
    #test_DICOMFolderTree()
    #test_SeriesSliders()


    print('-----------------------')
    print('wezel passed all tests!')
    print('-----------------------')