"""
Shape Memory Alloy Rendering of Experimental Analysis and Calibration Tool
(SMA-REACT)

Main launch script

Last updated: December 12th, 2023 (see GitHub for updates)
"""
import cgitb


from PyQt5 import QtGui, QtWidgets

from calibration.run_calibration_GUI import (
    CalibrationParametersWidget,
    )

from data_input.create_data_input import (
    DataInputWidget
    )

from calibration_progress.create_calibration_progress_widget import (
    CalibrationProgressWidget
    )

from calibration.model_funcs.test_optimizer_v2 import main



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
        # print(rect)
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


        self.tabs = QtWidgets.QTabWidget()
        self.tabs.resize(self.width,self.height)
        
        
        self.calibration_parameters_widget = CalibrationParametersWidget()

        self.data_input_widget = DataInputWidget()

        self.calibration_plotting_widget = CalibrationProgressWidget()

        self.tabs.addTab(
            self.data_input_widget,
            'Data Input'
            )
        self.tabs.addTab(
            self.calibration_parameters_widget,
            "Material Property Calibration"
            )


        self.tabs.addTab(
            self.calibration_plotting_widget,
            "Calibration Plotting Utility"
            )


        self.setCentralWidget(self.tabs)

        self.tabs.setTabEnabled(1,False)
        self.tabs.setTabEnabled(2,False)
        
        #connect the continue button to changing a tab
        self.data_input_widget.continue_button.clicked.connect(
            lambda: self.changeTabs(
                index=1
                )
            )
        
        #connect the calibration button to the optimization
        self.calibration_parameters_widget.pushButton.clicked.connect(self.runCalibration)

        self.show()
        
    def changeTabs(
            self,
            index,
            ):
        self.tabs.setTabEnabled(index,True)
        self.tabs.setCurrentIndex(index)
        
    def runCalibration(self):
        self.calibration_parameters_widget.getSpecifiedValues()
        bounds = self.calibration_parameters_widget.getBounds()
        print(self.calibration_parameters_widget.known_values)
        
        app.processEvents()
        
        self.changeTabs(index=2)
        # self.tabs.setTabEnabled(2,True)
        # self.tabs.setCurrentIndex(2)
        
        error = main(
            bounds,
            self.calibration_parameters_widget,
            self.data_input_widget.data,
            self.calibration_plotting_widget
            )



if __name__ == "__main__":
    import sys
    
    cgitb.enable(format="text") #for more detailed traceback reports
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ex = App()
    #ui = Ui_MainWindow()
    #ui.setupUi(MainWindow)
    # MainWindow.show()

    sys.exit(app.exec_())