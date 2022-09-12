# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:34:38 2022

@author: Tiago
"""


import math
def partial_Hcur_sigma( sigma, sigma_crit, k, Hsat, Hmin ):
    '''
    Function to solve for the partial derivative of the current
    transformation strain (Hcur) with respect to sigma (stress)    

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
    partial_Hcur_sigma : FLT
        Partial derivative of the current transformation strain with respect
        to current applied stress. 
    '''
    # first solve for the partial derivative of abs(sigma) with respect to sigma
    if sigma > 0:
        partial_abssigma = 1
    elif sigma < 0:
        partial_abssigma = -1
    else:
        partial_abssigma = 0


    # Solve for partial derivative of current transformation strain
    if abs(sigma) <= sigma_crit:
        partial_Hcur_sigma = 0
    else:
        partial_Hcur_sigma = k*(Hsat-Hmin)*math.exp(-k*(abs(sigma)-sigma_crit))*partial_abssigma

    return partial_Hcur_sigma
