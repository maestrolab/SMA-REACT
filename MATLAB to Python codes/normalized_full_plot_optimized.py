"""
Created on Wed May 18 18:11:01 2022

@author: Tiago
"""


# IMPORT STATEMENTS
from util_funcs import *
from Full_Model_stress import *
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


df = pd.read_excel('testing_data_c2_only.xlsx')
stress = df["Stress (N/mm^2)"]
strain = df["Strain"]
temp = df["Sample"]
integration_scheme = 'implicit'
elastic_check = 'No'
P = {'E_M':100,'E_A':80,"M_s":20,"M_s - M_f":10, "A_s":300,"A_s - A_f":100,'C_M':14, 'C_A':15,'H_min':12, 'H_max - H_min': 40, 'k':200, "n1":3,"n2":4,"n3":5,"n4":6}
x = np.array((1000000,800000,200000,100000,3000000,1000000,140000,150000,120000,400000,2000000,10,14,18,22))
ub = 50
lb = 20

def normalized_full_plot_optimized(x, lb, ub):
    # Inputs:
    # - x[0]: E_M
    # - x[1]: E_A
    # - x[2]: M_s
    # - x[3]: M_s - M_f
    # - x[4]: A_s
    # - x[5]: A_f - A_s
    # - x[6]: C_M
    # - x[7]: C_A
    # - x[8]: H_min
    # - x[9]: H_max - H_min
    # - x[10]: k
    # - x[11]: n_1
    # - x[12]: n_2
    # - x[13]: n_3
    # - x[14]: n_4
    # alphas and sigma_crit are equal to zero in thisproblem
    
    x = x*(ub - lb) + lb

    # Denormalizing
    data_7 = np.loadtxt("7 MPa Scootch.txt", dtype=float)
    data_50 = np.loadtxt("50 MPa Scootch.txt", dtype=float)
    data_100 = np.loadtxt("100 MPa Scootch.txt", dtype=float)
    data_150 = np.loadtxt("150 MPa Scootch.txt", dtype=float)
    data_200 = np.loadtxt("200 MPa Scootch.txt", dtype=float)
    #access the first column at index 0
    T_7 = data_7[:,0] + 273.15
    T_50 = data_50[:,0] + 273.15
    T_100 = data_100[:,0] + 273.15
    T_150 = data_150[:,0] + 273.15
    T_200 = data_200[:,0] + 273.15
    #access the second column at index 
    eps_7 = data_7[:,1]
    eps_50 = data_50[:,1]
    eps_100 = data_100[:,1]
    eps_150 = data_150[:,1]
    eps_200 = data_200[:,1]
    #find smallest element in array
    eps_7 = eps_7 - eps_7.min()
    eps_50 = eps_50 - eps_50.min()
    eps_100 = eps_100 - eps_100.min()
    eps_150 = eps_150 - eps_150.min()
    eps_200 = eps_200 - eps_200.min()
    #get third column at position 2
    sigma_7 = data_7[:,2]
    sigma_50 = data_50[:,2]
    sigma_100 = data_100[:,2]
    sigma_150 = data_150[:,2]
    sigma_200 = data_200[:,2]
    # get min value in array and its index
    min_T_7 = T_7.min()
    I_7 = np.argmax(T_7)
    min_T_50 = T_50.min()
    I_50 = np.argmax(T_50)
    min_T_100 = T_100.min()
    I_100 = np.argmax(T_100)
    min_T_150 = T_150.min()
    I_150 = np.argmax(T_150)
    min_T_200 = T_200.min()
    I_200 = np.argmax(T_200)
    # merginging into array consiting of increaseing vlaues till peak, the going from peak to min value
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
    
    # INPUT:
    # MATERIAL PARAMETERS (Structure: P)
    # Young's Modulus for Austenite and Martensite 
    P['E_M'] = x[0]
    P['E_A'] = x[0] - x[1]
    #P['E_A'] = 119E9
    #P['E_M'] = P['E_A']
    # Transformation temperatures (M:Martensite, A:Austenite), (s:start,f:final)
    P['M_s'] = x[2]
    P['M_f'] = x[2] - x[3]
    P['A_s'] = x[4]
    P['A_f'] = x[5] + x[4]
    
    # Slopes of transformation boundarings into austenite [C_A] and
    # martensite [C_M] at Calibration Stress 
    P['C_M'] = x[6]
    P['C_A'] = x[7]
    
    # Maximum and minimum transformation strain
    #Changing H_min to 0
    P['H_min'] = x[8]
    P['H_sat'] = x[8] + x[9]
    
    
    P['k'] = x[10]
    P['sig_crit'] = 0.
    
    # Coefficient of thermal expansion
    P['alpha'] = 0.
    
    # Smoothn hardening parameters 
    # NOTE: smoothness parameters must be 1 for explicit integration scheme
    P['n1'] = x[11]
    P['n2'] = x[12]
    P['n3'] = x[13]
    P['n4'] = x[14]
    
    # Algorithmic delta for modified smooth hardening function
    P['delta']=1e-5
    
    # Calibration Stress
    P['sig_cal']=200E6
    
    # Tolerance for change in MVF during implicit iteration
    P['MVF_tolerance']=1e-8
    
    print(P)
    #Transform into MPa
    #Transform into MPa
    sigma_7 = 1e6 * 7*np.ones(np.shape(sigma_7))
    sigma_50 = 1e6 * 50*np.ones(np.shape(sigma_50))
    sigma_100 = 1e6 * 100*np.ones(np.shape(sigma_100))
    sigma_150 = 1e6 * 150*np.ones(np.shape(sigma_150))
    sigma_200 = 1e6 * 200*np.ones(np.shape(sigma_200))
    
     # Elastic Prediction Check
    elastic_check = 'N'
    
     # Integration Scheme
    integration_scheme = 'I'
    
    
    [eps_num_7, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_7, sigma_7, P, elastic_check, integration_scheme )
    [eps_num_50, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_50, sigma_50, P, elastic_check, integration_scheme )
    [eps_num_100, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_100, sigma_100, P, elastic_check, integration_scheme )
    [eps_num_150, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_150, sigma_150, P, elastic_check, integration_scheme )
    [eps_num_200, MVF,eps_t,E,MVF_r,eps_t_r ] = Full_Model_stress( T_200, sigma_200, P, elastic_check, integration_scheme )
    
    eps_num_7 = eps_num_7 - min(eps_num_7)
    eps_num_50 = eps_num_50 - min(eps_num_50)
    eps_num_100 = eps_num_100 - min(eps_num_100)
    eps_num_150 = eps_num_150 - min(eps_num_150)
    eps_num_200 = eps_num_200 - min(eps_num_200)
    #figure out box on
    # plt.figure()
    plt.plot(T_7, eps_7,'k',linewidth=1.5)
    plt.plot(T_7, eps_num_7,'b',linewidth=1.5)
    # plt.xlabel('Temperature (K)')
    # plt.ylabel('Strain (m/m)')
    # plt.title('7 MPa')
    
    # plt.figure()
    plt.plot(T_50, eps_50,'g',linewidth=1.5)
    plt.plot(T_50, eps_num_50,'b',linewidth=1.5)
    # plt.xlabel('Temperature (K)')
    # plt.ylabel('Strain (m/m)')
    # plt.title('50 MPa')
    
    # plt.figure()
    plt.plot(T_100, eps_100,'c',linewidth=1.5)
    plt.plot(T_100, eps_num_100,'b',linewidth=1.5)
    # plt.xlabel('Temperature (K)')
    # plt.ylabel('Strain (m/m)')
    # plt.title('100 MPa')
    
    # plt.figure()
    plt.plot(T_150, eps_150,'m',linewidth=1.5)
    plt.plot(T_150, eps_num_150,'b',linewidth=1.5)
    # plt.xlabel('Temperature (K)')
    # plt.ylabel('Strain (m/m)')
    # plt.title('150 MPa')
    
     # plt.figure()
     # box on
     # hold on
     # plt.plot(MVF,'b',linewidth=1.5)
     # xlabel('Time')
     # ylabel('MVF')
     # title('150 MPa')
    
    
    # plt.figure()

    plt.plot(T_200, eps_200,'r',linewidth=1.5)
    plt.plot(T_200, eps_num_200,'b',linewidth=1.5)
    plt.xlabel('Temperature (K)')
    plt.ylabel('Strain (m/m)')
    plt.title('Strain vs Temperature')
    # plt.title('200 MPa')
    
     #Make a master figure
    
    #Separate each cycle into cooling and heating segments
    max_T_7 = T_7.max()
    I_7 = np.argmax(T_7)
    max_T_50 = T_50.max()
    I_50 = np.argmax(T_50)
    max_T_100 = T_100.max()
    I_100 = np.argmax(T_100)
    max_T_150 = T_150.max()
    I_150 = np.argmax(T_150)
    max_T_200 = T_200.max()
    I_200 = np.argmax(T_200)
    
    T_7 = T_7 -273.15
    T_50 = T_50 -273.15
    T_100 = T_100 -273.15
    T_150 = T_150 -273.15
    T_200 = T_200 -273.15
    
    heat_T_7 = T_7[0:I_7+1]
    cool_T_7 = T_7[I_7:]
    heat_eps_7 = eps_7[0:I_7+1]
    cool_eps_7 = eps_7[I_7:]
    heat_eps_num_7 = eps_num_7[0:I_7+1]
    cool_eps_num_7 = eps_num_7[I_7:]
    
    heat_T_50 = T_50[0:I_50+1]
    cool_T_50 = T_50[I_50:]
    heat_eps_50 = eps_50[0:I_50+1]
    cool_eps_50 = eps_50[I_50:]
    heat_eps_num_50 = eps_num_50[0:I_50+1]
    cool_eps_num_50 = eps_num_50[I_50:]
    
    heat_T_100 = T_100[0:I_100+1]
    cool_T_100 = T_100[I_100:]
    heat_eps_100 = eps_100[0:I_100+1]
    cool_eps_100 = eps_100[I_100:]
    heat_eps_num_100 = eps_num_100[0:I_100+1]
    cool_eps_num_100 = eps_num_100[I_100:]
    
    heat_T_150 = T_150[0:I_150+1]
    cool_T_150 = T_150[I_150:]
    heat_eps_150 = eps_150[0:I_150+1]
    cool_eps_150 = eps_150[I_150:]
    heat_eps_num_150 = eps_num_150[0:I_150+1]
    cool_eps_num_150 = eps_num_150[I_150:]
    
    heat_T_200 = T_200[0:I_200+1]
    cool_T_200 = T_200[I_200:]
    heat_eps_200 = eps_200[0:I_200+1]
    cool_eps_200 = eps_200[I_200:]
    heat_eps_num_200 = eps_num_200[0:I_200+1]
    cool_eps_num_200 = eps_num_200[I_200:]
# ------------------------------------------------------------------------------------------------------------

    temp_list = [T_7,T_7,T_50,T_50,T_100,T_100,T_150,T_150,T_200,T_200]
    eps_list = [eps_7,eps_num_7,eps_50,eps_num_50,eps_100,eps_num_100,eps_150,eps_num_150,eps_200,eps_num_200]

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111)
    plt.title("Temperature vs. Strain")
    plt.xlabel('Temperature')
    plt.ylabel('Strain')
    for i in range(len(temp_list)):
    

        if i%2 == 0:        
            cool_heat_flag = []
        
            cool_heat_cutoff = np.nanargmin(temp_list[i])
            cooling_temps = temp_list[i][0:cool_heat_cutoff + 1]
            cooling_strain = eps_list[i][0:cool_heat_cutoff + 1]
            heating_temps = temp_list[i][cool_heat_cutoff:]
            heating_strain = eps_list[i][cool_heat_cutoff:]
        
            cool_heat_flag.extend(["Cooling" for x in range(len(cooling_temps))])
            cool_heat_flag.extend(["Heating" for x in range(len(heating_temps) - 1)])
            
            ax1.plot(cooling_temps, cooling_strain, "b--")
            ax1.plot(heating_temps, heating_strain, "r--")
        
        
        else:
            cool_heat_flag = []
        
            cool_heat_cutoff = np.nanargmin(temp_list[i])
            cooling_temps = temp_list[i][0:cool_heat_cutoff + 1]
            cooling_strain = eps_list[i][0:cool_heat_cutoff + 1]
            heating_temps = temp_list[i][cool_heat_cutoff:]
            heating_strain = eps_list[i][cool_heat_cutoff:]
        
            cool_heat_flag.extend(["Cooling" for x in range(len(cooling_temps))])
            cool_heat_flag.extend(["Heating" for x in range(len(heating_temps) - 1)])
            
            ax1.plot(cooling_temps, cooling_strain, "b")
            ax1.plot(heating_temps, heating_strain, "r")

 # --------------------------------------------------------------------------------------------------------
            
normalized_full_plot_optimized(x, lb, ub)
