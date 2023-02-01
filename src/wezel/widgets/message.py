#from ast import literal_eval

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import (    
    QApplication,                          
    QStatusBar, 
    QProgressBar, 
    QFileDialog, 
    QMessageBox, 
    QDialog, 
    QFormLayout, 
    QDialogButtonBox, 
    QComboBox,
    QLabel, 
    QSpinBox, 
    QMessageBox, 
    QScrollBar,
    QDoubleSpinBox, 
    QLineEdit, 
    QListWidget, 
    QAbstractItemView 
)


class Dialog():

    def __init__(self, parent=None):

        self.parent = parent

    def information(self, message="Message in the box", title="Information"):
        """
        Information message. Press 'OK' to continue.
        """
        QMessageBox.information(self.parent, title, message)

    def warning(self, message="Message in the box", title="Warning"):
        """
        Warning message. Press 'OK' to continue.
        """
        QMessageBox.warning(self.parent, title, message)

    def error(self, message="Message in the box", title="Error"):
        """
        Error message. Press 'OK' to continue.
        """
        QMessageBox.critical(self.parent, title, message)

    def directory(self, message='Please select a folder', datafolder=None):
        """
        Select a directory.
        """
        return QFileDialog.getExistingDirectory(
            parent = self.parent, 
            caption = message, 
            directory = datafolder, 
            options = QFileDialog.ShowDirsOnly)

    def files(self, 
        title = 'Select files..', 
        initial_folder = None, 
        extension = "All files (*.*)"):
        """
        Select a file to read.
        """
        # dialog = QFileDialog()
        # dialog.setFileMode(QFileDialog.ExistingFiles)
        # #dialog.setNameFilter("Images (*.png *.xpm *.jpg)")
        # dialog.exec_()
        # return dialog.selectedFiles()
        # This selects files only - ideally want to select files and directories
        # This may be a solution 
        # https://stackoverflow.com/questions/6484793/multiple-files-and-folder-selection-in-a-qfiledialog
        names, _ = QFileDialog.getOpenFileNames(None, title, initial_folder, extension)
        return names

    def question(self, message="Do you wish to proceed?", title="Question for the user", cancel=False):
        """
        Displays a question window in the User Interface.
        
        The user has to click either "OK" or "Cancel" in order to continue using the interface.
        Returns False if reply is "Cancel" and True if reply is "OK".
        """
        if cancel:
            reply = QMessageBox.question(
                self.parent, title, message,
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, 
                QMessageBox.No)
        else:
            reply = QMessageBox.question(
                self.parent, title, message,
                QMessageBox.Yes | QMessageBox.No, 
                QMessageBox.No)
        if reply == QMessageBox.Yes: return "Yes"
        elif reply == QMessageBox.No: return "No"
        elif reply == QMessageBox.Cancel: return "Cancel"

    def file_to_open(self, 
        title = 'Open file..', 
        initial_folder = None, 
        extension = "All files (*.*)", 
        datafolder = None):
        """
        Select a file to read.
        """
        if initial_folder is None:
            initial_folder = datafolder
        filename, _ = QFileDialog.getOpenFileName(title, initial_folder, extension)
        if filename == '': 
            return None
        return filename

    def file_to_save(self, title='Save as ...', directory=None, filter="All files (*.*)", datafolder=None):
        """
        Select a filename to save.
        """
        if directory is None:
            directory = datafolder
        filename, _ = QFileDialog.getSaveFileName(caption=title, directory=directory, filter=filter)
        if filename == '': return None
        return filename

    def input(self, *fields, title="User input window", helpText=""):
        """
        Collect user input of various types.
        """
        input = UserInput(*fields, title=title, helpText=helpText)
        return input.cancel, input.values
        #return dialog.button=='Cancel', dialog.returnListParameterValues()


class StatusBar(QStatusBar):

    def __init__(self):
        super().__init__()

        self.progressBar = QProgressBar()
        self.progressBar.setFixedHeight(10)
        self.addPermanentWidget(self.progressBar)
        self.hide()

    def hide(self):

        self.message('')
        self.progressBar.hide()
        QApplication.processEvents() # allow gui to update

    def message(self, message=None):

        if message == None: 
            message = ''
        self.showMessage(message)
        QApplication.processEvents() # allow gui to update

    def progress(self, value, total, message=None):

        if message is not None: 
            self.message(message)
        self.progressBar.show()
        self.progressBar.setRange(0, total)
        self.progressBar.setValue(value)
        QApplication.processEvents() # allow gui to update - prevent freezing

    def cursorToHourglass(self):
        """
        Turns the arrow shape for the cursor into an hourglass. 
        """   
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

    def cursorToNormal(self):
        """
        Restores the cursor into an arrow after it was set to hourglass 
        """   
        QApplication.restoreOverrideCursor() 

    def pixelValue(self, x, y, array):
        text = ""
        if array is not None:
            if 0 <= x < array.shape[0]:
                if 0 <= y < array.shape[1]:
                    pixelValue = array[x,y]
                    text = "Signal ({}, {}) = {}".format(x, y, pixelValue)
        self.message(text)



class UserInput(QDialog):
    """
    This class  generates a pop-up dialog window with 
    one or more input widgets that can accept the following data types: 
        integer - spin box, 
        float - double spin box
        string - text box, drop down list or list view. 
  The order and type of input widgets is defined in the *fields
  input parameter in the class initialisation function. 
  
  Input Parameters
  *****************
  fields: 
            a list of dictionaries of one of the following types:
            {"type":"float", "label":"Name of the field", "value":1.0, "minimum": 0.0, "maximum": 1.0}
            {"type":"integer", "label":"Name of the field", "value":1, "minimum": 0, "maximum": 100}
            {"type":"string", "label":"Name of the field", "value":"My string"}
            {"type":"dropdownlist", "label":"Name of the field", "list":["item 1",...,"item n" ], "value":2}
            {"type":"listview", "label":"Name of the field", "list":["item 1",...,"item n"]}
          
          Widgets are created in the same order on the dialog they occupy in the dictionary; ie., 
          the first dictionary item is uppermost input widget on the dialog 
          and the last dictionary item is the last input widget on the dialog.
  
  title - optional string containing the input dialog title. 
          Has a default string "Input Parameters"
  helpText - optional help text to be displayed above the input widgets.
  """
    def __init__(self, *fields, title="Input Parameters", helpText=None):
        super().__init__()
        self.fields = fields
        self.setWindowTitle(title)
        #Hide ? help button
        #self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        #Hide top right hand corner X close button
        #self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowCloseButtonHint)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # The following line creates a Customized Window where there are no close and help buttons - relevant for MacOS
        # Consider Qt.FramelessWindowHint if it works for Mac OS
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint, True)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel   #OK and Cancel button
        #QBtn = QDialogButtonBox.Ok    #OK button only
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.clickedOK)   #OK button
        self.buttonBox.rejected.connect(self.clickedCancel)  #Cancel button
        #self.closeDialog = False
        self.layout = QFormLayout()
        if helpText:
            self.helpTextLbl = QLabel("<H4>" + helpText  +"</H4>")
            self.helpTextLbl.setWordWrap(True)
            self.layout.addRow(self.helpTextLbl)
        self.listWidget = []
        #listCounter = 0
        #paramDict, lists = self._processInput(*fields)
        #for key in paramDict:
            #paramType, value1, value2, value3 = self._getParamData(paramDict[key])
        for field in self._processInput(*fields):

            if field['type'] == "integer":
                self.input = QSpinBox()
                self.input.setMinimum(int(field['minimum']))
                self.input.setMaximum(int(field['maximum']))
                self.input.setValue(int(field['value']))

            elif field['type'] == "float":
                self.input = QDoubleSpinBox()
                self.input.setMinimum(float(field['minimum']))
                self.input.setMaximum(float(field['maximum']))
                self.input.setValue(float(field['value']))

            elif field['type'] == "string":
                self.input = QLineEdit()
                self.input.setText(str(field['value']))
                
            elif field['type'] == "dropdownlist":
                self.input = QComboBox()
                self.input.addItems([str(v) for v in field["list"]])
                self.input.setCurrentIndex(int(field['value'])) 

            elif field['type'] == "listview":
                self.input = QListWidget()
                self.input.setSelectionMode(QAbstractItemView.ExtendedSelection)
                self.input.addItems([str(v) for v in field["list"]])
                #self.input.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                #self.input.setCheckState(Qt.Unchecked)
                # scroll bar 
                scrollBar = QScrollBar(self) 
                # setting vertical scroll bar to it 
                self.input.setVerticalScrollBar(scrollBar)
                self.input.setMinimumHeight(self.input.sizeHintForColumn(0))
                self.input.setMinimumWidth(self.input.sizeHintForColumn(0))
                #Initialise selections
                for i in field['value']:
                    item = self.input.item(i)
                    item.setSelected(True)

            self.layout.addRow(field['label'], self.input)
            self.listWidget.append(self.input)

        self.layout.addRow("", self.buttonBox)
        self.setLayout(self.layout)
        self.exec_()  #display input dialog
        self.cancel = self.button=='Cancel'
        self.values = self.returnListParameterValues()



    def _processInput(self, *fields):
        """Processes the dictionary objects in *fields into a format that 
        can be used to create the widgets on the input dialog window.
        Parameters
        ----------
        fields: 
            a list of dictionaries of one of the following types:
            {"type":"float", "label":"Name of the field", "value":1.0, "minimum": 0.0, "maximum": 1.0}
            {"type":"integer", "label":"Name of the field", "value":1, "minimum": 0, "maximum": 100}
            {"type":"string", "label":"Name of the field", "value":"My string"}
            {"type":"dropdownlist", "label":"Name of the field", "list":["item 1",...,"item n" ], "value":2}
            {"type":"listview", "label":"Name of the field", "list":["item 1",...,"item n"]}
            The type and label keys are required, the others are optional.
        Return values
        -------------
        dict: 
            dictionary describing each widget on the input window
        lists:
            List of lists, where each individual list contains the items in drop down list
            and list view widgets on the input window.
        """
    
        # set default values for items that are not provided by the user
        for field in fields:

            if field['type'] not in ("integer", "float", "string", "dropdownlist", "listview"):
                msg = field['label'] + ' is not a valid type \n'
                msg += 'Must be either integer, float, string, dropdownlist or listview'
                raise TypeError(msg)

            if field['type'] == "listview":
                if "value" not in field: 
                    field['value'] = []

            elif field["type"] == "dropdownlist":
                if "value" not in field: 
                    field["value"] = 0

            elif field["type"] == "string":
                if "value" not in field: 
                    field["value"] = "Hello"

            elif field["type"] == "integer":
                if "value" not in field: 
                    field["value"] = 0 
                if "minimum" not in field: 
                    field["minimum"] = -2147483648
                if "maximum" not in field: 
                    field["maximum"] = +2147483647
                if field["value"] < field["minimum"]: 
                    field["value"] = field["minimum"]
                if field["value"] > field["maximum"]: 
                    field["value"] = field["maximum"]

            elif field["type"] == "float":
                if "value" not in field: 
                    field["value"] = 0.0  
                if "minimum" not in field: 
                    field["minimum"] = -1.0e+18
                if "maximum" not in field: 
                    field["maximum"] = +1.0e+18          
                if field["value"] < field["minimum"]: 
                    field["value"] = field["minimum"]
                if field["value"] > field["maximum"]: 
                    field["value"] = field["maximum"]

        return fields


    def clickedOK(self): # OK button clicked
        self.button = 'OK'
        self.accept()
    
    def clickedCancel(self): # Cancel button clicked
        self.button = 'Cancel'
        self.accept()


    def _processOutput(self, fields, outputList):
        if outputList is None: 
            return fields
        else:
            # Overwrite the value key with the returned parameter
            for f, field in enumerate(fields):
                if field["type"] == "listview":
                    value = outputList[f]
                    ls = [str(item) for item in field["list"]]
                    field["value"] = [ls.index(v) for v in value]
        
                elif field["type"] == "dropdownlist":
                    value = outputList[f]
                    ls = [str(item) for item in field["list"]]
                    field["value"] = ls.index(value) 
    
                elif field["type"] == "string":
                    field["value"] = outputList[f]
    
                elif field["type"] == "integer":
                    field["value"] = outputList[f]
    
                elif field["type"] == "float":
                    field["value"] = outputList[f]
            return fields


    def returnListParameterValues(self):
        """Returns a list of parameter values as input by the user, 
        in the same as order as the widgets
        on the input dialog from top most (first item in the list) 
        to the bottom most (last item in the list)."""

        paramList = []
        for item in self.listWidget:
            if isinstance(item, QLineEdit):
                paramList.append(item.text())
            elif isinstance(item, QComboBox):
                paramList.append(item.currentText())
            elif isinstance(item, QListWidget):
                paramList.append([itemText.text() for itemText in item.selectedItems()])
            else:
                paramList.append(item.value())

        return self._processOutput(self.fields, paramList)