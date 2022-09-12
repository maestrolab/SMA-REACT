# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 03:52:43 2022

@author: fanmu
"""
import numpy as np
import pandas as pd;
import matplotlib.pyplot as plt
global initial_error
global initial_delta_eps
initial_error = 0;
initial_delta_eps = 0;

# Inputs:
# - x(1): E_M
# - x(2): E_M - E_A
# - x(3): M_s
# - x(4): M_s - M_f
# - x(5): A_s
# - x(6): A_f - A_s
# - x(7): C_M
# - x(8): C_A
# - x(9): H_min
# - x(10): H_max - H_min
# - x(11): k
# - x(12): n_1 
# - x(13): n_2
# - x(14): n_3
# - x(15): n_4
#alphas and sigma_crit are equal to zero in this problem
# Initial guess (parameters calibrated from experiments)

# x0 = [37e9, 53e9, ...
#      273.15 + 55.74, 55.74 - 35.57, 273.15 + 72.93, 87.77 - 72.93, 4.54E6, 8.64E6, ...
#      0.1, 0.12, 0.0001, ...
#      .5, .5, .5, .5];
# x0 = [60e9, 60e9, ...
#      374.2813, 374.2813 - 290.7571, 318.9352,  397.9732 - 318.9352, 7.8E6, 7.8E6, ...
#      0.0952, -0.001, 0.0001, ...
#      .2215, .2059, .2040, .2856];
x0 = np.array([91.01E9,91.01E9-119.967E9, 273.15-45.85, -45.85--62.34, 273.15-17.66,-2.34--2.34, 8.15e6, 7.64E6,0.0015, 0.034 - 0.0015, 0.0102e-6, 0.2, 0.2, 0.2, 0.3])


A = np.array([])
b = np.array([])
Aeq = np.array([])
beq = np.array([])
#Getting rid of H_min as a DV
lb = np.array([20e9, -80e9, #E_M, E_M-E_A
     0, 273.15-45, 10,5, 4E6, 4E6,  #M_s, M_s - M_f, A_s, A_f-A_s, C_M, C_A
     0., 0.01,  0.001e-6, # H_Min, H_max-H_min, k
     0.1,0.1,0.1,0.1]) #n_1,n_2,n_3,n_4
 
ub = np.array([90e9, 50e9, #E_M, E_M-E_A
     273.15+20, 50, 273.15+10,50, 12E6, 12E6, #M_s, M_s - M_f, A_s, A_f-A_s, C_M, C_A
     0.05, 0.1,  0.1e-6, # H_Min, H_max-H_min, k
     0.9,0.9,0.9,0.9]) #n_1,n_2,n_3,n_4

# Normalized x0
n_x0 = np.divide((x0 - lb),(ub-lb))

# Normalized lower and upper bounds
n_lb = np.zeros(np.shape(lb))
n_ub = np.ones(np.shape(ub))

# Define function to be optimized
fun = lambda x: normalized_full_cost(x, lb, ub)
figure(1)
figure(10)
nonlcon = [];
hold on
options = optimoptions('fmincon','Display','iter','Algorithm','sqp', 'MaxFunEvals', 1000000, 'PlotFcns',{@optimplotx,...
    @optimplotfval,@optimplotfirstorderopt});

opts = gaoptimset(...
     'PopulationSize', 200, ...
     'Generations', 10, ...
     'Display', 'iter', ...
     'EliteCount', 2);
n_x0 = ga(fun, length(lb), A, b, Aeq, beq, n_lb, n_ub, nonlcon, opts);

#x = fmincon(fun, n_x0, A, b, Aeq, beq, n_lb, n_ub, nonlcon);
x = fmincon(fun, n_x0, A, b, Aeq, beq, n_lb, n_ub, nonlcon, options);

normalized_full_plot_optimized(x, lb, ub)