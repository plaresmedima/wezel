from LoggingWidget import LoggingWidget  as logWidget
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
import time

def myFunction(signals):
  for n in range(0, 5):
    time.sleep(3)
    signals.log.emit("Message " + str(n))
  signals.result.emit("Result of the calculation") 
  return "Done."

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Test Progress Display")
        self.createDisplay()
        self.progWindow.executeFunction()


    def createDisplay(self):
        self.progWindow = logWidget(myFunction)
        self.setCentralWidget(self.progWindow)
