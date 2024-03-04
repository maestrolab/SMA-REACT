import numpy as np
from .util_funcs import (
    H_cursolver,
    partial_Hcur_sigma,
    Elastic_Transformation_check_RI_stress,
    Elastic_Transformation_check_stress,
    Explicit_Transformation_Correction_stress,
    Implicit_Transformation_Correction_stress
    )


def Full_Model_stress(T, sigma, P, elastic_check, integration_scheme):
    '''
    Calculate strain history as a function of stress and temperature 
    in a one-dimensional SMA bar. This function assumes the material 
    starts in martensite (cold to hot). 

    Parameters
    ----------
    T : NUMPY ARRAY
        Temperature history
    sigma : NUMPY ARRAY
        Stress history
    P : DICT
        Material properties for the SMA. See the documentation for 
        all properties and their meaning.
    elastic_check : STR
        Possible values: 'Yes', 'Y', 'No', 'N'
        Yes or No binary that determines whether the transformation surface
        is rate-informed. Default value is 'N'
    integration_scheme : STR
        Possible values: 'I', 'E'
        Flag to perform implicit or explicit material integration (i.e.,
        the return mapping algorithm integration scheme).

    Returns
    -------
    eps : NUMPY ARRAY
        Calculated strain history
    MVF : NUMPY ARRAY
        Calculated martensitic volume fraction history
    eps_t : NUMPY ARRAY
        Calculated transformation strain history
    E : NUMPY ARRAY
        Calculated modulus history
    MVF_r : NUMPY ARRAY
        Calculated martensitic volume fraction at transformation reversal history
    eps_t_r : NUMPY ARRAY
        Calculated transformation strain at transformation reversal history

    '''

    # Transformation strain at calibration stress (H_cur)
    H_cur_cal = H_cursolver(P['sig_cal'], P['sig_crit'],
                            P['k'], P['H_min'], P['H_sat'])

    # Partial Derivative of H_cur at calibration stress (dH_cur)
    dH_cur = partial_Hcur_sigma(
        P['sig_cal'], P['sig_crit'], P['k'], P['H_sat'], P['H_min'])

    # Transformation Parameters (structure: TP)
    # Intermediate calculations 
    TP = {}
    TP['rho_delta_s0'] = (-2*(P['C_M']*P['C_A'])*(H_cur_cal+P['sig_cal']
                          * dH_cur+P['sig_cal']*(1/P['E_M']-1/P['E_A'])))/(P['C_M']+P['C_A'])
    TP['D'] = ((P['C_M']-P['C_A'])*(H_cur_cal+P['sig_cal']*dH_cur+P['sig_cal'] *
               (1/P['E_M']-1/P['E_A'])))/((P['C_M']+P['C_A'])*(H_cur_cal+P['sig_cal']*dH_cur))
    TP['a1'] = TP['rho_delta_s0']*(P['M_f']-P['M_s'])
    TP['a2'] = TP['rho_delta_s0']*(P['A_s']-P['A_f'])
    TP['a3'] = -TP['a1']/4*(1+1/(P['n_1']+1)-1/(P['n_2']+1)) + \
        TP['a2']/4*(1+1/(P['n_3']+1)-1/(P['n_4']+1))
    TP['rho_delta_u0'] = TP['rho_delta_s0']/2*(P['M_s']+P['A_f'])
    TP['Y_0_t'] = TP['rho_delta_s0']/2*(P['M_s']-P['A_f'])-TP['a3']

    # --------------------------------------------------------------------------
    # GENERATION OF MEMORY ARRAYS
    # --------------------------------------------------------------------------

    # Arrays of output variables
    # H_cur: Current maximum transformation strain
    H_cur = np.zeros((T.shape[0]), dtype=float)
    # eps_t: Transformation Strain
    eps_t = np.zeros((T.shape[0]), dtype=float)
    # eps: Total strain
    eps = np.zeros((T.shape[0]), dtype=float)
    # MVF: Martensitic Volume Fraction
    MVF = np.zeros((T.shape[0]), dtype=float)
    # E: Youngs Modulus
    E = np.zeros((T.shape[0]), dtype=float)
    # eps_t_r: transformation strain at transformation reversal
    eps_t_r = np.zeros((T.shape[0]), dtype=float)
    # MVF_r: Martensitic Volume Fraction at transformation reversal
    MVF_r = np.zeros((T.shape[0]), dtype=float)
    # Phi_fwd: Forward transformation surface
    Phi_fwd = np.zeros((T.shape[0]), dtype=float)
    # Phi_rev: Reverse transformation surface
    Phi_rev = np.zeros((T.shape[0]), dtype=float)

    # Initialize outputs
    
    #ASSUMES THE MATERIAL STARTS IN MARTENSITE
    #Assumes the reference temperature is the maximum temperature
    T_ref = max(T)
    
    H_cur[0] = H_cursolver(sigma[0], P['sig_crit'],
                           P['k'], P['H_min'], P['H_sat'])
    eps_t[0] = H_cur[0]
    eps[0] = H_cur[0] + sigma[0]/P['E_M'] + P['alpha']*(T[0] - T_ref) #NOTE: WILL NEED TO ADDRESS THIS. 
    MVF[0] = 1.
    E[0] = P['E_M']
    # eps_t[0] = 0.0
    # eps[0] = sigma[0]/P['E_A'] + P['alpha']*(T[0] - T_ref)
    # MVF[0] = 0. 
    # E[0] = P['E_A']
    # Array for number of iterations required for each load step
    increments = np.zeros((T.shape[0]), dtype=float)
    


    for i in range(1, T.shape[0]):
        increments[i] = 0
        # Initialize Output Variables
        MVF[i] = MVF[i-1]
        eps_t[i] = eps_t[i-1]
        E[i] = E[i-1]
        MVF_r[i] = MVF_r[i-1]
        eps_t_r[i] = eps_t_r[i-1]

        # Elastic prediction and transformation Check
        # Determine user input for transformation check
        if (elastic_check.lower() == 'No'.lower()) or (elastic_check.lower() == 'N'.lower()):
            # Non-transformation surface rate-informed selected
            eps_i, eps_t_i, MVF_i, H_cur_i, Phi_fwd_i, Phi_rev_i, chck = \
                Elastic_Transformation_check_stress(
                P, TP, sigma[i], eps[i-1], T[i], T[i-1], T_ref, 
                sigma[i-1], Phi_fwd[i-1], Phi_rev[i-1], E[i], 
                MVF[i], eps_t[i], eps_t_r[i], MVF_r[i])
            eps[i] = eps_i
            eps_t[i] = eps_t_i
            MVF[i] = MVF_i
            H_cur[i] = H_cur_i
            Phi_fwd[i] = Phi_fwd_i
            Phi_rev[i] = Phi_rev_i
        
         

        elif (elastic_check.lower() == 'Yes'.lower()) or (elastic_check.lower() == 'Y'.lower()):
            # Transformation surface rate-informed selected
            eps_i, eps_t_i, MVF_i, H_cur_i, Phi_fwd_i, Phi_rev_i, chck = \
                Elastic_Transformation_check_RI_stress(
                P, TP, sigma[i], eps[i-1], T[i], T[i-1], T_ref,
                sigma[i-1], Phi_fwd[i-1], Phi_rev[i-1], E[i], 
                MVF[i], eps_t[i], eps_t_r[i], MVF_r[i])

            eps[i] = eps_i
            eps_t[i] = eps_t_i
            MVF[i] = MVF_i
            H_cur[i] = H_cur_i
            Phi_fwd[i] = Phi_fwd_i
            Phi_rev[i] = Phi_rev_i

        else:
            # Display error if neither Yes or No are selected
            print(
                'Please input "No" or "Yes" for Elastic Prediction: Transformation Surface Rate-informed')
            break

        # Determine User input for transformation correction
        if (integration_scheme.lower() == 'explicit'.lower()) or (integration_scheme.lower() == 'E'.lower()):
            # Explicit integration scheme selected
            # Display error if n1,n2,n3, or n4 are not equal to 1
            if P['n_1'] != 1 or P['n_2'] != 1 or P['n_3'] != 1 or P['n_4'] != 1:
                h = print(
                    'Smoothness parameters must be changed to 1 for explicit integration scheme.', 'Error', 'error')
                break

            # Call function to return output variables for explicit correction
            MVF_i, eps_t_i, E_i, MVF_r_i, eps_t_r_i, \
            eps_i, Phi_fwd_i, Phi_rev_i = \
                Explicit_Transformation_Correction_stress(
                            P, TP, chck, MVF[i], eps_t[i], E[i], MVF_r[i],\
                            eps_t_r[i], sigma[i], H_cur[i], eps[i], T[i], \
                            T_ref, Phi_fwd[i], Phi_rev[i])
            MVF[i] = MVF_i
            eps_t[i] = eps_t_i
            E[i] = E_i
            MVF_r[i] = MVF_r_i
            eps_t_r[i] = eps_t_r_i
            eps[i] = eps_i
            Phi_fwd[i] = Phi_fwd_i
            Phi_rev[i] = Phi_rev_i
        elif (integration_scheme.lower() == 'implicit'.lower()) or (integration_scheme.lower() == 'I'.lower()):
            # Implicit integration scheme selected
            # Call function to return output variables for explicit correction

            MVF_i, eps_t_i, E_i, MVF_r_i, eps_t_r_i, \
            eps_i, Phi_fwd_i, Phi_rev_i = \
                Implicit_Transformation_Correction_stress(
                            P, TP, chck, MVF[i], eps_t[i], E[i], MVF_r[i],\
                            eps_t_r[i], sigma[i], H_cur[i], eps[i], T[i], \
                            T_ref, Phi_fwd[i], Phi_rev[i])
            MVF[i] = MVF_i
            eps_t[i] = eps_t_i
            E[i] = E_i
            MVF_r[i] = MVF_r_i
            eps_t_r[i] = eps_t_r_i
            eps[i] = eps_i
           
            Phi_fwd[i] = Phi_fwd_i
            Phi_rev[i] = Phi_rev_i
            
 
        else:
            # Display error if neither Implicit or Explicit are selected
            print('Please input "Implicit" or "Explicit" for integration scheme')
        
    return eps, MVF, eps_t, E, MVF_r, eps_t_r
       


