# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 15:23:12 2022

@author: pwalgren58
"""
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


xdata = [np.linspace(0,10,10),np.linspace(-1,1,10)]
ydata = [xdata[0]*0.1,xdata[1]*-0.1-0.5]

figure,ax = plt.subplots()
lines, = ax.plot([],[],'r-')


lines.set_xdata(xdata)
lines.set_ydata(ydata)

ax.relim()