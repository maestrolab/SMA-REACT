# -*- coding: utf-8 -*-
"""
Created on Fri Feb 25 11:22:39 2022

@author: fanmu
"""
from Explicit_fwd_transformation_correction_stress import *
from Explicit_rev_transformation_correction_stress import *
def Explicit_Transformation_Correction_stress( P, TP, chck,MVF, eps_t, E,\
                                              MVF_r,eps_t_r,sigma, H_cur,eps,\
                                                  T, T_0, Phi_fwd, Phi_rev ):
    '''
    Function to return the outputs for Martensitic volume fraction, stress,
    transformation strain, Young's modulus, etc. using explicit integration
    scheme. Input variables are from elastic prediction.

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)
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
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value

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
    Phi_rev : FLT
        Current Reverse transformation function value

    '''

    
    # Return elastic predictions if no transformation is occuring
    if chck == 0:
        return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev
     
    # Forward Transformation correction    
    if chck ==1:
        (MVF, eps_t, E, MVF_r,    \
         eps_t_r, eps, Phi_fwd) = \
            Explicit_fwd_transformation_correction_stress( \
                        MVF, eps_t, sigma, H_cur,eps, T, T_0,P,TP )
        
    # Reverse Transformation correction    
    elif chck == 2:
        (MVF, eps_t, E, MVF_r,     \
         eps_t_r, eps, Phi_rev ) = \
            Explicit_rev_transformation_correction_stress( \
                MVF, eps_t, MVF_r,eps_t_r,sigma, eps, T, T_0,P, TP )
    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_fwd, Phi_rev