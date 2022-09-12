# IMPORT STATEMENTS
import datetime
from data_reader import reader
import pandas as pd
from Geometry_Code_In_Console import *
import re
import pickle
import csv
import matplotlib.pyplot as plt


# CHECKING IF FLUKE DATA IS PRESENT
check = input("Do you have fluke data? (Yes/No): ")


if check.lower() == "yes":
    # EXTRACTING FLUKE DATA
    fluke = reader("Fluke Jacob 3 cycles.csv")
    fluke.extract()
    fluke_data = fluke.dataframe.copy()

    # CONVERTING THE DURATIONS TO TIME ELAPSED SINCE START AND FORMATTING THEM
    durations = fluke_data["Duration"].tolist()
    durations.insert(0, 0)
    durations.pop(len(durations) - 1)
    for z in range(1, len(durations)):
        if type(durations[z]) == str:
            if durations[z].count(":") == 2:
                durations[z] = datetime.datetime.strptime(durations[z], "%H:%M:%S.%f")
            elif durations[z].count(":") == 1:
                durations[z] = datetime.datetime.strptime(durations[z], "%M:%S.%f")
    for i in range(1, len(durations)):
        durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute, seconds=durations[i].second, microseconds=durations[i].microsecond)
        durations[i] = durations[i].total_seconds()
    for j in range(2, len(durations)):
        durations[j] = durations[j] + durations[j-1]
    for k in range(len(durations)):
        durations[k] = round(durations[k], 3)
    fluke_data["Duration"] = durations

    # RENAMING THE DURATIONS COLUMN TO TIME ELAPSED
    fluke_data = fluke_data.rename(columns={"Duration": "Time Elapsed (s)"})

    # EXTRACTING THE START TIME
    start_time = fluke.start_time

    # CONVERTING ALL THE DATA TO FLOATS
    for column_label in range(1, len(fluke_data.columns)):
        fluke_data[fluke_data.columns.tolist()[column_label]] = [float(x) for x in fluke_data[fluke_data.columns.tolist()[column_label]].tolist()]

    # PIVOTING FLUKE DATA
    #end = float(input("Enter end time in seconds(s) "))
    end = fluke_data["Time Elapsed (s)"].tolist()[len(fluke_data["Time Elapsed (s)"]) - 1]
    interval = float(input("Enter time interval in seconds(s) "))
    fluke_data = fluke_data.groupby(pd.cut(fluke_data["Time Elapsed (s)"], pd.interval_range(start=0, end=end, freq=interval, closed="left"))).mean()
    del fluke_data["Time Elapsed (s)"]

else:
    fluke_data = pd.DataFrame()
    start_time = input("Enter the start time for MTS (MM/DD/YYYY HH:MM:SS): ")
    end = float(input("Enter end time in seconds(s) "))
    interval = float(input("Enter time interval in seconds(s) "))


# EXTRACTING MTS DATA
mts = reader("3 cycles.txt")
mts.extract()
mts_data = mts.dataframe.copy()


# ---------------------------------------------------------
# Calculating Stress
load = ['Load', 'LOAD', 'load']  # List of possible names for Load

for column in mts_data:  # Finding Load column by searching all columns in dataframe
    List = column.split()
    for item in List:
        if item in load:
            key = item
            if len(item) > 1:
                unit = List[1]
            break

search = key + ' ' + unit
unit = re.sub('[()]', '', unit)

List_of_loads = mts_data.loc[:, search]

area, unit_out, shape = Geometry_input()
Stresses = []
for force in List_of_loads:
    stress = force / area
    Stresses.append(stress)

stress_col_name = 'Stress' + ' (' + unit + '/' + unit_out + '^2)'
mts_data[stress_col_name] = Stresses


# FINDING THE DISPLACEMENT
column_headers = mts_data.columns.tolist()
for col_index in range(len(column_headers)):
    for index in range(-1, -(len(column_headers[col_index]) - 1), -1):
        if column_headers[col_index][index] == " ":
            column_headers[col_index] = column_headers[col_index][:index]
            break
print(column_headers)
for ind in range(len(column_headers)):
    column_headers[ind] = column_headers[ind].lower().replace(" ", "")
disp_title = input("Enter the column from above you would like to use for displacement: ")
disp_check = False
while not disp_check:
    if disp_title.lower().replace(" ", "") in column_headers:
        disp_check = True
    else:
        print("That displacement does not exist")
        disp_title = input("Enter the column from above you would like to use for displacement: ")
displacement = mts_data[mts_data.columns[column_headers.index(disp_title.lower())]].tolist()
disp_units = mts_data.columns[column_headers.index(disp_title.lower())][-4:].strip()


# CALCULATING THE STRAIN FROM THE DISPLACEMENT AND LENGTH
length = float(input("Enter the length in {} used to calculate strain: ".format(disp_units)))
strains = []
for disp in displacement:
    strains.append(disp/length)
mts_data["Strain"] = strains


# PIVOTING MTS DATA
time_label = [y for y in mts_data.columns.tolist() if y.lower().find("time") >= 0]
mts_data = mts_data.groupby(pd.cut(mts_data[time_label[0]], pd.interval_range(start=0, end=end, freq=interval, closed="left"))).mean()
del mts_data[time_label[0]]


# COMBINING THE MTS AND FLUKE DATA
combined_data = pd.concat([fluke_data, mts_data], axis=1)

# INTERPOLATING THE DATA
for data_label in combined_data.columns:
    combined_data[data_label] = combined_data[data_label].interpolate(method="linear")


# RENAMING COLUMNS WTH UNITS
for label in combined_data.columns:
    if label.lower().find("sample") >= 0:
        combined_data = combined_data.rename(columns={label: "Sample (°C)"})
    elif label.lower().find("average") >= 0:
        combined_data = combined_data.rename(columns={label: "Average (°C)"})
    elif label.lower().find("max") >= 0:
        combined_data = combined_data.rename(columns={label: "Max (°C)"})

#  FILTERING DATA


# CREATING METADATA
metadata_dict = dict()
metadata_dict["Date Run"] = datetime.datetime.now()
metadata_dict["Start Time"] = start_time
metadata_dict["Cross Section"] = shape
metadata_dict["Cross Sectional Area"] = str(area) + " ({}^2)".format(unit_out)
metadata_dict["Length"] = str(length) + " " + disp_units


# CREATING METADATA DATAFRAME
metadata_list = [(key + ": " + str(value)) for key, value in metadata_dict.items() if type(value) != dict]
metadata = pd.DataFrame()
metadata["Metadata"] = metadata_list


# CREATING METADATA PICKLE
pkl_data = combined_data.to_dict()
pkl_data = {**pkl_data, **metadata_dict}
pickle.dump(pkl_data, open("metadata.pkl", "wb"))


# CREATING METADATA CSV
with open("metadata.csv", "w") as metafile:
    csv_writer = csv.writer(metafile)
    for key, value in metadata_dict.items():
        csv_writer.writerow([key, value])


# EXPORTING THE DATA FRAME TO AN EXCEL FILE
writer = pd.ExcelWriter("MTS + Fluke.xlsx")
combined_data.to_excel(writer, sheet_name="Data")
metadata.to_excel(writer, sheet_name="Metadata", index=False)
writer.save()
writer.close()


# GRAPHING FLUKE AND MTS TEMPERATURE VS STRAIN AND PICKING WHICH TEMPERATURE DATA TO USE
if check.lower() == "yes":
    fluke_temps = combined_data[combined_data.columns.tolist()[0]].tolist()
    mts_temps = combined_data["_COM1 (C)"].tolist()
    strains = combined_data["Strain"]
    plt.subplot(1, 2, 1)
    plt.plot(fluke_temps, strains)
    plt.title("Fluke Temperature vs. Strain")
    plt.subplot(1, 2, 2)
    plt.plot(mts_temps, strains)
    plt.title("MTS Temperature vs. Strain")
    plt.suptitle("Temperature vs. Strain")
    plt.show()
    choice = input("Which temperature data would you like to use (MTS or Fluke): ")
