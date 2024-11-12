# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:47:57 2024

@author: pwal5
"""
import scipy.io

import numpy as np

import matplotlib.pyplot as plt

import os


def celsius_to_kelvin(temperature):
    return temperature + 273.15 

def kelvin_to_celsius(temperature):
    return temperature - 273.15

'''MATPLOTLIB PRESETS'''
#Graphs in a separate window
get_ipython().run_line_magic('matplotlib', 'qt')
#Graphs inline (ala Jupyter notebook)
#get_ipython().run_line_magic('matplotlib', 'inline')
plt.rc('font', family='serif') 
plt.rc('font', serif='Times New Roman') 
plt.rc('text', usetex='False') 
plt.rcParams.update({'font.size': 10})
plt.rcParams['svg.fonttype'] = 'none'


stress_levels = [100,200,300,400]
red = [1, 0 , 0]
blue = [0, 0, 1]

ax = plt.figure().add_subplot(projection='3d')
ax.set_proj_type('ortho')  # FOV = 0 deg

def plot_3d(x,y,z,ax,color):
    X, Y = np.meshgrid(x,y)
    
    
    ax.plot(x,y,z, color)
    
    offset_x = -50
    offset_y = 0
    offset_z = 0
    # ax.plot(x,y,offset_z,'gray')
    # ax.plot(x,offset_y,z,'gray')
    # only plot the austenite
    if color == 'b':
        ax.plot(x[0],y[0],z[0],'red',marker="*")
        ax.plot(offset_x,y[0],z[0],'red',marker='*')
    
    

for i in range(len(stress_levels)):
    file_name = 'optimal_model_'+str(i)+'.csv'
    file_path = os.path.join(
        os.getcwd(),
        file_name
        )
    data = np.loadtxt(file_path,delimiter=',')
    
    max_temperature_index = np.argmax(data[:,0])
    
    model_heating = data[:max_temperature_index,0]-273.15
    model_heating_strain = data[:max_temperature_index,1]*100
    
    model_heating_stress = stress_levels[i]*np.ones(shape=(len(model_heating,)))
    
    model_cooling = data[max_temperature_index:,0]-273.15
    model_cooling_strain = data[max_temperature_index:,1]*100
    
    model_cooling_stress = stress_levels[i]*np.ones(shape=(len(model_cooling,)))
    
    plot_3d(model_cooling,model_cooling_stress,model_cooling_strain,ax,color='b')
    plot_3d(model_heating,model_heating_stress,model_heating_strain,ax,color='r')
    
#plot something at -100,0,0 to mark the origin
ax.plot(-50,0,0,'red',marker='*')
    # ax.plot(model_heating,model_heating_strain,'r--')
    # ax.plot(model_cooling,model_cooling_strain,'b--')
    
# secax_x = ax.secondary_xaxis(
#     -0.25, functions=(celsius_to_kelvin, kelvin_to_celsius))
# secax_x.set_xlabel('Temperature, K')
    
ax.set_xlabel('Temperature, $^\circ C$')
ax.set_zlabel('Strain, %')
ax.set_ylabel('Stress')

fig = plt.gcf()
fig.set_size_inches(6,4)

# fig.tight_layout()