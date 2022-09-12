# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 03:10:15 2022

@author: fanmu
"""

# Before running code, remember to check if csv files are in correct
# format, otherwise just open it in excel and save it.
global initial_error
global initial_delta_eps
import numpy as np

initial_error = 0;
initial_delta_eps = 0;
x = np.zeros(15)

x[0] = 38.03E9
x[1] = 18.46E9
# Transformation temperatures [M:Martensite, A:
# Austenite], [s:start,f:final]
x[2] = 273.15 + 62.38 #M_s
x[3] = 62.38 - 51.69  #M_s - M_f
x[4] = 273.15 + 70.96 #A_s
x[5] = 83.49 - 70.96 #A_f - A_s

# Slopes of transformation boundarings into austenite [C_A] and
# martensite [C_M] at Calibration Stress 
x[6] = 8.15e6; #C_M
x[7] = 7.64E6; #C_A

# Maximum and minimum transformation strain
x[8] =  0.0924617829295; #H_min
x[9] = 0.126325797371 -  0.0924617829295; #H_max - H_min

x[10] = 0.00524735758484e-6; #k
# sigma_crit = 140E6;

# Coefficient of thermal expansion
# P.alpha = 0; #1E-5;

# Smoothn hardening parameters 
# NOTE: smoothness parameters must be 1 for explicit integration scheme
x[11] = 0.8; #0.618;
x[12] = 0.8; #0.313;
x[13] = 0.8; #0.759;
x[14] = 0.8; #0.358;

lb = np.array([20e9, 10e9, 273.15 + 30, 0., 273.15 + 30, 0, 4E6, 4E6, 0.05, 0., 0., 0., 0., 0., 0.])
 
ub = np.array([50e9, 40e9, 273.15 + 100, 50., 273.15 + 140, 50., 10E6, 10E6, 0.15, 0.05, 0.1e-6, .5, .5, .5, .5])

 # Normalized x0
n_x = np.divide((x - lb),(ub-lb))

# Normalized lower and upper bounds
n_lb = np.zeros(np.shape(lb))
n_ub = np.ones(np.shape(ub))
r = normalized_full_cost(n_x, lb, ub)

full_plot_optimized(x)