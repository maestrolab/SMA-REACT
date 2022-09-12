# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:55:32 2022

@author: Tiago
"""

from numpy import sign
from numpy.linalg import inv 

def Explicit_fwd_transformation_correction_stress( MVF, eps_t, sigma, H_cur,eps, T, T_0,P, TP ):
    '''
    Function to correct for forward transformation using explicit integration scheme
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
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
    # P: Material Properties
    # TP: Transformation Properties

    # Calculate forward hardening function
    f_fwd=(1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-TP['Y_0_t']

    # Solve for corrected MVF (explicit formula only works for n1=n2=n3=n4=1)
    # Hold values of MVF from previous load to for calculation of eps_t 
    MVF_previous=MVF
    MVF=(f_fwd-TP['a3'])/TP['a1']
    # Correct if MVF bounds violated
    if MVF > 1:
        MVF = 1

    # Solve for transformation direction
    lamda = H_cur*sign(sigma)

    # Solve for transformation strain
    eps_t=eps_t+(MVF-MVF_previous)*lamda
    # Update transformation strain and martensitic volume fraction at transformation reversal
    eps_t_r=eps_t
    MVF_r=MVF

    # Update Output Variables
    # Solve for Young's Modulus
    E= inv(inv(P['E_A'])+MVF*(inv(P['E_M'])-inv(P['E_A'])))
    # Solve for Strain
    eps=sigma/E+P['alpha']*(T-T_0)+eps_t

    # Update the forward transformation surface
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']

    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd
