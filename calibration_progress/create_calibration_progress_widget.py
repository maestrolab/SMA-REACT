'''
calibration progress widget

updates all the dynamic plots on the calibration progress tab.
'''
import cgitb

import numpy as np

from PyQt5 import QtCore, QtWidgets

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import rcParams as rc

from .phase_diagram import plot_phase_diagram

cgitb.enable(format="text")

#%% Calibration window widget
class CalibrationProgressWidget(QtWidgets.QWidget):
    '''
    This widget defines all of the dynamic plots to track calibration progress.
    All of the plotting functions should remain in this class.
    '''
    def __init__(self):
        '''
        Initialize the tab.

        Returns
        -------
        None.

        '''
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
        self.main_layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.main_layout)

        # CANVASES/GRAPHS
        self.opt_progress_graph = Figure()
        self.opt_progress_canvas = FigureCanvas(self.opt_progress_graph)
        self.opt_progress_toolbar = NavigationToolbar(self.opt_progress_canvas, self)

        self.design_variables_graph = Figure()
        self.design_variables_canvas = FigureCanvas(self.design_variables_graph)
        self.design_variables_toolbar = NavigationToolbar(
            self.design_variables_canvas,
            self
            )
        #FIXME Make this dynamically linked to the model formulation.
        keys = ['E_M', 'E_A', 'M_s', 'M_s - M_f', 'A_s', 'A_f - A_s', \
                'C_M', 'C_A', 'H_min', 'H_max - H_min', 'k', \
                'n_1', 'n_2', 'n_3', 'n_4', 'sig_crit', 'alpha']
        y = np.zeros(len(keys))
        self.ax_design_variables = self.design_variables_graph.add_subplot(
            111,
            )
        self.bars = self.ax_design_variables.bar(keys, y, width=0.5)
        self.ax_design_variables.set_ylim([-0.1, 1.1])
        self.ax_design_variables.text(0.05,-0.066,'Lower bound')
        self.ax_design_variables.text(0.05,1.033,'Upper bound')
        self.ax_design_variables.set_ylabel('Normalized material property, -')
        self.ax_design_variables.axhline(0,color='black',linestyle='--')
        self.ax_design_variables.axhline(1,color='black',linestyle='--')

        self.design_variables_graph.autofmt_xdate(rotation=45, ha='right')

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

        #Add an export button at the bottom.
        self.export_button = QtWidgets.QPushButton(self)
        self.export_button.setMinimumSize(QtCore.QSize(100, 100))
        # self.load_button.setMaximumSize(QtCore.QSize(100, 16777215))
        self.export_button.setObjectName("export_button")
        self.export_button.setText('Export Calibration Data')
        # self.load_button.setFont(font)
        self.export_button.setEnabled(False)

        # ADDING TO WINDOW
        self.main_layout.addWidget(self.opt_progress_canvas, 0, 0)
        self.main_layout.addWidget(self.opt_progress_toolbar, 1, 0)
        self.main_layout.addWidget(self.design_variables_canvas, 2, 0)
        self.main_layout.addWidget(self.design_variables_toolbar, 3, 0)
        self.main_layout.addWidget(self.temp_strain_canvas, 0, 1)
        self.main_layout.addWidget(self.temp_strain_toolbar, 1, 1)
        self.main_layout.addWidget(self.phase_diagram_canvas, 2, 1)
        self.main_layout.addWidget(self.phase_diagram_toolbar, 3, 1)
        self.main_layout.addWidget(self.export_button,4,0,2,1)

        # self.export_button.clicked.connect(self.exportSolution)


        self.show()


    # def run(self, bounds, knownValues, design_variable_flags):
    #     QApplication.processEvents()
    #     main(bounds, knownValues, design_variable_flags, self)
        # self.export_button.setEnabled(True)


    def update_opt_progress(self, gen, min_func_val, avg, std=None):
        '''
        Plot the current best solution and average solution (per
        generation).

        Parameters
        ----------
        gen : list
            list of all generation numbers.
        min_func_val : list
            list of all current bests as a function of generation.
        avg : list
            list of all averages as a function of generation.
        std : list
            list of all standard deviations as a function of generation.
            Currently not implemented, but could be re-implemented by
            using the fill_between plotting command in matplotlib.

        Returns
        -------
        None.

        '''
        self.opt_progress_graph.clear()
        ax = self.opt_progress_graph.add_subplot(
            111,
            )
        ax.plot(gen, min_func_val, color='red', label='Current best solution')
        ax.plot(gen, avg, label='Average solution',color='black')
        if std is not None:
            pass
            #FIXME experimental, use caution.
            # ax.fill_between(
            #     gen,
            #     [x + y for x,y in zip(avg, std)],
            #     [x - y for x,y in zip(avg, std)],
            #     color='#888888',
            #     alpha=0.2
            #     )
        ax.legend(loc='best')
        ax.set_xlim([0, max(gen) + 1])
        ax.set_xlabel('Generation')
        ax.set_ylabel('Error')
        self.opt_progress_canvas.draw()
        self.opt_progress_graph.tight_layout()
        self.opt_progress_canvas.flush_events()


    def update_design_variable_vals(
            self,
            design_variables,
            design_variable_flags
            ):
        '''
        Update normalized values for the design variables on a bar chart.

        Parameters
        ----------
        design_variables : list
            list of all normalized [0,1] design variable values.
        design_variable_flags : list of bool
            list to signify if a design variable is active.

        Returns
        -------
        None.

        '''
        count = 0
        for i, bar_plot in enumerate(self.bars):
            if design_variable_flags[i] == True:
                bar_plot.set_height(design_variables[count])
                count +=1
            else:
                pass
                # bar.set_height(1)
                # bar.set_color('red')

        self.design_variables_canvas.draw()
        self.design_variables_canvas.flush_events()


    def plot_experimental(self, x, y, num_exps):
        '''
        Plots the experimental data

        Parameters
        ----------
        x : np array
            x-data (temperature)
        y : np array
            y-data (strain)
        num_exps : int
            number of total experiments being analyzed

        Returns
        -------
        None.

        '''
        self.ax_temp_strain.clear()
        self.ax_temp_strain.plot(x, y, 'bo',label='Experiment')
        self.temp_strain_canvas.draw()
        self.temp_strain_canvas.flush_events()

        self.lines = [self.ax_temp_strain.plot([], [], 'r-')[0] for _ in range(num_exps)]


    def update_temp_strain(self, temp, strain, num_exps):
        '''
        Update the model prediction of the temperature strain plot.

        Parameters
        ----------
        temp : numpy array
            temperature array (num_experiments, number of sample points)
        strain : numpy array
            strain array (num_experiments, number of sample points)
        num_exps : int
            number of total experiments being analyzed

        Returns
        -------
        None.

        '''
        for i in range(num_exps):
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


    def update_phase_diagram(self, P, sigma_inp):
        '''
        updates the dynamic plot for the phase diagram.

        Parameters
        ----------
        P : dict
            material properties dictionary
        sigma_inp : list
            [lower_stress, upper_stress] to plot

        Returns
        -------
        None.

        '''
        self.ax_phase_digram.clear()
        plot_phase_diagram(P, sigma_inp, self.ax_phase_digram)

        self.phase_diagram_canvas.draw()
        self.phase_diagram_canvas.flush_events()
