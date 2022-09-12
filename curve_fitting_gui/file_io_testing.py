import pandas as pd
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton, QApplication, QSpinBox, QComboBox, QTableWidget, \
    QHBoxLayout, QAbstractItemView, QFrame, QFileDialog, QTableWidgetItem
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtGui import QColor
import pandas as pd

import cgitb
cgitb.enable(format="text")


class fileIO(QWidget):
    def __init__(self):
        super().__init__()

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
        self.strain_units.addItems(['[%]', '[fraction]'])
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
        self.temp_color = QLabel(self)
        self.temp_color.setStyleSheet('background-color:rgb(0, 185, 80)')
        self.temp_key = QLabel(self)
        self.temp_key.setText('Temperature')
        self.strain_color = QLabel(self)
        self.strain_color.setStyleSheet('background-color:rgb(240, 228, 50)')
        self.strain_key = QLabel(self)
        self.strain_key.setText('Strain')
        self.stress_color = QLabel(self)
        self.stress_color.setStyleSheet('background-color:rgb(86, 200, 233)')
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
        self.main_layout.addWidget(self.stress_units, 5, 3)
        self.main_layout.addWidget(self.preview, 2, 4, 6, 6)
        self.main_layout.addWidget(self.asterisk, 6, 0, 1, 4)
        self.main_layout.addLayout(self.keys, 8, 4, 1, 4)

        #SIGNALS
        self.files_button.clicked.connect(self.openFiles)
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
        temp_units = self.temp_units.currentText()
        strain_units = self.strain_units.currentText()
        stress_units = self.stress_units.currentText()
        overlap = False
        if temp_col == strain_col or temp_col == stress_col or strain_col == stress_col:
            overlap = True

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

        # packaging data
        if not overlap:
            data = {'num_experiments': len(self.files)}
            for i, file in enumerate(self.files):
                df = pd.read_csv(file, header=None, skiprows=skip_rows, encoding='utf-8',
                                     sep=None, engine='python')
                df = df[[df.columns[strain_col], df.columns[temp_col], df.columns[stress_col]]]

                # converting stress
                if stress_units == '[psi]':
                    df[stress_col] = df[stress_col] * 6894.7572931783
                elif stress_units == '[MPa]':
                    df[stress_col] = df[stress_col] * 10E6

                # converting temperature
                if temp_units == '[°C]':
                    df[temp_col] = df[temp_col] + 273.15
                elif temp_units == '[°F]':
                    df[temp_col] = (df[temp_col] - 32) * 5/9 + 273.15

                # converting strain
                if strain_units == '[%]':
                    df[strain_col] = df[strain_col] * 100

                data['exp_{}'.format(i)] = df

            self.data = data



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

            # packaging data
            if not overlap:
                data = {'num_experiments': len(self.files)}
                for i, file in enumerate(self.files):
                    df = pd.read_csv(file, header=None, skiprows=skip_rows, encoding='utf-8',
                                     sep=None, engine='python')
                    df = df[[df.columns[strain_col], df.columns[temp_col], df.columns[stress_col]]]

                    # converting stress
                    if stress_units == '[psi]':
                        df[stress_col] = df[stress_col] * 6894.7572931783
                    elif stress_units == '[MPa]':
                        df[stress_col] = df[stress_col] * 10E6

                    # converting temperature
                    if temp_units == '[°C]':
                        df[temp_col] = df[temp_col] + 273.15
                    elif temp_units == '[°F]':
                        df[temp_col] = (df[temp_col] - 32) * 5 / 9 + 273.15

                    # converting strain
                    if strain_units == '[%]':
                        df[strain_col] = df[strain_col] * 100

                    data['exp_{}'.format(i)] = df

                self.data = data




class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)
        self.file_io = fileIO()
        self.main_layout.addWidget(self.file_io, 0, 0)



if __name__ == "__main__":
    import sys
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())