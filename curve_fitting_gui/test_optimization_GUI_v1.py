# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_base_hort.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import random
import numpy as np
from export import exportData
from PyQt5 import QtCore, QtGui, QtWidgets,QtSvg
from latex_translation import textToLatex
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QCheckBox
from import_vals import importData
from functools import partial

from model_funcs import test_optimizer_v2
import cgitb
cgitb.enable(format="text")

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        #MainWindow.resize(1552, 586)
        #MainWindow.showFullScreen()
        #Resize GUI to take up 75% of the screen (dynamic based on the user's resolution)
        app = QtWidgets.QApplication(sys.argv)
        screen = app.primaryScreen()
        
        header_font = 10
        header_weight = 75
        normal_font = 10
        normal_weight = 50
        
        lineEdit_height = 20
        lineEdit_width = 60 
        
        parameter_label_height = 44
        parameter_label_width = 145
        
        spacer_item_height = lineEdit_height
        spacer_item_small_width = 5
        spacer_item_width = 30
        #create ''master'' spacer item to use throughout
        spacerItem = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        
        spacerItem_2 = QtWidgets.QSpacerItem(spacer_item_small_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        #print('Screen: %s' % screen.name())
        #size = screen.size()
        #print('Size: %d x %d' % (size.width(), size.height()))
        rect = screen.availableGeometry()
        #print('Available: %d x %d' % (rect.width(), rect.height()))
        MainWindow.resize(int(rect.width()*0.75), int(rect.height()*0.75))
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        
        # DV_flags is an array of booleans (T/F) that determines whether
        # a specific design variable is active
        # True = Active (unconstrained)
        # False = Inactive (constrained)
        #Right now, we have 17 design variables possible. Need to revisit this
        self.DV_flags = np.array(np.ones(shape=17),dtype=bool)
        self.flags = {}
        self.flags['modulus_flag'] = False
        self.flags['slope_flag'] = False
        self.flags['smooth_hardening_flag'] = False
        # Elastic properties
        #%% E_M
        self.E_M = QtWidgets.QHBoxLayout()
        self.E_M.setObjectName("E_M")
        # self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6 = textToLatex("$E_{M}$ [$\mathrm{Pa}$]:", parameter_label_width, parameter_label_height, self.centralwidget)
        self.E_M.addWidget(self.label_6)
        # spacerItem36 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_M.addItem(spacerItem_2)
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit.sizePolicy().hasHeightForWidth())
        self.lineEdit.setSizePolicy(sizePolicy)
        self.lineEdit.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit.setObjectName("lineEdit")
        self.E_M.addWidget(self.lineEdit)
        #spacerItem38 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_M.addItem(spacerItem)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_2.setSizePolicy(sizePolicy)
        self.lineEdit_2.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_2.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.E_M.addWidget(self.lineEdit_2)
        #spacerItem37 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        #spacerItem38 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_M.addItem(spacerItem)
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.stateChanged.connect(self.uncheck)
        self.checkBox.setText("")
        self.checkBox.setObjectName("checkBox")
        self.E_M.addWidget(self.checkBox)
        
        self.E_M.addItem(spacerItem)
        self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_3.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.E_M.addWidget(self.lineEdit_3)        
        #spacerItem39 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        
        self.E_M.addItem(spacerItem)
        self.lineEdit_3.setEnabled(False)
        self.checkBox.toggled.connect(self.lineEdit_3.setEnabled)
        self.checkBox.toggled.connect(self.lineEdit_2.setDisabled)
        self.checkBox.toggled.connect(self.lineEdit.setDisabled)
        #%% E_A
        self.E_A = QtWidgets.QHBoxLayout()
        self.E_A.setObjectName("E_A")
        # self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12 = textToLatex("$E_{A}$ [$\mathrm{Pa}$]:", parameter_label_width, parameter_label_height, self.centralwidget)
        self.E_A.addWidget(self.label_12)
        # spacerItem64 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_A.addItem(spacerItem_2)
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_4.setSizePolicy(sizePolicy)
        self.lineEdit_4.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_4.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.E_A.addWidget(self.lineEdit_4)
        self.E_A.addItem(spacerItem)

        self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_5.setSizePolicy(sizePolicy)
        self.lineEdit_5.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_5.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.E_A.addWidget(self.lineEdit_5)
        # spacerItem65 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        # spacerItem66 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_A.addItem(spacerItem)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.stateChanged.connect(self.uncheck)
        self.checkBox_2.setText("")
        self.checkBox_2.setObjectName("checkBox_2")
        self.E_A.addWidget(self.checkBox_2)
        
        self.E_A.addItem(spacerItem)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_6.setSizePolicy(sizePolicy)
        self.lineEdit_6.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_6.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.E_A.addWidget(self.lineEdit_6)
        # spacerItem67 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.E_A.addItem(spacerItem)
        self.lineEdit_6.setEnabled(False)
        self.checkBox_2.toggled.connect(self.lineEdit_6.setEnabled)
        
        self.checkBox_2.toggled.connect(self.lineEdit_4.setDisabled)
        self.checkBox_2.toggled.connect(self.lineEdit_5.setDisabled)
        
        # Transformation temperatures 
        #%%M_s
        self.M_s = QtWidgets.QHBoxLayout()
        self.M_s.setObjectName("M_s")
        self.label_15 = QtWidgets.QLabel(self.centralwidget)
        self.label_15 = textToLatex("$M_{s}$ [$\mathrm{K}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.M_s.addWidget(self.label_15)
        self.M_s.addItem(spacerItem_2)
        self.lineEdit_13 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_13.sizePolicy().hasHeightForWidth())
        self.lineEdit_13.setSizePolicy(sizePolicy)
        self.lineEdit_13.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_13.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.M_s.addWidget(self.lineEdit_13)
        self.M_s.addItem(spacerItem)

        self.lineEdit_14 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_14.setSizePolicy(sizePolicy)
        self.lineEdit_14.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_14.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.M_s.addWidget(self.lineEdit_14)
        # spacerItem49 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.M_s.addItem(spacerItem)
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.stateChanged.connect(self.uncheck)
        self.checkBox_5.setText("")
        self.checkBox_5.setObjectName("checkBox_5")
        self.M_s.addWidget(self.checkBox_5)
        
        self.M_s.addItem(spacerItem)
        self.lineEdit_15 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_15.sizePolicy().hasHeightForWidth())
        self.lineEdit_15.setSizePolicy(sizePolicy)
        self.lineEdit_15.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_15.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.M_s.addWidget(self.lineEdit_15)
        # spacerItem50 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        # spacerItem51 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.M_s.addItem(spacerItem)
        self.lineEdit_15.setEnabled(False)
        self.checkBox_5.toggled.connect(self.lineEdit_15.setEnabled)
        self.checkBox_5.toggled.connect(self.lineEdit_13.setDisabled)
        self.checkBox_5.toggled.connect(self.lineEdit_14.setDisabled)
        #%% A_s
        self.A_s = QtWidgets.QHBoxLayout()
        self.A_s.setObjectName("A_s")
        # self.label_16 = QtWidgets.QLabel(self.centralwidget)
        self.label_16 = textToLatex("$A_{s}$ [$\mathrm{K}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.A_s.addWidget(self.label_16)
        self.A_s.addItem(spacerItem_2)
        self.lineEdit_16 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_16.sizePolicy().hasHeightForWidth())
        self.lineEdit_16.setSizePolicy(sizePolicy)
        self.lineEdit_16.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_16.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.A_s.addWidget(self.lineEdit_16)
        self.A_s.addItem(spacerItem)

        self.lineEdit_17 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_17.setSizePolicy(sizePolicy)
        self.lineEdit_17.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_17.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_17.setObjectName("lineEdit_17")
        self.A_s.addWidget(self.lineEdit_17)
        # spacerItem53 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.A_s.addItem(spacerItem)
        self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.stateChanged.connect(self.uncheck)
        self.checkBox_6.setText("")
        self.checkBox_6.setObjectName("checkBox_6")
        self.A_s.addWidget(self.checkBox_6)
        # self.A_s.addItem(spacerItem)
        self.lineEdit_18 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_18.sizePolicy().hasHeightForWidth())
        self.lineEdit_18.setSizePolicy(sizePolicy)
        self.lineEdit_18.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_18.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_18.setObjectName("lineEdit_18")
        self.A_s.addWidget(self.lineEdit_18)
        # spacerItem54 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        # spacerItem55 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.A_s.addItem(spacerItem)
        self.lineEdit_18.setEnabled(False)
        self.checkBox_6.toggled.connect(self.lineEdit_18.setEnabled)
        self.checkBox_6.toggled.connect(self.lineEdit_16.setDisabled)
        self.checkBox_6.toggled.connect(self.lineEdit_17.setDisabled)
        #%% M_s - M_f
        self.M_s_M_f = QtWidgets.QHBoxLayout()
        self.M_s_M_f.setObjectName("M_s - M_f")
        # self.label_25 = QtWidgets.QLabel(self.centralwidget)
        self.label_25 = textToLatex("$M_{s} - M_{f}$ [$\mathrm{K}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.M_s_M_f.addWidget(self.label_25)
        self.M_s_M_f.addItem(spacerItem_2)
        self.lineEdit_43 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_43.sizePolicy().hasHeightForWidth())
        self.lineEdit_43.setSizePolicy(sizePolicy)
        self.lineEdit_43.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_43.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_43.setObjectName("lineEdit_43")
        self.M_s_M_f.addWidget(self.lineEdit_43)
        self.M_s_M_f.addItem(spacerItem)

        self.lineEdit_44 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_44.setSizePolicy(sizePolicy)
        self.lineEdit_44.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_44.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_44.setObjectName("lineEdit_44")
        self.M_s_M_f.addWidget(self.lineEdit_44)
        # spacerItem69 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.M_s_M_f.addItem(spacerItem)
        self.checkBox_15 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_15.stateChanged.connect(self.uncheck)
        self.checkBox_15.setText("")
        self.checkBox_15.setObjectName("checkBox_15")
        self.M_s_M_f.addWidget(self.checkBox_15)
        self.M_s_M_f.addItem(spacerItem)
        self.lineEdit_45 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_45.sizePolicy().hasHeightForWidth())
        self.lineEdit_45.setSizePolicy(sizePolicy)
        self.lineEdit_45.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_45.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_45.setObjectName("lineEdit_45")
        self.M_s_M_f.addWidget(self.lineEdit_45)
        # spacerItem70 = QtWidgets.QSpacerItem(60, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)

        # spacerItem71 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.M_s_M_f.addItem(spacerItem)
        self.lineEdit_45.setEnabled(False)
        self.checkBox_15.toggled.connect(self.lineEdit_45.setEnabled)
        self.checkBox_15.toggled.connect(self.lineEdit_43.setDisabled)
        self.checkBox_15.toggled.connect(self.lineEdit_44.setDisabled)
        #%% A_f - A_s
        self.A_f_A_s = QtWidgets.QHBoxLayout()
        self.A_f_A_s.setObjectName("A_f - A_s")
        # self.label_26 = QtWidgets.QLabel(self.centralwidget)
        self.label_26 = textToLatex("$A_{f} - A_{s}$ [$\mathrm{K}$]:", parameter_label_width, parameter_label_height, self.centralwidget)
        self.A_f_A_s.addWidget(self.label_26)
        self.A_f_A_s.addItem(spacerItem_2)
        self.lineEdit_46 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_46.sizePolicy().hasHeightForWidth())
        self.lineEdit_46.setSizePolicy(sizePolicy)
        self.lineEdit_46.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_46.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_46.setObjectName("lineEdit_46")
        self.A_f_A_s.addWidget(self.lineEdit_46)
        self.A_f_A_s.addItem(spacerItem)

        self.lineEdit_47 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_47.setSizePolicy(sizePolicy)
        self.lineEdit_47.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_47.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_47.setObjectName("lineEdit_47")
        self.A_f_A_s.addWidget(self.lineEdit_47)
        # spacerItem73 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.A_f_A_s.addItem(spacerItem)
        self.lineEdit_48 = QtWidgets.QLineEdit(self.centralwidget)
        self.checkBox_16 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_16.stateChanged.connect(self.uncheck)
        self.checkBox_16.setText("")
        self.checkBox_16.setObjectName("checkBox_16")
        self.A_f_A_s.addWidget(self.checkBox_16)
        self.A_f_A_s.addItem(spacerItem)
        
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_48.sizePolicy().hasHeightForWidth())
        self.lineEdit_48.setSizePolicy(sizePolicy)
        self.lineEdit_48.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_48.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_48.setObjectName("lineEdit_48")
        self.A_f_A_s.addWidget(self.lineEdit_48)
        self.A_f_A_s.addItem(spacerItem)

        self.lineEdit_48.setEnabled(False)
        self.checkBox_16.toggled.connect(self.lineEdit_48.setEnabled)
        self.checkBox_16.toggled.connect(self.lineEdit_46.setDisabled)
        self.checkBox_16.toggled.connect(self.lineEdit_47.setDisabled)
        #%% C_A
        self.C_A = QtWidgets.QHBoxLayout()
        self.C_A.setObjectName("C_A")
        # self.label_27 = QtWidgets.QLabel(self.centralwidget)
        self.label_27 = textToLatex(r"$C_{A}$ [$\frac{\mathrm{Pa}}{\mathrm{K}}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.C_A.addWidget(self.label_27)
        self.C_A.addItem(spacerItem_2)
        self.lineEdit_49 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_49.sizePolicy().hasHeightForWidth())
        self.lineEdit_49.setSizePolicy(sizePolicy)
        self.lineEdit_49.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_49.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_49.setObjectName("lineEdit_49")
        self.C_A.addWidget(self.lineEdit_49)
        self.C_A.addItem(spacerItem)

        self.lineEdit_50 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_50.setSizePolicy(sizePolicy)
        self.lineEdit_50.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_50.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_50.setObjectName("lineEdit_50")
        self.C_A.addWidget(self.lineEdit_50)
        self.C_A.addItem(spacerItem)
        # spacerItem25 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.checkBox_17 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_17.stateChanged.connect(self.uncheck)
        self.checkBox_17.setText("")
        self.checkBox_17.setObjectName("checkBox_17")
        self.C_A.addWidget(self.checkBox_17)
        
        self.C_A.addItem(spacerItem)
        self.lineEdit_51 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_51.sizePolicy().hasHeightForWidth())
        self.lineEdit_51.setSizePolicy(sizePolicy)
        self.lineEdit_51.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_51.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_51.setObjectName("lineEdit_51")
        self.C_A.addWidget(self.lineEdit_51)
        self.C_A.addItem(spacerItem)

        self.lineEdit_51.setEnabled(False)
        self.checkBox_17.toggled.connect(self.lineEdit_51.setEnabled)
        self.checkBox_17.toggled.connect(self.lineEdit_49.setDisabled)
        self.checkBox_17.toggled.connect(self.lineEdit_50.setDisabled)
        #%% C_M
        self.C_M = QtWidgets.QHBoxLayout()
        self.C_M.setObjectName("C_M")
        self.label_17 = QtWidgets.QLabel(self.centralwidget)
        self.label_17 = textToLatex(r"$C_{M}$ [$\frac{\mathrm{Pa}}{\mathrm{K}}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.C_M.addWidget(self.label_17)
        self.C_M.addItem(spacerItem_2)
        self.lineEdit_19 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_19.setSizePolicy(sizePolicy)
        self.lineEdit_19.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_19.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_19.setObjectName("lineEdit_19")
        self.C_M.addWidget(self.lineEdit_19)
        self.C_M.addItem(spacerItem)

        self.lineEdit_20 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_20.setSizePolicy(sizePolicy)
        self.lineEdit_20.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_20.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_20.setObjectName("lineEdit_20")
        self.C_M.addWidget(self.lineEdit_20)
        # spacerItem45 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.C_M.addItem(spacerItem)
        self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.stateChanged.connect(self.uncheck)
        self.checkBox_7.setText("")
        self.checkBox_7.setObjectName("checkBox_7")
        self.C_M.addWidget(self.checkBox_7)
        self.C_M.addItem(spacerItem)
        self.lineEdit_21 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_21.setSizePolicy(sizePolicy)
        self.lineEdit_21.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_21.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_21.setObjectName("lineEdit_21")
        self.C_M.addWidget(self.lineEdit_21)
        self.C_M.addItem(spacerItem)

        self.lineEdit_21.setEnabled(False)
        self.checkBox_7.toggled.connect(self.lineEdit_21.setEnabled)
        self.checkBox_7.toggled.connect(self.lineEdit_19.setDisabled)
        self.checkBox_7.toggled.connect(self.lineEdit_20.setDisabled)
        
        # Transformation strain properties
        #%% H_min
        self.H_min = QtWidgets.QHBoxLayout()
        self.H_min.setObjectName("H_min")
        # self.label_18 = QtWidgets.QLabel(self.centralwidget)
        self.label_18 = textToLatex(r"$H_{min}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.H_min.addWidget(self.label_18)
        self.H_min.addItem(spacerItem_2)
        self.lineEdit_22 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_22.sizePolicy().hasHeightForWidth())
        self.lineEdit_22.setSizePolicy(sizePolicy)
        self.lineEdit_22.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_22.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_22.setObjectName("lineEdit_22")
        self.H_min.addWidget(self.lineEdit_22)
        self.H_min.addItem(spacerItem)

        self.lineEdit_23 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_23.setSizePolicy(sizePolicy)
        self.lineEdit_23.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_23.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.H_min.addWidget(self.lineEdit_23)
        self.H_min.addItem(spacerItem)
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.stateChanged.connect(self.uncheck)
        self.checkBox_8.setText("")
        self.checkBox_8.setObjectName("checkBox_8")
        self.H_min.addWidget(self.checkBox_8)
        # spacerItem41 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.H_min.addItem(spacerItem)
        self.lineEdit_24 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_24.setSizePolicy(sizePolicy)
        self.lineEdit_24.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_24.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.H_min.addWidget(self.lineEdit_24)

        self.H_min.addItem(spacerItem)
        self.lineEdit_24.setEnabled(False)
        self.checkBox_8.toggled.connect(self.lineEdit_24.setEnabled)
        self.checkBox_8.toggled.connect(self.lineEdit_22.setDisabled)
        self.checkBox_8.toggled.connect(self.lineEdit_23.setDisabled)
        #%% H_max - H_min
        self.H_max_H_min = QtWidgets.QHBoxLayout()
        self.H_max_H_min.setObjectName("H_max - H_min")
        # self.label_28 = QtWidgets.QLabel(self.centralwidget)
        self.label_28 = textToLatex(r"$H_{max} - H_{min}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.H_max_H_min.addWidget(self.label_28)
        spacerItem_90 = QtWidgets.QSpacerItem(5, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.H_max_H_min.addItem(spacerItem_90)
        self.lineEdit_52 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_52.sizePolicy().hasHeightForWidth())
        self.lineEdit_52.setSizePolicy(sizePolicy)
        self.lineEdit_52.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_52.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_52.setObjectName("lineEdit_52")
        self.H_max_H_min.addWidget(self.lineEdit_52)
        self.H_max_H_min.addItem(spacerItem)

        self.lineEdit_53 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_53.setSizePolicy(sizePolicy)
        self.lineEdit_53.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_53.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_53.setObjectName("lineEdit_53")
        self.H_max_H_min.addWidget(self.lineEdit_53)
        # spacerItem1 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.H_max_H_min.addItem(spacerItem)
        self.checkBox_18 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_18.stateChanged.connect(self.uncheck)
        self.checkBox_18.setText("")
        self.checkBox_18.setObjectName("checkBox_18")
        self.H_max_H_min.addWidget(self.checkBox_18)
        self.H_max_H_min.addItem(spacerItem)
        self.lineEdit_54 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_54.setSizePolicy(sizePolicy)
        self.lineEdit_54.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_54.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_54.setObjectName("lineEdit_54")
        self.H_max_H_min.addWidget(self.lineEdit_54)
        self.H_max_H_min.addItem(spacerItem)

        self.lineEdit_54.setEnabled(False)
        self.checkBox_18.toggled.connect(self.lineEdit_54.setEnabled)
        self.checkBox_18.toggled.connect(self.lineEdit_52.setDisabled)
        self.checkBox_18.toggled.connect(self.lineEdit_53.setDisabled)
        #self.chBoxPrjManager.toggled.connect(self.projManagerLineEdit.setEnabled)
        #%% sigma_0
        self.sigma_0 = QtWidgets.QHBoxLayout()
        self.sigma_0.setObjectName("sigma_0")
        # self.label_31 = QtWidgets.QLabel
        self.label_31 = textToLatex(r"$\sigma_{0}$ [$\mathrm{Pa}$]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.sigma_0.addWidget(self.label_31)
        self.sigma_0.addItem(spacerItem_2)
        self.lineEdit_61 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_61.sizePolicy().hasHeightForWidth())
        self.lineEdit_61.setSizePolicy(sizePolicy)
        self.lineEdit_61.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_61.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_61.setObjectName("lineEdit_61")
        self.sigma_0.addWidget(self.lineEdit_61)
        self.sigma_0.addItem(spacerItem)

        self.lineEdit_62 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_62.setSizePolicy(sizePolicy)
        self.lineEdit_62.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_62.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_62.setObjectName("lineEdit_62")
        self.sigma_0.addWidget(self.lineEdit_62)
        self.sigma_0.addItem(spacerItem)
        self.lineEdit_63 = QtWidgets.QLineEdit(self.centralwidget)
        self.checkBox_21 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_21.stateChanged.connect(self.uncheck)
        self.checkBox_21.setText("")
        self.checkBox_21.setObjectName("checkBox_21")
        self.sigma_0.addWidget(self.checkBox_21)
        self.sigma_0.addItem(spacerItem)
        
        self.lineEdit_63.setSizePolicy(sizePolicy)
        self.lineEdit_63.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_63.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_63.setObjectName("lineEdit_63")
        self.sigma_0.addWidget(self.lineEdit_63)
        self.sigma_0.addItem(spacerItem)

        self.lineEdit_63.setEnabled(False)
        self.checkBox_21.toggled.connect(self.lineEdit_63.setEnabled)
        self.checkBox_21.toggled.connect(self.lineEdit_61.setDisabled)
        self.checkBox_21.toggled.connect(self.lineEdit_62.setDisabled)        
        
        
        #%% k
        self.k = QtWidgets.QHBoxLayout()
        self.k.setObjectName("k")
        # self.label_19 = QtWidgets.QLabel(self.centralwidget)
        self.label_19 = textToLatex(r"$k~[\frac{1}{\mathrm{Pa}}]$:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.k.addWidget(self.label_19)
        self.k.addItem(spacerItem_2)
        self.lineEdit_25 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_25.sizePolicy().hasHeightForWidth())
        self.lineEdit_25.setSizePolicy(sizePolicy)
        self.lineEdit_25.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_25.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.k.addWidget(self.lineEdit_25)
        self.k.addItem(spacerItem)

        self.lineEdit_26 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_26.setSizePolicy(sizePolicy)
        self.lineEdit_26.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_26.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.k.addWidget(self.lineEdit_26)
        self.k.addItem(spacerItem)
        self.lineEdit_27 = QtWidgets.QLineEdit(self.centralwidget)
        self.checkBox_9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_9.stateChanged.connect(self.uncheck)
        self.checkBox_9.setText("")
        self.checkBox_9.setObjectName("checkBox_9")
        self.k.addWidget(self.checkBox_9)
        self.k.addItem(spacerItem)

        self.lineEdit_27.setSizePolicy(sizePolicy)
        self.lineEdit_27.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_27.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.k.addWidget(self.lineEdit_27)
        self.k.addItem(spacerItem)

        self.lineEdit_27.setEnabled(False)
        self.checkBox_9.toggled.connect(self.lineEdit_27.setEnabled)
        self.checkBox_9.toggled.connect(self.lineEdit_25.setDisabled)
        self.checkBox_9.toggled.connect(self.lineEdit_26.setDisabled)
        
        # Other properties 
        #%% n_1
        self.n_1 = QtWidgets.QHBoxLayout()
        self.n_1.setObjectName("n_1")
        # self.label_29 = QtWidgets.QLabel(self.centralwidget)
        self.label_29 = textToLatex(r"$n_{1}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.n_1.addWidget(self.label_29)
        self.n_1.addItem(spacerItem_2)
        self.lineEdit_55 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_55.sizePolicy().hasHeightForWidth())
        self.lineEdit_55.setSizePolicy(sizePolicy)
        self.lineEdit_55.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_55.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_55.setObjectName("lineEdit_55")
        self.n_1.addWidget(self.lineEdit_55)
        self.n_1.addItem(spacerItem)

        self.lineEdit_56 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_56.setSizePolicy(sizePolicy)
        self.lineEdit_56.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_56.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_56.setObjectName("lineEdit_56")
        self.n_1.addWidget(self.lineEdit_56)
        self.n_1.addItem(spacerItem)
        self.lineEdit_57 = QtWidgets.QLineEdit(self.centralwidget)
        # self.n_1.addItem(spacerItem)
        self.checkBox_19 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_19.stateChanged.connect(self.uncheck)
        self.checkBox_19.setText("")
        self.checkBox_19.setObjectName("checkBox_19")
        self.n_1.addWidget(self.checkBox_19)

        self.lineEdit_57.setSizePolicy(sizePolicy)
        self.lineEdit_57.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_57.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_57.setObjectName("lineEdit_57")
        self.n_1.addWidget(self.lineEdit_57)

        self.lineEdit_57.setEnabled(False)
        self.checkBox_19.toggled.connect(self.lineEdit_57.setEnabled)
        self.checkBox_19.toggled.connect(self.lineEdit_55.setDisabled)
        self.checkBox_19.toggled.connect(self.lineEdit_56.setDisabled)
        self.n_1.addItem(spacerItem)
        #%% n_2
        self.n_2 = QtWidgets.QHBoxLayout()
        self.n_2.setObjectName("n_2")
        # self.label_20 = QtWidgets.QLabel(self.centralwidget)
        self.label_20 = textToLatex(r"$n_{2}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.n_2.addWidget(self.label_20)
        self.n_2.addItem(spacerItem_2)
        self.lineEdit_28 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_28.sizePolicy().hasHeightForWidth())
        self.lineEdit_28.setSizePolicy(sizePolicy)
        self.lineEdit_28.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_28.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.n_2.addWidget(self.lineEdit_28)
        self.n_2.addItem(spacerItem)

        self.lineEdit_29 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_29.setSizePolicy(sizePolicy)
        self.lineEdit_29.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_29.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_29.setObjectName("lineEdit_29")
        self.n_2.addWidget(self.lineEdit_29)
        self.n_2.addItem(spacerItem)
        self.checkBox_10 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_10.stateChanged.connect(self.uncheck)
        self.checkBox_10.setText("")
        self.checkBox_10.setObjectName("checkBox_10")
        self.n_2.addWidget(self.checkBox_10)
        self.n_2.addItem(spacerItem)
        self.lineEdit_30 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_30.setSizePolicy(sizePolicy)
        self.lineEdit_30.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_30.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_30.setObjectName("lineEdit_30")
        self.n_2.addWidget(self.lineEdit_30)
        self.n_2.addItem(spacerItem)
        self.lineEdit_30.setEnabled(False)
        self.checkBox_10.toggled.connect(self.lineEdit_30.setEnabled)
        self.checkBox_10.toggled.connect(self.lineEdit_28.setDisabled)
        self.checkBox_10.toggled.connect(self.lineEdit_29.setDisabled)
        
        #%% n_3 
        self.n_3 = QtWidgets.QHBoxLayout()
        self.n_3.setObjectName("n_3")
        # self.label_30 = QtWidgets.QLabel(self.centralwidget)
        self.label_30 = textToLatex(r"$n_{3}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.n_3.addWidget(self.label_30)
        self.n_3.addItem(spacerItem_2)
        self.lineEdit_58 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_58.sizePolicy().hasHeightForWidth())
        self.lineEdit_58.setSizePolicy(sizePolicy)
        self.lineEdit_58.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_58.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_58.setObjectName("lineEdit_58")
        self.n_3.addWidget(self.lineEdit_58)
        self.n_3.addItem(spacerItem)

        self.lineEdit_59 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_59.setSizePolicy(sizePolicy)
        self.lineEdit_59.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_59.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_59.setObjectName("lineEdit_59")
        self.n_3.addWidget(self.lineEdit_59)
        self.n_3.addItem(spacerItem)
        self.checkBox_20 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_20.stateChanged.connect(self.uncheck)
        self.checkBox_20.setText("")
        self.checkBox_20.setObjectName("checkBox_20")
        self.n_3.addWidget(self.checkBox_20)
        # self.n_3.addItem(spacerItem)
        self.lineEdit_60 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_60.setSizePolicy(sizePolicy)
        self.lineEdit_60.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_60.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_60.setObjectName("lineEdit_60")
        self.n_3.addWidget(self.lineEdit_60)
        self.n_3.addItem(spacerItem)
        self.lineEdit_60.setEnabled(False)
        self.checkBox_20.toggled.connect(self.lineEdit_60.setEnabled)
        self.checkBox_20.toggled.connect(self.lineEdit_58.setDisabled)
        self.checkBox_20.toggled.connect(self.lineEdit_59.setDisabled)
        
        #%% n_4
        self.n_4 = QtWidgets.QHBoxLayout()
        self.n_4.setObjectName("n_4")
        # self.label_21 = QtWidgets.QLabel(self.centralwidget)
        self.label_21 = textToLatex(r"$n_{4}$ [-]:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.n_4.addWidget(self.label_21)
        self.n_4.addItem(spacerItem_2)
        self.lineEdit_31 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_31.sizePolicy().hasHeightForWidth())
        self.lineEdit_31.setSizePolicy(sizePolicy)
        self.lineEdit_31.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_31.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_31.setObjectName("lineEdit_31")
        self.n_4.addWidget(self.lineEdit_31)
        self.n_4.addItem(spacerItem)

        self.lineEdit_32 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_32.setSizePolicy(sizePolicy)
        self.lineEdit_32.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_32.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_32.setObjectName("lineEdit_32")
        self.n_4.addWidget(self.lineEdit_32)
        self.n_4.addItem(spacerItem)
        self.checkBox_11 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_11.stateChanged.connect(self.uncheck)
        self.checkBox_11.setText("")
        self.checkBox_11.setObjectName("checkBox_11")
        self.n_4.addWidget(self.checkBox_11)
        self.n_4.addItem(spacerItem)
        self.lineEdit_33 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_33.setSizePolicy(sizePolicy)
        self.lineEdit_33.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_33.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_33.setObjectName("lineEdit_33")
        self.n_4.addWidget(self.lineEdit_33)
        self.n_4.addItem(spacerItem)        
        self.lineEdit_33.setEnabled(False)
        self.checkBox_11.toggled.connect(self.lineEdit_33.setEnabled)
        self.checkBox_11.toggled.connect(self.lineEdit_31.setDisabled)
        self.checkBox_11.toggled.connect(self.lineEdit_32.setDisabled)
        #%% alpha
        self.alpha = QtWidgets.QHBoxLayout()
        self.alpha.setObjectName("alpha")
        # self.label_22 = QtWidgets.QLabel(self.centralwidget)
        self.label_22 = textToLatex(r"$\alpha~[\frac{1}{\mathrm{m}}]$:", parameter_label_width, parameter_label_height, self.centralwidget)

        self.alpha.addWidget(self.label_22)
        self.alpha.addItem(spacerItem_2)
        self.lineEdit_34 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_34.sizePolicy().hasHeightForWidth())
        self.lineEdit_34.setSizePolicy(sizePolicy)
        self.lineEdit_34.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_34.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_34.setObjectName("lineEdit_34")
        self.alpha.addWidget(self.lineEdit_34)
        self.alpha.addItem(spacerItem)

        self.lineEdit_35 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_35.setSizePolicy(sizePolicy)
        self.lineEdit_35.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_35.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_35.setObjectName("lineEdit_35")
        self.alpha.addWidget(self.lineEdit_35)
        self.alpha.addItem(spacerItem)
        self.checkBox_12 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_12.stateChanged.connect(self.uncheck)
        self.checkBox_12.setText("")
        self.checkBox_12.setObjectName("checkBox_12")
        self.alpha.addWidget(self.checkBox_12)
        self.alpha.addItem(spacerItem)
        self.lineEdit_36 = QtWidgets.QLineEdit(self.centralwidget)

        self.lineEdit_36.setSizePolicy(sizePolicy)
        self.lineEdit_36.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_36.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_36.setObjectName("lineEdit_36")
        self.alpha.addWidget(self.lineEdit_36)
        self.alpha.addItem(spacerItem)
        self.lineEdit_36.setEnabled(False)
        self.checkBox_12.toggled.connect(self.lineEdit_36.setEnabled)
        self.checkBox_12.toggled.connect(self.lineEdit_34.setDisabled)
        self.checkBox_12.toggled.connect(self.lineEdit_35.setDisabled)
        #%% Left labels 
        self.left_labels = QtWidgets.QHBoxLayout()
        self.left_labels.setContentsMargins(0, -1, 5, -1)
        self.left_labels.setObjectName("left_labels")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setMinimumSize(QtCore.QSize(parameter_label_width, parameter_label_height))
        self.label_2.setMaximumSize(QtCore.QSize(parameter_label_width, parameter_label_height))
        self.label_2.setText('Parameter')
        
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.left_labels.addWidget(self.label_2)
        self.left_labels.addItem(spacerItem_2)
        self.label = QtWidgets.QLabel(self.centralwidget)

        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label.setText('Lower Bound')
        self.left_labels.addWidget(self.label)
        self.left_labels.addItem(spacerItem)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)

        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label_3.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.label_3.setText('Upper Bound')
        self.left_labels.addWidget(self.label_3)
        
        self.left_labels.addItem(spacerItem)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)

        self.label_5.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_5.setText('Specify?')
        self.left_labels.addWidget(self.label_5)
        self.left_labels.addItem(spacerItem)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)

        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label_4.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_4.setWordWrap(True)
        self.label_4.setText("Value")
        
        self.left_labels.addWidget(self.label_4)

        #%% Right labels
        self.right_labels = QtWidgets.QHBoxLayout()
        self.right_labels.setContentsMargins(0, -1, 5, -1)
        self.right_labels.setObjectName("right_labels")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setMinimumSize(QtCore.QSize(parameter_label_width, parameter_label_height))
        self.label_7.setMaximumSize(QtCore.QSize(parameter_label_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_7.setText('Parameter')
        self.right_labels.addWidget(self.label_7)
        self.right_labels.addItem(spacerItem_2)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)

        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label_8.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.label_8.setText('Lower Bound')
        self.right_labels.addWidget(self.label_8)
        self.right_labels.addItem(spacerItem)
        self.label_9 = QtWidgets.QLabel(self.centralwidget)

        self.label_9.setSizePolicy(sizePolicy)
        self.label_9.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label_9.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.label_9.setText('Upper Bound')
        self.right_labels.addWidget(self.label_9)
        self.right_labels.addItem(spacerItem)
        self.label_11 = QtWidgets.QLabel(self.centralwidget)

        self.label_11.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_11.setText('Specify?')
        self.right_labels.addWidget(self.label_11)
        self.right_labels.addItem(spacerItem)
        self.label_10 = QtWidgets.QLabel(self.centralwidget)

        self.label_10.setSizePolicy(sizePolicy)
        self.label_10.setMinimumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        self.label_10.setMaximumSize(QtCore.QSize(lineEdit_width, parameter_label_height))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_10.setWordWrap(True)
        self.label_10.setText('Value')
        self.right_labels.addWidget(self.label_10)

        
        #%% Pushbuttons 
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton_3.setSizePolicy(sizePolicy)
        self.pushButton_3.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_3.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setText('Import')
        
        self.buttons.addWidget(self.pushButton_3)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton_2.setSizePolicy(sizePolicy)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setText('Guess')
        
        self.buttons.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)

        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 30))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('Calibrate')
        self.buttons.addWidget(self.pushButton)
        self.defaults_button = QtWidgets.QPushButton(self.centralwidget)

        self.defaults_button.setSizePolicy(sizePolicy)
        self.defaults_button.setMinimumSize(QtCore.QSize(100, 30))
        self.defaults_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.defaults_button.setObjectName("defaults_button")
        self.defaults_button.setText('Defaults')
        self.buttons.addWidget(self.defaults_button)
        #%% Design variable flags
        self.prop_constraints_label = QtWidgets.QHBoxLayout()
        self.prop_constraints_label.setContentsMargins(-1, -1, 5, -1)
        self.prop_constraints_label.setObjectName("prop_params_label")
        
        # Header
        self.prop_constraints_header = QtWidgets.QLabel(self.centralwidget)
        self.prop_constraints_header.setText('Material property constraints')
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.opt_param_header.sizePolicy().hasHeightForWidth())
        # self.opt_param_header.setSizePolicy(sizePolicy)
        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.prop_constraints_header.setFont(font)
        self.prop_constraints_header.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.prop_constraints_header.setObjectName("prop_constraints_header")
        self.prop_constraints_label.addStretch()
        self.prop_constraints_label.addWidget(self.prop_constraints_header)
        self.prop_constraints_label.addStretch()
        
        #Modulus Flag
        
        self.modulus_flag = QtWidgets.QHBoxLayout()
        self.modulus_flag.setContentsMargins(-1, -1, 5, -1)
        self.modulus_flag.setObjectName("modulus_flag")
        
        # self.prop_constraints = QtWidgets.QHBoxLayout()
        # self.prop_constraints.setContentsMargins(-1, -1, 5, -1)
        # self.prop_constraints.setObjectName("prop_constraints")
        # self.modulus_label = QtWidgets.QLabel(self.centralwidget)
        self.modulus_label = textToLatex(r"$E_A = E_M$", 90, 43, self.centralwidget)

        self.modulus_label.setSizePolicy(sizePolicy)
        self.modulus_label.setMinimumSize(QtCore.QSize(90, 0))
        self.modulus_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.modulus_label.setFont(font)
        self.modulus_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.modulus_label.setObjectName("modulus_label")
        self.modulus_flag.addWidget(self.modulus_label)
        
        
        self.checkBox_modulus_flag = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_modulus_flag.stateChanged.connect(self.uncheck)
        self.checkBox_modulus_flag.setText("")
        self.checkBox_modulus_flag.setObjectName("checkBox_modulus_flag")
        self.modulus_flag.addWidget(self.checkBox_modulus_flag)
        
        #spacerItem77 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.prop_constraints.addItem(spacerItem77)
        
        # Slope flag
        
        self.slope_flag = QtWidgets.QHBoxLayout()
        self.slope_flag.setContentsMargins(-1, -1, 5, -1)
        self.slope_flag.setObjectName("slope_flag")
        
        # self.slope_label = QtWidgets.QLabel(self.centralwidget)
        self.slope_label = textToLatex(r"$C_A = C_M$", 90, 43, self.centralwidget)

        self.slope_label.setSizePolicy(sizePolicy)
        self.slope_label.setMinimumSize(QtCore.QSize(90, 0))
        self.slope_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.slope_label.setFont(font)
        self.slope_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.slope_label.setObjectName("slope_label")
        self.slope_flag.addWidget(self.slope_label)
        
        
        self.checkBox_slope_flag = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_slope_flag.stateChanged.connect(self.uncheck)
        self.checkBox_slope_flag.setText("")
        self.checkBox_slope_flag.setObjectName("checkBox_slope_flag")
        self.slope_flag.addWidget(self.checkBox_slope_flag)
        
        
        #spacerItem76 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.prop_constraints.addItem(spacerItem76)
        # self.smooth_hardening_label = QtWidgets.QLabel(self.centralwidget)
        
        
        self.smooth_hardening_flag = QtWidgets.QHBoxLayout()
        self.smooth_hardening_flag.setContentsMargins(-1, -1, 5, -1)
        self.smooth_hardening_flag.setObjectName("smooth_hardening_flag")
        
        # Smooth hardening flag
        self.smooth_hardening_label = textToLatex(r"$n_1=n_2=n_3=n_4$", 200, 43, self.centralwidget)
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.smooth_hardening_label.sizePolicy().hasHeightForWidth())
        # self.smooth_hardening_label.setSizePolicy(sizePolicy)
        # self.smooth_hardening_label.setMinimumSize(QtCore.QSize(90, 0))
        # self.smooth_hardening_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.smooth_hardening_label.setFont(font)
        self.smooth_hardening_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.smooth_hardening_label.setObjectName("smooth_hardening_label")
        self.smooth_hardening_flag.addWidget(self.smooth_hardening_label)
        
        
        self.checkBox_smooth_hardening_flag = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_smooth_hardening_flag.stateChanged.connect(self.uncheck)
        self.checkBox_smooth_hardening_flag.setText("")
        self.checkBox_smooth_hardening_flag.setObjectName("checkBox_smooth_hardening_flag")
        self.smooth_hardening_flag.addWidget(self.checkBox_smooth_hardening_flag)
        
        

        #%% Algorithmic parameters
        
        self.alg_params_label = QtWidgets.QHBoxLayout()
        self.alg_params_label.setContentsMargins(-1, -1, 5, -1)
        self.alg_params_label.setObjectName("alg_params_label")
        # self.gen_label = 
        
        # Header
        self.alg_param_header = QtWidgets.QLabel(self.centralwidget)
        self.alg_param_header.setText('Algorithmic Parameters')
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.opt_param_header.sizePolicy().hasHeightForWidth())
        # self.opt_param_header.setSizePolicy(sizePolicy)
        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.alg_param_header.setFont(font)
        self.alg_param_header.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.alg_param_header.setObjectName("opt_param_header")
        self.alg_params_label.addStretch()
        self.alg_params_label.addWidget(self.alg_param_header)
        self.alg_params_label.addStretch()
        
        self.non_op_params = QtWidgets.QHBoxLayout()
        self.non_op_params.setContentsMargins(-1, -1, 5, -1)
        self.non_op_params.setObjectName("non_op_params")
        
        
        # delta
        self.delta = QtWidgets.QHBoxLayout()
        self.delta.setContentsMargins(-1, -1, 5, -1)
        self.delta.setObjectName("delta")
        
        
        # self.label_34 = QtWidgets.QLabel(self.centralwidget)
        self.label_34 = textToLatex("$\delta$:", 90, 43, self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_34.sizePolicy().hasHeightForWidth())
        self.label_34.setSizePolicy(sizePolicy)
        self.label_34.setMinimumSize(QtCore.QSize(90, 0))
        self.label_34.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_34.setFont(font)
        self.label_34.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_34.setObjectName("label_34")
        self.delta.addWidget(self.label_34)
        self.lineEdit_64 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_64.sizePolicy().hasHeightForWidth())
        self.lineEdit_64.setSizePolicy(sizePolicy)
        self.lineEdit_64.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_64.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_64.setObjectName("lineEdit_64")
        self.delta.addWidget(self.lineEdit_64)
        
        
        #spacerItem76 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.non_op_params.addItem(spacerItem76)
        
        
        self.sigma_cal = QtWidgets.QHBoxLayout()
        self.sigma_cal.setContentsMargins(-1, -1, 5, -1)
        self.sigma_cal.setObjectName("sigma_cal")
        
        
        # self.label_33 = QtWidgets.QLabel(self.centralwidget)
        self.label_33 = textToLatex("$\sigma_{cal}:$", 90, 43, self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_33.sizePolicy().hasHeightForWidth())
        self.label_33.setSizePolicy(sizePolicy)
        self.label_33.setMinimumSize(QtCore.QSize(90, 0))
        self.label_33.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_33.setFont(font)
        self.label_33.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_33.setObjectName("label_33")
        self.sigma_cal.addWidget(self.label_33)
        self.lineEdit_65 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_65.sizePolicy().hasHeightForWidth())
        self.lineEdit_65.setSizePolicy(sizePolicy)
        self.lineEdit_65.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_65.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_65.setObjectName("lineEdit_65")
        self.sigma_cal.addWidget(self.lineEdit_65)
        
        
        # spacerItem77 = QtWidgets.QSpacerItem(spacer_item_width, spacer_item_height, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        # self.non_op_params.addItem(spacerItem77)
        
        #MVF_tolerance
        
        
        self.MVF_tol = QtWidgets.QHBoxLayout()
        self.MVF_tol.setContentsMargins(-1, -1, 5, -1)
        self.MVF_tol.setObjectName("MVF_tol")
        
        # self.label_32 = QtWidgets.QLabel(self.centralwidget)
        self.label_32 = textToLatex(r"$MVF_{tol}:$", 90, 43, self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_32.sizePolicy().hasHeightForWidth())
        self.label_32.setSizePolicy(sizePolicy)
        self.label_32.setMinimumSize(QtCore.QSize(90, 0))
        self.label_32.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_32.setFont(font)
        self.label_32.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_32.setObjectName("label_32")
        self.MVF_tol.addWidget(self.label_32)
        self.lineEdit_66 = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_66.sizePolicy().hasHeightForWidth())
        self.lineEdit_66.setSizePolicy(sizePolicy)
        self.lineEdit_66.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_66.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.lineEdit_66.setObjectName("lineEdit_66")
        self.MVF_tol.addWidget(self.lineEdit_66)
        MainWindow.setCentralWidget(self.centralwidget)
        
        #%%Optimization parameters
        #Might need to make this a grid with labels on the left and line edits on the right
        
        self.op_params_label = QtWidgets.QHBoxLayout()
        self.op_params_label.setContentsMargins(-1, -1, 5, -1)
        self.op_params_label.setObjectName("op_params")
        # self.gen_label = 
        
        # Header
        self.opt_param_header = QtWidgets.QLabel(self.centralwidget)
        self.opt_param_header.setText('Optimization Parameters')
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.opt_param_header.sizePolicy().hasHeightForWidth())
        # self.opt_param_header.setSizePolicy(sizePolicy)
        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(header_font)
        font.setBold(True)
        font.setWeight(header_weight)
        self.opt_param_header.setFont(font)
        self.opt_param_header.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.opt_param_header.setObjectName("opt_param_header")
        self.op_params_label.addStretch()
        self.op_params_label.addWidget(self.opt_param_header)
        self.op_params_label.addStretch()
        
        # Number of generations
        self.num_gens = QtWidgets.QHBoxLayout()
        self.num_gens.setContentsMargins(-1, -1, 5, -1)
        self.num_gens.setObjectName("num_gens")
        
        
        self.gen_label = QtWidgets.QLabel(self.centralwidget)
        self.gen_label.setText('Number of generations')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        #sizePolicy.setHorizontalStretch(0)
        
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gen_label.sizePolicy().hasHeightForWidth())
        self.gen_label.setSizePolicy(sizePolicy)
        #self.gen_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.gen_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(normal_font)
        font.setBold(False)
        font.setWeight(normal_weight)
        self.gen_label.setFont(font)
        self.gen_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.gen_label.setObjectName("gen_label")
        self.num_gens.addWidget(self.gen_label)
        self.num_gens.addStretch()
        self.gen_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gen_line.sizePolicy().hasHeightForWidth())
        self.gen_line.setSizePolicy(sizePolicy)
        self.gen_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.gen_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.gen_line.setObjectName("gen_line")
        self.num_gens.addWidget(self.gen_line)
        
        self.pop_size = QtWidgets.QHBoxLayout()
        self.pop_size.setContentsMargins(-1, -1, 5, -1)
        self.pop_size.setObjectName("pop_size")
        
        self.pop_label = QtWidgets.QLabel(self.centralwidget)
        self.pop_label.setText('Population size')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pop_label.sizePolicy().hasHeightForWidth())
        self.pop_label.setSizePolicy(sizePolicy)
        #self.pop_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.pop_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(normal_font)
        font.setBold(False)
        font.setWeight(normal_weight)
        self.pop_label.setFont(font)
        self.pop_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing)
        self.pop_label.setObjectName("pop_label")
        self.pop_size.addWidget(self.pop_label)
        self.pop_size.addStretch()
        self.pop_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pop_line.sizePolicy().hasHeightForWidth())
        self.pop_line.setSizePolicy(sizePolicy)
        self.pop_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.pop_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.pop_line.setObjectName("pop_line")

        self.pop_size.addWidget(self.pop_line)
        
        self.num_iters = QtWidgets.QHBoxLayout()
        self.num_iters.setContentsMargins(-1, -1, 5, -1)
        self.num_iters.setObjectName("num_iters")
        
        self.iter_label = QtWidgets.QLabel(self.centralwidget)
        self.iter_label.setText('Gradient-based iterations')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iter_label.sizePolicy().hasHeightForWidth())
        self.iter_label.setSizePolicy(sizePolicy)
        #self.iter_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.iter_label.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(normal_font)
        font.setBold(False)
        font.setWeight(normal_weight)
        self.iter_label.setFont(font)
        self.iter_label.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.iter_label.setObjectName("iter_label")
        self.num_iters.addWidget(self.iter_label)
        self.num_iters.addStretch()
        self.iter_line = QtWidgets.QLineEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.iter_line.sizePolicy().hasHeightForWidth())
        self.iter_line.setSizePolicy(sizePolicy)
        self.iter_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.iter_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.iter_line.setObjectName("iter_line")

        self.num_iters.addWidget(self.iter_line)
        
        #%% Phase diagram and strain-temperature plots
        
        #app = QtGui.QApplication(sys.argv) 
        # self.phase_diagram = QtSvg.QSvgWidget('test_phase_diagram.svg')
        # self.phase_diagram.setGeometry(50,50,759,668)
    
        #svgWidget.show()
        
        
        
        self.strain_temp_label = QtWidgets.QVBoxLayout()
        
        self.strain_temp_text = QtWidgets.QLabel(self.centralwidget)
        self.strain_temp_text.setText('Example SMA response')
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pop_label.sizePolicy().hasHeightForWidth())
        self.strain_temp_text.setSizePolicy(sizePolicy)
        self.strain_temp_label.addWidget(self.strain_temp_text)
        
        self.figures = QtWidgets.QVBoxLayout()
        self.explanation = QtSvg.QSvgWidget('test_phase_diagram.svg')
        self.explanation.setGeometry(0, 0, int(rect.width() * 0.5), int(rect.height() * 0.5))
        self.phase_diagram = QtSvg.QSvgWidget('test_phase_diagram.svg')
        self.phase_diagram.setGeometry(0,0,int(rect.width()*0.5), int(rect.height()*0.5))
    
        
        #self.phase_diagram = QtWidgets.QLabel()
        #self.phase_diagram.setGeometry(50,200,500,500)
        #renderer =  QtSvg.QSvgRenderer('test_phase_diagram.svg')
        #self.phase_diagram.resize(renderer.defaultSize())
        # painter = QtGui.QPainter(self.phase_diagram)
        # painter.restore()
        # renderer.render(painter)
        self.figures.addWidget(self.explanation)
        self.figures.addWidget(self.phase_diagram)

        #%% file i/o
        # file i/o
        # self.file_io = QtWidgets.QGridLayout(self.centralwidget)
        # font = QtGui.QFont()
        # font.setPointSize(header_font)
        # font.setBold(True)
        # font.setWeight(header_weight)
        # file_io_title = QtWidgets.QLabel(self.centralwidget)
        # file_io_title.setText("File I/O")
        # file_io_title.setFont(font)
        # file_io_title.setAlignment(QtCore.Qt.AlignCenter)
        # file_select_label = QtWidgets.QLabel()
        # file_select_label.setText('Choose files to analyze:')
        # file_select_label.setFont(font)
        # self.file_button = QtWidgets.QPushButton(self.centralwidget)
        # self.file_button.setText('Open Files')
        # # self.file_button.setFont(font)
        # self.file_labels = QtWidgets.QLabel(self.centralwidget)
        # self.file_labels.setText('')
        # self.file_labels.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        # self.file_io.addWidget(file_io_title, 0, 0, 1, 2)
        # self.file_io.addWidget(file_select_label, 1, 0)
        # self.file_io.addWidget(self.file_button, 1, 1)
        # self.file_io.addWidget(self.file_labels, 2, 0, 1, 2)
        
        #%% Grid layout commands
        #Will need to figure out gridLayout at a later date. 
        #Elastic properties
        self.gridLayout.addLayout(self.E_M, 1, 0, 1, 1)
        self.gridLayout.addLayout(self.E_A, 1, 1, 1, 1)
        #Phase diagram properties
        self.gridLayout.addLayout(self.M_s, 2, 0, 1, 1)
        self.gridLayout.addLayout(self.M_s_M_f, 2, 1, 1, 1)
        self.gridLayout.addLayout(self.A_s, 3, 0, 1, 1)
        self.gridLayout.addLayout(self.A_f_A_s, 3, 1, 1, 1)
        self.gridLayout.addLayout(self.C_M, 4, 0, 1, 1)
        self.gridLayout.addLayout(self.C_A, 4, 1, 1, 1)
        #Transformation strain properties
        self.gridLayout.addLayout(self.H_min, 5, 0, 1, 1)
        self.gridLayout.addLayout(self.H_max_H_min, 5, 1, 1, 1)
        self.gridLayout.addLayout(self.sigma_0, 6, 0, 1, 1)
        self.gridLayout.addLayout(self.k, 6, 1, 1, 1)
        #Other properties 
        self.gridLayout.addLayout(self.n_1, 7, 0, 1, 1)
        self.gridLayout.addLayout(self.n_2, 7, 1, 1, 1)
        self.gridLayout.addLayout(self.n_3, 8, 0, 1, 1)
        self.gridLayout.addLayout(self.n_4, 8, 1, 1, 1)
        self.gridLayout.addLayout(self.alpha, 9, 0, 1, 1)
        
        self.gridLayout.addLayout(self.prop_constraints_label,10,0,1,1)
        self.gridLayout.addLayout(self.modulus_flag,11,0,1,1)
        self.gridLayout.addLayout(self.slope_flag,12,0,1,1)
        self.gridLayout.addLayout(self.smooth_hardening_flag,13,0,1,1)
        
        #Algorithmic parameters
        self.gridLayout.addLayout(self.alg_params_label,10,1,1,1)
        self.gridLayout.addLayout(self.delta,11,1,1,1)
        self.gridLayout.addLayout(self.sigma_cal,12,1,1,1)
        self.gridLayout.addLayout(self.MVF_tol,13,1,1,1)
        
        #self.gridLayout.addLayout(self.non_op_params, 11, 1, 1, 1)
        
        #Optimization parameters
        self.gridLayout.addLayout(self.op_params_label, 10, 2, 1, 1)
        self.gridLayout.addLayout(self.num_gens, 11, 2, 1, 1)
        self.gridLayout.addLayout(self.pop_size, 12, 2, 1, 1)
        self.gridLayout.addLayout(self.num_iters, 13, 2, 1, 1)
        
        #Example figures
        self.gridLayout.addLayout(self.strain_temp_label, 0, 2, 1, 1)
        self.gridLayout.addLayout(self.figures, 1, 2, 8, 2)

        # File I/O
        # self.gridLayout.addLayout(self.file_io, 9, 3, 1, 1)
        # self.gridLayout.addLayout(self.file_io, 9, 2, 4, 1)
        
        #Buttons and Labels

        self.gridLayout.addLayout(self.buttons, 18, 0, 1, 2)
        self.gridLayout.addLayout(self.right_labels, 0, 1, 1, 1)
        self.gridLayout.addLayout(self.left_labels, 0, 0, 1, 1)
        
        
        #%% Alignment commands need to be after the grid layout
        
        
        
        self.prop_constraints_label.setAlignment(QtCore.Qt.AlignRight)
        self.modulus_flag.setAlignment(QtCore.Qt.AlignRight)
        self.slope_flag.setAlignment(QtCore.Qt.AlignRight)
        self.smooth_hardening_flag.setAlignment(QtCore.Qt.AlignRight)
        
        
        self.pop_line.setAlignment(QtCore.Qt.AlignRight)
        self.iter_line.setAlignment(QtCore.Qt.AlignRight)

        
        self.num_gens.setAlignment(QtCore.Qt.AlignLeft)
        self.pop_size.setAlignment(QtCore.Qt.AlignLeft)
        self.num_iters.setAlignment(QtCore.Qt.AlignLeft)

        #%% Signals and connections
        self.retranslateUi(MainWindow)
        # INITIAL CONDITIONS
        self.loadDefaults()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # SIGNALS
        self.pushButton_3.clicked.connect(self.importVals)
        self.pushButton_2.clicked.connect(self.guess)
        self.pushButton.clicked.connect(self.calibrate)
        #self.file_button.clicked.connect(self.openFiles)
        #self.pushButton.clicked.connect(self.export)
        self.defaults_button.clicked.connect(self.loadDefaults)
        
        sliders = self.centralwidget.findChildren(QtWidgets.QSlider)
        for slider in sliders:
            slider.setMinimumSize(QtCore.QSize(150, 20))
            slider.setMaximumSize(QtCore.QSize(150, 20))

    #%% Functions
    def toggleFullScreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))



    # FUNCTIONS
    def openFiles(self):
        file_browser = QtWidgets.QFileDialog()
        file_browser.setFileMode(QFileDialog.ExistingFiles)
        files = file_browser.getOpenFileNames(self.centralwidget, 'Browse Files', '', 'All Files(*)')[0]
        text = ''
        for file in files:
            filename = file[file.rindex('/') + 1:]
            text += filename + '\n'
        self.file_labels.setText(text)


    def importVals(self):
        fileloc = QFileDialog.getOpenFileName(None, "Open MTS Data File", "", "CSV Files (*.csv)")
        if fileloc:
            file = str(fileloc[0])
            params = importData(file)
            for i in range(1, 10):
                for j in range(2):
                    for key in params.keys():
                        if key == self.gridLayout.itemAtPosition(i, j).objectName():
                            if "Lower Bound" in params[key]:
                                self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().setText(str(params[key]["Lower Bound"]))
                            if "Upper Bound" in params[key]:
                                self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().setText(str(params[key]["Upper Bound"]))
                            if "Guess" in params[key]:
                                self.gridLayout.itemAtPosition(i, j).itemAt(6).widget().setText(str(params[key]["Guess"]))

    def uncheck(self,state):
        if state == QtCore.Qt.Checked:
            if self.E_M.sender() == self.checkBox:
                print('The E_M checkbox is checked')
                self.DV_flags[0] = False
                
            if self.E_A.sender() == self.checkBox_2:
                print('The E_A checkbox is checked')
                if self.flags['modulus_flag'] == True:
                    self.lineEdit_6.setEnabled(False)

                self.DV_flags[1] = False
                
            if self.M_s.sender() == self.checkBox_5:
                print('The M_s checkbox is checked')
                self.DV_flags[2] = False
                
            if self.M_s_M_f.sender() == self.checkBox_15:
                print('The M_s - M_f checkbox is checked')
                self.DV_flags[3] = False
                
            if self.A_s.sender() == self.checkBox_6:
                print('The A_s checkbox is checked')
                self.DV_flags[4] = False
                
            if self.A_f_A_s.sender() == self.checkBox_16:
                print('The A_f - A_s checkbox is checked')
                self.DV_flags[5] = False
                
            if self.C_M.sender() == self.checkBox_7:
                print('The C_M checkbox is checked')
                self.DV_flags[6] = False

            if self.C_A.sender() == self.checkBox_17:
                print('The C_A checkbox is checked')
                self.DV_flags[7] = False
                
            if self.H_min.sender() == self.checkBox_8:
                print('The H_min checkbox is checked')
                self.DV_flags[8] = False
                
            if self.H_max_H_min.sender() == self.checkBox_18:
                print('The H_max - H_min checkbox is checked')
                self.DV_flags[9] = False
                
            if self.k.sender() == self.checkBox_9:
                print('The k checkbox is checked')
                self.DV_flags[10] = False
                
            if self.n_1.sender() == self.checkBox_19:
                print('The n_1 checkbox is checked')
                self.DV_flags[11] = False
                
            if self.n_2.sender() == self.checkBox_10: 
                print('The n_2 checkbox is checked')
                self.DV_flags[12] = False
                
            if self.n_3.sender() == self.checkBox_20: 
                print('The n_3 checkbox is checked')
                self.DV_flags[13] = False
                
            if self.n_4.sender() == self.checkBox_11: 
                print('The n_4 checkbox is checked')
                self.DV_flags[14] = False
                
            if self.sigma_0.sender() == self.checkBox_21:
                print('The sigma_0 checkbox is checked')
                self.DV_flags[15] = False
                                
            if self.alpha.sender() == self.checkBox_12: 
                print('The alpha checkbox is checked')
                self.DV_flags[16] = False
                
            if self.modulus_flag.sender() == self.checkBox_modulus_flag:
                # The modulus flag does the following:
                    # 1. Eliminates the design variable for E_A from the opt. problem.
                    # 2. Sets the modulus flag = True s.t. E_A = E_M
                    # 3. Clears and disables the text edit for E_A specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Modulus flag checked')
                self.DV_flags[1]=False
                self.flags['modulus_flag'] = True
                self.checkBox_2.setEnabled(False)
                self.lineEdit_4.setEnabled(False)
                self.lineEdit_5.setEnabled(False)
                self.lineEdit_6.setEnabled(False)
                
            if self.slope_flag.sender() == self.checkBox_slope_flag:
                # The slope flag does the following:
                    # 1. Eliminates the design variable for C_A from the opt. problem.
                    # 2. Sets the slope flag = True s.t. C_A = C_M
                    # 3. Clears and disables the text edit for C_A specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Slope flag checked')
                self.DV_flags[7]=False
                self.flags['slope_flag'] = True
                self.checkBox_17.setEnabled(False)
                self.lineEdit_49.setEnabled(False)
                self.lineEdit_50.setEnabled(False)
                self.lineEdit_51.setEnabled(False)
                
            if self.smooth_hardening_flag.sender() == self.checkBox_smooth_hardening_flag:
                # The smooth hardening flag does the following:
                    # 1. Eliminates the design variables for n_2, n_3
                    #    n_4 from the opt. problem.
                    # 2. Sets the smooth hardening flag = True s.t. 
                    #    n_1 = n_2 = n_3 = n_4
                    # 3. Clears and disables the text edit for n_2_n_4 specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Smooth hardening flag checked')
                self.DV_flags[12]=False #n_2
                self.DV_flags[13]=False #n_3
                self.DV_flags[14]=False #n_4
                self.flags['smooth_hardening_flag'] = True
                
                #n_2
                self.checkBox_10.setEnabled(False)
                self.lineEdit_28.setEnabled(False)
                self.lineEdit_29.setEnabled(False)
                self.lineEdit_30.setEnabled(False)

                #n_3
                self.checkBox_20.setEnabled(False)
                self.lineEdit_58.setEnabled(False)
                self.lineEdit_59.setEnabled(False)
                self.lineEdit_60.setEnabled(False)  
                
                #n_4
                self.checkBox_11.setEnabled(False)
                self.lineEdit_31.setEnabled(False)
                self.lineEdit_32.setEnabled(False)
                self.lineEdit_33.setEnabled(False)
                
        elif state == QtCore.Qt.Unchecked:
            if self.E_M.sender() == self.checkBox:
                print('The E_M checkbox is unchecked')
                self.DV_flags[0] = True
                
            if self.E_A.sender() == self.checkBox_2:
                print('The E_A checkbox is unchecked')
                self.DV_flags[1] = True
                
            if self.M_s.sender() == self.checkBox_5:
                print('The M_s checkbox is unchecked')
                self.DV_flags[2] = True
                
            if self.M_s_M_f.sender() == self.checkBox_15:
                print('The M_s - M_f checkbox is unchecked')
                self.DV_flags[3] = True
                
            if self.A_s.sender() == self.checkBox_6:
                print('The A_s checkbox is unchecked')
                self.DV_flags[4] = True
                
            if self.A_f_A_s.sender() == self.checkBox_16:
                print('The A_f - A_s checkbox is unchecked')
                self.DV_flags[5] = True
                
            if self.C_M.sender() == self.checkBox_7:
                print('The C_M checkbox is unchecked')
                self.DV_flags[6] = True

            if self.C_A.sender() == self.checkBox_17:
                print('The C_A checkbox is unchecked')
                self.DV_flags[7] = True
                
            if self.H_min.sender() == self.checkBox_8:
                print('The H_min checkbox is unchecked')
                self.DV_flags[8] = True
                
            if self.H_max_H_min.sender() == self.checkBox_18:
                print('The H_max - H_min checkbox is unchecked')
                self.DV_flags[9] = True
                
            if self.k.sender() == self.checkBox_9:
                print('The k checkbox is unchecked')
                self.DV_flags[10] = True
                
            if self.n_1.sender() == self.checkBox_19:
                print('The n_1 checkbox is unchecked')
                self.DV_flags[11] = True
                
            if self.n_2.sender() == self.checkBox_10: 
                print('The n_2 checkbox is unchecked')
                self.DV_flags[12] = True
                
            if self.n_3.sender() == self.checkBox_20: 
                print('The n_3 checkbox is unchecked')
                self.DV_flags[13] = True
                
            if self.n_4.sender() == self.checkBox_11: 
                print('The n_4 checkbox is unchecked')
                self.DV_flags[14] = True
                
            if self.sigma_0.sender() == self.checkBox_21:
                print('The sigma_0 checkbox is unchecked')
                self.DV_flags[15] = True
                                
            if self.alpha.sender() == self.checkBox_12: 
                print('The alpha checkbox is unchecked')
                self.DV_flags[16] = True
                
            if self.modulus_flag.sender() == self.checkBox_modulus_flag:
                # The modulus flag does the following:
                    # 1. Eliminates the design variable for E_A from the opt. problem.
                    # 2. Sets the modulus flag = True s.t. E_A = E_M
                    # 3. Clears and disables the text edit for E_A specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Modulus flag unchecked')
                self.DV_flags[1]=True
                self.flags['modulus_flag'] = False
                self.checkBox_2.setEnabled(True)
                self.checkBox_2.setChecked(False)
                self.lineEdit_4.setEnabled(True)
                self.lineEdit_5.setEnabled(True)
                self.lineEdit_6.setEnabled(False)
                
            if self.slope_flag.sender() == self.checkBox_slope_flag:
                # The slope flag does the following:
                    # 1. Eliminates the design variable for C_A from the opt. problem.
                    # 2. Sets the slope flag = True s.t. C_A = C_M
                    # 3. Clears and disables the text edit for C_A specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Slope flag unchecked')
                self.DV_flags[7]=True
                self.flags['slope_flag'] = False
                self.checkBox_17.setEnabled(True)
                self.checkBox_17.setChecked(False)
                self.lineEdit_49.setEnabled(True)
                self.lineEdit_50.setEnabled(True)
                self.lineEdit_51.setEnabled(False)

            if self.smooth_hardening_flag.sender() == self.checkBox_smooth_hardening_flag:
                # The smooth hardening flag does the following:
                    # 1. Eliminates the design variables for n_2, n_3
                    #    n_4 from the opt. problem.
                    # 2. Sets the smooth hardening flag = True s.t. 
                    #    n_1 = n_2 = n_3 = n_4
                    # 3. Clears and disables the text edit for n_2_n_4 specified 
                    #   value and bounds
                    # I WILL NEED TO ACCOUNT FOR THIS IN THE GET SPECIFIED VALUES
                    # FUNCTION
                print('Smooth hardening flag unchecked')
                self.DV_flags[12]=True #n_2
                self.DV_flags[13]=True #n_3
                self.DV_flags[14]=True #n_4
                self.flags['smooth_hardening_flag'] = False
                
                #n_2
                self.checkBox_10.setEnabled(True)
                self.checkBox_10.setChecked(False)
                self.lineEdit_28.setEnabled(True)
                self.lineEdit_29.setEnabled(True)
                self.lineEdit_30.setEnabled(False)

                #n_3
                self.checkBox_20.setEnabled(True)
                self.checkBox_20.setChecked(False)
                self.lineEdit_58.setEnabled(True)
                self.lineEdit_59.setEnabled(True)
                self.lineEdit_60.setEnabled(False)  
                
                #n_4
                self.checkBox_11.setEnabled(True)
                self.checkBox_11.setChecked(False)
                self.lineEdit_31.setEnabled(True)
                self.lineEdit_32.setEnabled(True)
                self.lineEdit_33.setEnabled(False)
            
        print(self.DV_flags)
                

        



    def guess(self):
        invalid = False
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    continue
                try:
                    bound = str(self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().text())
                    upper_bound = float(bound)
                    bound = str(self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().text())
                    lower_bound = float(bound)
                    guess = round(random.uniform(lower_bound, upper_bound), 2)
                    self.gridLayout.itemAtPosition(i, j).itemAt(6).widget().setText(str(guess))
                except:
                    error = QtWidgets.QMessageBox(self.centralwidget)
                    error.setIcon(QMessageBox.Critical)
                    error.setText("Please fill all bounds first")
                    error.setWindowTitle("Error")
                    error.show()
                    invalid = True
                if invalid:
                    break
            if invalid:
                break


    def export(self):
        data = {}
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    continue
                key = self.gridLayout.itemAtPosition(i, j).objectName()
                data[key] = {}
                try:
                    bound = str(self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().text())
                    upper_bound = float(bound)
                    bound = str(self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().text())
                    lower_bound = float(bound)
                    guess = float(self.gridLayout.itemAtPosition(i, j).itemAt(6).widget().text())
                    data[key]["Lower Bound"] = lower_bound
                    data[key]["Upper Bound"] = upper_bound
                    data[key]["Guess"] = guess
                except:
                    continue
        exportData(data, "bounds.csv")
        
    def calibrate(self):
        self.getSpecifiedValues()
        bounds = self.getBounds()
        print(self.known_values)
        #print(bounds)

        error = test_optimizer_v2.main(bounds,self.known_values,self.DV_flags)
        


    def loadDefaults(self):
        #Current order:
            #E_M, E_A, M_s, M_s-M_f, A_s, A_f - A_s, C_M, C_A, H_min,
            #H_max - H_min, k, n_1, n_2, n_3, n_4, sigma_crit, alpha
        lower_bound_defaults = [20E9,20E9,223.0,10.0,273.0,10.0,2E6,2E6,0.0,
                                0.01,1E-8,0.01,0.01,0.01,0.01,0.0,0.0]
        upper_bound_defaults = [110E9,110E9,273.0,50.0,323.0,50.0,15E6,15E6,0.03,
                                0.05,1E-6,1.0,1.0,1.0,1.0,60E6,1E-6]
        
        #E_M
        self.lineEdit.setText("{:.2e}".format(lower_bound_defaults[0]))
        self.lineEdit_2.setText("{:.2e}".format(upper_bound_defaults[0]))
        
        #E_A
        self.lineEdit_4.setText("{:.2e}".format(lower_bound_defaults[1]))
        self.lineEdit_5.setText("{:.2e}".format(upper_bound_defaults[1]))
        
        #M_s
        self.lineEdit_13.setText("{:.0f}".format(lower_bound_defaults[2]))
        self.lineEdit_14.setText("{:.0f}".format(upper_bound_defaults[2]))
        
        #M_s-M_f
        self.lineEdit_43.setText("{:.0f}".format(lower_bound_defaults[3]))
        self.lineEdit_44.setText("{:.0f}".format(upper_bound_defaults[3]))
        
        #A_s
        self.lineEdit_16.setText("{:.0f}".format(lower_bound_defaults[4]))
        self.lineEdit_17.setText("{:.0f}".format(upper_bound_defaults[4]))
        
        #A_f - A_s
        self.lineEdit_46.setText("{:.0f}".format(lower_bound_defaults[5]))
        self.lineEdit_47.setText("{:.0f}".format(upper_bound_defaults[5]))
        
        #C_M
        self.lineEdit_19.setText("{:.2e}".format(lower_bound_defaults[6]))
        self.lineEdit_20.setText("{:.2e}".format(upper_bound_defaults[6]))
        
        #C_A
        self.lineEdit_49.setText("{:.2e}".format(lower_bound_defaults[7]))
        self.lineEdit_50.setText("{:.2e}".format(upper_bound_defaults[7]))
        
        #H_min
        self.lineEdit_22.setText("{:.2f}".format(lower_bound_defaults[8]))
        self.lineEdit_23.setText("{:.2f}".format(upper_bound_defaults[8]))
        
        #H_max - H_min
        self.lineEdit_52.setText("{:.2f}".format(lower_bound_defaults[9]))
        self.lineEdit_53.setText("{:.2f}".format(upper_bound_defaults[9]))
        
        #k
        self.lineEdit_25.setText("{:.2e}".format(lower_bound_defaults[10]))
        self.lineEdit_26.setText("{:.2e}".format(upper_bound_defaults[10]))
        
        #n_1
        self.lineEdit_55.setText("{:.2f}".format(lower_bound_defaults[11]))
        self.lineEdit_56.setText("{:.2f}".format(upper_bound_defaults[11]))
        
        #n_2
        self.lineEdit_28.setText("{:.2f}".format(lower_bound_defaults[12]))
        self.lineEdit_29.setText("{:.2f}".format(upper_bound_defaults[12]))
        
        #n_3
        self.lineEdit_58.setText("{:.2f}".format(lower_bound_defaults[13]))
        self.lineEdit_59.setText("{:.2f}".format(upper_bound_defaults[13]))
        
        #n_4
        self.lineEdit_31.setText("{:.2f}".format(lower_bound_defaults[14]))
        self.lineEdit_32.setText("{:.2f}".format(upper_bound_defaults[14]))
        
        #sigma_crit
        self.lineEdit_61.setText("{:.2e}".format(lower_bound_defaults[15]))
        self.lineEdit_62.setText("{:.2e}".format(upper_bound_defaults[15]))
        
        #alpha
        self.lineEdit_34.setText("{:.2e}".format(lower_bound_defaults[16]))
        self.lineEdit_35.setText("{:.2e}".format(upper_bound_defaults[16]))
        


    def updateVal(self):
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    break
                upper_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().text())
                lower_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().text())
                slider_val = self.gridLayout.itemAtPosition(i, j).itemAt(3).widget().value()
                guess = self.gridLayout.itemAtPosition(i, j).itemAt(6).widget()
                step = (upper_bound - lower_bound)/100
                guess.setText(str(slider_val * step + lower_bound))


    def updateSlider(self):
        for i in range(1, 10):
            for j in range(2):
                if i == 9 and j == 1:
                    break
                val = self.gridLayout.itemAtPosition(i, j).itemAt(6).widget().text()
                if (not val == ""):
                    upper_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().text())
                    lower_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().text())
                    if float(val) < lower_bound:
                        print('Setting lower bound to specified value for visualization')
                        lower_bound = self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().setText(str(val))
                    elif float(val) > upper_bound:
                        print('Setting upper bound to specified value for visualization')
                        upper_bound = self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().setText(str(val))
                    upper_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(4).widget().text())
                    lower_bound = float(self.gridLayout.itemAtPosition(i, j).itemAt(2).widget().text())    
                    step = (upper_bound - lower_bound)/100
                
                    val = float(val)
                    normalized_value = int(val/step-int(lower_bound)/step)
                    self.gridLayout.itemAtPosition(i, j).itemAt(3).widget().setValue(normalized_value)
                    
                        
    def getBounds(self):
        # initialize bounds list of lists
        bounds = []
        
        #E_M
        bounds.append([float(self.lineEdit.text()),
                       float(self.lineEdit_2.text())])
        
        #E_A
        bounds.append([float(self.lineEdit_4.text()),
                       float(self.lineEdit_5.text())])
        
        #M_s
        bounds.append([float(self.lineEdit_13.text()),
                       float(self.lineEdit_14.text())])
        
        #M_s-M_f
        bounds.append([float(self.lineEdit_43.text()),
                       float(self.lineEdit_44.text())])

        #A_s
        bounds.append([float(self.lineEdit_16.text()),
                       float(self.lineEdit_17.text())])
        
        #A_f - A_s
        bounds.append([float(self.lineEdit_46.text()),
                       float(self.lineEdit_47.text())])
        
        #C_M
        bounds.append([float(self.lineEdit_19.text()),
                       float(self.lineEdit_20.text())])
        
        #C_A
        bounds.append([float(self.lineEdit_49.text()),
                       float(self.lineEdit_50.text())])
        
        #H_min
        bounds.append([float(self.lineEdit_22.text()),
                       float(self.lineEdit_23.text())])
        #H_max - H_min
        bounds.append([float(self.lineEdit_52.text()),
                       float(self.lineEdit_53.text())])
        #k
        bounds.append([float(self.lineEdit_25.text()),
                       float(self.lineEdit_26.text())])
        
        #n_1
        bounds.append([float(self.lineEdit_55.text()),
                       float(self.lineEdit_56.text())])
        
        #n_2
        bounds.append([float(self.lineEdit_28.text()),
                       float(self.lineEdit_29.text())])
        
        #n_3
        bounds.append([float(self.lineEdit_58.text()),
                       float(self.lineEdit_59.text())])
        
        #n_4
        bounds.append([float(self.lineEdit_31.text()),
                       float(self.lineEdit_32.text())])
        
        #sigma_crit
        bounds.append([float(self.lineEdit_61.text()),
                       float(self.lineEdit_62.text())])
        
        #alpha
        bounds.append([float(self.lineEdit_34.text()),
                       float(self.lineEdit_35.text())])
        
        specified_parameter_indices = [i for i, x in enumerate(self.DV_flags) if x==False]
        #Remove all bounds that are already specified. 
        for index in sorted(specified_parameter_indices,reverse=True):
            del bounds[index]


        return bounds
    

        
    
    def getSpecifiedValues(self):
        #get the values that were specified to be constrained
        ## MAYBE: ONLY MAKE THE TEXT BOXES ABLE TO BE ACCESSED WHEN THE ASSOCIATED
        ## CHECKBOX IS CLICKED
        self.known_values = {}
        
        DV_order = ['E_M','E_A', 'M_s', 'M_s-M_f', 'A_s', 'A_f - A_s', 'C_M', 'C_A', 'H_min',
                    'H_max - H_min', 'k', 'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']
        
        
        lineEdits = [self.lineEdit_3,self.lineEdit_6,self.lineEdit_15,self.lineEdit_45,self.lineEdit_18,
                     self.lineEdit_48,self.lineEdit_21,self.lineEdit_51,self.lineEdit_24,self.lineEdit_54,
                     self.lineEdit_27,self.lineEdit_57,self.lineEdit_30,self.lineEdit_60,self.lineEdit_33,
                     self.lineEdit_63,self.lineEdit_36]
        
        for counter in range(len(DV_order)):
            if self.DV_flags[counter] == False:
                self.known_values[DV_order[counter]] = float(lineEdits[counter].text())
        


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())