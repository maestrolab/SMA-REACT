# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 17:24:37 2022

@author: fanmu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
x = np.array([.5,.8, .8, .9, .34,.21, .33, .48, .5, .7, .22, 0.2, 0.2, 0.3, .6])

X = pd.Series(['E_M','E_M-E_A','M_s','M_s-M_f',
'A_s','A_s-A_f','C_M','C_A','H_min','H_max-H_min','k',
'n_1','n_2','n_3','n_4'], dtype ="category")

Y = x
plt.figure(3)
plt.barh(X,Y)
plt.show()
plt.pause(.6)
plt.clf()
x = np.array([.7,.4, .75, .3, .34,.28, .39, .78, .53, .72, .25, 0.5, 0.2, 0.8, .6])
Y = x
plt.pause(.6)
plt.barh(X,Y)