__all__ = ['SeriesViewerMetaData']
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import ( QApplication, QFileDialog, QLineEdit,                            
        QMdiArea, QMessageBox, QWidget, QGridLayout, QVBoxLayout, QSpinBox,
        QMdiSubWindow,  QMainWindow, QHBoxLayout, QDoubleSpinBox,
        QPushButton, QStatusBar, QLabel,  QHeaderView,
        QTreeWidgetItem, QGridLayout, QSlider, QCheckBox, QLayout, QAbstractItemView,
        QProgressBar, QComboBox, QTableWidget, QTableWidgetItem, QFrame)

import os
import pydicom
import pandas as pd


localStyleSheet = """
    QTableWidget {
    alternate-background-color: #dce2f2;background-color: #b6bdd1;
                                            }           
    QTableWidget::item {
        border: 5px solid rgba(68, 119, 170, 150);
        }

    QHeaderView, QHeaderView::section {
        background-color: rgba(125, 125, 125, 125);
        font-weight: bold;
        font-size: x-large;}
            """

class SeriesViewerMetaData(QWidget):
    """Display DICOM Series Metadata in a table."""

    def __init__(self, series):  
        """
        Constructs the composite widget for displaying a table of DICOM series metadata
        """
        super().__init__()
        #Get the DICOM object for the first image in the series
        #The DICOM object for an image contains the metadata for the whole series
        self._objectDICOM = series.children(0).read() 

        self.setLayout(QVBoxLayout())
        self.setAttribute(Qt.WA_DeleteOnClose)
        tableTitle = "Metadata for series, {}".format(series.label())
        lblImageName = QLabel('<H4>' + tableTitle + '</H4>')
        self.layout().addWidget(lblImageName)

        # Add Search Bar
        self.searchField = QLineEdit()
        self.searchField.textEdited.connect(lambda x=self.searchField.text(): self.searchTable(DICOM_Metadata_Table_View, x))
        
        # Add export to Excel/CSV buttons
        self.export_excel_button = QPushButton('&Export To Excel', clicked=lambda: self.exportToFile(self, DICOM_Metadata_Table_View, excel=True))
        self.export_csv_button = QPushButton('&Export To CSV', clicked=lambda: self.exportToFile(self, DICOM_Metadata_Table_View, csv=True))

        self.horizontalBox = QHBoxLayout()
        self.horizontalBox.addWidget(self.searchField)
        self.horizontalBox.addWidget(self.export_excel_button)
        self.horizontalBox.addWidget(self.export_csv_button)

        self.layout().addLayout(self.horizontalBox)

        DICOM_Metadata_Table_View = self.buildTableView()
        self.layout().addWidget(DICOM_Metadata_Table_View) 
        
    
    def buildTableView(self):
        """Builds a Table View displaying DICOM image metadata
        as Tag, name, VR & Value"""
        try:
            tableWidget = QTableWidget()
            tableWidget.setAlternatingRowColors(True)
            tableWidget.setStyleSheet(localStyleSheet) 
            tableWidget.setShowGrid(True)
            tableWidget.setColumnCount(4)
            tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

            self.createHeaderRow(tableWidget)
            
            if self._objectDICOM:
                # Loop through the DICOM group (0002, XXXX) first
                for meta_element in self._objectDICOM.file_meta:
                    rowPosition = tableWidget.rowCount()
                    tableWidget.insertRow(rowPosition)
                    tableWidget.setItem(rowPosition , 0, 
                                    QTableWidgetItem(str(meta_element.tag)))
                    tableWidget.setItem(rowPosition , 1, 
                                    QTableWidgetItem(meta_element.name))
                    tableWidget.setItem(rowPosition , 2, 
                                    QTableWidgetItem(meta_element.VR))
                    if meta_element.VR == "OW" or meta_element.VR == "OB" or meta_element.VR == "UN":
                        try:
                            valueMetadata = str(list(meta_element))
                        except:
                            valueMetadata = str(meta_element.value)
                    else:
                        valueMetadata = str(meta_element.value)
                    if meta_element.VR == "SQ":
                        tableWidget.setItem(rowPosition , 3, QTableWidgetItem(""))
                        tableWidget = self.iterateSequenceTag(tableWidget, meta_element, level=">")
                    else:
                        tableWidget.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))
                
                for data_element in self._objectDICOM:
                    # Exclude pixel data from metadata listing
                    if data_element.name == 'Pixel Data':
                        continue
                    rowPosition = tableWidget.rowCount()
                    tableWidget.insertRow(rowPosition)
                    tableWidget.setItem(rowPosition , 0, 
                                    QTableWidgetItem(str(data_element.tag)))
                    tableWidget.setItem(rowPosition , 1, 
                                    QTableWidgetItem(data_element.name))
                    tableWidget.setItem(rowPosition , 2, 
                                    QTableWidgetItem(data_element.VR))
                    if data_element.VR == "OW" or data_element.VR == "OB" or data_element.VR == "UN":
                        try:
                            #valueMetadata = str(data_element.value.decode('utf-8'))
                            valueMetadata = str(list(data_element))
                        except:
                            try:
                                #valueMetadata = str(list(data_element))
                                valueMetadata = str(data_element.value.decode('utf-8'))
                            except:
                                valueMetadata = str(data_element.value)
                    else:
                        valueMetadata = str(data_element.value)
                    if data_element.VR == "SQ":
                        tableWidget.setItem(rowPosition , 3, QTableWidgetItem(""))
                        tableWidget = self.iterateSequenceTag(tableWidget, data_element, level=">")
                    else:
                        tableWidget.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))
            
            #Resize columns to fit contents
            header = tableWidget.horizontalHeader()
            header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
            header.setSectionResizeMode(3, QHeaderView.ResizeMode(QHeaderView.AdjustToContentsOnFirstShow))
            tableWidget.setWordWrap(True)
            return tableWidget
        except Exception as e:
            print('Error in : SeriesViewerMetaData.buildTableView' + str(e))
            logger.error('Error in : SeriesViewerMetaData.buildTableView' + str(e))


    def createHeaderRow(self, tableWidget):
        headerItem = QTableWidgetItem(QTableWidgetItem("Tag\n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        tableWidget.setHorizontalHeaderItem(0,headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("Name \n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        tableWidget.setHorizontalHeaderItem(1, headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("VR \n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        tableWidget.setHorizontalHeaderItem(2, headerItem)
        headerItem = QTableWidgetItem(QTableWidgetItem("Value\n")) 
        headerItem.setTextAlignment(Qt.AlignLeft)
        tableWidget.setHorizontalHeaderItem(3 , headerItem)


    def iterateSequenceTag(self, table, dataset, level=">"):
        try:
            for data_element in dataset:
                if isinstance(data_element, pydicom.dataset.Dataset):
                    table = self.iterateSequenceTag(table, data_element, level=level)
                else:
                    rowPosition = table.rowCount()
                    table.insertRow(rowPosition)
                    table.setItem(rowPosition , 0, QTableWidgetItem(level + str(data_element.tag)))
                    table.setItem(rowPosition , 1, QTableWidgetItem(data_element.name))
                    table.setItem(rowPosition , 2, QTableWidgetItem(data_element.VR))
                    if data_element.VR == "OW" or data_element.VR == "OB":
                        try:
                            valueMetadata = str(data_element.value.decode('utf-8'))
                        except:
                            try:
                                valueMetadata = str(list(data_element))
                            except:
                                valueMetadata = str(data_element.value)
                    else:
                        valueMetadata = str(data_element.value)
                    if data_element.VR == "SQ":
                        table.setItem(rowPosition , 3, QTableWidgetItem(""))
                        table = self.iterateSequenceTag(table, data_element, level=level+">")
                        level = level[:-1]
                    else:
                        table.setItem(rowPosition , 3, QTableWidgetItem(valueMetadata))
            return table
        except Exception as e:
            print('Error in : SeriesViewerMetaData.iterateSequenceTag' + str(e))
            logger.error('Error in : SeriesViewerMetaData.iterateSequenceTag' + str(e))


    def exportToFile(self, parent, table, excel=False, csv=False):
        try:
            columHeaders = []
            for i in range(table.model().columnCount()):
                columHeaders.append(table.horizontalHeaderItem(i).text())
            df = pd.DataFrame(columns=columHeaders)
            for row in range(table.rowCount()):
                for col in range(table.columnCount()):
                    df.at[row, columHeaders[col]] = table.item(row, col).text()
            if excel:
                filename, _ = QFileDialog.getSaveFileName( parent, 'Save Excel file as ...',  'Metadata.xlsx', "Excel files (*.xlsx)") #os.path.join(wezel.data_folder(),
                if filename != '':
                    df.to_excel(filename, index=False)
                    QMessageBox.information(parent, "Export to Excel", "File " + filename + " saved successfully")
            if csv:
                filename, _ = QFileDialog.getSaveFileName(parent, 'Save CSV file as ...', 'Metadata.csv', "CSV files (*.csv)") #os.path.join(wezel.data_folder(),
                if filename != '':
                    df.to_csv(filename, index=False)
                    QMessageBox.information(parent, "Export to CSV", "File " + filename + " saved successfully")
        except Exception as e:
            print('Error in : SeriesViewerMetaData.exportToFile: ' + str(e))
            logger.error('Error in : SeriesViewerMetaData.exportToFile: ' + str(e))


    def searchTable(self, table, expression):
        try:
            table.clearSelection()
            if expression:
                items = table.findItems(expression, Qt.MatchContains)
                if items:  # we have found something
                    for item in items:
                        item.setSelected(True)
                        #table.item(item).setSelected(True)
                    table.scrollToItem(items[0])
                    #item = items[0]  # take the first
                    #table.table.setCurrentItem(item)
        except Exception as e:
            print('Error in : SeriesViewerMetaData.searchTable: ' + str(e))
            logger.error('Error in : SeriesViewerMetaData.searchTable: ' + str(e))











