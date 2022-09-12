# importing libraries
import sys
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
  
# main window class
class   Window(QMainWindow):
  
    # constructor
    def __init__(self):
        super().__init__()
  
        # calling the method for widgets
        self.initUI()
  
    def initUI(self):
  
        # creating check box
        self.checkBoxNone = QCheckBox("Don't know ?", self)
  
        # setting geometry
        self.checkBoxNone.setGeometry(200, 150, 100, 30)
  
        # creating check box
        self.checkBoxA = QCheckBox("Geek", self)
  
        # setting geometry
        self.checkBoxA.setGeometry(200, 180, 100, 30)
  
        # creating check box
        self.checkBoxB = QCheckBox(" Not a geek ?", self)
  
        # setting geometry
        self.checkBoxB.setGeometry(200, 210, 100, 30)
  
        # calling the uncheck method if any check box state is changed
        self.checkBoxNone.stateChanged.connect(self.uncheck)
        self.checkBoxA.stateChanged.connect(self.uncheck)
        self.checkBoxB.stateChanged.connect(self.uncheck)
  
        # setting window title
        self.setWindowTitle('Python')
  
        # setting geometry of window
        self.setGeometry(100, 100, 600, 400)
  
        # showing all the widgets
        self.show()
  
    # uncheck method
    def uncheck(self, state):
  
        # checking if state is checked
        if state == Qt.Checked:
  
            # if first check box is selected
            if self.sender() == self.checkBoxNone:
  
                print('First box checked')
  
            # if second check box is selected
            elif self.sender() == self.checkBoxA:
  
                print('Second box checked')
  
            # if third check box is selected
            elif self.sender() == self.checkBoxB:
  
                print('Third box checked')
                
        elif state == Qt.Unchecked:
              # if first check box is selected
            if self.sender() == self.checkBoxNone:
  
                print('First box unchecked')
  
            # if second check box is selected
            elif self.sender() == self.checkBoxA:
  
                print('Second box unchecked')
  
            # if third check box is selected
            elif self.sender() == self.checkBoxB:
  
                print('Third box unchecked')
  
  
  
# create pyqt5 app
App = QApplication(sys.argv)
  
# create the instance of our Window
window = Window()
  
# start the app
sys.exit(App.exec())