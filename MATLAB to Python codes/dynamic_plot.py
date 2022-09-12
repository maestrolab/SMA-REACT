# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 10:41:34 2022

@author: pwalgren58
"""
#Spyder presets
get_ipython().run_line_magic('matplotlib', 'qt') #plot in new window.
import matplotlib.pyplot as plt
import numpy as np
import time
plt.ion()
class DynamicUpdate():
    #Suppose we know the x range
    min_x = 0
    max_x = 10

    def on_launch(self,x_data,y_data):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'r-')
        self.exp, = self.ax.plot(x_data,y_data,'bo')
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        self.ax.set_xlim(self.min_x, self.max_x)
        #Other stuff
        self.ax.grid()
        ...

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    #Example
    def __call__(self):
        self.on_launch()
        xdata = []
        ydata = []
        for x in np.arange(0,10,0.5):
            xdata.append(x)
            ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
            self.on_running(xdata, ydata)
            time.sleep(1)
        return xdata, ydata

d = DynamicUpdate()

d.on_launch()

xdata = []
ydata = []
for x in np.arange(0,10,0.5):
    xdata.append(x)
    ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
    d.on_running(xdata, ydata)
    time.sleep(1)
