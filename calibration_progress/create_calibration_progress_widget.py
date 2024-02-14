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

from PyQt5.QtWidgets import QFileDialog, QMessageBox, QTabWidget,\
    QGridLayout, QLabel, QPushButton, QApplication, QSpinBox, QComboBox, QTableWidget, \
    QHBoxLayout, QAbstractItemView, QFrame, QTableWidgetItem
from PyQt5.QtGui import QFont, QColor

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import rcParams as rc

from .phase_diagram import plot_phase_diagram

import cgitb
cgitb.enable(format="text")

#%% Calibration window widget
class CalibrationProgressWidget(QtWidgets.QWidget):
    def __init__(self):
        super(QtWidgets.QWidget,self).__init__()

        rc.update(
            {'font.size': 18,
             'font.family':"sans-serif",
             'font.sans-serif':"Arial",
             "text.usetex":False,
             }
            )
        # rc["font.serif"] = "Palatino Linotype"
        # rc["font.family"] = "serif"
        # rc["text.usetex"] = True

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
        #FIXME Pull this from something in the calibration parameters widget. 
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






# if __name__ == "__main__":
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     MainWindow = QtWidgets.QMainWindow()
#     ex = App()
#     #ui = Ui_MainWindow()
#     #ui.setupUi(MainWindow)
#     #MainWindow.show()
#     sys.exit(app.exec_())