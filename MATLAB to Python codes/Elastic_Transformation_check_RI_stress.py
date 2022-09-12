from util_funcs import *

def Elastic_Transformation_check_RI_stress( P, TP, sigma, eps_prev, T, T_prev, T0, \
                                           sigma_prev, Phi_fwd_prev, Phi_rev_prev, \
                                               E, MVF, eps_t, eps_t_r, MVF_r ):
    '''
    Function to return elastic prediction and check for transformation using
    scaled elastic projections (transformation surface rate-informed)
    
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
    
    # Solve for current transformational strain  
    H_cur=H_cursolver(sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    
    # Solve for hardening functions 
    f_fwd = .5*TP['a1']*(1+MVF**P['n1']-(1-MVF)**P['n2'])+TP['a3']
    f_rev = .5*TP['a2']*(1+MVF**P['n3']-(1-MVF)**P['n4'])-TP['a3']
    
    # Solve for the forward transformation surface
    Phi_fwd = (1-TP['D'])*abs(sigma)*H_cur+.5*(1/P['E_M']-1/P['E_A'])*sigma**2+TP['rho_delta_s0']*T-TP['rho_delta_u0']-f_fwd-TP['Y_0_t']
    
    # Solve for the reverse transformation surface
    Phi_rev=0;
    if MVF_r == 0:
        MVR_r =0
        # Reverse transformation strain remains zero if Martensitic Strain at
        # transformation reversal is zero
    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']
    
    # Find the scaled projections of strain, temperature (and the scaled change
    # (delta) in these values
    # s: scaling factor
    s = 0.001
    scaled_d_eps = s*(eps - eps_prev);
    scaled_d_T = s*(T - T_prev);
    scaled_T = scaled_d_T + T_prev;
    
    # Find the scaled projection of stress using scaled projections for strain
    # and temperature
    scaled_d_sigma= E*((eps_prev+scaled_d_eps) - P['alpha']*(scaled_T - T0) - eps_t) - sigma_prev
    scaled_sigma= scaled_d_sigma + sigma_prev;
    
    # Calculate the scaled projections for forward and reverse transformation
    # surface
    # Calculate the current transformational strain for these scaled values
    # (required to find the transformation surfaces)
    scaled_H_cur = H_cursolver(scaled_sigma,P['sig_crit'],P['k'],P['H_min'],P['H_sat'])
    # Forward transformation surface for scaled values
    scaled_Phi_fwd = (1-TP['D'])*abs(scaled_sigma)*scaled_H_cur+.5*(1/P['E_M']-1/P['E_A'])*scaled_sigma**2+TP['rho_delta_s0']*scaled_T - TP['rho_delta_u0'] - f_fwd - TP['Y_0_t']
    # Reverse transformation surface for scaled values
    scaled_Phi_rev=0;
    if MVF_r == 0:
        MVR_r =0
    else:
        scaled_Phi_rev = -(1+TP['D'])*scaled_sigma*eps_t_r/MVF_r - .5*(1/P['E_M']-1/P['E_A'])*scaled_sigma**2 - TP['rho_delta_s0']*scaled_T + TP['rho_delta_u0']+f_rev-TP['Y_0_t']
    
    
    # Check for transformation
    # Determine change in transformation surface from the previous value to the
    # scaled projection
    scaled_d_Phi_fwd = scaled_Phi_fwd - Phi_fwd_prev
    scaled_d_Phi_rev = scaled_Phi_rev - Phi_rev_prev
    
    # Forward Transformation Check
    if scaled_d_Phi_fwd > 0 and scaled_d_Phi_rev <= 0:
        if Phi_fwd > 0 and MVF < 1:
            # Forward transformation
            chck = 1
        else:
            # No transformation
            chck = 0
    # Reverse transformation check    
    elif scaled_d_Phi_rev > 0 and scaled_d_Phi_fwd <= 0:
        if Phi_rev > 0 and MVF > 0:
            # Reverse transformation
            chck = 2
        else:
            #No transformation
            chck = 0
        
    elif scaled_d_Phi_rev <= 0 and scaled_d_Phi_fwd <=0:
        # No transformation
        chck = 0
        
    elif scaled_d_Phi_fwd > 0 and scaled_d_Phi_rev > 0:
        if Phi_fwd <= 0 and Phi_rev <=0:
            #No transformation
            chck = 0
        elif Phi_fwd > 0 and Phi_rev <= 0:
            # Check for forward transformation
            if Phi_fwd > 0 and MVF < 1:
                # Forward transformation
                chck = 1
            else:
                # No transformation
                chck = 0
        
        elif Phi_rev > 0 and Phi_fwd <= 0:
            # Check for reverse transformation
            if Phi_rev > 0 and MVF > 0:
                # Reverse transformation
                chck = 2
            else:
                #No transformation
                chck = 0
        # If both transformation surfaces are greater than zero, check which one
        # has the higher rate of change
        elif Phi_fwd > 0 and Phi_rev > 0:
            if scaled_d_Phi_fwd > scaled_d_Phi_rev:
                # Check for forward transformation
                if Phi_fwd > 0 and MVF < 1:
                    # Forward transformation
                    chck = 1
                else:
                    # No transformation
                    chck = 0
            
            else:
                # Check for reverse transformation
                if Phi_rev > 0 and MVF > 0:
                    # Reverse transformation
                    chck = 2
                else:
                    #No transformation
                    chck = 0

    #chck
    return eps, eps_t, MVF, H_cur, Phi_fwd, Phi_rev, chck
