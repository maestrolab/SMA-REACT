# IMPORT STATEMENTS
from functions import *
from data_reader import reader
from Geometry_Code_In_Console import *
from find_cycles import find_cycles
from moving_average_filter import movavg_filter
from plot_temp_vs_strain import plot_temp_vs_strain


def analyze_mts():
    # EXTRACTING MTS DATA
    mts = reader("+7 cycles.txt")
    mts.extract()
    mts_data = mts.dataframe.copy()


    # INITIALIZING THE START TIME, END TIME, AND TIME INTERVAL
    start_time = input("Enter the start time for MTS (MM/DD/YYYY HH:MM:SS): ")
    end = float(input("Enter end time in seconds(s) "))
    interval = float(input("Enter time interval in seconds(s) "))


    # INITIALIZING MTS TEMPERATURE TITLE VARIABLE
    temp_title_unformat, column_list = header_choice(mts_data.columns.tolist(), "MTS temperature")
    temp_title = mts_data.columns[column_list.index(temp_title_unformat.lower().replace(" ", ""))]


    # ACCOUNTING FOR GLITCH IN THE MTS
    print("Sometimes the MTS glitches at 0 degrees.")
    glitch_check = input("Would you like to account for this glitch in the MTS and delete all spurious zeroes (Yes/No)? ")
    if glitch_check.lower() == "yes":
        for k in range(20):
            delete_list = []
            j=1
            for i in range(1, len(mts_data[temp_title])):
                if mts_data[temp_title].iloc[i] == 0 and mts_data[temp_title].iloc[i+1] < 0.5:
                    delete_list.append(i)
                    j += 1
            mts_data = mts_data.drop(mts_data.index[delete_list])


    # PIVOTING MTS DATA
    time_label = [y for y in mts_data.columns.tolist() if y.lower().find("time") >= 0]
    mts_data = mts_data.groupby(pd.cut(mts_data[time_label[0]], pd.interval_range(start=0, end=end, freq=interval, closed="left"))).mean()
    del mts_data[time_label[0]]


    # INTERPOLATING THE DATA
    for data_label in mts_data.columns:
        mts_data[data_label] = mts_data[data_label].interpolate(method="linear")


    # FINDING THE DISPLACEMENT
    column_headers = mts_data.columns.tolist()
    disp_title_unformat, new_headers = header_choice(column_headers, "displacement")
    displacement = mts_data[mts_data.columns[new_headers.index(disp_title_unformat.lower())]].tolist()
    disp_units = mts_data.columns[new_headers.index(disp_title_unformat.lower())][-4:].strip()
    disp_title = mts_data.columns[new_headers.index(disp_title_unformat.lower())]


    # MOVING AVERAGE FILTER
    List_of_loads, mov_avg_set, unit = movavg_filter(mts_data, temp_title, disp_title)


    # CALCULATING STRESS AND ADDING IT TO MTS DATAFRAME
    area, unit_out, shape = Geometry_input()
    Stresses = []
    for force in List_of_loads:
        stress = force / area
        Stresses.append(stress)

    stress_col_name = 'Stress' + ' (' + unit + '/' + unit_out + '^2)'
    mts_data[stress_col_name] = Stresses


    # CALCULATING THE STRAIN FROM THE DISPLACEMENT AND LENGTH
    length = float(input("Enter the length in {} used to calculate strain: ".format(disp_units)))
    strains = []
    if "extension" in mov_avg_set or "all" in mov_avg_set:
        for disp in mts_data["Extension Moving Average"].tolist():
            strains.append(disp/length)
    else:
        for disp in displacement:
            strains.append(disp / length)
    mts_data["Strain"] = strains


    # ADDING CYCLE NUMBERS TO THE DATAFRAME
    find_cycles(mts_data, temp_title)


    # EXPORTING DATA
    export_all(mts_data, start_time, shape, area, unit_out, length, disp_units, "MTS_ONLY.xlsx")


    # PLOTTING DATA
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        plot_temp_vs_strain(mts_data, "MTS Temperature Moving Average")
    else:
        plot_temp_vs_strain(mts_data, temp_title)
