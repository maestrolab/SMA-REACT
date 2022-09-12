# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 20:12:31 2022

@author: Tiago
"""


from numpy import sign
from util_funcs import *

def Implicit_rev_transformation_correction_stress( MVF, eps_t, E,MVF_r,eps_t_r,sigma, eps, T, T_0, Phi_rev,P, TP):
    # Function to correct for reverse transformation using implicit integration scheme
    # Input variables are from elastic prediction/ transformation check
    
    # Find initial values for iteration (k=1)
    # Transformation Direction for reverse transformation
    Lamda = eps_t_r/MVF_r

    # Iterate MVF until its change after an iteration is negligible (less than
    # assigned tolerance MVF_tolerance) or until MVF reaches bound of 0

    maxiter = 100
    for i in range(maxiter):
        
        # Determine the partial derivative of the transformation
        # surface (Phi) with respect to stress
        partial_Phi_rev_sigma_k=-(1+TP['D'])*eps_t_r/MVF_r-(1/P['E_M']-1/P['E_A'])*sigma
        
        # Determine the partial derivative of transformation surface
        # (Phi) with respect to Martensitic volume fraction
        partial_Phi_rev_MVF_k=partial_Phi_rev_MVF(MVF,P['delta'],P['n3'],P['n4'],TP['a1'],TP['a2'],TP['a3'])
        
        # Use partial derivatives and MVF evolution to solve A^t
        A_t=partial_Phi_rev_MVF_k-partial_Phi_rev_sigma_k*E*((1/P['E_M']-1/P['E_A'])*sigma+Lamda)
        
        # Determine the correction for MVF for the current iteration
        delta_MVF=-Phi_rev/partial_Phi_rev_MVF_k
        
        # Update MVF using the delta MVF value
        # Hold the MVF value of the previous iteration in case of
        # MVF < 0 correction
        MVF_k=MVF
        MVF=MVF+delta_MVF
        
        # Correct if MVF reaches a bound of 0
        if MVF < 0:
            MVF = 0
            # Recalculate transformation strain for corrected MVF
            eps_t=eps_t+(MVF-MVF_k)*Lamda
            # Youngs Modulus for austenite material
            E=P['E_A']
            # Update transformation reversal values to zero
            eps_t_r=0
            MVF_r=0
        
    
        # Update transformation strain using calculated values for change in
        # MVF (delta_MVF) and transformation direction
        eps_t=eps_t+delta_MVF*Lamda
        # Update value for Young's Modulus and use this value to determine
        # stress (sigma)
        
        E=(1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**-1
    
        
        # Update transformation surface/output variables for next
        # iteration
        # Update transformation direction
        Lamda = eps_t_r/MVF_r
        # Update hardening function
        f_rev = .5*TP['a2']*(1+(MVF**(1/P['n3'])/(MVF+P['delta'])**(1/P['n3']-1))**P['n3']-((1-MVF)**(1/P['n4'])/(1-MVF+P['delta'])**(1/P['n4']-1))**P['n4'])-TP['a3']
        # Update transformation surface
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
        
        # Transformation reversal values remain the same
        if abs(delta_MVF) < P['MVF_tolerance']:
            break
    
        
        if iter == maxiter:
            raise exception(['ERROR: MAXIMUM NUMBER OF ITERATIONS (', num2str(iter),  ') REACHED IN THE RMA'])


    # Update strain (eps) using known values of sigma, T and updated values 
    # of E and eps_t
    eps= sigma/E + P['alpha']*(T-T_0)+eps_t
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_rev



# TEST NUMBERS -------------------------------------------------


E = 200

eps = 13

eps_t = 0.6

eps_t_r = 50

MVF = 30

MVF_r = 30

Phi_rev = 6.5

sigma = 9

T = 7

T_0 = 11

P = {"E_M":2,"E_A":5,"delta":4, "n3":3,"n4":6,"alpha":7,"MVF_tolerance":20}

TP = {"D":6,"a1":7,"a2":3,"a3":5,"rho_delta_s0":8,"rho_delta_u0":9,"Y_0_t":10}