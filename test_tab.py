# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 15:28:08 2023

@author: pwal5
"""
from PyQt5 import QtCore, QtGui, QtWidgets
import sys


class createTab1(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget,self).__init__()

        
        # self.central_widget = QtWidgets.QWidget(self)
        
        
        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)
        
        print(self.main_layout)
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setText('Change Tab')

        self.main_layout.addWidget(self.pushButton_2)
        
        self.pushButton_2.clicked.connect(self.changeTabs)
        

        