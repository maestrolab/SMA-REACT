# -*- coding: utf-8 -*-
"""
Created on Thu Oct  7 11:18:07 2021

@author: Tiago
"""
# Imports
from tkinter import *
from PIL import ImageTk, Image
from Geometry_Code_For_GUI import *

root = Tk()
root.geometry('2000x3000')
  
Shape_Options = ['Circle', 'Rectangle', 'Square', 'Special']
Units_in = ['in','mm','m']
Units_out = ['in^2','mm^2','m^2']

# SELECTING SHAPE

l1 = Label(root, text = "Select shape of cross-section:") 
l1.config(font =("Arial", 15,'bold'))
l1.pack(pady=(0,20))

Shape_selection = StringVar(root)
Shape_selection.set('--') 
dm1 = OptionMenu(root, Shape_selection, *Shape_Options) # dm1 = dropdown menu 1
dm1.pack(pady=20)



def Shape_Chosen():    
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
        

        len_prompt = Label(root, text="Length:", font = ('Arial',10,'bold')).pack(pady=(80,6))
        l = StringVar(root)
        length_entry = Entry(root,textvariable=l).pack(pady=6)

        width_prompt = Label(root, text="Width:", font = ('Arial',10,'bold')).pack(pady=6)
        w = StringVar(root)
        width_entry = Entry(root,textvariable=w).pack(pady=6)
        

        l2 = Label(root, text = "Select units for length and width:")
        l2.config(font =("Arial", 10,'bold'))
        l2.pack(pady=6)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm2 = dropdown menu 2
        dm2.pack(pady=6)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 10,'bold'))
        l3.pack(pady=6)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=6)

        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            length = float(l.get())
            width = float(w.get())
            unit_in=Units_i.get()
            unit_out=Units_o.get()
            
            dimensions = [length,width]
            Area = Geometry_input(Shape,dimensions,unit_in,unit_out)
            Area = str(Area)
            # print(Shape,length,width,unit_in,unit_out)
            # print(Area + ' '  + unit_out)
            l5 = Label(root,text='Area: ' + Area + ' ' + unit_out)
            l5.config(font =("Arial", 10,'bold'))
            l5.pack(pady=6)
            button1['state'] = DISABLED

            # list of all widgets
        button1 = Button(root, text="Calculate", command=Dimensions_Selection)
        button1.pack(pady =6)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 6)
        
        

################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################### CIRCLE ####################################################
        
    if Shape == 'Circle': 
        
        # img = Image.open('Circle.png')
        # img = img.resize((150,150))
        # image = ImageTk.PhotoImage(img)
        # Label(root, image = image).pack()



        Label(root, text="Diameter:", font = ('Arial',10,'bold')).pack(pady=(80,6))
        d = StringVar(root)
        diameter_entry = Entry(root,textvariable=d).pack(pady=6)       
        

        l2 = Label(root, text = "Select units for diameter:")
        l2.config(font =("Arial", 10,'bold'))
        l2.pack(pady=6)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm3 = dropdown menu 3
        dm2.pack(pady=6)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 10,'bold'))
        l3.pack(pady=6)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=6)

        
        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            diameter = float(d.get())
            unit_in=Units_i.get()
            unit_out=Units_o.get()
            
            dimensions = [diameter]
            Area = Geometry_input(Shape,dimensions,unit_in,unit_out)
            Area = str(Area)
            # print(Shape,length,width,unit_in,unit_out)
            print(Area + ' '  + unit_out)
            l5 = Label(root,text='Area: ' + Area + ' ' + unit_out)
            l5.config(font =("Arial", 10,'bold'))
            l5.pack(pady=6)
            button1['state'] = DISABLED

        button1 = Button(root, text="Calculate", command=Dimensions_Selection)
        button1.pack(pady =10)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 10)
        
        
################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
#################################################### SQUARE ####################################################

    if Shape == 'Square': 


        Label(root, text="Side:", font = ('Arial',10,'bold')).pack(pady=(80,6))
        s = StringVar(root)
        square_entry = Entry(root,textvariable=s).pack(pady=6)       
        

        l2 = Label(root, text = "Select units for side:")
        l2.config(font =("Arial", 10,'bold'))
        l2.pack(pady=6)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm3 = dropdown menu 3
        dm2.pack(pady=6)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 10,'bold'))
        l3.pack(pady=6)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=6)

 
        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5            
            side = float(s.get())
            unit_in=Units_i.get()
            unit_out=Units_o.get()
            
            dimensions = [side]
            Area = Geometry_input(Shape,dimensions,unit_in,unit_out)
            Area = str(Area)
            # print(Shape,length,width,unit_in,unit_out)
            print(Area + ' '  + unit_out)
            l5 = Label(root,text='Area: ' + Area + ' ' + unit_out)
            l5.config(font =("Arial", 10,'bold'))
            l5.pack(pady=6)
            button1['state'] = DISABLED


        button1 = Button(root, text="Calculate", command=Dimensions_Selection)
        button1.pack(pady =10)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 10)
        
    

################################################################################################################
#//////////////////////////////////////////////////////////////////////////////////////////////////////////////#
################################################# SPECIAL ######################################################

    if Shape == 'Special': 
        

        diameter_prompt = Label(root, text="Diameter:", font = ('Arial',10,'bold')).pack(pady=(80,6))
        d = StringVar(root)
        diameter_entry = Entry(root,textvariable=d).pack(pady=6)

        side_prompt = Label(root, text="Side:", font = ('Arial',10,'bold')).pack(pady=6)
        s = StringVar(root)
        side_entry = Entry(root,textvariable=s).pack(pady=6)
        

        l2 = Label(root, text = "Select units for diameter and side:")
        l2.config(font =("Arial", 10,'bold'))
        l2.pack(pady=6)
        Units_i = StringVar(root)
        Units_i.set('--') 
        dm2 = OptionMenu(root, Units_i, *Units_in) # dm2 = dropdown menu 2
        dm2.pack(pady=6)
        

        l3 = Label(root, text = "Select desired units for area:")
        l3.config(font =("Arial", 10,'bold'))
        l3.pack(pady=6)
        Units_o = StringVar(root)
        Units_o.set('--') 
        dm3 = OptionMenu(root, Units_o, *Units_out) # dm3 = dropdown menu 3
        dm3.pack(pady=6)

        def Calc_new_area():
            l5.destroy()
            button1['state'] = NORMAL

        def Dimensions_Selection():
            global l4
            global l5
            diameter = float(d.get())
            side = float(s.get())
            unit_in=Units_i.get()
            unit_out=Units_o.get()
            
            dimensions = [diameter,side]
            Area = Geometry_input(Shape,dimensions,unit_in,unit_out)
            Area = str(Area)
            # print(Shape,length,width,unit_in,unit_out)
            # print(Area + ' '  + unit_out)
            l5 = Label(root,text='Area: ' + Area + ' ' + unit_out)
            l5.config(font =("Arial", 10,'bold'))
            l5.pack(pady=6)
            button1['state'] = DISABLED

            # list of all widgets
        button1 = Button(root, text="Calculate", command=Dimensions_Selection)
        button1.pack(pady =6)
        reset_button = Button(root, text = 'Click to reset area', command = Calc_new_area).pack(pady = 6)
        
        

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

shape_selection_button = Button(root, text="Enter", command=Shape_Chosen).pack(pady=20)

clear_shape_button = button = Button(root, text="Clear", command=Clear_Shape).pack(pady=20)
   
  
        
        
mainloop()
