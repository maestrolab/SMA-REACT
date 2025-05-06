# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'loading_screen.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie

class Ui_Loading(object):
    def setupUi(self, Loading):
        Loading.setObjectName("Loading")
        Loading.resize(600, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Loading.sizePolicy().hasHeightForWidth())
        Loading.setSizePolicy(sizePolicy)
        Loading.setMinimumSize(QtCore.QSize(600, 600))
        Loading.setMaximumSize(QtCore.QSize(618, 600))
        Loading.setStyleSheet("background-color: #540404;\nborder-radius: 30px;")
        Loading.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.centralwidget = QtWidgets.QWidget(Loading)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(600, 444))
        self.label.setMaximumSize(QtCore.QSize(600, 444))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(600, 132))
        self.label_2.setMaximumSize(QtCore.QSize(600, 132))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(35)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #ffffff")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        Loading.setCentralWidget(self.centralwidget)

        self.retranslateUi(Loading)
        QtCore.QMetaObject.connectSlotsByName(Loading)

        self.label.setText("")
        movie = QMovie("output-onlinegiftools (3).gif")
        movie.setSpeed(300)
        self.label.setMovie(movie)

        movie.start()

    def retranslateUi(self, Loading):
        _translate = QtCore.QCoreApplication.translate
        Loading.setWindowTitle(_translate("Loading", "MainWindow"))
        self.label.setText(_translate("Loading", "TextLabel"))
        self.label_2.setText(_translate("Loading", "<strong>Loading SMA React..."))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_Loading()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())



# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from PyQt5 import QtCore
# from PyQt5.QtGui import QMovie
# import sys
#
# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         self.setFixedWidth(600)
#         self.setFixedHeight(600)
#         self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         self.setStyleSheet("background-color: #3d4855")
#
#         label = QLabel(self)
#         label.setGeometry(QtCore.QRect(0, 0, 600, 444))
#         movie = QMovie("ezgif.com-gif-maker (1).gif")
#         label.setMovie(movie)
#         movie.start()
#         # label.setText("sdgjnsfkjgn")
#
#
#
#
#
# app = QApplication([])
# window = Window()
# window.show()
# sys.exit(app.exec())

