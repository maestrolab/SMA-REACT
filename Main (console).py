# IMPORT STATEMENTS
import datetime
from data_reader import reader
import pandas as pd
from Geometry_Code_In_Console import *
import re
import pickle
import csv
import matplotlib.pyplot as plt

##################################### CREATING METADATA DICTIONARY ############################################
# Metadata dictionary is created in beginning of script so that every user input can be added to it
metadata_dict = dict()


###################################### CHECKING IF FLUKE DATA IS PRESENT ######################################
check = input("Do you have fluke data? (Yes/No): ")
metadata_dict["Do you have fluke data?"] = check

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
    interval = float(input("Enter time interval in seconds(s): "))
    metadata_dict['Time interval'] = interval
    fluke_data = fluke_data.groupby(pd.cut(fluke_data["Time Elapsed (s)"], pd.interval_range(start=0, end=end, freq=interval, closed="left"))).mean()
    del fluke_data["Time Elapsed (s)"]
    
else:
    fluke_data = pd.DataFrame()
    start_time = input("Enter the start time for MTS (MM/DD/YYYY HH:MM:SS): ")
    end = float(input("Enter end time in seconds(s): "))
    interval = float(input("Enter time interval in seconds(s): "))
    metadata_dict['MTS start time'] = start_time
    metadata_dict['End time in seconds'] = end
    metadata_dict['Time interval'] = interval
###############################################################################################################

# EXTRACTING MTS DATA
mts = reader("3 cycles.txt")
mts.extract()
mts_data = mts.dataframe.copy()

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


###############################################################################################################
#                                         DELETING TEMP ZEROS                                                 #
###############################################################################################################
    #delete any datapoints where the temperature goes to 0 
    # when the temperature is slightly negative (glitch in the MTS)
temp_with_zeros = combined_data['_COM1 (C)'] # To check if filter works
for k in range(20): #20 is the amount of datapoints that can be glitched consecutively 
    deleteList=[]
    j=1;
    for i in range(1,len(combined_data['_COM1 (C)'])):
        if combined_data['_COM1 (C)'].iloc[i] ==0 and combined_data['_COM1 (C)'].iloc[i+1] < .5:
            deleteList.append(i)
            j+=1
    for i in deleteList:
        if (i != 0) and (i != len(combined_data['_COM1 (C)'])):
            combined_data.loc[i,'_COM1 (C)'] = 0.5*(combined_data.loc[i-1,'_COM1 (C)'] + combined_data.loc[i+1,'_COM1 (C)'])

temp_without_zeros = combined_data['_COM1 (C)'] # To check if filter works

###################################### DELETING "NAN" VALUES ##################################################

combined_data = combined_data.dropna(how='all')


###############################################################################################################
###############################################################################################################
#                                              MOVING AVERAGE FILTERS                                         #
###############################################################################################################
###############################################################################################################
# Finding Load column
load = ['Load', 'LOAD', 'load']  # List of possible names for Load

for column in combined_data:  # Finding Load column by searching all columns in dataframe
    List = column.split()
    for item in List:
        if item in load:
            key = item
            if len(item) > 1:
                unit = List[1]
            break

search = key + ' ' + unit
unit = re.sub('[()]', '', unit)

List_of_loads = combined_data.loc[:, search]

###################################### SELECTING DISPLACEMENT COLUMN NAME #####################################
column_headers = combined_data.columns.tolist()
for col_index in range(len(column_headers)):
    for index in range(-1, -(len(column_headers[col_index]) - 1), -1):
        if column_headers[col_index][index] == " ":
            column_headers[col_index] = column_headers[col_index][:index]
            break
print()
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
displacement = combined_data[combined_data.columns[column_headers.index(disp_title.lower())]].tolist()
disp_units = combined_data.columns[column_headers.index(disp_title.lower())][-4:].strip()
    
column_headers = combined_data.columns.tolist()
for col_index in range(len(column_headers)):
    for index in range(-1, -(len(column_headers[col_index]) - 1), -1):
        if column_headers[col_index][index] == " ":
            column_headers[col_index] = column_headers[col_index][:index]
            break
for i in column_headers:
    if disp_title == i.lower():
        disp_title = i
column_headers = combined_data.columns.tolist()
for title in column_headers:
    items = title.split(' ')
    if disp_title == items[0]:
        disp_title = title
metadata_dict['Column used for Displacement'] = disp_title

######################################## SELECTING TEMPERATURE COLUMN NAME ####################################
column_headers = combined_data.columns.tolist()
for col_index in range(len(column_headers)):
    for index in range(-1, -(len(column_headers[col_index]) - 1), -1):
        if column_headers[col_index][index] == " ":
            column_headers[col_index] = column_headers[col_index][:index]
            break
print()
print(column_headers)
for ind in range(len(column_headers)):
    column_headers[ind] = column_headers[ind].lower().replace(" ", "")
temp_title = input("Enter the column from above you would like to use for mts temperature: ")
temp_check = False
while not temp_check:
    if temp_title.lower().replace(" ", "") in column_headers:
        temp_check = True
    else:
        print("That temperature does not exist")
        temp_title = input("Enter the column from above you would like to use for mts temperature: ")
mts_temp = combined_data[combined_data.columns[column_headers.index(temp_title.lower())]].tolist()
# # ADDING MOVING AVERAGE OF TEMPERATURE 
column_headers = combined_data.columns.tolist()
for col_index in range(len(column_headers)):
    for index in range(-1, -(len(column_headers[col_index]) - 1), -1):
        if column_headers[col_index][index] == " ":
            column_headers[col_index] = column_headers[col_index][:index]
            break
for i in column_headers:
    if temp_title == i.lower():
        temp_title = i
column_headers = combined_data.columns.tolist()
for title in column_headers:
    items = title.split(' ')
    if temp_title == items[0]:
        temp_title = title
metadata_dict['Column used for Temperature'] = temp_title

######################################## ASKING USER WHAT THEY WANT TO FILTER #################################

print()
print("A moving average filter can be applied to the Load, Temperature, and Extension.")
print()
print("Please list the measurements from the list above to which you would like to apply a moving average filter. Type 'all' if you would like to apply the filter to all measurements, and type 'done' if you don't want to apply a moving average filter to any measurement or when you are finished: ")

allowable_inputs = ['load', 'temperature', 'extension','all','done']
mov_avg_set = set()

while True:
    user_inp = input().lower()
    if user_inp.lower() == 'done':
        break
    while user_inp not in allowable_inputs:
        print()
        print('Invalid input, please type the name of one of the measurements from the list [Load, Temperature, Extension, All, Done].')
        print('Input:')
        user_inp = input().lower()
    mov_avg_set.add(user_inp)
    
metadata_dict['Filtered Measurements'] = mov_avg_set

if 'all' in mov_avg_set:
    temp_MovAvg_points = []
    ext_MovAvg_points = []
    load_MovAvg_points = []
else:
    if 'temperature' in mov_avg_set:
        temp_MovAvg_points = []
    if 'extension' in mov_avg_set:
        ext_MovAvg_points = []
    if 'load' in mov_avg_set:
        load_MovAvg_points = []
################################################# SATISFACTION LOOP ###########################################
# Checking user satisfaction with filter
if len(mov_avg_set) != 0:
    satisfaction = 'no'
    while satisfaction == 'no':
        
        for measurement in mov_avg_set:  
            
            if measurement == 'temperature': 
                number_of_points = int(input('How many datapoints would you like to use for the temperature moving average? '))
                combined_data['Temperature Moving Average'] = combined_data[temp_title].rolling(window=number_of_points).mean()
                temp_MovAvg_points.append(number_of_points)


            if measurement == 'load':
                number_of_points = int(input('How many datapoints would you like to use for the load moving average? '))
                mv_avg_load_col_name = 'Load Moving Average (' + unit + ')'
                combined_data[mv_avg_load_col_name] = combined_data[search].rolling(window=number_of_points).mean()
                load_MovAvg_points.append(number_of_points)


            if measurement == 'extension': 
                number_of_points = int(input('How many datapoints would you like to use for the extension moving average? '))
                combined_data['Extension Moving Average'] = combined_data[disp_title].rolling(window=number_of_points).mean()
                ext_MovAvg_points.append(number_of_points)


            if measurement == 'all':
                number_of_points = int(input('How many datapoints would you like to use for the temperature moving average? '))
                temp_MovAvg_points.append(number_of_points)
                combined_data['Temperature Moving Average'] = combined_data[temp_title].rolling(window=number_of_points).mean()
                
                number_of_points = int(input('How many datapoints would you like to use for the load moving average? '))
                load_MovAvg_points.append(number_of_points)
                mv_avg_load_col_name = 'Load Moving Average (' + unit + ')'
                combined_data[mv_avg_load_col_name] = combined_data[search].rolling(window=number_of_points).mean()
                
                number_of_points = int(input('How many datapoints would you like to use for the extension moving average? '))
                ext_MovAvg_points.append(number_of_points)
                combined_data['Extension Moving Average'] = combined_data[disp_title].rolling(window=number_of_points).mean()


# Plotting different scenarios so user can say if they are satisfied
        mts_temp = combined_data[temp_title].tolist()
        extension = combined_data[disp_title]
        load = combined_data[search]
        
        # DONE
        if mov_avg_set == {'temperature', 'load'}:
            filtered_temp = combined_data['Temperature Moving Average']        
            filtered_load = combined_data[mv_avg_load_col_name]
            plt.subplot(1, 3, 1)
            plt.plot(mts_temp, load)
            plt.plot(filtered_temp, filtered_load)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Filtered Load and Filtered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")
            plt.subplot(1, 3, 2)
            plt.plot(mts_temp, load)
            plt.plot(mts_temp, filtered_load)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Filtered Load and Unfiltered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")
            plt.subplot(1, 3, 3)
            plt.plot(mts_temp, load)
            plt.plot(filtered_temp, load)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Unfiltered Load and Filtered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")
        
        # DONE
        if mov_avg_set == {'temperature', 'extension'}:
            filtered_temp = combined_data['Temperature Moving Average']
            filtered_extension = combined_data['Extension Moving Average']
            plt.subplot(1, 3, 1)
            plt.plot(mts_temp, extension)
            plt.plot(filtered_temp, filtered_extension)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Filtered Extension and Filtered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
            plt.subplot(1, 3, 2)
            plt.plot(mts_temp, extension)
            plt.plot(mts_temp, filtered_extension)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Filtered Extension and Unfiltered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
            plt.subplot(1, 3, 3)
            plt.plot(mts_temp, extension)
            plt.plot(filtered_temp, extension)
            plt.legend(["Unfiltered","Filtered"])
            plt.title("Unfiltered Extension and Filtered Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
            
        # DONE
        if mov_avg_set == {'all'}:
            print()
            print('-----------------------------------------------------------------------------------------------------------------------')
            print('Note: All graphs are printed with unfiltered temperature and unfiltered measurement (load or extension) for comparison.')
            print('-----------------------------------------------------------------------------------------------------------------------')
            print()
            fig,axs = plt.subplots(2,3)
            filtered_temp = combined_data['Temperature Moving Average']
            filtered_extension = combined_data['Extension Moving Average']
            filtered_load = combined_data[mv_avg_load_col_name]
            
            axs[0,0].plot(mts_temp, extension)
            axs[0,0].plot(filtered_temp, filtered_extension)
            axs[0,0].legend(["Unfiltered measurements","Filtered measurements"])
            axs[0,0].set_title("Filtered Extension and Filtered Temp")
         
            
            axs[0,1].plot(mts_temp, extension)
            axs[0,1].plot(mts_temp, filtered_extension)
            axs[0,1].legend(["Unfiltered measurements","Filtered measurements"])
            axs[0,1].set_title("Filtered Extension and Unfiltered Temp")
            
            axs[0,2].plot(mts_temp, extension)
            axs[0,2].plot(filtered_temp, extension)
            axs[0,2].legend(["Unfiltered measurements","Filtered measurements"])
            axs[0,2].set_title("Unfiltered Extension and Filtered Temp")
            
            axs[1,0].plot(mts_temp, load)
            axs[1,0].plot(filtered_temp, filtered_load)
            axs[1,0].legend(["Unfiltered measurements","Filtered measurements"])
            axs[1,0].set_title("Filtered Load and Filtered Temp")
            
            axs[1,1].plot(mts_temp, load)
            axs[1,1].plot(mts_temp, filtered_load)
            axs[1,1].legend(["Unfiltered measurements","Filtered measurements"])
            axs[1,1].set_title("Filtered Load and Unfiltered Temp")
            
            axs[1,2].plot(mts_temp, load)
            axs[1,2].plot(filtered_temp, load)
            axs[1,2].legend(["Unfiltered measurements","Filtered measurements"])
            axs[1,2].set_title("Unfiltered Load and Filtered Temp")            
            
        # DONE
        if mov_avg_set == {'load','extension'}:
            filtered_load = combined_data[mv_avg_load_col_name]
            filtered_extension = combined_data['Extension Moving Average']
            plt.subplot(1, 2, 1)
            plt.plot(mts_temp, extension)
            plt.plot(mts_temp, filtered_extension)
            plt.legend(["Unfiltered extension","Filtered extension"])
            plt.title("Extension vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
            plt.subplot(1, 2, 2)
            plt.plot(mts_temp, load)
            plt.plot(mts_temp, filtered_load)
            plt.legend(["Unfiltered load","Filtered load"])
            plt.title("Load vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")
        
        # DONE
        if mov_avg_set == {'load'}:
            filtered_load = combined_data[mv_avg_load_col_name]
            plt.plot(mts_temp, load)
            plt.plot(mts_temp, filtered_load)
            plt.legend(["Unfiltered load","Filtered load"])
            plt.title("Load vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")
        
        # DONE
        if mov_avg_set == {'extension'}:
            filtered_extension = combined_data['Extension Moving Average']
            plt.plot(mts_temp, extension)
            plt.plot(mts_temp, filtered_extension)
            plt.legend(["Unfiltered extension","Filtered extension"])
            plt.title("Extension vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
                        
            
        if mov_avg_set == {'temperature'}:
            print()
            print('------------------------------------------------------------------------------------------------------------------------------------------')
            print('Note: These plots show the unfiltered load and unfiltered extensions plotted with both filtered and unfiltered temperature for comparison.')
            print('------------------------------------------------------------------------------------------------------------------------------------------')
            print()
            filtered_temp = combined_data['Temperature Moving Average']
            plt.subplot(1, 2, 1)
            plt.plot(mts_temp, extension)
            plt.plot(filtered_temp, extension)
            plt.legend(["Unfiltered Temperature","Filtered Temperature"])
            plt.title("Extension vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel("Extension [mm]")
            plt.subplot(1, 2, 2)
            plt.plot(mts_temp, load)
            plt.plot(filtered_temp, load)
            plt.legend(["Unfiltered Temperature","Filtered Temperature"])
            plt.title("Load vs. Temperature")
            plt.xlabel("Temperature [C]")
            plt.ylabel(f"Load [{unit}]")

        
        print()
        print('Please close plot window to continue.')
        print()
        satisfaction = input('Are you satisfied with the filtered data or would you like to try filtering again using a different number of data points? [yes or no] ').lower()
    

if 'all' in mov_avg_set:
    metadata_dict['Number of datapoints used for Temperature moving average filter'] = temp_MovAvg_points
    metadata_dict['Number of datapoints used for Extension moving average filter'] = ext_MovAvg_points
    metadata_dict['Number of datapoints used for Load moving average filter'] = load_MovAvg_points
else:
    if 'temperature' in mov_avg_set:
        metadata_dict['Number of datapoints used for Temperature moving average filter'] = temp_MovAvg_points
    if 'extension' in mov_avg_set:
        metadata_dict['Number of datapoints used for Extension moving average filter'] = ext_MovAvg_points
    if 'load' in mov_avg_set:
        metadata_dict['Number of datapoints used for Load moving average filter'] = load_MovAvg_points

###############################################################################################################
###############################################################################################################
#                                         CALCULATING STRESS AND STRAIN                                       #
###############################################################################################################
###############################################################################################################

area, unit_out, shape = Geometry_input()
Stresses = []
for force in List_of_loads:
    stress = force / area
    Stresses.append(stress)

stress_col_name = 'Stress (' + unit + '/' + unit_out + '^2)'
combined_data[stress_col_name] = Stresses

if 'load' in mov_avg_set:
    mv_avg_stress_col_name = 'Stress Moving Average (' + unit + '/' + unit_out + '^2)'
    mov_avg_stress = []
    for avg_load in combined_data[mv_avg_load_col_name]:
        mov_avg_stress.append(avg_load/area)
    combined_data[mv_avg_stress_col_name] = mov_avg_stress


length = float(input("Enter the length of bar in {} used to calculate strain: ".format(disp_units)))
strains = []
for disp in displacement:
    strains.append(disp/length)
combined_data["Strain"] = strains

if 'extension' in mov_avg_set: 
    mov_avg_strain = []
    for avg_disp in combined_data['Extension Moving Average']:
        mov_avg_strain.append(avg_disp/length)
    combined_data['Strain Moving Average'] = mov_avg_strain




###############################################################################################################
###############################################################################################################
#                                             POPULATING METADATA                                             #
###############################################################################################################
###############################################################################################################

# POPULATING METADATA
metadata_dict["Date Run"] = datetime.datetime.now()
metadata_dict["Start Time"] = start_time
metadata_dict["Cross Section"] = shape
metadata_dict["Cross Sectional Area"] = str(area) + " ({}^2)".format(unit_out)
metadata_dict["Bar Length"] = str(length) + " " + disp_units


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




###############################################################################################################
###############################################################################################################
#                                               EXPORTING TO A CSV                                            #
###############################################################################################################
###############################################################################################################
        
# EXPORTING THE DATA FRAME TO AN EXCEL FILE
writer = pd.ExcelWriter("MTS + Fluke.xlsx")
combined_data.to_excel(writer, sheet_name="Data")
metadata.to_excel(writer, sheet_name="Metadata", index=False)
writer.save()
writer.close()


# GRAPHING FLUKE AND MTS TEMPERATURE VS STRAIN AND PICKING WHICH TEMPERATURE DATA TO USE
# if check.lower() == "yes":
#     fluke_temps = combined_data[combined_data.columns.tolist()[0]].tolist()
#     mts_temps = combined_data["_COM1 (C)"].tolist()
#     strains = combined_data["Strain"]
#     plt.subplot(1, 2, 1)
#     plt.plot(fluke_temps, strains)
#     plt.title("Fluke Temperature vs. Strain")
#     plt.subplot(1, 2, 2)
#     plt.plot(mts_temps, strains)
#     plt.title("MTS Temperature vs. Strain")
#     plt.suptitle("Temperature vs. Strain")
#     plt.show()
#     choice = input("Which temperature data would you like to use (MTS or Fluke): ")
    
    


