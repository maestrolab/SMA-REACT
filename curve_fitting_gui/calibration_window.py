# IMPORT STATEMENTS
from PyQt5.QtWidgets import QWidget, QGridLayout, QApplication
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure


class calibrationWindow(QWidget):
    def __init__(self):
        super().__init__()

        # SETUP
        self.setWindowTitle('Calibration Window')
        self.main_layout = QGridLayout(self)
        self.setLayout(self.main_layout)

        # CANVASES/GRAPHS
        self.opt_progress_graph = Figure()
        self.ax_opt_progress = self.opt_progress_graph.add_subplot(111)
        self.opt_progress_canvas = FigureCanvas(self.opt_progress_graph)
        self.opt_progress_toolbar = NavigationToolbar(self.opt_progress_canvas, self)

        self.dv_vals_graph = Figure()
        self.ax_dv_vals = self.dv_vals_graph.add_subplot(111)
        self.dv_vals_canvas = FigureCanvas(self.dv_vals_graph)
        self.dv_vals_toolbar = NavigationToolbar(self.dv_vals_canvas, self)

        self.temp_strain_graph = Figure()
        self.ax_temp_strain = self.temp_strain_graph.add_subplot(111)
        self.temp_strain_canvas = FigureCanvas(self.temp_strain_graph)
        self.temp_strain_toolbar = NavigationToolbar(self.temp_strain_canvas, self)

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



if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = calibrationWindow()
    window.show()
    sys.exit(app.exec())