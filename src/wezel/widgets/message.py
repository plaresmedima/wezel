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
        if total > 1:
            self.progressBar.show()
            self.progressBar.setRange(0, total)
            self.progressBar.setValue(value)
        else:
            self.progressBar.hide()
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
        
        self.setWindowTitle(title)
        self.setWindowFlag(QtCore.Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.setWindowFlag(QtCore.Qt.CustomizeWindowHint, True)
        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel   #OK and Cancel button
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.clickedOK)   #OK button
        self.buttonBox.rejected.connect(self.clickedCancel)  #Cancel button
        self.layout = QFormLayout()
        if helpText:
            self.helpTextLbl = QLabel("<H4>" + helpText  +"</H4>")
            self.helpTextLbl.setWordWrap(True)
            self.layout.addRow(self.helpTextLbl)

        self.fields = fields
        self.listWidget = []
        for field in self._processInput(*fields):

            if field['type'] == "integer":
                widget = QSpinBox()
                widget.setMinimum(int(field['minimum']))
                widget.setMaximum(int(field['maximum']))
                widget.setValue(int(field['value']))

            elif field['type'] == "float":
                widget = QDoubleSpinBox()
                widget.setMinimum(float(field['minimum']))
                widget.setMaximum(float(field['maximum']))
                widget.setValue(float(field['value']))

            elif field['type'] == "string":
                widget = QLineEdit()
                widget.setText(str(field['value']))
                
            elif field['type'] == "dropdownlist":
                widget = QComboBox()
                widget.addItems([str(v) for v in field["list"]])
                widget.setCurrentIndex(int(field['value'])) 

            elif field['type'] == "listview":
                widget = QListWidget()
                widget.setSelectionMode(QAbstractItemView.ExtendedSelection)
                widget.addItems([str(v) for v in field["list"]])
                scrollBar = QScrollBar(self) 
                widget.setVerticalScrollBar(scrollBar)
                widget.setMinimumHeight(widget.sizeHintForColumn(0))
                widget.setMinimumWidth(widget.sizeHintForColumn(0))
                for i in field['value']:
                    item = widget.item(i)
                    item.setSelected(True)

            self.layout.addRow(field['label'], widget)
            self.listWidget.append(widget)

        self.layout.addRow("", self.buttonBox)
        self.setLayout(self.layout)
        self.exec_()  
        self.cancel = self.button=='Cancel'
        self.values = self._processOutput()


    def _processInput(self, *fields):
        """Processes the dictionary objects in *fields into a format that 
        can be used to create the widgets on the input dialog window.
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


    def _processOutput(self):
        """Returns a list of parameter values as input by the user, 
        in the same as order as the widgets
        on the input dialog from top most (first item in the list) 
        to the bottom most (last item in the list)."""
  
        # Overwrite the value key with the returned parameter
        for f, field in enumerate(self.fields):
            widget = self.listWidget[f]

            if field["type"] == "listview":
                n, sel = widget.count(), widget.selectedItems()
                field["value"] = [i for i in range(n) if widget.item(i) in sel]
    
            elif field["type"] == "dropdownlist":
                field["value"] = widget.currentIndex()

            elif field["type"] == "string":
                field["value"] = widget.text()

            elif field["type"] == "integer":
                field["value"] = widget.value()

            elif field["type"] == "float":
                field["value"] = widget.value()

        return self.fields


    def clickedOK(self): # OK button clicked
        self.button = 'OK'
        self.accept()
    
    def clickedCancel(self): # Cancel button clicked
        self.button = 'Cancel'
        self.accept()


