# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:41:32 2022

@author: Tiago
"""

import numpy as np
import math
def H_cursolver( sigma, sigma_crit, k, H_min, H_sat):
    '''
    Function to determine the current transformation strain H^cur using
    inputs for stress, critical stress, k, Hsat and Hmin.

    Parameters
    ----------
    sigma : FLT
        current material stress
    sigma_crit : FLT
        critical stress at which transformation strain initiates.
    k : FLT
        coefficient that governs the evolution of transformation 
        strain with respect to applied stress. For more information, 
        see IJP, 2012, eq. 3.7 (DOI: https://doi.org/10.1016/j.ijplas.2011.10.009)
    H_min : FLT
        minimium transformation strain
    H_sat : FLT
        maximum, or saturated transformation strain

    Returns
    -------
    H_cur : FLT
        current available transformation strain

    '''

    if abs(sigma) <= sigma_crit:
        H_cur=H_min
    else:
        H_cur = H_min + (H_sat - H_min)*(1-math.exp(-k*(abs(sigma)-sigma_crit)))

    return H_cur
