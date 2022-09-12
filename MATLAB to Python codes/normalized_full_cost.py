# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 04:10:21 2022

@author: fanmu
"""
import pandas as pd;
import matplotlib.pyplot as plt
import math
def normalized_full_cost(x, lb, ub):

    global initial_error
    global initial_delta_eps
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
    
    # # Upper and lower bounds used in normalization
    # lb = [20e9, 10e9, ...
    #      273.15 + 30, 0, 273.15 + 30, 0, 4E6, 4E6, ...
    #      0.05, 0., 0, ...
    #      0., 0., 0., 0.];
    #  
    # ub = [50e9, 40e9, ...
    #      273.15 + 100, 50., 273.15 + 140, 50., 10E6, 10E6, ...
    #      0.15, 0.05, 0.1e-6, ...
    #      1., 1., 1., 1.];
    # 
    
    plt.figure(10)
    plt.clf(10)
    
    
    X = pd.Series({'E_M','E_M-E_A','M_s','M_s-M_f',
        'A_s','A_s-A_f','C_M','C_A','H_min','H_max-H_min','k',
        'n_1','n_2','n_3','n_4'}, dtype ="category")
    
    # preserve order when graphed
    #X = reordercats(X,{'E_M','E_M-E_A','M_s','M_s-M_f',
    #    'A_s','A_s-A_f','C_M','C_A','H_min','H_max-H_min','k',
    #    'n_1','n_2','n_3','n_4'});
    
    
    #X = categorical({'E_M','E_M-E_A','M_s-M_f',...
    #    'A_s','A_s-A_f','C_M','C_A','H_{max}-H_{min}','k'});
    #X = reordercats(X,{'E_M','E_M-E_A','M_s-M_f',...
    #    'A_s','A_s-A_f','C_M','C_A','H_{max}-H_{min}','k'});
    Y = x;
    plt.barh(X,Y);
    plt.show

    #ylim(axes1,[0 1]);
    #ylim([0 1])
    
    # Denormalizing
    x = x*(ub - lb) + lb;
        
    #Read data from experiments. For constant stress sigma:
    # - data_sigma(1): Temperature (in Celsius)
    # - data_sigma(2): Strain
    # - data_sigma(3): Stress
    data_7 = textread('7 MPa Scootch.txt');
    data_50 = textread('50 MPa Scootch.txt');
    data_100 = textread('100 MPa Scootch.txt');
    data_150 = textread('150 MPa Scootch.txt');
    data_200 = textread('200 MPa Scootch.txt');
    

    
    T_7 = np.concatenate((T_7[I_7:],T_7[0:I_7+1]))
    T_50 = np.concatenate((T_50[I_50:],T_7[0:I_50+1]))
    T_100 = np.concatenate((T_100[I_100:],T_100[0:I_100+1]))
    T_150 = np.concatenate((T_150[I_150:],T_150[0:I_150+1]))
    T_200 = np.concatenate((T_200[I_200:],T_200[0:I_200+1]))
    
    eps_7 = np.concatenate((eps_7[I_7:],eps_7[0:I_7+1]))
    eps_50 = np.concatenate((eps_50[I_50:],eps_7[0:I_50+1]))
    eps_100 = np.concatenate((eps_100[I_100:],eps_100[0:I_100+1]))
    eps_150 = np.concatenate((eps_150[I_150:],eps_150[0:I_150+1]))
    eps_200 = np.concatenate((eps_200[I_200:],eps_200[0:I_200+1]))
    
    sigma_7 = np.concatenate((sigma_7[I_7:],sigma_7[0:I_7+1]))
    sigma_50 = np.concatenate((sigma_50[I_50:],sigma_7[0:I_50+1]))
    sigma_100 = np.concatenate((sigma_100[I_100:],sigma_100[0:I_100+1]))
    sigma_150 = np.concatenate((sigma_150[I_150:],sigma_150[0:I_150+1]))
    sigma_200 = np.concatenate((sigma_200[I_200:],sigma_200[0:I_200+1]))
    # plot(T_50,eps_50)
    # hold on
    # plot(T_100,eps_100)
    # plot(T_150,eps_150)
    
    
    # INPUT:
    # MATERIAL PARAMETERS (Structure: P)
    # Young's Modulus for Austenite and Martensite 
    P.E_M = x[1]
    P.E_A = x[1] - x[2]
    #P.E_A = 119E9;
    #P.E_M = P.E_A; 
    # Transformation temperatures (M:Martensite, A:
    # Austenite), (s:start,f:final)
    P.M_s = x[3]
    P.M_f = x[3] - x[4]
    P.A_s = x[5];
    P.A_f = x[6] + x[5]
    
    # Slopes of transformation boundarings into austenite [C_A] and
    # martensite [C_M] at Calibration Stress 
    P.C_M = x[7]
    P.C_A = x[8]
    
    # Maximum and minimum transformation strain
    #Changing H_min to 0
    P.H_min = x[9];
    P.H_sat = x[9] + x[10]
    
    
    P.k = x[11]
    P.sig_crit = 0

    # Coefficient of thermal expansion
    P.alpha = 0.
    
    # Smoothn hardening parameters 
    # NOTE: smoothness parameters must be 1 for explicit integration scheme
    P.n1 = x[12]
    P.n2 = x[13]
    P.n3 = x[14]
    P.n4 = x[15]
    
    # Algorithmic delta for modified smooth hardening function
    P.delta=1e-5
    
    # Calibration Stress
    P.sig_cal=200E6
    
    # Tolerance for change in MVF during implicit iteration
    P.MVF_tolerance=1e-8
    
    #Transform into MPa
    sigma_7 = 1e6 * 7*np.ones(np.shape(sigma_7));
    sigma_50 = 1e6 * 50*np.ones(np.shape(sigma_50));
    sigma_100 = 1e6 * 100*np.ones(np.shape(sigma_100));
    sigma_150 = 1e6 * 150*np.ones(np.shape(sigma_150));
    sigma_200 = 1e6 * 200*np.ones(np.shape(sigma_200));
    
    # Elastic Prediction Check
    elastic_check = 'N'
    
    # Integration Scheme
    integration_scheme = 'I'
    
    try:
        [eps_num_7, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_7, sigma_7, P, elastic_check, integration_scheme );
        [eps_num_50, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_50, sigma_50, P, elastic_check, integration_scheme );
        [eps_num_100, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_100, sigma_100, P, elastic_check, integration_scheme );
        [eps_num_150, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_150, sigma_150, P, elastic_check, integration_scheme );
        [eps_num_200, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_200, sigma_200, P, elastic_check, integration_scheme );
    
        eps_num_7 = eps_num_7 - min(eps_num_7);
        eps_num_50 = eps_num_50 - min(eps_num_50);
        eps_num_100 = eps_num_100 - min(eps_num_100);
        eps_num_150 = eps_num_150 - min(eps_num_150);
        eps_num_200 = eps_num_200 - min(eps_num_200);
        
        plt.figure(1)
        plt.clf(1)
        plt.plot(T_50,eps_num_50,'r', 'linewidth',2)
        plt.plot(T_7,eps_num_7,'k','linewidth',2)
        plt.plot(T_100,eps_num_100,'b', 'linewidth',2)
        plt.plot(T_150,eps_num_150,'g', 'linewidth',2)
        plt.plot(T_200,eps_num_200,'k', 'linewidth',2)
        plt.plot(T_7,eps_7,'--k','linewidth',2)
        plt.plot(T_50,eps_50,'--r', 'linewidth',2)
        plt.plot(T_100,eps_100,'--b', 'linewidth',2)
        plt.plot(T_150,eps_150,'--g', 'linewidth',2)
        plt.plot(T_200,eps_200,'--k', 'linewidth',2)
        
        # Root-mean squared error:
        output = math.sqrt(sum((eps_50-eps_num_50)**2)/numel(eps_50))
        output = output + math.sqrt(sum((eps_7-eps_num_7)**2)/numel(eps_7))
        output = output + math.sqrt(sum((eps_100-eps_num_100)**2)/numel(eps_100))
        output = output + math.sqrt(sum((eps_150-eps_num_150)**2)/numel(eps_150))
        output = output + math.sqrt(sum((eps_200-eps_num_200)**2)/numel(eps_200))
    
        if (initial_error == 0):
            initial_error = output
    
    
        delta_eps_7 = (max(eps_7) - min(eps_7)) - (max(eps_num_7) - min(eps_num_7))
        delta_eps_50 = (max(eps_50) - min(eps_50)) - (max(eps_num_50) - min(eps_num_50))
        delta_eps_100 = (max(eps_100) - min(eps_100)) - (max(eps_num_100) - min(eps_num_100))
        delta_eps_150 = (max(eps_150) - min(eps_150)) - (max(eps_num_150) - min(eps_num_150))
        delta_eps_200 = (max(eps_200) - min(eps_200)) - (max(eps_num_200) - min(eps_num_200))
    #     disp(delta_eps_50)
    #     disp(delta_eps_100)
    #     disp(delta_eps_150)
    #     disp(delta_eps_200)
        delta_eps_error = sqrt((delta_eps_7**2 + delta_eps_50**2 + ...
            delta_eps_100**2 + delta_eps_150**2+ delta_eps_200**2)/3.)
    
        if (initial_delta_eps == 0):
            initial_delta_eps = delta_eps_error
        
        output = output/initial_error + delta_eps_error/initial_delta_eps
    
    except
     	output = 100.
    return output
    
    
    
