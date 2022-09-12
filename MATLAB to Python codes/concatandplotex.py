# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 02:06:22 2022

@author: fanmu
"""
import numpy as np
import matplotlib.pyplot as plt
import math
print(math.sqrt(25))
T_7 = np.array([5,4,3,2,1,2,3,4,5]);
eps_7 = np.array([10,9,8,7,6,7,8,9,10]);
print(eps_7[1:5])
I_7 = 4;

T_7= np.concatenate((T_7[I_7:],T_7[0:I_7+1]))
eps_7 = np.concatenate((eps_7[I_7:],eps_7[0:I_7+1]))
print(T_7)
print(eps_7)
plt.plot(T_7, eps_7,'b', linewidth =1.5)
plt.xlabel('Temperature (K)')
plt.ylabel('Strain (m/m)')
plt.title('7 MPa')