# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 10:45:22 2022

@author: fanmu
"""
from util_funcs import *
from numpy import sign
def Implicit_fwd_transformation_correction_stress( MVF, eps_t, E,MVF_r,eps_t_r,sigma, H_cur,eps, T, T_0, Phi_fwd,P, TP ):
    '''
    Function to correct for forward transformation using implicit integration scheme.
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
    H_cur : FLT
        Current maximum transformation strain
    eps : FLT
        Current total strain
    T : FLT
        Current temperature
    T0 : FLT
        Initial temperature
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations

    Raises
    ------
    exception
        Return mapping algorithm failed. 

    Returns
    -------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    E : FLT
        Youngs modulus
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    eps : FLT
        Current total strain
    Phi_fwd : FLT
        Current Forward transformation function value

    '''

    
    # Find initial values for iteration (k=1)
    # Evaluate transformation direction (Lambda)
    Lambda = H_cur*sign(sigma)
    # Iterate MVF until its change after an iteration is negligible (less than
    # assigned tolerance MVF_tolerance) or until Martensitic volume fraction
    # reaches bound of 1
    maxiter = 1000
    for i in range(maxiter):
        # Determine the partial derivative of the current
        # transformation strain (Hcur) and transformation surface (Phi)
        # with respect to stress using functions for these equations
        partial_Hcur_sigma_k=partial_Hcur_sigma(sigma,P['sig_crit'],P['k'],P['H_sat'],P['H_min'])
        partial_Phi_fwd_sigma_k=partial_Phi_fwd_sigma(sigma,H_cur,TP['D'],partial_Hcur_sigma_k,P['E_M'],P['E_A'])
        
        # Determine the partial derivative of transformation surface
        # (Phi) with respect to Martensitic volume fraction
        partial_Phi_fwd_MVF_k=partial_Phi_fwd_MVF(MVF,P['delta'],P['n1'],P['n2'],TP['a1'],TP['a2'],TP['a3'])
        
        # Use partial derivatives and MVF evolution to solve A^t
        A_t=partial_Phi_fwd_MVF_k-partial_Phi_fwd_sigma_k*E*((1/P['E_M']-1/P['E_A'])*sigma+Lambda)
        
        # Determine the correction for MVF for the current iteration
        delta_MVF=-Phi_fwd/partial_Phi_fwd_MVF_k
        
        # Hold the MVF value of the previous iteration in case of
        # MVF > 1 correction
        MVF_k=MVF
        # Update MVF using the delta MVF value
        MVF=MVF+delta_MVF
        
        # Correct if MVF reaches a bound of 1
        if MVF > 1:
            MVF = 1
            # Recalculate transformation strain for corrected MVF
            eps_t=eps_t+(MVF-MVF_k)*Lambda
            # Youngs Modulus for completely martensite material
            E=P['E_M']
            # Update transformation reversal values
            eps_t_r=eps_t
            MVF_r=MVF
            break        
        # Update transformation strain using  calculated values for change in
        # MVF (delta_MVF) and transformation direction
        eps_t=eps_t+delta_MVF*Lambda;
        # Update value for Young's Modulus 
        E=(1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**(-1)
        
        # Update transformation surface/output variables for next
        # iteration using values for current transformation strain,
        # transformation direction and hardening function
        # Update current transformation strain
        H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
        # Update transformation direction
        Lambda = H_cur*sign(sigma);
        # Update hardeing function
        f_fwd = .5*TP['a1']*(1+(MVF**(1/P['n1'])/(MVF+P['delta'])**(1/P['n1']-1))**P['n1']-((1-MVF)**(1/P['n2'])/(1-MVF+P['delta'])**(1/P['n2']-1))**P['n2'])+TP['a3']
        # Update transformation surface
        Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
        
        # Update transformation reversal values
        eps_t_r=eps_t
        MVF_r=MVF
        
        if abs(delta_MVF) < P['MVF_tolerance']:
            break
        
        if iter == maxiter:
            raise exception(['ERROR: MAXIMUM NUMBER OF ITERATIONS (', num2str(iter),  ') REACHED IN THE RMA'])
        
        
    # Update strain (eps) using known values of sigma, T and updated values
    # of E and eps_t
    eps= sigma/E + P['alpha']*(T-T_0)+eps_t
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd
