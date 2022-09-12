# IMPORT STATEMENTS
from data_reader import reader
from Geometry_Code_In_Console import *
from find_cycles import find_cycles
from functions import *
from moving_average_filter import movavg_filter
from plot_temp_vs_strain import plot_temp_vs_strain


def analyze_fmts():
    # EXTRACTING FLUKE DATA
    fluke = reader("Fluke Jacob 3 cycles.csv")
    fluke.extract()
    fluke_data = fluke.dataframe.copy()
    fluke_temp_title = fluke.temperature_title


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
        durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute, seconds=durations[i].second,
                                          microseconds=durations[i].microsecond)
        durations[i] = durations[i].total_seconds()
    for j in range(2, len(durations)):
        durations[j] = durations[j] + durations[j - 1]
    for k in range(len(durations)):
        durations[k] = round(durations[k], 3)
    fluke_data["Duration"] = durations


    # RENAMING THE DURATIONS COLUMN TO TIME ELAPSED
    fluke_data = fluke_data.rename(columns={"Duration": "Time Elapsed (s)"})


    # EXTRACTING THE START TIME
    start_time = fluke.start_time


    # CONVERTING ALL THE DATA TO FLOATS
    for column_label in range(1, len(fluke_data.columns)):
        fluke_data[fluke_data.columns.tolist()[column_label]] = [float(x) for x in fluke_data[
            fluke_data.columns.tolist()[column_label]].tolist()]


    # PIVOTING FLUKE DATA
    # end = float(input("Enter end time in seconds(s) "))
    end = fluke_data["Time Elapsed (s)"].tolist()[len(fluke_data["Time Elapsed (s)"]) - 1]
    interval = float(input("Enter time interval in seconds(s) "))
    fluke_data = fluke_data.groupby(pd.cut(fluke_data["Time Elapsed (s)"], pd.interval_range(start=0, end=end, freq=interval, closed="left"))).mean()
    del fluke_data["Time Elapsed (s)"]


    # EXTRACTING MTS DATA
    mts = reader("3 cycles.txt")
    mts.extract()
    mts_data = mts.dataframe.copy()


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


    # COMBINING THE MTS AND FLUKE DATA
    combined_data = pd.concat([fluke_data, mts_data], axis=1)


    # INTERPOLATING THE DATA
    for data_label in combined_data.columns:
        combined_data[data_label] = combined_data[data_label].interpolate(method="linear")


    # FINDING THE DISPLACEMENT
    column_headers = combined_data.columns.tolist()
    disp_title_unformat, new_headers = header_choice(column_headers, "displacement")
    displacement = combined_data[combined_data.columns[new_headers.index(disp_title_unformat.lower())]].tolist()
    disp_units = combined_data.columns[new_headers.index(disp_title_unformat.lower())][-4:].strip()
    disp_title = combined_data.columns[new_headers.index(disp_title_unformat.lower())]


    # MOVING AVERAGE FILTER
    List_of_loads, mov_avg_set, unit = movavg_filter(combined_data, temp_title, disp_title, fluke_check=True, fluke_temp_title=fluke_temp_title)


    # INTERPOLATING THE MOVING AVERAGES
    for column in combined_data.columns:
        if "Moving Average" in column:
            combined_data[column] = combined_data[column].interpolate(method="linear", limit_direction="backward")


    # CALCULATING STRESS AND ADDING IT TO DATAFRAME
    area, unit_out, shape = Geometry_input()
    Stresses = []
    for force in List_of_loads:
        stress = force / area
        Stresses.append(stress)

    stress_col_name = 'Stress' + ' (' + unit + '/' + unit_out + '^2)'
    combined_data[stress_col_name] = Stresses


    # CALCULATING THE STRAIN FROM THE DISPLACEMENT AND LENGTH
    length = float(input("Enter the length in {} used to calculate strain: ".format(disp_units)))
    strains = []
    if "extension" in mov_avg_set or "all" in mov_avg_set:
        for disp in combined_data["Extension Moving Average"].tolist():
            strains.append(disp/length)
    else:
        for disp in displacement:
            strains.append(disp / length)
    combined_data["Strain"] = strains


    # RENAMING COLUMNS WTH UNITS
    for label in combined_data.columns:
        if label.lower().find("sample") >= 0:
            combined_data = combined_data.rename(columns={label: "Sample (°C)"})


    # ADDING CYCLE NUMBERS TO THE DATAFRAME
    find_cycles(combined_data, temp_title)


    # EXPORTING DATA
    export_all(combined_data, start_time, shape, area, unit_out, length, disp_units, "MTS + Fluke.xlsx")


    # PLOTTING DATA
    if "temperature" in mov_avg_set or "all" in mov_avg_set:
        plot_temp_vs_strain(combined_data, "MTS Temperature Moving Average", fluke_check=True, fluke_temp_title="Fluke Temperature Moving Average")
    else:
        plot_temp_vs_strain(combined_data, temp_title, fluke_check=True, fluke_temp_title=combined_data.columns.tolist()[1])