# -*- coding: utf-8 -*-
"""
plot_dv_evolution.py

Plots the evolution of design variables with respect to their
bounds for different calibrations.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

import matplotlib.colors as mcolors



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

dv_order = ['E^M, GPa',
            'E^A, GPa',
            "C^M, MPa",
            "C^A, MPa",
            "H_{max}-H_{min}, mm/mm",
            "M_s, ^\circ\!C",
            "M_s-M_f, ^\circ\!C",
            "A_s, ^\circ\!C",
            "A_f-A_s, ^\circ\!C",
            "H_{min}, mm/mm",
            "\sigma_{crit}, MPa",
            "k, 1/MPa",
            r"\alpha, 1/^\circ\!C",
            "n_1, -",
            "n_2, -",
            "n_3, -",
            "n_4, -"
            ]


dim_x = 5
dim_y = 2

marker_size = 60

fig, ax = plt.subplots(dim_y,dim_x)

file_name = "collected_parameters.xlsx"
sheet_name = "1"

colors = ['darkgray','dimgray','black']

labels = ['Initial calibration $\\varepsilon = 1.51\%$',
          'Updated bounds $\\varepsilon = 1.34\%$',
          'Final calibration $\\varepsilon = 1.30\%$'
          ]

x = 0
for sheet_name in ["1","2","3"]:
    
    label = labels[x]
    
    data = pd.read_excel(
        file_name,
        sheet_name,
        dtype={'Parameter': str, 'Value': float,
               "Specified":str,'Lower Bound':float,
               "Upper Bound":float,
               }
        )
    
    i,j,counter = 0,0,0
    

    for dv in dv_order:
        if dv in [
                "H_{min}, mm/mm",
                "\sigma_{crit}, MPa",
                "k, 1/MPa",
                r"\alpha, 1/^\circ\!C",
                "n_2, -",
                "n_3, -",
                "n_4, -"
                ]:
            counter +=1
            pass
        else:
            ax[i,j].set_title(r"$"+dv+"$")
            if data['Specified'].iloc[counter] == 'Y':
                marker = '*'
            else:
                marker = 'd'
                
                lower_bound = data['Lower bound with units'].iloc[counter]
                upper_bound = data['Upper bound with units'].iloc[counter]
                
                ax[i,j].errorbar(
                    x,
                    (lower_bound+upper_bound)/2.0,
                    (upper_bound-lower_bound)/2.0,
                    fmt='none',
                    capsize=5,
                    color=colors[x],
                    linestyle=''
                    )
                # box = [Rectangle(
                #     xy = (x-0.5,lower_bound),
                #     width = 1,
                #     height = upper_bound-lower_bound,
                #     )
                #     ]
                
                # # Create patch collection with specified colour/alpha
                # pc = PatchCollection(box, facecolor="none", alpha=0.75,
                #                      edgecolor="black")
            
                # # Add collection to Axes
                # ax[i,j].add_collection(pc)
            ax[i,j].scatter(
                x,
                data['Value with units'].iloc[counter],
                s = marker_size,
                marker=marker,
                color=colors[x],
                label=label,
                )
    
            # Remove x-axis labels and ticks
            ax[i,j].set_xticks([])
            ax[i,j].set_xlim([-0.5,2.5])
            j+=1
            counter +=1
            if j > dim_x-1:
                j = 0
                i +=1
    x += 1
    
# Delete the subplot at position (dim_x,dim_y)
# ax[dim_y-1, dim_x-1].remove()

#Add one master legend
handles, labels = ax[0,2].get_legend_handles_labels()
fig.legend(handles, labels, loc='lower center',ncol=len(labels))

# Set the y-axis to log scale for k
# ax[1,4].set_yscale('log')
# ax[1,4].set_ylim([5E-4,2E0])
# with open(file_name) as json_file:
#     data = json.load(json_file)
    
#     final_solution = data['final_solution']
#     i,j = 0,0
#     for dv in dv_order:
#         print(i,j,dv)
#         if dv == 'A_f-A_s':
#             value = final_solution['A_f'] - final_solution['A_s']
#         elif dv == 'M_f-M_s':
#             value = final_solution['M_f'] - final_solution['M_s']
#         else:
#             value = final_solution[dv]
#         ax[i,j].scatter(0,value)



# fig.set_size_inches(6,3.5)

# fig.tight_layout()

