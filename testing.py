# # from data_reader import reader
# # import pandas as pd
# # import datetime
# #
# # with open("Fluke Jacob 3 cycles.csv") as file:
# #     # FINDING START TIME
# #     line = file.readline()
# #     while not "Start Time" in line:
# #         line = file.readline()
# #     stime_index = line.split(",").index("Start Time")
# #     line = file.readline()
# #     start_time = line.split(",")[stime_index]
# #
# #     # FINDING THE LABELS
# #     while not "Duration" in line:
# #         line = file.readline()
# #     labels = line.split(",")
# #     labels = [x.strip() for x in labels]
# #
# #     # PARSING DATA
# #     data = {}
# #     for label in labels:
# #         data[label] = []
# #
# #     while (True):
# #         line = file.readline()
# #         vals = line.split(",")
# #         blank = True
# #         for i in range(len(vals)):
# #             if not blank:
# #                 break
# #             if vals[i].strip() != "":
# #                 blank = False
# #         if blank:
# #             break
# #         # if len(vals) != len(labels):
# #         #     break
# #         for i in range(len(vals)):
# #             data[labels[i]].append(vals[i].strip())
# #
# #     # DELETING UNNECESSARY DATA
# #     copy_dict = {}
# #     for label in data.keys():
# #         if label != "":
# #             copy_dict[label] = data[label]
# #
# #
# #     # CONVERTING TO DATAFRAME
# #     fluke = pd.DataFrame.from_dict(copy_dict)
# #     print(fluke)
# #
# # fluke = fluke.head(-1)
# # durations = fluke["Duration"].tolist()
# # for z in range(len(durations)):
# #     if type(durations[z]) == str:
# #         if durations[z].count(":") == 2:
# #             durations[z] = datetime.datetime.strptime(durations[z], "%H:%M:%S.%f")
# #         elif durations[z].count(":") == 1:
# #             durations[z] = datetime.datetime.strptime(durations[z], "%M:%S.%f")
# # for i in range(len(durations)):
# #     durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute, seconds=durations[i].second,
# #                                       microseconds=durations[i].microsecond)
# #     durations[i] = durations[i].total_seconds()
# # for j in range(1, len(durations)):
# #     durations[j] = durations[j] + durations[j - 1]
# # for k in range(len(durations)):
# #     durations[k] = round(durations[k], 3)
# # fluke["Duration"] = durations
# #
# # print(fluke)
#
# from low_pass_filter import lowpassFilter
# from high_pass_filter import highpassFilter
# import matplotlib.pyplot as plt
# import numpy as np
# import pandas as pd
#
# def sine_generator(amplitude, sinefreq, theta, fs):
#     num_samples = 10 * fs
#     t = np.arange(0, num_samples, 1)
#     # print(t)
#     func = amplitude * np.sin(2 * np.pi * sinefreq * t + theta)
#     return func
#
#
# order = 1
# cutoff = 20
# fs = 45
# T = 5.0         # value taken in seconds
# n = int(T * fs) # indicates total samples
# t = np.linspace(0, T, n, endpoint=False)
#
# data = np.sin(2*np.pi*t) + 0.5 * np.cos(10*np.pi*t) + np.sin(2*np.pi*t)
#
# plt.plot(t, data)
#
# y = lowpassFilter(order, fs, cutoff, data)
# plt.plot(t, y)
# plt.show()
#
#
# # # order = 2
# # # cutoff = 30
# # #
# # # fps = 30
# # # sine_fq = 10
# # # duration = 10
# # # sine_5Hz = sine_generator(fps,sine_fq,duration)
# # # sine_fq = 1
# # # duration = 10
# # # sine_1Hz = sine_generator(fps,sine_fq,duration)
# # # sine = sine_5Hz + sine_1Hz
# # # plt.plot(range(len(sine)), sine)
# # #
# # # filtered = highpassFilter(order, fps, cutoff, sine.data)
# # # # plt.plot(t, data)
# # # plt.plot(range(len(sine)), filtered)
# # # plt.show()
# #
# # # sinewave1 = sine_generator(3, 0.1, 0)
# # sinewave2 = sine_generator(3, 45, 0, 30)
# # x = range(len(sinewave2))
# # plt.plot(x, sinewave2)
# # plt.show()
# # sinewave3 = sine_generator(0.5, 20, 0, 30)
# # # plt.plot(x, sinewave3)
# # # plt.show()
# # sinewave1 = sine_generator(1, 30, 0, 30)
# # # plt.plot(x, sinewave1)
# # # plt.show()
# # sinewave = sinewave1 + sinewave2 + sinewave3
# # # print(sinewave)
# # plt.plot(range(len(sinewave)), sinewave)
# # lowpass = highpassFilter(10, 30, 8, sinewave)
# # plt.plot(range(len(sinewave)), lowpass)
# #
# #
# #
# # plt.show()
# #
# #
# from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
# from latex_translation import textToLatex
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
#         # self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
#         # self.setStyleSheet("background-color: #3d4855")
#
#         label = textToLatex('$H_{max} - H_{min}\colon$', 132, 44, self, -0.05, -0.02)
#         layout = QVBoxLayout()
#         layout.addWidget(label)
#         self.setLayout(layout)
#         # label.setGeometry(QtCore.QRect(0, 0, 600, 444))
#         # movie = QMovie("ezgif.com-gif-maker (1).gif")
#         # label.setMovie(movie)
#         # movie.start()
#         # # label.setText("sdgjnsfkjgn")
#
#
#
#
#
# app = QApplication([])
# window = Window()
# window.show()
# sys.exit(app.exec())

# IMPORT STATEMENTS
from data_reader import reader
import datetime
import pandas as pd
import numpy as np
from find_cycles import find_cycles
from plot_temp_vs_strain import plot_temp_vs_strain
from moving_average_filter import movavg_filter
from plot_3d import plotSST
from low_pass_filter import lowpassFilter
from high_pass_filter import highpassFilter

# parameters
disp_title = "Extension (mm)"
mts_temp_title = "_COM1 (C)"
fluke_temp_title = "Sample"
area = 40
area_unit = "mm"
orig_length = 10
mov_avg_set = {"all"}
datapoints = {"MTS Temperature": 30, "Fluke Temperature": 30, "Load": 30, "Displacement": 30}
bandpass = {"Choice": False}
mts_start_time = "1/23/2019 9:27:54"
no_cycles = False
glitch_check = "yes"
cycle_determiner = "fluke"
relative_start_time = 10145.8
relative_end_time = 15780.7


# EXTRACTING FLUKE DATA
fluke_data = reader("Fluke Jacob 3 cycles.csv")
fluke_data.extract_fluke()
start_time = fluke_data.start_time
fluke = fluke_data.dataframe
start_time = start_time.split()[0] + " " + start_time.split()[1]
fluke_start = datetime.datetime.strptime(start_time, "%m/%d/%Y %H:%M:%S")
fluke["Start Time"] = [datetime.datetime.strptime(x, "%m/%d/%Y %H:%M:%S.%f") for x in fluke["Start Time"]]
for col in fluke.columns:
    try:
        fluke[col] = fluke[col].astype(float)
    except:
        pass

# EXTRACTING MTS DATA
mts_data = reader("3 cycles.txt")
mts_data.extract_txt()
mts = mts_data.dataframe
time_col = mts.iloc[:, 0]
mts_start = datetime.datetime.strptime(mts_start_time, "%m/%d/%Y %H:%M:%S")
abs_times = [mts_start + datetime.timedelta(seconds=time) for time in time_col]
mts.insert(0, "Global Time", abs_times)

# ACCOUNTING FOR GLITCH IN THE MTS
if glitch_check.lower() == "yes":
    for k in range(20):
        delete_list = []
        j = 1
        for i in range(1, len(mts[mts_temp_title])):
            if mts[mts_temp_title].iloc[i] == 0 and mts[mts_temp_title].iloc[i + 1] < 0.5:
                delete_list.append(i)
                j += 1
        mts = mts.drop(mts.index[delete_list])

# FINDING MIN TIME SEPARATION
fluke_time = fluke["Start Time"].to_numpy()
mts_time = np.array(abs_times)
fluke_diffs_min = min(np.diff(fluke_time))/np.timedelta64(1, 's')
mts_diffs_min = min(np.diff(mts_time)).total_seconds()
min_time_sep = min(mts_diffs_min, fluke_diffs_min)

# RESAMPLING THE MTS AND FLUKE DATA
sep = "{}S".format(min_time_sep)
mts = mts.set_index("Global Time").resample(sep).interpolate()
fluke = fluke.set_index("Start Time").resample(sep).interpolate()
final_df = pd.concat([fluke, mts], axis=1)

# ADDING A RELATIVE TIME COLUMN
relative_time = [x * min_time_sep for x in range(len(final_df.index))]
final_df.insert(0, "Relative Time", relative_time)

# FINDING LOAD COLUMN
load_col_name = [x for x in final_df.columns if "load" in x.lower()][0]
load_col_unit = load_col_name[load_col_name.index('(') + 1: load_col_name.index(")")]

# MOVING AVERAGE FILTERING
if len(mov_avg_set) != 0 and "none" not in mov_avg_set:
    mts_mov_avg_fig, fluke_mov_avg_fig = movavg_filter(final_df, mts_temp_title, disp_title, load_col_name,
                                                       mov_avg_set, datapoints, True, fluke_temp_title)

# CALCULATING STRESS
if "load" in mov_avg_set or "all" in mov_avg_set:
    stress = [load/area for load in final_df["Load Moving Average"]]
else:
    stress = [load/area for load in final_df[load_col_name]]
stress_title = "Stress ({}/{}^2)".format(load_col_unit, area_unit)
final_df[stress_title] = stress

# CALCULATING STRAIN
if "displacement" in mov_avg_set or "all" in mov_avg_set:
    strain = [disp/orig_length for disp in final_df["Displacement Moving Average"]]
else:
    strain = [disp/orig_length for disp in final_df[disp_title]]
final_df["Strain"] = strain

# BANDPASS FILTERING
choice = bandpass["Choice"]
if choice:
    if bandpass["Type"] == "low":
        final_df["Filtered Strain"] = lowpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                         bandpass["Cutoff Frequency"], final_df["Strain"])
    elif bandpass["Type"] == "high":
        final_df["Filtered Strain"] = highpassFilter(bandpass["Order"], bandpass["Sample Rate"],
                                                          bandpass["Cutoff Frequency"], final_df["Strain"])

# ADDING CYCLE NUMBERS TO THE DATAFRAME
if cycle_determiner.lower() == "fluke":
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        find_cycles(final_df, "Fluke Temperature Moving Average")
    else:
        find_cycles(final_df, fluke_temp_title)
elif cycle_determiner.lower() == "mts":
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        find_cycles(final_df, "MTS Temperature Moving Average")
    else:
        find_cycles(final_df, mts_temp_title)

# # EXPORTING FOR ASMADA
asm_cols = [mts_temp_title, fluke_temp_title, stress_title, "Strain"]
if "temperature" in mov_avg_set or "all" in mov_avg_set:
    asm_cols.insert(2, "MTS Temperature Moving Average")
    asm_cols.insert(3, "Fluke Temperature Moving Average")
if choice:
    asm_cols.append("Filtered Strain")
asmada_df = final_df[asm_cols]
asmada_df.to_csv("ASMADA Data.csv", index=False)

# EXPORTING DATA
# final_df.to_csv("TESTING.csv", index=True)

# PLOTTING DATA
start_index = final_df["Relative Time"].searchsorted(relative_start_time, side="left")
end_index = final_df["Relative Time"].searchsorted(relative_end_time, side="right")
df_to_plot = final_df.iloc[start_index:end_index + 1, :]
if "temperature" in mov_avg_set or "all" in mov_avg_set:
    temp_vs_strain_plot = plot_temp_vs_strain(df_to_plot, "MTS Temperature Moving Average", choice, no_cycles, True,
                                              "Fluke Temperature Moving Average")
    temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, "MTS Temperature Moving Average", stress_title, choice, True,
                                          "Fluke Temperature Moving Average")
else:
    temp_vs_strain_plot = plot_temp_vs_strain(df_to_plot, mts_temp_title, choice, no_cycles, True, fluke_temp_title)
    temp_vs_stress_vs_strain_plot = plotSST(df_to_plot, mts_temp_title, stress_title, choice, True, fluke_temp_title)

# RETURNING PLOTS
plots = [temp_vs_strain_plot, temp_vs_stress_vs_strain_plot]
if len(mov_avg_set) != 0 and "none" not in mov_avg_set:
    plots.extend([mts_mov_avg_fig, fluke_mov_avg_fig])
# return plots




