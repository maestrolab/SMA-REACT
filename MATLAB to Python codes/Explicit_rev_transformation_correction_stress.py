def Explicit_rev_transformation_correction_stress( MVF, eps_t, MVF_r,eps_t_r,sigma, eps, T, T_0,P, TP ):
    '''
    Function to correct for reverse transformation using implicit integration scheme
    Input variables are from elastic prediction

    Parameters
    ----------
    MVF : FLT
        Current martensitic volume fraction
    eps_t : FLT
        Current transformation strain
    MVF_r : FLT
        Current value for martensitic volume fraction at transformation reversal
    eps_t_r : FLT
        Current value for transformation strain at transformation reversal
    sigma : FLT
        Current stress
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
    Phi_rev : FLT
        Current Reverse transformation function value

    '''
    # Calculate reverse hardening function
    f_rev=-(-(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']-TP['Y_0_t'])

    # Hold values of MVF from previous load to for calculation of eps_t 
    MVF_previous=MVF
    # Solve for corrected MVF (explicit formula only works for n1=n2=n3=n4=1)
    MVF=(f_rev+TP['a3'])/TP['a2']
    # Correct if MVF bounds violated
    if MVF < 0:
        MVF = 0

    # Solve for Transformation Direction
    lamda = eps_t_r/MVF_r

    # Solve for transformation strain
    eps_t=eps_t+(MVF-MVF_previous)*lamda
    # eps_t_r does not change

    # Update transformation strain and martensitic volume fraction at transformation reversal
    if MVF == 0:
        MVF_r = 0
        eps_t_r = 0


    # Update Output Variables
    # Solve for Young's Modulus
    E = (1/P['E_A']+MVF*(1/P['E_M']-1/P['E_A']))**-1
    # Solve for Strain
    eps=sigma/E+P['alpha']*(T-T_0)+eps_t

    # Solve for the reverse transformation surface
    Phi_rev=0
    if MVF_r == 0:
        # Reverse transformation strain remains zero if Martensitic Strain at transformation reversal is zero
        Phi_rev=0

    else:
        Phi_rev = -(1+TP['D'])*sigma*eps_t_r/MVF_r-.5*(1/P['E_M']-1/P['E_A'])*sigma**2-TP['rho_delta_s0']*T+TP['rho_delta_u0']+f_rev-TP['Y_0_t']

    return MVF, eps_t, E, MVF_r, eps_t_r, eps, Phi_rev
