# -*- coding: utf-8 -*-
"""


@author: fanmu
"""
from H_cursolver import H_cursolver

def Elastic_Transformation_check_stress( P,TP,sigma, eps_prev, T, T_prev, T0, \
                                        sigma_prev, Phi_fwd_prev, Phi_rev_prev,\
                                        E, MVF, eps_t, eps_t_r, MVF_r ):
    '''
    Function to return Elastic prediction and also check for transformation
    without using scaled projections (non-transformation surface rate-informed)
    
    Returns chck=1 for forward transformation, 2 for reverse transformation 
    and 0 for no transformation
    

    Parameters
    ----------
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meanings.
    TP : DICT
        Transformation properties for the SMA. Just another dictionary 
        comprised of intermediate calculations
    sigma : FLT
        Current stress
    eps_prev : FLT
        Previous total strain
    T : FLT
        Current temperature
    T_prev : FLT
        Previous temperature
    T0 : FLT
        Initial temperature
    sigma_prev : FLT
        Previous stress
    Phi_fwd_prev : FLT
        Forward transformation function value for the previous increment
    Phi_rev_prev : FLT
        Reverse transformation function value for the previous increment
    E : FLT
        Youngs modulus
    MVF : FLT
        Current value for martensitic volume fraction
    eps_t : FLT
        Current value for transformation strain
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal

    Returns
    -------
    eps : FLT
        Current total strain
    eps_t : FLT
        Current transformation strain
    MVF : FLT
        Current martensitic volume fraction
    H_cur : FLT
        Current maximum transformation strain
    Phi_fwd : FLT
        Current Forward transformation function value
    Phi_rev : FLT
        Current Reverse transformation function value
    chck : INT
        Flag to describe if transformation is occuring, and in what direction.
        chck=1 for forward transformation (A->M)
             2 for reverse transformation (M->A)
             0 for no transformation (Elastic)
    '''

    # Solve for strain using elastic prediciton
    eps=sigma/E+P['alpha']*(T-T0)+eps_t
    
    #  Solve for current transformational strain
    H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    
    # Solve for hardening functions 
    f_fwd = .5*TP['a1']*(1+MVF**P['n1']-(1-MVF)**P['n2'])+TP['a3']
    f_rev = .5*TP['a2']*(1+MVF**P['n3']-(1-MVF)**P['n4'])-TP['a3']
    
    # Solve for the forward transformation surface
    chck=0
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+\
              .5*(1/P['E_M']-1/P['E_A'])*sigma**2+\
              TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
    # If the forward transformation surface is greater than zero the material
    # is undergoing a forward transformation (chck=1)
    if Phi_fwd >0:
        chck=1
    
    # Solve for the reverse transformation surface
    Phi_rev=0
    
    if MVF_r == 0:
        # Reverse transformation strain remains zero if Martensitic Strain at
        # transformation reversal is zero
        MVR_r = 0
        
    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-\
                 0.5*(1/P['E_M']-1/P['E_A'])*sigma**2-\
                 TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
        # If the revverse transformation surface is greater than zero the material
        # is undergoing a forward transformation (chck=2)
        if Phi_rev > 0:
            chck=2
    return eps, eps_t, MVF, H_cur, Phi_fwd,Phi_rev, chck
    
