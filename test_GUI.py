# -*- coding: utf-8 -*-
"""
Created on Tue Dec  5 19:21:59 2023

@author: pwal5
"""
from PyQt5 import QtWidgets
import sys

from test_tab import createTab1

class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__() #Inherits all of the objects from QMainWindow


        app = QtWidgets.QApplication(sys.argv)
        
        self.setGeometry(200, 200, 1600, 900)
        
        
        self.layout = QtWidgets.QVBoxLayout(self) 


        self.tabs = QtWidgets.QTabWidget()

        self.tab2 = QtWidgets.QWidget()
        
        
        self.tab3 = createTab1()
        
        
        self.tab1 = QtWidgets.QWidget()
        self.tab1.layout = QtWidgets.QVBoxLayout(self)
        self.tab1.setLayout(self.tab1.layout)
        self.tab1.pushButton = QtWidgets.QPushButton(self)
        self.tab1.pushButton.setText('Change Tab')

        self.tab1.layout.addWidget(self.tab1.pushButton)

        
        self.tab1.pushButton.clicked.connect(self.changeTabs)
        
        self.tab3.pushButton_2.clicked.connect(self.changeTabs)
        
        self.tabs.addTab(self.tab1,"Tab 1")
        self.tabs.addTab(self.tab2,"Tab 2")
        
        self.tabs.addTab(self.tab3,"Tab 3")
        
        self.setCentralWidget(self.tabs)

        self.tabs.setTabEnabled(1,False)

        self.show()
        
    def changeTabs(self):
        ex.tabs.setTabEnabled(1,True)
        ex.tabs.setCurrentIndex(1)
        

        # self.show()
        
        # self.setCentralWidget(self.layout)
        
        # self.pushButton.clicked.connect(self.changeTabs)
        
    # def changeTabs(self):
    #     self.tabs.setTabEnabled(1,True)
    #     ex.tabs.setCurrentIndex(1)
        

        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ex = App()
    sys.exit(app.exec_())
