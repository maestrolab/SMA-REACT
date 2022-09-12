# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 23:24:59 2021

@author: Tiago
"""


from Geometry_Code_In_Console import *    
import numpy as np 
import re
import datetime
from TEST_data_reader import reader
import pandas as pd
from tkinter import *
from PIL import ImageTk, Image
from Geometry_Code_For_GUI import *

# CHECKING IF FLUKE DATA IS PRESENT
# check = input("Do you have fluke data? (Yes/No): ")


# EXTRACTING MTS DATA
mts = reader("250MPa 2Cmin.txt")
mts.extract()
mts_data = mts.dataframe.copy()


# COMBINING THE MTS AND FLUKE DATA AND MOVING BOTH TIME COLUMNS TO THE LEFT
combined_data = pd.concat([mts_data], axis=1)
columns = combined_data.columns.tolist()
for b in combined_data.columns:
    if b.lower().find("time") >= 0:
        columns.remove(b)
        columns.insert(0, b)
        combined_data = combined_data.reindex(columns=columns)


# RENAMING COLUMNS WTH UNITS
for label in combined_data.columns:
    if label.lower().find("time") >= 0 and len(label.lower()) <= 9:
        combined_data = combined_data.rename(columns={label: "Time Elapsed MTS (s)"})
    elif label.lower().find("duration") >= 0:
        combined_data = combined_data.rename(columns={label: "Time Elapsed Fluke (s)"})
    elif label.lower().find("sample") >= 0:
        combined_data = combined_data.rename(columns={label: "Sample (°C)"})
    elif label.lower().find("average") >= 0:
        combined_data = combined_data.rename(columns={label: "Average (°C)"})
    elif label.lower().find("max") >= 0:
        combined_data = combined_data.rename(columns={label: "Max (°C)"})


column_headers = combined_data.columns.tolist()
# --------------------------------------------------------------------------------------------------------------

# GUI

root = Tk()
root.geometry('2000x3000')
  

# Selecting strain from options

# SELECTING SHAPE
Shape_Options = ['Rectangle', 'Circle', 'Square', 'Square with hole','Input Area directly'] # Name ideas: 'Square peg in a round hole', 'Square Donut', 'Tumble Dry', 'Offset inscribed circle in a symmetric rectangle (square)', 'Square cupholder', 'Squircle'
Units_in = ['in','mm','m']
Units_out = ['in^2','mm^2','m^2']
l1 = Label(root, text = "Select shape of cross-section:") 
l1.config(font =("Arial", 9,'bold'))
l1.pack()

Shape_selection = StringVar(root)
Shape_selection.set('--') 
dm1 = OptionMenu(root, Shape_selection, *Shape_Options) # dm1 = dropdown menu 1
dm1.pack()


def Shape_Chosen():
    global Shape
    Shape = Shape_selection.get()
    # Unit_in = Units_in_Selection.get()
    # Unit_out = Units_out_Selection.get()
    print ("Shape is: " + Shape)
    
    # print ("Units in are: " + Unit_in)
    # print ("Units out are: " + Unit_out)
    
################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
################################################### RECTANGLE ##################################################

    if Shape == 'Rectangle': 
        
        # ------------------------------------ #
        # ----------- LENGTH INPUT ----------- #
        # ------------------------------------ #
        LENGTH = Label(root,text='----------------Length----------------')
        LENGTH.config(font =("Arial",10,'bold'))
        LENGTH.pack(pady=(8,0))
        length_label = Label(root, text = "Input length of specimen:") 
        length_label.config(font =("Arial", 7,'bold'))
        length_label.pack()
        length = StringVar(root)
        length_entry = Entry(root,textvariable=length).pack(pady=3)
        
        length_unit_label = Label(root, text = "Select units for length:")
        length_unit_label.config(font =("Arial", 7,'bold'))
        length_unit_label.pack()
        Units_len = StringVar(root)
        Units_len.set('--') 
        dm_l = OptionMenu(root, Units_len, *Units_in) # dm2 = dropdown menu 2
        dm_l.pack()  
        
        def Input_new_length():
            len_label.destroy()
            input_length['state'] = NORMAL
            
        def length_function():
            global len_label
            global length_val
            global length_unit
            length_val = float(length.get())
            length_unit = Units_len.get()
            len_label = Label(root,text='Length: ' + str(length_val) + ' ' + length_unit)
            len_label.config(font =("Arial", 7,'bold'))
            len_label.pack()
            input_length['state'] = DISABLED
            
        input_length = Button(root, text="Enter length", command=length_function)
        input_length.pack()
        length_reset = Button(root, text = 'Click to reset length', command = Input_new_length).pack(pady = 3)

        
        
        # ------------------------------------------- #
        # ----------- FLUKE AND MTS INPUT ----------- #
        # ------------------------------------------- #
        DATA = Label(root,text='----------------Data----------------')
        DATA.config(font =("Arial",10,'bold'))
        DATA.pack(pady=(8,0))
        
        fluke_label = Label(root, text = "Insert name of file for Fluke data (include extension, type 'none' if file is not used):")
        fluke_label.config(font =("Arial", 7,'bold'))
        fluke_label.pack()
        fluke = StringVar(root)
        fluke_entry = Entry(root,textvariable=fluke).pack()
        
        
        MTS_label = Label(root, text = "Insert name of file for MTS data (include extension, type 'none' if file is not used):")
        MTS_label.config(font =("Arial", 7,'bold'))
        MTS_label.pack()
        MTS = StringVar(root)
        MTS_entry = Entry(root,textvariable=MTS).pack()
        
        
        Time_label = Label(root, text = "Insert time information [in seconds] for data formatted as such (start time, end time, interval):")
        Time_label.config(font =("Arial", 7,'bold'))
        Time_label.pack()
        Time = StringVar(root)
        Time_entry = Entry(root,textvariable=Time).pack()
        
        
        
        
        
        def data_function():
            global fluke_dataframe
            global MTS_dataframe
            global start_time
            fluke_name = fluke.get() # getting name of fluke data file
            fluke_data = reader(fluke_name)
            MTS_name = MTS.get()# getting name of MTS data file
            MTS_data = reader(MTS_name) 
            time_info = Time.get()
            time_info_list = time_info.split(',')
            start_time = time_info_list[0]
            end = float(time_info_list[1].strip()) 
            interval = float(time_info_list[2].strip()) 



            if fluke_name.lower() != "none":
                # EXTRACTING FLUKE DATA
                fluke_data.extract()
                fluke_dataframe = fluke_data.dataframe.copy()

                # CONVERTING THE DURATIONS TO TIME ELAPSED SINCE START AND FORMATTING THEM
                durations = fluke_dataframe["Duration"].tolist()
                for z in range(len(durations)):
                    if type(durations[z]) == str:
                        if durations[z].count(":") == 2:
                            durations[z] = datetime.datetime.strptime(durations[z], "%H:%M:%S.%f")
                        elif durations[z].count(":") == 1:
                            durations[z] = datetime.datetime.strptime(durations[z], "%M:%S.%f")
                for i in range(len(durations)):
                    durations[i] = datetime.timedelta(hours=durations[i].hour, minutes=durations[i].minute, seconds=durations[i].second, microseconds=durations[i].microsecond)
                    durations[i] = durations[i].total_seconds()
                for j in range(1, len(durations)):
                    durations[j] = durations[j] + durations[j-1]
                for k in range(len(durations)):
                    durations[k] = round(durations[k], 3)
                fluke_dataframe["Duration"] = durations

               # RENAMING THE DURATION COLUMNS TO TIME ELAPSED
                fluke_dataframe = fluke_dataframe.rename(columns={"Duration": "Time Elapsed (s)"})

                # EXTRACTING THE START TIME
                start_time = fluke_data.start_time

                # CONVERTING ALL THE DATA TO FLOATS
                for column_label in range(1, len(fluke_dataframe.columns)):
                    fluke_dataframe[fluke_dataframe.columns.tolist()[column_label]] = [float(x) for x in fluke_dataframe[fluke_dataframe.columns.tolist()[column_label]].tolist()]

                # PIVOTING FLUKE DATA
                fluke_dataframe = fluke_dataframe.groupby(pd.cut(fluke_dataframe["Time Elapsed (s)"], np.arange(0, end + interval, interval))).mean()
                del fluke_dataframe["Time Elapsed (s)"]

            else:
                fluke_dataframe = pd.DataFrame()
           
            MTS_data.extract()
            MTS_dataframe = MTS_data.dataframe.copy()
        
            # PIVOTING MTS DATA
            time_label = [y for y in MTS_dataframe.columns.tolist() if y.lower().find("time") >= 0]
            MTS_dataframe = MTS_dataframe.groupby(pd.cut(MTS_dataframe[time_label[0]], np.arange(0, end + interval, interval))).mean()
            del MTS_dataframe[time_label[0]]

            # COMBINING THE MTS AND FLUKE DATA
            combined_data = pd.concat([fluke_dataframe, MTS_dataframe], axis=1)
                
                
        input_data = Button(root, text="Enter data info", command=data_function)
        input_data.pack()
                
                
        
                
        # ------------------------------------------- #
        # ----------- CROSS SECTION INPUT ----------- #
        # ------------------------------------------- #

        CROSS_SECTION = Label(root,text='-----Cross Section-----')
        CROSS_SECTION.config(font =("Arial", 8,'bold'))
        CROSS_SECTION.pack(pady=(8,0))
        
        sides_label = Label(root, text = "Input sides for cross-section:") 
        sides_label.config(font =("Arial", 7,'bold'))
        sides_label.pack()
        len_prompt = Label(root, text="Side 1:", font = ('Arial',7,'bold')).pack(pady=3)
        l = StringVar(root)
        length_entry = Entry(root,textvariable=l).pack()

        width_prompt = Label(root, text="Side 2:", font = ('Arial',7,'bold')).pack(pady=3)
        w = StringVar(root)
        width_entry = Entry(root,textvariable=w).pack()

        l2 = Label(root, text = "Select units for sides:")
        l2.config(font =("Arial", 7,'bold'))
        l2.pack()
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm2 = dropdown menu 2
        dm2.pack()

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 7,'bold'))
        l3.pack()
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack()

        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            global Area,Unit_o
            side1 = float(l.get())
            side2 = float(w.get())
            unit_in=Units_i.get()
            Unit_o=Units_o.get()
            dimensions = [side1,side2]
            Area = Geometry_input(Shape,dimensions,unit_in,Unit_o)
            l5 = Label(root,text='Area: ' + str(Area) + ' ' + Unit_o)
            l5.config(font =("Arial", 7,'bold'))
            l5.pack(pady=3)
            button1['state'] = DISABLED
            

        button1 = Button(root, text="Calculate Area", command=Dimensions_Selection)
        button1.pack(pady =3)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 3)
        


################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################### CIRCLE ####################################################
        
    if Shape == 'Circle': 
        
        # img = Image.open('Circle.png')
        # img = img.resize((150,150))
        # image = ImageTk.PhotoImage(img)
        # Label(root, image = image).pack()

        LENGTH = Label(root,text='-----------Length-----------')
        LENGTH.config(font =("Arial", 12,'bold'))
        LENGTH.pack(pady=(45,0))
        length_label = Label(root, text = "Input length of specimen:") 
        length_label.config(font =("Arial", 7,'bold'))
        length_label.pack(pady=3)
        length = StringVar(root)
        length_entry = Entry(root,textvariable=length).pack(pady=3)
        
        length_unit_label = Label(root, text = "Select units for length:")
        length_unit_label.config(font =("Arial", 7,'bold'))
        length_unit_label.pack(pady=3)
        Units_len = StringVar(root)
        Units_len.set('--') 
        dm_l = OptionMenu(root, Units_len, *Units_in) # dm2 = dropdown menu 2
        dm_l.pack(pady=3)  
        
        def Input_new_length():
            len_label.destroy()
            input_length['state'] = NORMAL
            
        def length_function():
            global len_label
            global length_val
            global length_unit
            length_val = float(length.get())
            length_unit = Units_len.get()
            len_label = Label(root,text='Length: ' + str(length_val) + ' ' + length_unit)
            len_label.config(font =("Arial", 7,'bold'))
            len_label.pack(pady=3)
            input_length['state'] = DISABLED
        
        input_length = Button(root, text="Enter length", command=length_function)
        input_length.pack(pady=3)
        length_reset = Button(root, text = 'Click to reset length', command = Input_new_length).pack(pady = 3)

        
        
        CROSS_SECTION = Label(root,text='-----Cross Section-----')
        CROSS_SECTION.config(font =("Arial", 12,'bold'))
        CROSS_SECTION.pack(pady=(45,0))


        Label(root, text="Diameter:", font = ('Arial',7,'bold')).pack(pady=3)
        d = StringVar(root)
        diameter_entry = Entry(root,textvariable=d).pack(pady=3)       

        l2 = Label(root, text = "Select units for diameter:")
        l2.config(font =("Arial", 7,'bold'))
        l2.pack(pady=3)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm3 = dropdown menu 3
        dm2.pack(pady=3)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 7,'bold'))
        l3.pack(pady=3)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=3)

        
        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            global Area,Unit_o
            diameter = float(d.get())
            unit_in=Units_i.get()
            Unit_o=Units_o.get()
            
            dimensions = [diameter]
            Area = Geometry_input(Shape,dimensions,unit_in,Unit_o)
            l5 = Label(root,text='Area: ' + str(Area) + ' ' + Unit_o)
            l5.config(font =("Arial", 7,'bold'))
            l5.pack(pady=3)
            button1['state'] = DISABLED
            

        button1 = Button(root, text="Calculate Area", command=Dimensions_Selection)
        button1.pack(pady =3)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 3)

        
################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################### SQUARE ####################################################

    if Shape == 'Square': 

        
        LENGTH = Label(root,text='-----------Length-----------')
        LENGTH.config(font =("Arial", 12,'bold'))
        LENGTH.pack(pady=(45,0))
        length_label = Label(root, text = "Input length of specimen:") 
        length_label.config(font =("Arial", 7,'bold'))
        length_label.pack(pady=3)
        length = StringVar(root)
        length_entry = Entry(root,textvariable=length).pack(pady=3)
        
        length_unit_label = Label(root, text = "Select units for length:")
        length_unit_label.config(font =("Arial", 7,'bold'))
        length_unit_label.pack(pady=3)
        Units_len = StringVar(root)
        Units_len.set('--') 
        dm_l = OptionMenu(root, Units_len, *Units_in) # dm2 = dropdown menu 2
        dm_l.pack(pady=3)  
        
        def Input_new_length():
            len_label.destroy()
            input_length['state'] = NORMAL
            
        def length_function():
            global len_label
            global length_val
            global length_unit
            length_val = float(length.get())
            length_unit = Units_len.get()
            len_label = Label(root,text='Length: ' + str(length_val) + ' ' + length_unit)
            len_label.config(font =("Arial", 7,'bold'))
            len_label.pack(pady=3)
            input_length['state'] = DISABLED
            
        
        input_length = Button(root, text="Enter length", command=length_function)
        input_length.pack(pady=3)
        length_reset = Button(root, text = 'Click to reset length', command = Input_new_length).pack(pady = 3)

        
        
        CROSS_SECTION = Label(root,text='-----Cross Section-----')
        CROSS_SECTION.config(font =("Arial", 12,'bold'))
        CROSS_SECTION.pack(pady=(45,0))

        Label(root, text="Side:", font = ('Arial',7,'bold')).pack(pady=3)
        s = StringVar(root)
        square_entry = Entry(root,textvariable=s).pack(pady=3)       
        

        l2 = Label(root, text = "Select units for side:")
        l2.config(font =("Arial", 7,'bold'))
        l2.pack(pady=3)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm3 = dropdown menu 3
        dm2.pack(pady=3)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 7,'bold'))
        l3.pack(pady=3)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=3)

 
        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            global Area,Unit_o    
            side = float(s.get())
            unit_in=Units_i.get()
            Unit_o=Units_o.get()
            
            dimensions = [side]
            Area = Geometry_input(Shape,dimensions,unit_in,Unit_o)
            l5 = Label(root,text='Area: ' + str(Area) + ' ' + Unit_o)
            l5.config(font =("Arial", 7,'bold'))
            l5.pack(pady=3)
            button1['state'] = DISABLED
            


        button1 = Button(root, text="Calculate Area", command=Dimensions_Selection)
        button1.pack(pady =7)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 7)


################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
########################################### SQUARE WITH HOLE ###################################################

    if Shape == 'Square with hole': 
        
        
        LENGTH = Label(root,text='-----------Length-----------')
        LENGTH.config(font =("Arial", 12,'bold'))
        LENGTH.pack(pady=(45,0))
        length_label = Label(root, text = "Input length of specimen:") 
        length_label.config(font =("Arial", 7,'bold'))
        length_label.pack(pady=3)
        length = StringVar(root)
        length_entry = Entry(root,textvariable=length).pack(pady=3)
        
        length_unit_label = Label(root, text = "Select units for length:")
        length_unit_label.config(font =("Arial", 7,'bold'))
        length_unit_label.pack(pady=3)
        Units_len = StringVar(root)
        Units_len.set('--') 
        dm_l = OptionMenu(root, Units_len, *Units_in) # dm2 = dropdown menu 2
        dm_l.pack(pady=3)  
        
        def Input_new_length():
            len_label.destroy()
            input_length['state'] = NORMAL
            
        def length_function():
            global len_label
            global length_val
            global length_unit

            length_val = float(length.get())
            length_unit = Units_len.get()
            len_label = Label(root,text='Length: ' + str(length_val) + ' ' + length_unit)
            len_label.config(font =("Arial", 7,'bold'))
            len_label.pack(pady=3)
            input_length['state'] = DISABLED
        
        input_length = Button(root, text="Enter length", command=length_function)
        input_length.pack(pady=3)
        length_reset = Button(root, text = 'Click to reset length', command = Input_new_length).pack(pady = 3)

        
        
        CROSS_SECTION = Label(root,text='-----Cross Section-----')
        CROSS_SECTION.config(font =("Arial", 12,'bold'))
        CROSS_SECTION.pack(pady=(45,0))

        diameter_prompt = Label(root, text="Diameter:", font = ('Arial',7,'bold')).pack(pady=3)
        d = StringVar(root)
        diameter_entry = Entry(root,textvariable=d).pack(pady=3)

        side_prompt = Label(root, text="Side:", font = ('Arial',7,'bold')).pack(pady=3)
        s = StringVar(root)
        side_entry = Entry(root,textvariable=s).pack(pady=3)
        

        l2 = Label(root, text = "Select units for diameter and side:")
        l2.config(font =("Arial", 7,'bold'))
        l2.pack(pady=3)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm2 = dropdown menu 2
        dm2.pack(pady=3)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 7,'bold'))
        l3.pack(pady=3)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=3)

        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            global Area,Unit_o
            diameter = float(d.get())
            side = float(s.get())
            unit_in=Units_i.get()
            Unit_o=Units_o.get()
            
            dimensions = [diameter,side]
            Area = Geometry_input(Shape,dimensions,unit_in,Unit_o)
            l5 = Label(root,text='Area: ' + str(Area) + ' ' + Unit_o)
            l5.config(font =("Arial", 7,'bold'))
            l5.pack(pady=3)
            button1['state'] = DISABLED
            

        button1 = Button(root, text="Calculate Area", command=Dimensions_Selection)
        button1.pack(pady =3)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 3)
        
        
        

        
################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
######################################### INPUT AREA DIRECTLY ##################################################
    if Shape == 'Input Area directly': 
        
        LENGTH = Label(root,text='-----------Length-----------')
        LENGTH.config(font =("Arial", 12,'bold'))
        LENGTH.pack(pady=(45,0))
        length_label = Label(root, text = "Input length of specimen:") 
        length_label.config(font =("Arial", 7,'bold'))
        length_label.pack(pady=3)
        length = StringVar(root)
        length_entry = Entry(root,textvariable=length).pack(pady=6)
        
        length_unit_label = Label(root, text = "Select units for length:")
        length_unit_label.config(font =("Arial", 7,'bold'))
        length_unit_label.pack(pady=3)
        Units_len = StringVar(root)
        Units_len.set('--') 
        dm_l = OptionMenu(root, Units_len, *Units_in) # dm2 = dropdown menu 2
        dm_l.pack(pady=3)  
        
        def Input_new_length():
            len_label.destroy()
            input_length['state'] = NORMAL
            
        def length_function():
            global len_label
            global length_val
            global length_unit
            length_val = float(length.get())
            length_unit = Units_len.get()
            len_label = Label(root,text='Length: ' + str(length_val) + ' ' + length_unit)
            len_label.config(font =("Arial", 7,'bold'))
            len_label.pack(pady=3)
            input_length['state'] = DISABLED
        
        input_length = Button(root, text="Enter length", command=length_function)
        input_length.pack(pady=3)
        length_reset = Button(root, text = 'Click to reset length', command = Input_new_length).pack(pady = 3)
        
        
        
        AREA_title = Label(root,text='-----------Area-----------')
        AREA_title.config(font =("Arial", 12,'bold'))
        AREA_title.pack(pady=(45,0))
        area_prompt_label = Label(root, text = "Input cross-sectional area of specimen:") 
        area_prompt_label.config(font =("Arial", 7,'bold'))
        area_prompt_label.pack(pady=3)
        area = StringVar(root)
        area_entry = Entry(root,textvariable=area).pack(pady=3)
        
        area_unit_label = Label(root, text = "Select units for area:")
        area_unit_label.config(font =("Arial", 7,'bold'))
        area_unit_label.pack(pady=3)
        Units_area = StringVar(root)
        Units_area.set('--') 
        dm_a = OptionMenu(root, Units_area, *Units_out) # dm2 = dropdown menu 2
        dm_a.pack(pady=3)  
        
        def Input_new_area():
            area_label.destroy()
            input_area['state'] = NORMAL
            
        def area_function():
            global area_label
            global Area,Unit_o
            Area = float(area.get())
            Unit_o = Units_area.get()
            area_label = Label(root,text='Area: ' + str(Area) + ' ' + Unit_o)
            area_label.config(font =("Arial", 7,'bold'))
            area_label.pack(pady=3)
            input_area['state'] = DISABLED
            
        
        
        input_area = Button(root, text="Enter area", command=area_function)
        input_area.pack(pady=3)
        area_reset = Button(root, text = 'Click to reset area', command = Input_new_area).pack(pady = 3)
        
################################################################################################################
# Disabling shape-selection button
    shape_selection_button['state'] = DISABLED
    
    
    prompt1 = Label(root, text= "-----Select the column to use for displacement-----")
    prompt1.config(font =("Arial", 12,'bold'))
    prompt1.pack(pady=(10,7))
    disp = StringVar(root)
    disp.set('--')
    options = OptionMenu(root,disp,*column_headers)
    options.pack(pady=7)



    def Displacement_Selection():
        disp_title = disp.get()
        print(disp_title)
        displacement_list = disp_title.split()
        disp_unit = displacement_list[1]
        disp_unit = re.sub('[()]','',disp_unit)
        displacement = combined_data[combined_data.columns[column_headers.index(disp_title)]].tolist()
        strains = []
        for d in displacement:
            strains.append(float(d)/length_val)
            
        column_name = 'Strain' + '(' + disp_unit + '/'  + length_unit + ')'
        combined_data[column_name] = strains

    displacement_selection_button = Button(root, text="Select", command=Displacement_Selection)
    displacement_selection_button.pack(pady=5)
    
    
    

################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
################################################################################################################





def Clear_Shape():
    List =  root.winfo_children()

    # print(len(List))
    List.pop(0)
    List.pop(0)
    List.pop(0)
    List.pop(0)
    for widget in List:
        widget.destroy()
    shape_selection_button['state'] = NORMAL


# Input length of specimen


shape_selection_button = Button(root, text="Select", command=Shape_Chosen)
shape_selection_button.pack(pady=5)

clear_shape_button  = Button(root, text="Clear", command=Clear_Shape).pack(pady=5)

            

mainloop()  

# -------------------------------------------------- #
# --------------------- STRESS --------------------- #
# -------------------------------------------------- #

load = ['Load','LOAD','load'] # List of possible names for Load
                                         
for column in combined_data: # Finding Load column by seaching all columns in dataframe
    List = column.split()
    for item in List:
        if item in load:
            key = List[0]
            unit = List[1]  
            break
    
search = key + ' ' + unit
unit = re.sub('[()]','',unit)
List_of_loads = combined_data.loc[:,search]
Stresses = []
for force in List_of_loads:
    stress = force / Area
    Stresses.append(stress)
stress_col_name = 'Stress' + ' (' + unit +'/'+ Unit_o +')'
combined_data[stress_col_name] = Stresses
    

# -------------------------------------------------- #
# ----------------- COMBINED DATA ------------------ #
# -------------------------------------------------- #

writer = pd.ExcelWriter("MTS + Fluke.xlsx")
combined_data.to_excel(writer)
writer.save()
writer.close()
   




    
metadata = combined_data.to_dict()
metadata["Start Time"] = start_time
metadata["Cross Section"] = Shape
metadata["Cross Sectional Area"] = str(Area) + " ({})".format(Unit_o)
metadata["Length"] = str(length_val) + ' ' + length_unit
metadata["Date Run"] = datetime.datetime.now() 

print(combined_data)

# --------------------------------------------------------------------------------------------------------------

