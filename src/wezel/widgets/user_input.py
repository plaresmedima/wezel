"""This module contains classes for the creation of a custom widget 
    for a pop-up dialog window with one or more input widgets to accept input data."""
__all__ = ['ParameterInputDialog']

from ast import literal_eval

from PyQt5.QtWidgets import (QDialog, QFormLayout, QDialogButtonBox, QComboBox,
                             QLabel, QSpinBox, QMessageBox, QScrollBar,
                             QDoubleSpinBox, QLineEdit, QListWidget, QAbstractItemView )
from PyQt5 import QtCore


# User-defined exceptions
class Error(Exception):
   """Base class for other exceptions"""
   pass

class IncorrectParameterTypeError(Error):
   """Raised when a parameter type is not 'integer', 'float' or 'string'.
   A unit test for developers to avoid typos."""
   pass

class ParameterInputDialog(QDialog):
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
        try:
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
            self.buttonBox.accepted.connect(self.accept)   #OK button
            self.buttonBox.rejected.connect(self.close)  #Cancel button
            self.closeDialog = False
            self.layout = QFormLayout()
            if helpText:
                self.helpTextLbl = QLabel("<H4>" + helpText  +"</H4>")
                self.helpTextLbl.setWordWrap(True)
                self.layout.addRow(self.helpTextLbl)
            self.listWidget = []
            listCounter = 0
            paramDict, lists = self._processInput(*fields)
            for key in paramDict:
                paramType, value1, value2, value3 = self._getParamData(paramDict[key])
                if paramType.lower() not in ("integer", "float", "string", "dropdownlist", "listview"):
                    #This unit test is for developers who mistype the above 5 parameter 
                    #types when they are developing new WEZEL tools that need
                    #an input dialog
                    raise IncorrectParameterTypeError
                if paramType == "integer":
                    self.input = QSpinBox()
                    if value2:
                        self.input.setMinimum(int(value2))
                    if value3:
                        self.input.setMaximum(int(value3))
                    if value1:
                        self.input.setValue(int(value1))
                elif paramType == "float":
                    self.input = QDoubleSpinBox()
                    if value2:
                        self.input.setMinimum(float(value2))
                    if value3:
                        self.input.setMaximum(float(value3))
                    if value1:
                        self.input.setValue(float(value1))
                elif paramType == "string":
                    self.input = QLineEdit()
                    if key=="Password": self.input.setEchoMode(QLineEdit.Password)
                    if value1:
                        self.input.setText(value1)
                    else:
                        self.input.setPlaceholderText("Enter your text")
                    #uncomment to set an input mask
                    #self.input.setInputMask('000.000.000.000;_')
                elif paramType == "dropdownlist":
                    self.input = QComboBox()
                    self.input.addItems(lists[listCounter])
                    listCounter += 1
                    if value1:
                        self.input.setCurrentIndex(int(value1))   
                elif paramType == "listview":
                    self.input = QListWidget()
                    self.input.setSelectionMode(QAbstractItemView.ExtendedSelection)
                    self.input.addItems(lists[listCounter])
                    #self.input.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    #self.input.setCheckState(Qt.Unchecked)
                    # scroll bar 
                    scrollBar = QScrollBar(self) 
                    # setting vertical scroll bar to it 
                    self.input.setVerticalScrollBar(scrollBar)
                    self.input.setMinimumHeight(self.input.sizeHintForColumn(0))
                    self.input.setMinimumWidth(self.input.sizeHintForColumn(0))
                    listCounter += 1
                    
                self.layout.addRow(key, self.input)
                self.listWidget.append(self.input)
            self.layout.addRow("", self.buttonBox)
            self.setLayout(self.layout)
            self.exec_()  #display input dialog
        except IncorrectParameterTypeError:
            str1 = 'Cannot procede because the parameter type for an input field '
            str2 = 'in the parameter input dialog is incorrect. ' 
            str3 = chr(34) + paramType + chr(34)+  ' was used. '
            str4 = 'Permitted types are' + chr(34) + 'integer,' + chr(34) + 'float' + chr(34) 
            str5 = ' and ' + chr(34) + 'string' + chr(34) + ' input as strings.'
            warningString =  str1 + str2 + str3 + str4 + str5
            print(warningString)
            #logger.info('InputDialog - ' + warningString)
            QMessageBox().critical( self,  "Parameter Input Dialog", warningString, QMessageBox.Ok)
        except Exception as e:
            print('Error in class ParameterInputDialog.__init__: ' + str(e))
            #logger.error('Error in class ParameterInputDialog.__init__: ' + str(e)) 


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
            if field['type'] == "listview": 
                field['value'] = [0]

            elif field["type"] == "dropdownlist":
                if "value" not in field: field["value"] = 0

            elif field["type"] == "string":
                if "value" not in field: field["value"] = "Hello"

            elif field["type"] == "integer":
                if "minimum" not in field: 
                    field["minimum"] = -2147483648
                if "maximum" not in field: 
                    field["maximum"] = +2147483647
                if "value" not in field: 
                    field["value"] = field["minimum"] 
                    field["value"] += 0.5*(field["maximum"]-field["minimum"])
                    field["value"] = int(field["value"])
                if field["value"] < field["minimum"]: 
                    field["value"] = field["minimum"]
                if field["value"] > field["maximum"]: 
                    field["value"] = field["maximum"]

            elif field["type"] == "float":
                if "minimum" not in field: 
                    field["minimum"] = -1.0e+18
                if "maximum" not in field: 
                    field["maximum"] = +1.0e+18
                if "value" not in field: 
                    field["value"] = field["minimum"] 
                    field["value"] += 0.5*(field["maximum"]-field["minimum"])              
                if field["value"] < field["minimum"]: 
                    field["value"] = field["minimum"]
                if field["value"] > field["maximum"]: 
                    field["value"] = field["maximum"]

        # first ensure each label is unique 
        for f, field in enumerate(fields):
            for field_next in fields[f+1:]:
                if field_next["label"] == field["label"]:
                    field_next["label"] += '_'

        # next build a single dictionary
        dict = {}
        for field in fields:
            dict[field["label"]] = field["type"]

            if field["type"] == "dropdownlist":
                dict[field["label"]] += ", " + str(field["value"])

            elif field["type"] == "string":
                dict[field["label"]] += ", " + str(field["value"])

            elif field["type"] == "integer":
                dict[field["label"]] += ", " + str(field["value"])
                dict[field["label"]] += ", " + str(field["minimum"])
                dict[field["label"]] += ", " + str(field["maximum"])

            elif field["type"] == "float":
                dict[field["label"]] += ", " + str(field["value"])
                dict[field["label"]] += ", " + str(field["minimum"])
                dict[field["label"]] += ", " + str(field["maximum"])

        # then build a single list of lists         
        lists = []
        for field in fields:
            if field["type"] == "listview":
                lists.append(field["list"])
            elif field["type"] == "dropdownlist":
                lists.append(field["list"])
        return dict, lists


    def _getParamData(self, paramDescription):
        commaCount = paramDescription.count(',')
        if commaCount == 0:
            return paramDescription, None, None, None
        elif commaCount == 1:
            paramList = paramDescription.split(",")
            return paramList[0], paramList[1], None, None
        elif commaCount == 2:
            paramList = paramDescription.split(",")
            return paramList[0], paramList[1], paramList[2], None
        elif commaCount == 3:
            paramList = paramDescription.split(",")
            return paramList[0], paramList[1], paramList[2], paramList[3]


    def close(self):
        self.closeDialog =True
        #Now programmatically click OK to close the dialog
        self.accept()


    def _closeInputDialog(self):
            return self.closeDialog


    def _processOutput(self, fields, listParams):
        outputList = []
        # Sometimes the values parsed could be list or hexadecimals in strings
        for param in listParams:
            try:
                outputList.append(literal_eval(param))
            except:
                outputList.append(param)
    
        if outputList is None: 
            return 1, fields
        else:
            # Overwrite the value key with the returned parameter
            for f, field in enumerate(fields):
                if field["type"] == "listview":
                    value_list = outputList[f]
                    for v, value in enumerate(value_list):
                        value_list[v] = field["list"].index(value) 
                    field["value"] = value_list
        
                elif field["type"] == "dropdownlist":
                    value = outputList[f]
                    field["value"] = field["list"].index(value) 
    
                elif field["type"] == "string":
                    field["value"] = outputList[f]
    
                elif field["type"] == "integer":
                    field["value"] = outputList[f]
    
                elif field["type"] == "float":
                    field["value"] = outputList[f]
            return 0, fields


    def returnListParameterValues(self):
        """Returns a list of parameter values as input by the user, 
        in the same as order as the widgets
        on the input dialog from top most (first item in the list) 
        to the bottom most (last item in the list)."""
        try:
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
        except Exception as e:
            print('Error in class ParameterInputDialog.returnListParameterValues: ' + str(e))
            #logger.error('Error in class ParameterInputDialog.returnListParameterValues: ' + str(e)) 