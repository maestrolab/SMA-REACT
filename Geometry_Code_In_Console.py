"""
Created on Mon Sep 27 13:06:07 2021
@author: Tiago
"""

# SMAEAT Geometry Code


################################################################################################################
# ------------------------------------------AREA-CALCULATION-FUNCTION-------------------------------------------#
################################################################################################################
from math import *


def Geometry_input(shape, unit_in, unit_out, meas1, meas2=0):
    ''' Calculates area of cross section given dimensions and performs unit conversion'''

    ########################################### SHAPE SELECTION ###############################################

    # print()
    # print(
    #     'This code calculates the area of a cross-section specified by the user.')  # Creating function for calculating the cross-sectional area of 'Test specimen'.
    # shape = input(
    #     'Select shape of cross-section from list [(C)ircle, (S)quare, (R)ectangle, S(p)ecial]: ')  # Creates an input variable. This variable will be the letter representing one of the shapes for the cross-section. This will allow code to determine what parameters to ask for to calculate the area.
    # shape = shape.upper()  # Makes variable 'shape' be upper case to make it easier to check if user's input is one of the acceptable inputs (C, S, R, P).
    # acceptable = ['C', 'S', 'R','P']  # This list represents allowable inputs. If input does not match one of the letters in "acceptable" list, program will ask user to input again.
    #
    # while shape not in acceptable:  # If user inputs a letter that is not in the list of acceptable letters, this loop begins. This while loop continues until user inputs a valid letter.
    #     print()
    #     print('Invalid input.')  # Message to user to inform them that input is not valid.
    #     print()
    #     shape = input('Please select shape of cross-section from list [(C)ircle, (S)quare, (R)ectangle, S(p)ecial]: ')
    #     shape = shape.upper()

        ########################################### UNIT SELECTION ################################################

    # print()  # Asks user for units for input measurements
    # unit_in = input('Select unit for input measurements from list [in, mm, m]: ')
    # unit_in = unit_in.upper()
    # while unit_in not in ['IN', 'MM', 'M']:
    #     print()
    #     print('Invalid input.')
    #     print()
    #     unit_in = input('Please select unit for input measurements from list [in, mm, m]: ')
    #     unit_in = unit_in.upper()
    #
    # print()  # Asks user for desired units of output measurements
    # unit_out = input('Select desired unit for output area from list [in, mm, m] (units will be squared): ')
    # unit_out = unit_out.upper()
    # while unit_out not in ['IN', 'MM', 'M']:
    #     print()
    #     print('Invalid input.')
    #     print()
    #     unit_out = input('Please select desired unit for output area from list [in, mm, m] (units will be squared): ')
    #     unit_out = unit_out.upper()

    ########################################## UNIT CONVERSION ################################################
    unit_in = unit_in.upper()
    unit_out = unit_out.upper()
    # For m to mm
    if (unit_in == 'M') and (unit_out == 'MM'):
        cf = 1000  # cf = conversion factor

    # For mm to m
    if (unit_in == 'MM') and (unit_out == 'M'):
        cf = 1 / 1000

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
        cf = 0.0254

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

    ########################################### AREA CACULATION ###############################################

    if shape == 'Circle':  # If statement to calculate area for circle
        # diameter = input('Input diameter: ')
        try:
            area = 0.25 * pi * (cf * float(meas1)) ** 2
            #print(f'The area of the circle is {area} {unit_out}^2.')
        except ValueError:
            print("Input invalid, please type a number for the diameter.")

    if shape == 'Square':  # If statement to calculate area for square
        # side = input('Input side legth: ')
        try:
            area = (cf * float(meas1)) ** 2
            #print(f'The area of the square is {area} {unit_out}^2.')
        except ValueError:
            print("Input invalid, please type a number for the side.")

    if shape == 'Rectangle':  # If statement to calculate area for rectangle
        # length = input('Input length: ')
        # width = input('Input width: ')
        try:
            area = (cf * float(meas1)) * (cf * float(meas2))

            #print(f'The area of the rectangle is {area} {unit_out}^2.')
        except ValueError:
            print("Input invalid, please type numbers for the length and width.")

    if shape == 'Cintraquad':  # If statement for calculating cross-sectional area of suqare with circular hole in middle
        # side = input('Input side: ')
        # diameter = input('Input diameter of hole: ')
        try:
            area = (cf * float(meas1)) ** 2 - (0.25 * pi * (cf * float(meas2)) ** 2)
            # print(f'The area of the cross-section is {area} {unit_out}^2.')
        except ValueError:
            print("Input invalid, please type numbers for the side and diameter.")

    if shape == "Custom":
        area = meas1

    return area


################################################################################################################
# -------------------------------------------UNIT-CONVERSION-FUNCTION-------------------------------------------#
################################################################################################################

def Unit_Conversion():
    ''' This function performs unit conversion calculations'''
    ########################################## FORCE/LENGTH/STRESS ############################################
    measurement = input(
        'Select the measurement you would like to covert the units for  [(F)orce, (L)ength, (S)tress]: ').upper()  # Selecting what to perform conversion on
    while measurement not in ['F', 'L', 'S']:  # Checking if input is acceptable. If not acceptable, while loop starts
        print()
        print('Invalid input.')
        print()
        measurement = input(
            'Please select the measurement you would like to covert the units for [(F)orce, (L)ength, (S)tress]: ').upper()

    # ------------------------------------------------ FORCE -------------------------------------------------
    if measurement == 'F':
        ########################################### UNIT SELECTION ############################################

        print()  # Asks user for units for input measurements
        unit_in = input('Select unit for input Force from list [N, lbf]: ')
        unit_in = unit_in.upper()
        while unit_in not in ['N', 'LBF']:
            print()
            print('Invalid input.')
            print()
            unit_in = input('Please select unit for input Force from list [N, lbf]: ')
            unit_in = unit_in.upper()

        print()  # Asks user for desired units of output measurements
        unit_out = input('Select desired unit for output Force from list [N, lbf]: ')
        unit_out = unit_out.upper()
        while unit_out not in ['N', 'LBF']:
            print()
            print('Invalid input.')
            print()
            unit_out = input('Please select desired unit for output Force from list [N, lbf]: ')
            unit_out = unit_out.upper()

        ########################################## UNIT CONVERSION ############################################

        # For N to N
        if (unit_in == 'N') and (unit_out == 'N'):
            cf = 1  # cf = conversion factor

        # For lbf to lbf
        if (unit_in == 'LBF') and (unit_out == 'LBF'):
            cf = 1

        # For lbf to N
        if (unit_in == 'LBF') and (unit_out == 'N'):
            cf = 4.44822

        # For N to lbf
        if (unit_in == 'N') and (unit_out == 'LBF'):
            cf = 0.224809

        if unit_out == 'LBF':
            unit_out = unit_out.lower()

        ############################################# FORCE INPUT #############################################

        force_in = input('Input force magnitude: ')
        try:
            force_in = float(force_in)
            force_out = force_in * cf
            print(f'Output force: {force_out} {unit_out} .')

        except:
            print('Error: Force input is not a number.')

    # ------------------------------------------------ LENGTH -------------------------------------------------
    if measurement == 'L':
        ########################################### UNIT SELECTION ################################################

        print()  # Asks user for units for input measurements
        unit_in = input('Select unit for input length from list [in, mm, m]: ')
        unit_in = unit_in.upper()
        while unit_in not in ['IN', 'MM', 'M']:
            print()
            print('Invalid input.')
            print()
            unit_in = input('Please select unit for input length from list [in, mm, m]: ')
            unit_in = unit_in.upper()

        print()  # Asks user for desired units of output measurements
        unit_out = input('Select desired unit for output length from list [in, mm, m]: ')
        unit_out = unit_out.upper()
        while unit_out not in ['IN', 'MM', 'M']:
            print()
            print('Invalid input.')
            print()
            unit_out = input('Please select desired unit for output length from list [in, mm, m]: ')
            unit_out = unit_out.upper()

        ########################################## UNIT CONVERSION ################################################

        # For m to mm
        if (unit_in == 'M') and (unit_out == 'MM'):
            cf = 1000  # cf = conversion factor

        # For mm to m
        if (unit_in == 'MM') and (unit_out == 'M'):
            cf = 1 / 1000

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
            cf = 0.0254

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

        length_in = input("Input length magnitude:")
        try:
            length_in = float(length_in)

            length_out = length_in * cf
            print(f"Output length: {length_out} {unit_out} .")

        except ValueError:
            print('Error: length input is not a number.')

    # ------------------------------------------------- STRESS ---------------------------------------------------
    if measurement == 'S':
        ########################################### UNIT SELECTION ################################################

        print()  # Asks user for units for input stress
        unit_in = input('Select unit for input stress from list [psi, ksi, MPa, Pa]: ')
        unit_in = unit_in.upper()
        while unit_in not in ['PSI', 'KSI', 'MPA', 'PA']:
            print()
            print('Invalid input.')
            print()
            unit_in = input('Please select unit for input stress from list [psi, ksi, MPa, Pa]: ')
            unit_in = unit_in.upper()

        print()  # Asks user for desired units of output stress
        unit_out = input('Select desired unit for output stress from list [psi, ksi, MPa, Pa]: ')
        unit_out = unit_out.upper()
        while unit_out not in ['PSI', 'KSI', 'MPA', 'PA']:
            print()
            print('Invalid input.')
            print()
            unit_out = input('Please select desired unit for output stress from list [psi, ksi, MPa, Pa]: ')
            unit_out = unit_out.upper()

        ########################################## UNIT CONVERSION ################################################

        # For psi to psi
        if (unit_in == 'PSI') and (unit_out == 'PSI'):
            cf = 1  # cf = conversion factor

        # For ksi to ksi
        if (unit_in == 'KSI') and (unit_out == 'KSI'):
            cf = 1

        # For MPa to MPa
        if (unit_in == 'MPA') and (unit_out == 'MPA'):
            cf = 1

        # For Pa to Pa
        if (unit_in == 'PA') and (unit_out == 'PA'):
            cf = 1

            # For Pa to MPa
        if (unit_in == 'PA') and (unit_out == 'MPA'):
            cf = 1 / 1000000

            # For Pa to psi
        if (unit_in == 'PA') and (unit_out == 'PSI'):
            cf = 0.000145038

        # For Pa to ksi
        if (unit_in == 'PA') and (unit_out == 'KSI'):
            cf = 0.000145038 / 1000

        # For MPa to Pa
        if (unit_in == 'MPA') and (unit_out == 'PA'):
            cf = 10000000

        # For MPA to psi
        if (unit_in == 'MPA') and (unit_out == 'PSI'):
            cf = 145.038

        # For MPA to ksi
        if (unit_in == 'MPA') and (unit_out == 'KSI'):
            cf = 0.145038

        # For psi to ksi
        if (unit_in == 'PSI') and (unit_out == 'KSI'):
            cf = 1 / 1000

        # For psi to MPa
        if (unit_in == 'PSI') and (unit_out == 'MPA'):
            cf = 0.00689476

        # For psi to Pa
        if (unit_in == 'PSI') and (unit_out == 'PA'):
            cf = 6894.76

        # For ksi to Pa
        if (unit_in == 'KSI') and (unit_out == 'PA'):
            cf = 6894760

        # For ksi to MPa
        if (unit_in == 'KSI') and (unit_out == 'MPA'):
            cf = 6.89476

        # For ksi to psi
        if (unit_in == 'KSI') and (unit_out == 'PSI'):
            cf = 1000

        if unit_out == 'MPA':  # Changing from all uppercase [MPA, PA, PSI, KSI] to appropriate format [MPa, Pa, psi, ksi]
            unit_out = 'MPa'
        elif unit_out == 'PA':
            unit_out = 'Pa'
        else:
            unit_out = unit_out.lower()

        stress_in = input('Input stress magnitude: ')

        try:
            stress_in = float(stress_in)

            stress_out = stress_in * cf
            print(f"Output stress: {stress_out} {unit_out} .")

        except ValueError:
            print('Error: stress input is not a number.')