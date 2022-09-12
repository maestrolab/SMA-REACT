# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 13:07:17 2022

@author: fanmu
"""
import numpy as np
File_data = np.loadtxt("7 MPa Scootch.txt", dtype=float)
T_7 = File_data[:,0] + 273.15;
numcol = File_data.shape[0]
print(numcol)
H_cur = np.zeros((File_data.shape[0],1),float)
print(H_cur)