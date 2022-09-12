"""
Created on Mon Sep 27 13:06:07 2021

@author: Tiago
"""

# SMAEAT Geometry Code


################################################################################################################
#------------------------------------------AREA-CALCULATION-FUNCTION-------------------------------------------#
################################################################################################################
from math import *
def Geometry_input(shape,dimensions,unit_in,unit_out): 
    ''' Calculates area of cross section given dimensions and performs unit conversion'''


    ########################################## UNIT CONVERSION ################################################
        
    # For m to mm
    if (unit_in == 'm') and (unit_out == 'mm^2'):
        cf = 1000 # cf = conversion factor
        
    # For mm to m
    if (unit_in == 'mm') and (unit_out == 'm^2'):
        cf = 1/1000
    
    # For mm to in
    if (unit_in == 'mm') and (unit_out == 'in^2'):
        cf = 0.0393701
    
    # For in to mm
    if (unit_in == 'in') and (unit_out == 'mm^2'):
        cf = 25.4  
        
    # For m to in
    if (unit_in == 'm') and (unit_out == 'in^2'):
        cf = 39.3701 
        
    # For in to m
    if (unit_in == 'in') and (unit_out == 'm^2'):
        cf =   0.0254
        
    # For m to m
    if (unit_in == 'm') and (unit_out == 'm^2'):
        cf = 1
    
    # For in to in
    if (unit_in == 'in') and (unit_out == 'in^2'):
        cf = 1
        
    # For mm to mm
    if (unit_in == 'mm') and (unit_out == 'mm^2'):
        cf = 1
        


    ########################################### AREA CACULATION ###############################################
        
    if shape == 'Circle': # If statement to calculate area for circle 
        
        diameter = dimensions[0] # for Circle, dimensions input is a list with only one item equivalent to the diameter of the circle
        A = 0.25 * pi * (cf*diameter)**2
        
            
    
    if shape == 'Square': # If statement to calculate area for square
    
        side = dimensions[0] # for Square, dimensions input is a list with only one item equivalent to the side of the square
        A = (cf*side)**2
            
    
    
    if shape == 'Rectangle': # If statement to calculate area for rectangle
        
        length = dimensions[0] # for Rectangle, dimensions input is a list with two items, length and width
        width = dimensions[1]
        A = (cf*length) * (cf*width)
            
        
        
    if shape == 'Special':  # If statement for calculating cross-sectional area of suqare with circular hole in middle
        diameter = dimensions [0]
        side = dimensions[1]
        A = (cf*side)**2 - (0.25*pi*(cf*diameter)**2)
            
            
    return A


################################################################################################################
#-------------------------------------------UNIT-CONVERSION-FUNCTION-------------------------------------------#
################################################################################################################

def Unit_Conversion(dimension):
    
    ''' This function performs unit conversion calculations'''
    ########################################### UNIT SELECTION ################################################
    
    print() # Asks user for units for input measurements
    unit_in = input ('Select unit for input measurements from list [in, mm, m]: ')
    unit_in = unit_in.upper()
    while unit_in not in ['IN','MM','M']:
        print()
        print('Invalid input, please type a unit abbreviation from list [in, mm, m].')
        print()
        unit_in = input ('Select unit for input measurements from list [in, mm, m]: ')
        unit_in = unit_in.upper()
        
    print() # Asks user for desired units of output measurements
    unit_out = input ('Select desired unit for output area from list [in, mm, m] (units will be squared): ')
    unit_out = unit_out.upper()
    while unit_out not in ['IN','MM','M']:
        print()
        print('Invalid input, please type a unit abbreviation from list [in, mm, m].')
        print()
        unit_out = input ('Select desired unit for output area from list [in, mm, m] (units will be squared): ')
        unit_out = unit_out.upper()
        
        
        
    ########################################## UNIT CONVERSION ################################################
        
    # For m to mm
    if (unit_in == 'M') and (unit_out == 'MM'):
        cf = 1000 # cf = conversion factor
        
    # For mm to m
    if (unit_in == 'MM') and (unit_out == 'M'):
        cf = 1/1000
    
    # For mm to in
    if (unit_in == 'MM') and (unit_out == 'IN'):
        cf = 0.0393701
    
    # For in to mm
    if (unit_in == 'IN') and (unit_out == 'MM'):
        cf = 25.4  
        
    # For m to in
    if (unit_in == 'M') and (unit_out == 'IN'):
        cf = 39.3701 
        
    # For in to m
    if (unit_in == 'IN') and (unit_out == 'M'):
        cf =   0.0254
        
    # For m to m
    if (unit_in == 'M') and (unit_out == 'M'):
        cf = 1
    
    # For in to in
    if (unit_in == 'IN') and (unit_out == 'IN'):
        cf = 1
        
    # For mm to mm
    if (unit_in == 'MM') and (unit_out == 'MM'):
        cf = 1
        
    unit_out = unit_out.lower()
    return()