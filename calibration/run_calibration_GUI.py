# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_base_hort.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
import random
import pandas as pd
import numpy as np


from PyQt5 import QtCore, QtGui, QtWidgets
from utility.latex_translation import textToLatex
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTabWidget,\
    QGridLayout, QLabel, QPushButton, QApplication, QSpinBox, QComboBox, QTableWidget, \
    QHBoxLayout, QAbstractItemView, QFrame, QTableWidgetItem
from PyQt5.QtGui import QFont, QColor

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from model_funcs.phase_diagram import plot_phase_diagram
from model_funcs.test_optimizer_v2 import main
from utility.export import exportData
from utility.import_vals import importData
from matplotlib import rcParams as rc
from model_funcs import test_optimizer_v2
import cgitb
cgitb.enable(format="text")



class App(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # Formatting
        self.title = 'Shape Memory Alloy REACT (Rendering of Experimental Analysis and Calibration Tool)'
        #MainWindow.resize(1552, 586)
        #MainWindow.showFullScreen()
        #Resize GUI to take up 75% of the screen (dynamic based on the user's resolution)
        app = QtWidgets.QApplication(sys.argv)
        screen = app.primaryScreen()
        rect = screen.availableGeometry()
        print(rect)
        # width = rect.width()
        # height = rect.height()
        width = 1600
        height = 900
        # width = int(rect.width()*0.90)
        # height = int(rect.height()*0.90)
        self.left = int(rect.width()*0.05)
        self.top = int(rect.height()*0.05)
        self.width = width
        self.height = height
        # self.width = int(width*0.75)
        # self.height = int(height*0.75)
        #Resize to be exactly the resolution on my work computer.

        #Set window icon to be the A&M Logo (of course)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("TAM-LogoBox.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        self.setWindowIcon(icon)
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)


        self.tabs = QTabWidget()
        self.tabs.resize(self.width,self.height)
        self.table_widget = MyTableWidget(self)

        self.data_input_widget = DataInputWidget(self)

        self.calibration_plotting = CalibrationWindow(self)

        self.tabs.addTab(self.data_input_widget,'Data Input')
        self.tabs.addTab(self.table_widget,"Material Property Calibration")


        self.tabs.addTab(self.calibration_plotting,"Calibration Plotting Utility")


        self.setCentralWidget(self.tabs)

        self.tabs.setTabEnabled(1,False)
        self.tabs.setTabEnabled(2,False)

        self.show()

class MyTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget,self).__init__(parent)

        header_font_size = 10
        header_weight = 75
        normal_font_size = 10
        normal_weight = 50

        lineEdit_height = 30
        lineEdit_width = 100

        parameter_label_height = 60
        parameter_label_width = 200

        spacer_item_height = lineEdit_height
        spacer_item_small_width = 5
        spacer_item_width = 30
        #create ''master'' spacer item to use throughout
        regular_spacer = QtWidgets.QSpacerItem(
            spacer_item_width,
            spacer_item_height,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
            )

        small_spacer = QtWidgets.QSpacerItem(
            spacer_item_small_width,
            spacer_item_height,
            QtWidgets.QSizePolicy.Fixed,
            QtWidgets.QSizePolicy.Minimum
            )


        self.centralwidget = QtWidgets.QWidget(self)
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
        self.create_material_property(
            self.E_M,
            "E_M",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% E_A
        self.E_A = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.E_A,
            "E_A",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Transformation temperatures
        #%%M_s
        self.M_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.M_s,
            "M_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% A_s
        self.A_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.A_s,
            "A_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% M_s - M_f
        self.M_s_M_f = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.M_s_M_f,
            "M_s-M_f",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% A_f - A_s
        self.A_f_A_s = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.A_f_A_s,
            "A_f-A_s",
            "K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% C_A
        self.C_A = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.C_A,
            "C_A",
            "Pa/K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% C_M
        self.C_M = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.C_M,
            "C_M",
            "MPa/K",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Transformation strain properties
        #%% H_min
        self.H_min = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.H_min,
            "H_{min}",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% H_max - H_min
        self.H_max_H_min = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.H_max_H_min,
            "H_{max} - H_{min}",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% sigma_0
        self.sigma_0 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.sigma_0,
            r"\sigma_0",
            "Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% k
        self.k = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.k,
            "k",
            "1/Pa",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        # Other properties
        #%% n_1
        self.n_1 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_1,
            "n_1",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% n_2
        self.n_2 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_2,
            "n_2",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )


        #%% n_3
        self.n_3 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_3,
            "n_3",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% n_4
        self.n_4 = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.n_4,
            "n_4",
            "-",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )
        #%% alpha
        self.alpha = QtWidgets.QHBoxLayout()
        self.create_material_property(
            self.alpha,
            r"\alpha",
            "1/m",
            parameter_label_width,
            parameter_label_height,
            lineEdit_width,
            lineEdit_height,
            small_spacer,
            regular_spacer,
            )

        #%% Left labels
        self.left_labels = QtWidgets.QHBoxLayout()
        self.left_labels.setContentsMargins(0, -1, 5, -1)
        self.left_labels.setObjectName("left_labels")
        self.parameter_label = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.parameter_label,
                "Parameter",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.parameter_label)
        self.left_labels.addItem(small_spacer)
        self.lower_bound_label = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.lower_bound_label,
                "Lower Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.lower_bound_label)
        self.left_labels.addItem(regular_spacer)


        self.upper_bound_label = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.upper_bound_label,
                "Upper Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.upper_bound_label)

        self.left_labels.addItem(regular_spacer)

        self.specify_label = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.specify_label,
                "Specify?",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.specify_label)
        self.left_labels.addItem(regular_spacer)
        self.value_label = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.value_label,
                "Value",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.left_labels.addWidget(self.value_label)

        #%% Right labels
        self.right_labels = QtWidgets.QHBoxLayout()
        self.right_labels.setContentsMargins(0, -1, 5, -1)
        self.right_labels.setObjectName("right_labels")

        self.parameter_label_right = QtWidgets.QLabel(self.centralwidget)
        self.lower_bound_label_right = QtWidgets.QLabel(self.centralwidget)
        self.upper_bound_label_right = QtWidgets.QLabel(self.centralwidget)
        self.specify_label_right = QtWidgets.QLabel(self.centralwidget)
        self.value_label_right = QtWidgets.QLabel(self.centralwidget)

        self.create_label(
                self.parameter_label_right,
                "Parameter",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.parameter_label_right)
        self.right_labels.addItem(small_spacer)

        self.create_label(
                self.lower_bound_label_right,
                "Lower Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.lower_bound_label_right)
        self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.upper_bound_label_right,
                "Upper Bound",
                header_font_size,
                header_weight,
                lineEdit_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.upper_bound_label_right)
        self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.specify_label_right,
                "Specify?",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.specify_label_right)

        self.right_labels.addItem(regular_spacer)

        self.create_label(
                self.value_label_right,
                "Value",
                header_font_size,
                header_weight,
                parameter_label_width,
                parameter_label_height,
                )

        self.right_labels.addWidget(self.value_label_right)


        #%% Pushbuttons
        self.buttons = QtWidgets.QHBoxLayout()
        self.buttons.setObjectName("buttons")

        font_size = 14
        font_weight = 75

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = False
            )

        # self.buttons.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)

        size_policy = self.set_size_policy(
            self.pushButton
            )
        self.pushButton.setSizePolicy(
            size_policy
            )

        self.pushButton.setMinimumSize(QtCore.QSize(200, 100))
        self.pushButton.setMaximumSize(QtCore.QSize(200, 100))
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText('Calibrate')
        self.buttons.addWidget(self.pushButton)

        #%% Design variable flags
        self.prop_constraints_label = QtWidgets.QHBoxLayout()
        self.prop_constraints_label.setContentsMargins(-1, -1, 5, -1)
        self.prop_constraints_label.setObjectName("prop_params_label")

        # Header
        self.prop_constraints_header = QtWidgets.QLabel(self.centralwidget)
        self.prop_constraints_header.setText('Material property constraints')

        header_font = self.create_font(
            header_font_size,
            header_weight,
            bold_flag = True
            )

        self.prop_constraints_header.setFont(header_font)
        self.prop_constraints_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.prop_constraints_header.setObjectName("prop_constraints_header")
        self.prop_constraints_label.addStretch()
        self.prop_constraints_label.addWidget(self.prop_constraints_header)
        self.prop_constraints_label.addStretch()

        #Modulus Flag

        self.modulus_flag = QtWidgets.QHBoxLayout()

        self.create_constraint(
            self.modulus_flag,
            "modulus_flag",
            r"$E_A = E_M$",
            text_width = 90,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )

        # Slope flag

        self.slope_flag = QtWidgets.QHBoxLayout()
        self.create_constraint(
            self.slope_flag,
            "slope_flag",
            r"$C_A = C_M$",
            text_width = 90,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )

        self.smooth_hardening_flag = QtWidgets.QHBoxLayout()

        self.create_constraint(
            self.smooth_hardening_flag,
            "smooth_hardening_flag",
            r"$n_1=n_2=n_3=n_4$",
            text_width = 120,
            text_height = 43,
            font_weight = 75,
            font_size = 12,
            latex_flag = True
            )


        #%% Algorithmic parameters

        self.alg_params_label = QtWidgets.QHBoxLayout()
        self.alg_params_label.setContentsMargins(-1, -1, 5, -1)
        self.alg_params_label.setObjectName("alg_params_label")
        # self.gen_label =

        # Header
        self.alg_param_header = QtWidgets.QLabel(self.centralwidget)
        self.alg_param_header.setText('Algorithmic Parameters')

        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))

        self.alg_param_header.setFont(header_font)
        self.alg_param_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.alg_param_header.setObjectName("opt_param_header")
        self.alg_params_label.addStretch()
        self.alg_params_label.addWidget(self.alg_param_header)
        self.alg_params_label.addStretch()

        self.non_op_params = QtWidgets.QHBoxLayout()
        self.non_op_params.setContentsMargins(-1, -1, 5, -1)
        self.non_op_params.setObjectName("non_op_params")


        # delta
        self.delta = QtWidgets.QHBoxLayout()

        self.create_parameter(
                parameter_object=self.delta,
                name='delta',
                text=r"$\delta$",
                text_width=90,
                text_height=43,
                text_size=12,
                text_weight=75,
                lineEdit_width=lineEdit_width,
                lineEdit_height=lineEdit_height,
                latex_flag = True,
                )

        self.sigma_cal = QtWidgets.QHBoxLayout()

        self.create_parameter(
                parameter_object=self.sigma_cal,
                name='sigma_cal',
                text=r"$\sigma_{cal}$",
                text_width=90,
                text_height=43,
                text_size=12,
                text_weight=75,
                lineEdit_width=lineEdit_width,
                lineEdit_height=lineEdit_height,
                latex_flag = True,
                )

        #MVF_tolerance
        self.MVF_tol = QtWidgets.QHBoxLayout()

        self.create_parameter(
                parameter_object=self.MVF_tol,
                name='MVF_tol',
                text="MVF Tol",
                text_width=120,
                text_height=43,
                text_size=12,
                text_weight=75,
                lineEdit_width=lineEdit_width,
                lineEdit_height=lineEdit_height,
                latex_flag = False,
                )

        #%%Optimization parameters
        #Might need to make this a grid with labels on the left and line edits on the right

        self.op_params_label = QtWidgets.QHBoxLayout()
        self.op_params_label.setContentsMargins(-1, -1, 5, -1)
        self.op_params_label.setObjectName("op_params")
        # self.gen_label =

        # Header
        self.opt_param_header = QtWidgets.QLabel(self.centralwidget)
        self.opt_param_header.setText('Optimization Parameters')
        # self.opt_param_header.setMinimumSize(QtCore.QSize(90, 0))
        # self.opt_param_header.setMaximumSize(QtCore.QSize(90, 16777215))

        self.opt_param_header.setFont(header_font)
        self.opt_param_header.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
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

        size_policy = self.set_size_policy(
            self.gen_label
            )
        self.gen_label.setSizePolicy(
            size_policy
            )

        #self.gen_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.gen_label.setMaximumSize(QtCore.QSize(90, 16777215))

        normal_font = self.create_font(
            normal_font_size,
            normal_weight,
            bold_flag = False
            )

        self.gen_label.setFont(normal_font)
        self.gen_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.gen_label.setObjectName("gen_label")
        self.num_gens.addWidget(self.gen_label)
        self.num_gens.addStretch()
        self.gen_line = QtWidgets.QLineEdit(self.centralwidget)

        size_policy = self.set_size_policy(
            self.gen_line
            )
        self.gen_line.setSizePolicy(
            size_policy
            )


        self.gen_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.gen_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.gen_line.setObjectName("gen_line")
        self.num_gens.addWidget(self.gen_line)

        self.pop_size = QtWidgets.QHBoxLayout()
        self.pop_size.setContentsMargins(-1, -1, 5, -1)
        self.pop_size.setObjectName("pop_size")

        self.pop_label = QtWidgets.QLabel(self.centralwidget)
        self.pop_label.setText('Population size')


        size_policy = self.set_size_policy(
            self.pop_label
            )
        self.pop_label.setSizePolicy(
            size_policy
            )

        #self.pop_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.pop_label.setMaximumSize(QtCore.QSize(90, 16777215))

        self.pop_label.setFont(normal_font)
        self.pop_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.pop_label.setObjectName("pop_label")
        self.pop_size.addWidget(self.pop_label)
        self.pop_size.addStretch()
        self.pop_line = QtWidgets.QLineEdit(self.centralwidget)


        size_policy = self.set_size_policy(
            self.pop_line
            )
        self.pop_line.setSizePolicy(
            size_policy
            )


        self.pop_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.pop_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.pop_line.setObjectName("pop_line")

        self.pop_size.addWidget(self.pop_line)

        self.num_iters = QtWidgets.QHBoxLayout()
        self.num_iters.setContentsMargins(-1, -1, 5, -1)
        self.num_iters.setObjectName("num_iters")

        self.iter_label = QtWidgets.QLabel(self.centralwidget)
        self.iter_label.setText('Gradient-based iterations')


        size_policy = self.set_size_policy(
            self.iter_label
            )
        self.iter_label.setSizePolicy(
            size_policy
            )

        #self.iter_label.setMinimumSize(QtCore.QSize(90, 0))
        #self.iter_label.setMaximumSize(QtCore.QSize(90, 16777215))

        self.iter_label.setFont(normal_font)
        self.iter_label.setAlignment(
            QtCore.Qt.AlignLeft|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        self.iter_label.setObjectName("iter_label")
        self.num_iters.addWidget(self.iter_label)
        self.num_iters.addStretch()
        self.iter_line = QtWidgets.QLineEdit(self.centralwidget)


        size_policy = self.set_size_policy(
            self.iter_line
            )
        self.iter_line.setSizePolicy(
            size_policy
            )

        self.iter_line.setMinimumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.iter_line.setMaximumSize(QtCore.QSize(lineEdit_width, lineEdit_height))
        self.iter_line.setObjectName("iter_line")

        self.num_iters.addWidget(self.iter_line)


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

        self.gridLayout.addLayout(self.prop_constraints_label,0,2,1,1)
        self.gridLayout.addLayout(self.modulus_flag,1,2,1,1)
        self.gridLayout.addLayout(self.slope_flag,2,2,1,1)
        self.gridLayout.addLayout(self.smooth_hardening_flag,3,2,1,1)

        #Algorithmic parameters
        self.gridLayout.addLayout(self.alg_params_label,4,2,1,1)
        self.gridLayout.addLayout(self.delta,5,2,1,1)
        self.gridLayout.addLayout(self.sigma_cal,6,2,1,1)
        self.gridLayout.addLayout(self.MVF_tol,7,2,1,1)

        #Optimization parameters
        self.gridLayout.addLayout(self.op_params_label, 8, 2, 1, 1)
        self.gridLayout.addLayout(self.num_gens, 9, 2, 1, 1)
        self.gridLayout.addLayout(self.pop_size, 10, 2, 1, 1)
        self.gridLayout.addLayout(self.num_iters, 11, 2, 1, 1)
        #Buttons and Labels

        self.gridLayout.addLayout(self.buttons, 12, 2, 2, 2)
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
        # self.pushButton_3.clicked.connect(self.importVals)
        # self.pushButton_2.clicked.connect(self.guess)
        self.pushButton.clicked.connect(self.calibrate)
        #self.file_button.clicked.connect(self.openFiles)
        #self.pushButton.clicked.connect(self.export)
        # self.defaults_button.clicked.connect(self.loadDefaults)

        sliders = self.centralwidget.findChildren(QtWidgets.QSlider)
        for slider in sliders:
            slider.setMinimumSize(QtCore.QSize(150, 20))
            slider.setMaximumSize(QtCore.QSize(150, 20))


        # self.tabs = QTabWidget()
        # self.tabs.addTab(self.centralwidget,"Material Property Calibration")
        # self.tab2 = QtWidgets.QWidget()
        # self.tabs.addTab(self.tab2,'tab 2')

        # MainWindow.setCentralWidget(self.tabs)



    #%% Functions
    def changeTabs(self):
        ex.tabs.setCurrentIndex(2)

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
        files = file_browser.getOpenFileNames(
            self.centralwidget,
            'Browse Files',
            '',
            'All Files(*)'
            )[0]
        text = ''
        for file in files:
            filename = file[file.rindex('/') + 1:]
            text += filename + '\n'
        self.file_labels.setText(text)


    def importVals(self):
        fileloc = QFileDialog.getOpenFileName(
            None,
            "Open MTS Data File",
            "",
            "CSV Files (*.csv)"
            )
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
            if self.E_M.sender() == self.E_M.checkBox:
                print('The E_M checkbox is checked')
                self.DV_flags[0] = False

            if self.E_A.sender() == self.E_A.checkBox:
                print('The E_A checkbox is checked')
                # if self.flags['modulus_flag'] == True:
                #     self.E_A.specified_value.setEnabled(False)

                self.DV_flags[1] = False

            if self.M_s.sender() == self.M_s.checkBox:
                print('The M_s checkbox is checked')
                self.DV_flags[2] = False

            if self.M_s_M_f.sender() == self.M_s_M_f.checkBox:
                print('The M_s - M_f checkbox is checked')
                self.DV_flags[3] = False

            if self.A_s.sender() == self.A_s.checkBox:
                print('The A_s checkbox is checked')
                self.DV_flags[4] = False

            if self.A_f_A_s.sender() == self.A_f_A_s.checkBox:
                print('The A_f - A_s checkbox is checked')
                self.DV_flags[5] = False

            if self.C_M.sender() == self.C_M.checkBox:
                print('The C_M checkbox is checked')
                self.DV_flags[6] = False

            if self.C_A.sender() == self.C_A.checkBox:
                print('The C_A checkbox is checked')
                self.DV_flags[7] = False

            if self.H_min.sender() == self.H_min.checkBox:
                print('The H_min checkbox is checked')
                self.DV_flags[8] = False

            if self.H_max_H_min.sender() == self.H_max_H_min.checkBox:
                print('The H_max - H_min checkbox is checked')
                self.DV_flags[9] = False

            if self.k.sender() == self.k.checkBox:
                print('The k checkbox is checked')
                self.DV_flags[10] = False

            if self.n_1.sender() == self.n_1.checkBox:
                print('The n_1 checkbox is checked')
                self.DV_flags[11] = False

            if self.n_2.sender() == self.n_2.checkBox:
                print('The n_2 checkbox is checked')
                self.DV_flags[12] = False

            if self.n_3.sender() == self.n_3.checkBox:
                print('The n_3 checkbox is checked')
                self.DV_flags[13] = False

            if self.n_4.sender() == self.n_4.checkBox:
                print('The n_4 checkbox is checked')
                self.DV_flags[14] = False

            if self.sigma_0.sender() == self.sigma_0.checkBox:
                print('The sigma_0 checkbox is checked')
                self.DV_flags[15] = False

            if self.alpha.sender() == self.alpha.checkBox:
                print('The alpha checkbox is checked')
                self.DV_flags[16] = False

            if self.modulus_flag.sender() == self.modulus_flag.checkbox:
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
                self.E_A.checkBox.setEnabled(False)
                self.E_A.minimum_bound.setEnabled(False)
                self.E_A.maximum_bound.setEnabled(False)
                self.E_A.specified_value.setEnabled(False)
                self.E_A.specified_value.setText('')

            if self.slope_flag.sender() == self.slope_flag.checkbox:
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
                self.C_A.checkBox.setEnabled(False)
                self.C_A.minimum_bound.setEnabled(False)
                self.C_A.maximum_bound.setEnabled(False)
                self.C_A.specified_value.setEnabled(False)
                self.C_A.specified_value.setText('')

            if self.smooth_hardening_flag.sender() == self.smooth_hardening_flag.checkbox:
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
                self.n_2.checkBox.setEnabled(False)
                self.n_2.minimum_bound.setEnabled(False)
                self.n_2.maximum_bound.setEnabled(False)
                self.n_2.specified_value.setEnabled(False)
                self.n_2.specified_value.setText('')

                #n_3
                self.n_3.checkBox.setEnabled(False)
                self.n_3.minimum_bound.setEnabled(False)
                self.n_3.maximum_bound.setEnabled(False)
                self.n_3.specified_value.setEnabled(False)
                self.n_3.specified_value.setText('')

                #n_4
                self.n_4.checkBox.setEnabled(False)
                self.n_4.minimum_bound.setEnabled(False)
                self.n_4.maximum_bound.setEnabled(False)
                self.n_4.specified_value.setEnabled(False)
                self.n_4.specified_value.setText('')

        elif state == QtCore.Qt.Unchecked:
            if self.E_M.sender() == self.E_M.checkBox:
                print('The E_M checkbox is unchecked')
                self.DV_flags[0] = True

            if self.E_A.sender() == self.E_A.checkBox:
                print('The E_A checkbox is unchecked')
                self.DV_flags[1] = True

            if self.M_s.sender() == self.M_s.checkBox:
                print('The M_s checkbox is unchecked')
                self.DV_flags[2] = True

            if self.M_s_M_f.sender() == self.M_s_M_f.checkBox:
                print('The M_s - M_f checkbox is unchecked')
                self.DV_flags[3] = True

            if self.A_s.sender() == self.A_s.checkBox:
                print('The A_s checkbox is unchecked')
                self.DV_flags[4] = True

            if self.A_f_A_s.sender() == self.A_f_A_s.checkBox:
                print('The A_f - A_s checkbox is unchecked')
                self.DV_flags[5] = True

            if self.C_M.sender() == self.C_M.checkBox:
                print('The C_M checkbox is unchecked')
                self.DV_flags[6] = True

            if self.C_A.sender() == self.C_A.checkBox:
                print('The C_A checkbox is unchecked')
                self.DV_flags[7] = True

            if self.H_min.sender() == self.H_min.checkBox:
                print('The H_min checkbox is unchecked')
                self.DV_flags[8] = True

            if self.H_max_H_min.sender() == self.H_max_H_min.checkBox:
                print('The H_max - H_min checkbox is unchecked')
                self.DV_flags[9] = True

            if self.k.sender() == self.k.checkBox:
                print('The k checkbox is unchecked')
                self.DV_flags[10] = True

            if self.n_1.sender() == self.n_1.checkBox:
                print('The n_1 checkbox is unchecked')
                self.DV_flags[11] = True

            if self.n_2.sender() == self.n_2.checkBox:
                print('The n_2 checkbox is unchecked')
                self.DV_flags[12] = True

            if self.n_3.sender() == self.n_3.checkBox:
                print('The n_3 checkbox is unchecked')
                self.DV_flags[13] = True

            if self.n_4.sender() == self.n_4.checkBox:
                print('The n_4 checkbox is unchecked')
                self.DV_flags[14] = True

            if self.sigma_0.sender() == self.sigma_0.checkBox:
                print('The sigma_0 checkbox is unchecked')
                self.DV_flags[15] = True

            if self.alpha.sender() == self.alpha.checkBox:
                print('The alpha checkbox is unchecked')
                self.DV_flags[16] = True

            if self.modulus_flag.sender() == self.modulus_flag.checkbox:
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
                self.E_A.checkBox.setEnabled(True)
                self.E_A.checkBox.setChecked(False)
                self.E_A.minimum_bound.setEnabled(True)
                self.E_A.maximum_bound.setEnabled(True)
                self.E_A.specified_value.setEnabled(False)
                self.E_A.specified_value.setText('')

            if self.slope_flag.sender() == self.slope_flag.checkbox:
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
                self.C_A.checkBox.setEnabled(True)
                self.C_A.checkBox.setChecked(False)
                self.C_A.minimum_bound.setEnabled(True)
                self.C_A.maximum_bound.setEnabled(True)
                self.C_A.specified_value.setEnabled(False)
                self.C_A.specified_value.setText('')

            if self.smooth_hardening_flag.sender() == self.smooth_hardening_flag.checkbox:
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
                self.n_2.checkBox.setEnabled(True)
                self.n_2.checkBox.setChecked(False)
                self.n_2.minimum_bound.setEnabled(True)
                self.n_2.maximum_bound.setEnabled(True)
                self.n_2.specified_value.setEnabled(False)
                self.n_2.specified_value.setText('')

                #n_3
                self.n_3.checkBox.setEnabled(True)
                self.n_3.checkBox.setChecked(False)
                self.n_3.minimum_bound.setEnabled(True)
                self.n_3.maximum_bound.setEnabled(True)
                self.n_3.specified_value.setEnabled(False)
                self.n_3.specified_value.setText('')

                #n_4
                self.n_4.checkBox.setEnabled(True)
                self.n_4.checkBox.setChecked(False)
                self.n_4.minimum_bound.setEnabled(True)
                self.n_4.maximum_bound.setEnabled(True)
                self.n_4.specified_value.setEnabled(False)
                self.n_4.specified_value.setText('')

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
        QApplication.processEvents()
        ex.tabs.setTabEnabled(2,True)
        self.changeTabs()

        error = test_optimizer_v2.main(bounds,
                                       self,
                                       ex.data_input_widget.data,
                                       ex.calibration_plotting)



    def loadDefaults(self):
        #Current order:
            #E_M, E_A, M_s, M_s-M_f, A_s, A_f - A_s, C_M, C_A, H_min,
            #H_max - H_min, k, n_1, n_2, n_3, n_4, sigma_crit, alpha
        lower_bound_defaults = [20E9,20E9,223.0,10.0,273.0,10.0,2E6,2E6,0.0,
                                0.01,1E-8,0.01,0.01,0.01,0.01,0.0,0.0]
        upper_bound_defaults = [110E9,110E9,273.0,50.0,323.0,50.0,15E6,15E6,0.03,
                                0.05,1E-6,1.0,1.0,1.0,1.0,60E6,1E-6]

        objects = [
            self.E_M,
            self.E_A,
            self.M_s,
            self.M_s_M_f,
            self.A_s,
            self.A_f_A_s,
            self.C_M,
            self.C_A,
            self.H_min,
            self.H_max_H_min,
            self.k,
            self.n_1,
            self.n_2,
            self.n_3,
            self.n_4,
            self.sigma_0,
            self.alpha,
            ]

        variable_formats = [
            "{:.2e}",
            "{:.2e}",
            "{:.0f}",
            "{:.0f}",
            "{:.0f}",
            "{:.0f}",
            "{:.2e}",
            "{:.2e}",
            "{:.2f}",
            "{:.2f}",
            "{:.2e}",
            "{:.2f}",
            "{:.2f}",
            "{:.2f}",
            "{:.2f}",
            "{:.2e}",
            "{:.2e}"
            ]

        for property_object,lower_bound,upper_bound,variable_format in \
            zip(objects,lower_bound_defaults,upper_bound_defaults,variable_formats):

            property_object.minimum_bound.setText(variable_format.format(lower_bound))
            property_object.maximum_bound.setText(variable_format.format(upper_bound))

        #delta
        self.delta.lineEdit.setText('1e-6')

        #sigma cal
        self.sigma_cal.lineEdit.setText('100e6')

        #MVF_tol
        self.MVF_tol.lineEdit.setText('1e-4')

        #number of generations
        self.gen_line.setText('15')

        #population size
        self.pop_line.setText('20')

        #number of iterations
        self.iter_line.setText('100')



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
                if not val == "":
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
        bounds.append([float(self.E_M.minimum_bound.text()),
                       float(self.E_M.maximum_bound.text())])

        #E_A
        # if self.flags['modulus_flag'] == False:
        bounds.append([float(self.E_A.minimum_bound.text()),
                       float(self.E_A.maximum_bound.text())])

        #M_s
        bounds.append([float(self.M_s.minimum_bound.text()),
                       float(self.M_s.maximum_bound.text())])

        #M_s-M_f
        bounds.append([float(self.M_s_M_f.minimum_bound.text()),
                       float(self.M_s_M_f.maximum_bound.text())])

        #A_s
        bounds.append([float(self.A_s.minimum_bound.text()),
                       float(self.A_s.maximum_bound.text())])

        #A_f - A_s
        bounds.append([float(self.A_f_A_s.minimum_bound.text()),
                       float(self.A_f_A_s.maximum_bound.text())])

        #C_M
        bounds.append([float(self.C_M.minimum_bound.text()),
                       float(self.C_M.maximum_bound.text())])

        #C_A
        # if self.flags['slope_flag'] == False:
        bounds.append([float(self.C_A.minimum_bound.text()),
                        float(self.C_A.maximum_bound.text())])

        #H_min
        bounds.append([float(self.H_min.minimum_bound.text()),
                       float(self.H_min.maximum_bound.text())])
        #H_max - H_min
        bounds.append([float(self.H_max_H_min.minimum_bound.text()),
                       float(self.H_max_H_min.maximum_bound.text())])
        #k
        bounds.append([float(self.k.minimum_bound.text()),
                       float(self.k.maximum_bound.text())])

        #n_1
        bounds.append([float(self.n_1.minimum_bound.text()),
                       float(self.n_1.maximum_bound.text())])

        #n_2
        # if self.flags['smooth_hardening_flag'] == False:
        bounds.append([float(self.n_2.minimum_bound.text()),
                       float(self.n_2.maximum_bound.text())])

        #n_3
        bounds.append([float(self.n_3.minimum_bound.text()),
                       float(self.n_3.maximum_bound.text())])

        #n_4
        bounds.append([float(self.n_4.minimum_bound.text()),
                       float(self.n_4.maximum_bound.text())])

        #sigma_crit
        bounds.append([float(self.sigma_0.minimum_bound.text()),
                       float(self.sigma_0.maximum_bound.text())])

        #alpha
        bounds.append([float(self.alpha.minimum_bound.text()),
                       float(self.alpha.maximum_bound.text())])

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


        lineEdits = [
            self.E_M.specified_value,
            self.E_A.specified_value,
            self.M_s.specified_value,
            self.M_s_M_f.specified_value,
            self.A_s.specified_value,
            self.A_f_A_s.specified_value,
            self.C_M.specified_value,
            self.C_A.specified_value,
            self.H_min.specified_value,
            self.H_max_H_min.specified_value,
            self.k.specified_value,
            self.n_1.specified_value,
            self.n_2.specified_value,
            self.n_3.specified_value,
            self.n_4.specified_value,
            self.sigma_0.specified_value,
            self.alpha.specified_value,
            ]

        for counter in range(len(DV_order)):
            if DV_order[counter] == 'E_A' and self.flags['modulus_flag'] == True:
                pass
            elif DV_order[counter] == 'C_A' and self.flags['slope_flag'] == True:
                pass
            elif DV_order[counter] in ['n_2','n_3','n_4'] and self.flags['smooth_hardening_flag'] == True:
                pass
            elif self.DV_flags[counter] == False:
                self.known_values[DV_order[counter]] = float(lineEdits[counter].text())

        self.delta = float(self.delta.lineEdit.text())
        self.sigma_cal = float(self.sigma_cal.lineEdit.text())
        self.MVF_tol = float(self.MVF_tol.lineEdit.text())

        self.num_gens = float(self.gen_line.text())
        self.pop_size = float(self.pop_line.text())
        self.num_iters = float(self.iter_line.text())

    def create_label(
            self,
            label_object,
            label_text,
            font_size,
            font_weight,
            parameter_label_width,
            parameter_label_height,
            ):


        size_policy = self.set_size_policy(
            label_object
            )
        label_object.setSizePolicy(
            size_policy
            )

        label_object.setMinimumSize(
            QtCore.QSize(
                parameter_label_width,
                parameter_label_height
                )
            )
        label_object.setMaximumSize(
            QtCore.QSize(
                parameter_label_width,
                parameter_label_height
                )
            )

        label_object.setWordWrap(True)
        label_object.setText(label_text)

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = True
            )

        label_object.setFont(font)
        label_object.setAlignment(QtCore.Qt.AlignCenter)
        label_object.setObjectName(label_text)



    def create_material_property(
            self,
            property_object,
            name,
            units,
            parameter_label_width,
            parameter_label_height,
            line_edit_width,
            line_edit_height,
            small_spacer,
            regular_spacer):

        property_object.setObjectName(str(name))

        property_object.label = textToLatex(
            r"$"+name+"$ [$\mathrm{"+str(units)+"}$]:",
            parameter_label_width,
            parameter_label_height,
            self.centralwidget
            )
        property_object.addWidget(property_object.label)

        property_object.addItem(small_spacer)

        property_object.minimum_bound = QtWidgets.QLineEdit(self.centralwidget)

        size_policy = self.set_size_policy(
            property_object.minimum_bound
            )
        property_object.minimum_bound.setSizePolicy(
            size_policy
            )
        property_object.minimum_bound.setMinimumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.minimum_bound.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.setObjectName(str(name)+"_minimum_bound")
        property_object.addWidget(property_object.minimum_bound)

        property_object.addItem(regular_spacer)

        property_object.maximum_bound = QtWidgets.QLineEdit(self.centralwidget)

        size_policy = self.set_size_policy(
            property_object.maximum_bound
            )
        property_object.maximum_bound.setSizePolicy(
            size_policy
            )
        property_object.maximum_bound.setMinimumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.maximum_bound.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.setObjectName(str(name)+"_maximum_bound")
        property_object.addWidget(property_object.maximum_bound)

        property_object.addItem(regular_spacer)

        property_object.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        property_object.checkBox.stateChanged.connect(self.uncheck)
        property_object.checkBox.setText("")
        property_object.checkBox.setObjectName(str(name)+"_checkBox")
        property_object.addWidget(property_object.checkBox)

        property_object.addItem(regular_spacer)

        property_object.specified_value = QtWidgets.QLineEdit(
            self.centralwidget
            )
        property_object.specified_value.setSizePolicy(
            size_policy
            )
        property_object.specified_value.setMinimumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.specified_value.setMaximumSize(
            QtCore.QSize(line_edit_width, line_edit_height)
            )
        property_object.setObjectName(str(name)+"_specified_value")
        property_object.addWidget(property_object.specified_value)

        property_object.addItem(regular_spacer)
        property_object.specified_value.setEnabled(False)
        property_object.checkBox.toggled.connect(
            property_object.specified_value.setEnabled
            )
        property_object.checkBox.toggled.connect(
            property_object.maximum_bound.setDisabled
            )
        property_object.checkBox.toggled.connect(
            property_object.minimum_bound.setDisabled
            )

    def create_constraint(
            self,
            constraint_object,
            name,
            text,
            text_width,
            text_height,
            font_weight,
            font_size,
            latex_flag = False):

        constraint_object.setContentsMargins(-1, -1, 5, -1)
        constraint_object.setObjectName(name)

        if latex_flag == False:
            pass
        else:
            constraint_object.label = textToLatex(
                text,
                text_width,
                text_height,
                self.centralwidget
                )

        font = self.create_font(
            font_size,
            font_weight,
            bold_flag = True,
            )

        constraint_object.label.setFont(font)
        constraint_object.label.setAlignment(
            QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter
            )
        constraint_object.label.setObjectName(name+"_label")
        constraint_object.addWidget(constraint_object.label)

        constraint_object.checkbox = QtWidgets.QCheckBox(self.centralwidget)
        constraint_object.checkbox.stateChanged.connect(self.uncheck)
        constraint_object.checkbox.setText("")
        constraint_object.checkbox.setObjectName(name+"_flag")
        constraint_object.addWidget(constraint_object.checkbox)

    def create_parameter(
            self,
            parameter_object,
            name,
            text,
            text_width,
            text_height,
            text_size,
            text_weight,
            lineEdit_width,
            lineEdit_height,
            latex_flag = False,
            ):

        parameter_object.setContentsMargins(-1, -1, 5, -1)
        parameter_object.setObjectName(name)


        # self.label_34 = QtWidgets.QLabel(self.centralwidget)
        if latex_flag == True:
            parameter_object.label = textToLatex(
                text,
                text_width,
                text_height,
                self.centralwidget
                )
        else:
            parameter_object.label = QtWidgets.QLabel(self.centralwidget)
            parameter_object.label.setText(text)
            pass

        size_policy = self.set_size_policy(
            parameter_object.label
            )
        parameter_object.label.setSizePolicy(
            size_policy
            )

        parameter_object.label.setMinimumSize(
            QtCore.QSize(
                text_width,
                0
                )
            )
        parameter_object.label.setMaximumSize(
            QtCore.QSize(
                text_width,
                16777215
                )
            )

        font = self.create_font(
            text_size,
            text_weight,
            bold_flag = True
            )

        parameter_object.label.setFont(font)

        parameter_object.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)

        parameter_object.label.setObjectName(name+"_label")
        parameter_object.addWidget(parameter_object.label)


        parameter_object.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        size_policy = self.set_size_policy(
            parameter_object.lineEdit
            )
        parameter_object.lineEdit.setSizePolicy(
            size_policy
            )

        parameter_object.lineEdit.setMinimumSize(QtCore.QSize(
            lineEdit_width,
            lineEdit_height
            )
            )
        parameter_object.lineEdit.setMaximumSize(
            QtCore.QSize(
                lineEdit_width,
                lineEdit_height
                )
            )
        parameter_object.lineEdit.setObjectName(name+"_lineEdit")
        parameter_object.addWidget(parameter_object.lineEdit)




    def set_size_policy(
            self,
            lineEdit,
            ):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            lineEdit.sizePolicy().hasHeightForWidth()
            )
        return sizePolicy

    def create_font(
            self,
            font_size,
            font_weight,
            bold_flag = False,
            ):
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(bold_flag)
        font.setWeight(font_weight)

        return font


    # # Questionable if I need this.
    # @pyqtSlot()
    # def on_click(self):
    #     print("\n")
    #     for currentQTableWidgetItem in self.tableWidget.selectedItems():
    #         print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())

#%% Data input widget
class DataInputWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget,self).__init__(parent)
        self.main_layout = QGridLayout(self)
        self.main_layout.setSpacing(20)
        self.setLayout(self.main_layout)
        self.files = []
        self.data = {}

        #FONTS
        title_font = QFont()
        title_font.setBold(True)
        title_font.setPointSize(12)

        bold_normal_font = QFont()
        bold_normal_font.setBold(True)
        bold_normal_font.setPointSize(10)

        table_font = QFont()
        table_font.setPointSize(8)

        self.bold_table_font = QFont()
        self.bold_table_font.setBold(True)
        self.bold_table_font.setPointSize(8)

        self.title = QLabel(self)
        self.title.setText('File I/O')
        self.title.setFont(title_font)
        self.select_files_label = QLabel(self)
        self.select_files_label.setText('Select files to analyze:')
        self.select_files_label.setFont(bold_normal_font)
        self.files_button = QPushButton(self)
        self.files_button.setText('Open Files')
        self.files_display = QLabel(self)
        self.files_display.setText('')
        self.header_skips_label = QLabel(self)
        self.header_skips_label.setText('Header rows to skip:')
        self.skips = QSpinBox(self)
        self.skips.setMinimum(0)
        self.skips.setMaximum(999)
        self.skip_units = QLabel(self)
        self.skip_units.setText('row(s)')
        self.temp_data_col = QLabel(self)
        self.temp_data_col.setText('Column for Temperature data:')
        self.temp_col = QSpinBox(self)
        self.temp_col.setMinimum(1)
        self.temp_col.setMaximum(999)
        self.temp_units = QComboBox(self)
        self.temp_units.addItems(['[°C]', '[°F]', '[K]'])
        self.strain_data_col = QLabel(self)
        self.strain_data_col.setText('Column for Strain data:')
        self.strain_col = QSpinBox(self)
        self.strain_col.setMinimum(1)
        self.strain_col.setMaximum(999)
        self.strain_units = QComboBox(self)
        self.strain_units.addItems(['[mm/mm]', '[%]'])
        self.stress_data_col = QLabel(self)
        self.stress_data_col.setText('Column for Stress data:')
        self.stress_col = QSpinBox(self)
        self.stress_col.setMinimum(1)
        self.stress_col.setMaximum(999)
        self.stress_units = QComboBox(self)
        self.stress_units.addItems(['[MPa]', '[Pa]', '[psi]'])
        self.preview = QTableWidget(self)
        self.preview.setRowCount(100)
        self.preview.setColumnCount(3)
        self.preview.setDragDropOverwriteMode(False)
        self.preview.setFont(table_font)
        self.preview.setSelectionMode(QAbstractItemView.NoSelection)
        self.preview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.preview.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.preview.setFrameShape(QFrame.StyledPanel)
        self.preview.setFrameShadow(QFrame.Plain)
        self.preview.setLineWidth(1)
        self.preview.setMidLineWidth(0)
        self.preview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.preview.setAutoScrollMargin(16)
        self.preview.setShowGrid(True)
        self.preview.setGridStyle(QtCore.Qt.SolidLine)
        self.preview.setWordWrap(False)
        self.preview.setCornerButtonEnabled(True)
        self.preview.setTabKeyNavigation(False)
        self.preview.setProperty("showDropIndicator", False)
        self.preview.verticalHeader().setVisible(False)
        self.asterisk = QLabel(self)
        self.asterisk.setText('*All files must be formatted the same')

        self.keys = QHBoxLayout(self)
        # self.spacer = QSpacerItem()
        # self.spacer2 = QSpacerItem()
        # self.spacer3 = QSpacerItem()
        # self.spacer4 = QSpacerItem()
        min_color_height = 20
        max_color_height = 50

        min_color_width = 20
        max_color_width = 50

        self.temp_color = QLabel(self)
        self.temp_color.setStyleSheet('background-color:rgb(0, 185, 80)')
        self.temp_color.setMinimumSize(QtCore.QSize(min_color_width, min_color_height))
        self.temp_color.setMaximumSize(QtCore.QSize(max_color_width, max_color_height))
        self.temp_key = QLabel(self)
        self.temp_key.setText('Temperature')
        self.strain_color = QLabel(self)
        self.strain_color.setStyleSheet('background-color:rgb(240, 228, 50)')
        self.strain_color.setMinimumSize(QtCore.QSize(min_color_width, min_color_height))
        self.strain_color.setMaximumSize(QtCore.QSize(max_color_width, max_color_height))
        self.strain_key = QLabel(self)
        self.strain_key.setText('Strain')
        self.stress_color = QLabel(self)
        self.stress_color.setStyleSheet('background-color:rgb(86, 200, 233)')
        self.stress_color.setMinimumSize(QtCore.QSize(min_color_width, min_color_height))
        self.stress_color.setMaximumSize(QtCore.QSize(max_color_width, max_color_height))
        self.stress_key = QLabel(self)
        self.stress_key.setText('Stress')
        # self.keys.addSpacerItem(self.spacer)
        self.keys.addWidget(self.temp_color)
        self.keys.addWidget(self.temp_key)
        # self.keys.addSpacerItem(self.spacer2)
        self.keys.addWidget(self.strain_color)
        self.keys.addWidget(self.strain_key)
        # self.keys.addSpacerItem(self.spacer3)
        self.keys.addWidget(self.stress_color)
        self.keys.addWidget(self.stress_key)
        # self.keys.addSpacerItem(self.spacer4)

        #Push buttons
        font_size = 14
        font_weight = 75
        font = QtGui.QFont()
        font.setPointSize(font_size)
        font.setBold(False)
        font.setWeight(font_weight)

        self.buttons = QtWidgets.QHBoxLayout(self)
        self.buttons.setObjectName("buttons")
        self.load_button = QtWidgets.QPushButton(self)
        self.load_button.setMinimumSize(QtCore.QSize(100, 100))
        # self.load_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.load_button.setObjectName("load_button")
        self.load_button.setText('Load Data')
        self.load_button.setFont(font)
        self.load_button.setEnabled(False)

        self.continue_button = QtWidgets.QPushButton(self)
        self.continue_button.setMinimumSize(QtCore.QSize(100, 100))
        # self.continue_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.continue_button.setObjectName("continue_button")
        self.continue_button.setText('Continue to calibration')
        self.continue_button.setFont(font)
        self.continue_button.setEnabled(False)

        self.main_layout.addWidget(self.title, 0, 0)
        self.main_layout.addWidget(self.select_files_label, 1, 0)
        self.main_layout.addWidget(self.files_button, 1, 1, 1, 2)
        self.main_layout.addWidget(self.files_display, 1, 4)
        self.main_layout.addWidget(self.header_skips_label, 2, 0)
        self.main_layout.addWidget(self.skips, 2, 2)
        self.main_layout.addWidget(self.skip_units, 2, 3)
        self.main_layout.addWidget(self.temp_data_col, 3, 0)
        self.main_layout.addWidget(self.temp_col, 3, 2)
        self.main_layout.addWidget(self.temp_units, 3, 3)
        self.main_layout.addWidget(self.strain_data_col, 4, 0)
        self.main_layout.addWidget(self.strain_col, 4, 2)
        self.main_layout.addWidget(self.strain_units, 4, 3)
        self.main_layout.addWidget(self.stress_data_col, 5, 0)
        self.main_layout.addWidget(self.stress_col, 5, 2)
        self.main_layout.addWidget(self.load_button, 7, 0,3,2)
        self.main_layout.addWidget(self.continue_button, 7, 2,3,2)
        self.main_layout.addWidget(self.stress_units, 5, 3)
        self.main_layout.addWidget(self.preview, 2, 4, 6, 6)
        self.main_layout.addWidget(self.asterisk, 6, 0, 1, 1)
        self.main_layout.addLayout(self.keys, 8, 4, 1, 4)



        #SIGNALS
        self.files_button.clicked.connect(self.openFiles)
        self.load_button.clicked.connect(self.loadFiles)
        self.continue_button.clicked.connect(self.changeTabs)
        self.skips.valueChanged.connect(self.updatePreview)
        self.temp_col.valueChanged.connect(self.updatePreview)
        self.strain_col.valueChanged.connect(self.updatePreview)
        self.stress_col.valueChanged.connect(self.updatePreview)

    #FUNCTIONS
    def openFiles(self):
        file_browser = QFileDialog()
        file_browser.setFileMode(QFileDialog.ExistingFiles)
        self.files = file_browser.getOpenFileNames(self, 'Browse Files', '', 'All Files(*)')[0]

        text = ''
        for file in self.files:
            filename = file[file.rindex('/') + 1:]
            text += filename + ', '
        self.files_display.setText(text[:-2])

        # getting inputs
        skip_rows = self.skips.value()
        temp_col = self.temp_col.value() - 1
        strain_col = self.strain_col.value() - 1
        stress_col = self.stress_col.value() - 1

        overlap = False
        if temp_col == strain_col or temp_col == stress_col or strain_col == stress_col:
            overlap = True

        if overlap == False:
            self.load_button.setEnabled(True)
        else:
            self.load_button.setEnabled(False)

        # loading data
        df_preview = pd.read_csv(self.files[0], nrows=100, header=None, skiprows=skip_rows, encoding='utf-8',
                                 sep=None, engine='python')
        col_labels = [str(x) for x in df_preview.columns]
        self.preview.setColumnCount(len(col_labels))
        self.preview.setHorizontalHeaderLabels(col_labels)
        for i in range(len(col_labels)):
            self.preview.horizontalHeaderItem(i).setFont(self.bold_table_font)

        # filling table
        for i in range(len(df_preview.index)):
            for j in range(len(col_labels)):
                try:
                    item = QTableWidgetItem('{:.3f}'.format(df_preview.iloc[i, j]))
                except:
                    item = QTableWidgetItem(df_preview.iloc[i, j])

                # colors
                if j in [temp_col, stress_col, strain_col] and not overlap:
                    if j == temp_col:
                        item.setBackground(QColor(0, 185, 80))
                    elif j == strain_col:
                        item.setBackground(QColor(240, 228, 50))
                    elif j == stress_col:
                        item.setBackground(QColor(86, 200, 233))

                self.preview.setItem(i, j, item)


    def loadFiles(self):
        # getting inputs
        skip_rows = self.skips.value()
        temp_col = self.temp_col.value() - 1
        strain_col = self.strain_col.value() - 1
        stress_col = self.stress_col.value() - 1
        temp_units = self.temp_units.currentText()
        strain_units = self.strain_units.currentText()
        stress_units = self.stress_units.currentText()
        overlap = False
        if temp_col == strain_col or temp_col == stress_col or strain_col == stress_col:
            overlap = True



        # packaging data
        if not overlap:
            data = {'num_experiments': len(self.files)}
            for i, file in enumerate(self.files):
                df = pd.read_csv(file, header=None, skiprows=skip_rows, encoding='utf-8',
                                     sep=None, engine='python')

                # df = df[[df.columns[strain_col], df.columns[temp_col], df.columns[stress_col]]]

                #Re-organize data to go from cold to hot
                eps = df[df.columns[strain_col]].to_numpy()
                sigma = df[df.columns[stress_col]].to_numpy()
                T = df[df.columns[temp_col]].to_numpy()

                min_T = T.min()
                I = np.argmin(T)

                T = np.concatenate((T[I:],T[0:I+1]))
                sigma = np.concatenate((sigma[I:],sigma[0:I+1]))
                eps = np.concatenate((eps[I:],eps[0:I+1]))

                df = pd.DataFrame({"strain":eps, "temperature":T, "stress":sigma})

                # converting stress
                if stress_units == '[psi]':
                    df["stress"] = df["stress"] * 6894.7572931783
                elif stress_units == '[MPa]':
                    df["stress"] = df["stress"] * 1E6

                # converting temperature
                if temp_units == '[°C]':
                    df["temperature"] = df["temperature"] + 273.15
                elif temp_units == '[°F]':
                    df["temperature"] = (df["temperature"] - 32) * 5/9 + 273.15

                # converting strain
                if strain_units == '[%]':
                    df["strain"] = df["strain"] * 100

                # column_names = ['strain','temperature','stress']
                # df.columns = column_names

                data['exp_{}'.format(i)] = df

            self.data = data
            ex.tabs.setTabEnabled(1,True)
            self.continue_button.setEnabled(True)

    def changeTabs(self):
        ex.tabs.setCurrentIndex(1)



    def updatePreview(self):
        if len(self.files) != 0:
            # getting inputs
            skip_rows = self.skips.value()
            temp_col = self.temp_col.value() - 1
            strain_col = self.strain_col.value() - 1
            stress_col = self.stress_col.value() - 1
            temp_units = self.temp_units.currentText()
            strain_units = self.strain_units.currentText()
            stress_units = self.stress_units.currentText()
            overlap = False
            if temp_col == strain_col or temp_col == stress_col or strain_col == stress_col:
                overlap = True

            if overlap == False:
                self.load_button.setEnabled(True)
            else:
                self.load_button.setEnabled(False)

            # loading data
            df_preview = pd.read_csv(self.files[0], nrows=100, header=None, skiprows=skip_rows, encoding='utf-8',
                                     sep=None, engine='python')
            col_labels = [str(x) for x in df_preview.columns]
            if not overlap:
                col_labels[temp_col] = 'Temperature'
                col_labels[strain_col] = 'Strain'
                col_labels[stress_col] = 'Stress'
            self.preview.setColumnCount(len(col_labels))
            self.preview.setHorizontalHeaderLabels(col_labels)
            for i in range(len(col_labels)):
                self.preview.horizontalHeaderItem(i).setFont(self.bold_table_font)

            # filling table
            for i in range(len(df_preview.index)):
                for j in range(len(col_labels)):
                    try:
                        item = QTableWidgetItem('{:.3f}'.format(df_preview.iloc[i, j]))
                    except:
                        item = QTableWidgetItem(df_preview.iloc[i, j])

                    # colors
                    if j in [temp_col, stress_col, strain_col] and not overlap:
                        if j == temp_col:
                            item.setBackground(QColor(0, 185, 80))
                        elif j == strain_col:
                            item.setBackground(QColor(240, 228, 50))
                        elif j == stress_col:
                            item.setBackground(QColor(86, 200, 233))

                    self.preview.setItem(i, j, item)


#%% Calibration window widget
class CalibrationWindow(QtWidgets.QWidget):
    def __init__(self,parent):
        super(QtWidgets.QWidget,self).__init__(parent)

        rc.update({'font.size': 18})

        # SETUP
        #self.setWindowTitle('Calibration Window')
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        # CANVASES/GRAPHS
        self.opt_progress_graph = Figure()
        self.opt_progress_canvas = FigureCanvas(self.opt_progress_graph)
        self.opt_progress_toolbar = NavigationToolbar(self.opt_progress_canvas, self)

        self.dv_vals_graph = Figure()
        self.dv_vals_canvas = FigureCanvas(self.dv_vals_graph)
        self.dv_vals_toolbar = NavigationToolbar(self.dv_vals_canvas, self)
        keys = ['E_M', 'E_A', 'M_s', 'M_s - M_f', 'A_s', 'A_f - A_s', 'C_M', 'C_A', 'H_min', 'H_max - H_min', 'k',
                'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']
        y = np.zeros(len(keys))
        self.ax_dv_vals = self.dv_vals_graph.add_subplot(111)
        self.bars = self.ax_dv_vals.bar(keys, y, width=0.5)
        self.ax_dv_vals.set_ylim([-0.1, 1.1])
        self.ax_dv_vals.text(0.05,-0.066,'Lower bound')
        self.ax_dv_vals.text(0.05,1.033,'Upper bound')
        self.ax_dv_vals.set_ylabel('Normalized material property, -')
        self.ax_dv_vals.axhline(0,color='black',linestyle='--')
        self.ax_dv_vals.axhline(1,color='black',linestyle='--')

        self.dv_vals_graph.autofmt_xdate(rotation=45, ha='right')

        self.temp_strain_graph = Figure()
        self.ax_temp_strain = self.temp_strain_graph.add_subplot(111)
        self.temp_strain_canvas = FigureCanvas(self.temp_strain_graph)
        self.temp_strain_toolbar = NavigationToolbar(self.temp_strain_canvas, self)
        self.ax_temp_strain.set_autoscaley_on(True)
        self.ax_temp_strain.set_xlabel('Temperature, K')
        self.ax_temp_strain.set_ylabel('Strain, mm/mm')
        self.ax_temp_strain.grid()

        self.phase_diagram_graph = Figure()
        self.ax_phase_digram = self.phase_diagram_graph.add_subplot(111)
        self.phase_diagram_canvas = FigureCanvas(self.phase_diagram_graph)
        self.phase_diagram_toolbar = NavigationToolbar(self.phase_diagram_canvas, self)

        # ADDING TO WINDOW
        self.main_layout.addWidget(self.opt_progress_canvas, 0, 0)
        self.main_layout.addWidget(self.opt_progress_toolbar, 1, 0)
        self.main_layout.addWidget(self.dv_vals_canvas, 2, 0)
        self.main_layout.addWidget(self.dv_vals_toolbar, 3, 0)
        self.main_layout.addWidget(self.temp_strain_canvas, 0, 1)
        self.main_layout.addWidget(self.temp_strain_toolbar, 1, 1)
        self.main_layout.addWidget(self.phase_diagram_canvas, 2, 1)
        self.main_layout.addWidget(self.phase_diagram_toolbar, 3, 1)
        self.show()


    def run(self, bounds, knownValues, DV_flags):
        QApplication.processEvents()
        main(bounds, knownValues, DV_flags, self)


    def updateOptProgress(self, gen, min_func_val, avg, std):
        self.opt_progress_graph.clear()
        ax = self.opt_progress_graph.add_subplot(111)
        ax.plot(gen, min_func_val, color='red', label='Current best solution')
        ax.plot(gen, avg, label='Average solution',color='black')
        #ax.fill_between(gen, [x + y for x,y in zip(avg, std)], [x - y for x,y in zip(avg, std)],
        #                                  color='#888888', alpha=0.2)
        ax.legend(loc='best')
        ax.set_xlim([0, max(gen) + 1])
        ax.set_xlabel('Generation')
        ax.set_ylabel('Error')
        self.opt_progress_canvas.draw()
        self.opt_progress_canvas.flush_events()


    def updateDVVals(self, dv,DV_flags):
        count = 0
        for i, bar in enumerate(self.bars):
            if DV_flags[i] == True:
                bar.set_height(dv[count])
                count +=1
            else:
                pass
                # bar.set_height(1)
                # bar.set_color('red')

        self.dv_vals_canvas.draw()
        self.dv_vals_canvas.flush_events()


    def plotExperimental(self, x, y, numExps):
        self.ax_temp_strain.clear()
        self.ax_temp_strain.plot(x, y, 'bo',label='Experiment')
        self.temp_strain_canvas.draw()
        self.temp_strain_canvas.flush_events()

        self.lines = [self.ax_temp_strain.plot([], [], 'r-')[0] for _ in range(numExps)]


    def updateTempStrain(self, temp, strain, numExps):
        for i in range(numExps):
            self.lines[i].set_xdata(temp[i])
            self.lines[i].set_ydata(strain[i])

        self.lines[i].set(label='Model prediction')
        self.ax_temp_strain.legend(loc='best')
        self.ax_temp_strain.set_xlabel('Temperature, K',fontsize=18)
        self.ax_temp_strain.set_ylabel('Strain, mm/mm',fontsize=18)

        self.ax_temp_strain.relim()
        self.ax_temp_strain.autoscale_view()

        self.temp_strain_canvas.draw()
        self.temp_strain_canvas.flush_events()


    def updatePhaseDiagram(self, P, sigma_inp):
        self.ax_phase_digram.clear()
        plot_phase_diagram(P, sigma_inp, self.ax_phase_digram)

        self.phase_diagram_canvas.draw()
        self.phase_diagram_canvas.flush_events()






if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ex = App()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    #MainWindow.show()
    sys.exit(app.exec_())