# -*- coding: utf-8 -*-
"""
Created on Tue Feb 13 16:03:57 2024

@author: pwal5
"""

import scipy.io

import numpy as np

import matplotlib.pyplot as plt

get_ipython().run_line_magic('matplotlib','qt')

file_name = 'Fig2a_FAT01_429_E195HT_550C3hrAC_T_C_H_LB True 2ndCycle.mat'

mat = scipy.io.loadmat(file_name)

temperature = mat['Xdata_SampTemp_degC']

strain = mat['Ydata_TrueStrain_pct']

colors = mat['LineColors']

stress_levels = [400, 300, 200, 100, 50, 0]
# red = [1, 0 , 0]
# blue = [0, 0, 1]

# fig, ax = plt.subplots(1,1)

data = {}

for i in range(int(len(temperature[0,:])/2)):
    heating_temperature = temperature[0,2*i].T
    cooling_temperature = temperature[0,2*i+1].T
    
    heating_strain = strain[0,2*i].T
    cooling_strain = strain[0,2*i+1].T
    
    total_temperature = np.concatenate(
        (heating_temperature,cooling_temperature)
        )
    total_strain = np.concatenate(
        (heating_strain,cooling_strain)
        )
    total_stress = np.full(
        shape=(len(total_temperature),1),
        fill_value = stress_levels[i]
        )
    
    data = np.zeros((len(total_temperature),3))
    
    data[:,0] = total_temperature[:,0]
    data[:,1] = total_strain[:,0]
    data[:,2] = total_stress[:,0]
    
    file_name = str(stress_levels[i])+' MPa.txt'
    
    np.savetxt(file_name,data,delimiter='\t')
    
    # data['experiment'+str(i)] = {}
    
    # data['experiment'+str(i)]['Temperature'] = total_temperature
    # data['experiment'+str(i)]['Stress'] = total_stress
    # data['experiment'+str(i)]['Strain'] = total_strain
    
    
    
    
    # if colors[0,i][0,0] == 1:
    #     color = 'r'
    # elif colors[0,i][0,2] == 1:
    #     color = 'b'
        
    # ax.scatter(temperature[0,i],strain[0,i],label=i)
    
    # plt.show()
    


