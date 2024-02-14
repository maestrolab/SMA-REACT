import numpy as np
import matplotlib.pyplot as plt
from calibration.model_funcs.util_funcs import (
    H_cursolver,
    partial_Hcur_sigma,
    )

def plot_phase_diagram(P,sigma_inp, ax):
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

    #Create stress array
    sigma = np.linspace(sigma_inp[0],sigma_inp[1])
    
    #Create zero arrays for transformation surfaces
    # T_fwd_0: Temperature array for forward transformation at MVF=0
    T_fwd_0 = np.zeros(shape=len(sigma))

    # T_fwd_1: Temperature array for forward transformation at MVF=1
    T_fwd_1 = np.zeros(shape=len(sigma))

    # T_rev_0: Temperature array for reverse transformation at MVF=0
    T_rev_0 = np.zeros(shape=len(sigma))

    # T_rev_0: Temperature array for reverse transformation at MVF=1
    T_rev_1 = np.zeros(shape=len(sigma))
    
    for i in range(len(sigma)):
        T_fwd_0[i] = forward_transformation(sigma[i],0,P,TP)
        T_fwd_1[i] = forward_transformation(sigma[i],1,P,TP)
        T_rev_0[i] = reverse_transformation(sigma[i],0,P,TP)
        T_rev_1[i] = reverse_transformation(sigma[i],1,P,TP)
        
    ax.ticklabel_format(axis='y', style='sci', scilimits=(6,6))

    ax.plot(T_fwd_1,sigma,'b--',label='Martensite finish')
    ax.plot(T_fwd_0,sigma,'b',label='Martensite start')
    ax.plot(T_rev_1,sigma,'r',label='Austenite start')
    ax.plot(T_rev_0,sigma,'r--',label='Austenite finish')
    
    ax.legend(loc='upper left')
    ax.set_xlabel('Temperature, K')
    ax.set_ylabel('Stress, Pa')
    ax.set_ylim([sigma_inp[0],sigma_inp[1]])
  
    return

def forward_transformation(sigma,MVF,P,TP):
    ''' Function to return the Temperature (T) value for a stress (sigma)under a
     forward transformation at an inputed Martensite Volume Fraction (MVF) '''
    
    # Calculate the hardening function
    f_fwd = .5*TP['a1']*(1.0+MVF**P['n_1']-(1.0-MVF)**P['n_2'])+TP['a3']
    
    delta_S=(1/P['E_M']-1/P['E_A'])
    H_cur= H_cursolver(sigma, P['sig_crit'],
                            P['k'], P['H_min'], P['H_sat'])
    
    # Output the temperature using the Transformation Surface equation (set
    # equal to 0 during transformation)
    T = (TP['Y_0_t']+f_fwd+TP['rho_delta_u0']-1.0/2.0*delta_S*sigma**2.0-(1.0-TP['D'])*abs(sigma)*H_cur)/TP['rho_delta_s0']
    
    return T

    


def reverse_transformation(sigma,MVF,P,TP):
    ''' Function to return the Temperature (T) value for a stress (sigma)under a
    reverse transformation at an inputed Martensite Volume Fraction (MVF)'''

    # Calculate the hardening function
    f_rev = .5*TP['a2']*(1.0+MVF**P['n_3']-(1.0-MVF)**P['n_4'])-TP['a3']

    delta_S=(1/P['E_M']-1/P['E_A'])


    # Output the temperature using the Transformation Surface equation (set
    # equal to 0 during transformation)
    # Note: assumed MVF_r=1 for Phase Diagram
    MVF_r=1.0;
    eps_t_r= H_cursolver(sigma, P['sig_crit'],
                            P['k'], P['H_min'], P['H_sat'])
    T = (-(1.0+TP['D'])*sigma*eps_t_r/MVF_r-1.0/2.0*delta_S*sigma**2.0+TP['rho_delta_u0']+f_rev-TP['Y_0_t'])/TP['rho_delta_s0']
    
    return T

if __name__ == "__main__":
    P = {}
    P['E_M'], P['E_A'] = 70E9,30E9
    P['M_s'],P['M_f'] = 273,253
    P['A_s'],P['A_f'] = 303,323
    P['C_A'],P['C_M'] = 6E6,12E6
    P['H_min'] = 0.02
    P['H_sat'] = 0.04
    P['k'] = 1E-6
    P['sig_crit'] = 100E6
    P['n_1'],P['n_2'],P['n_3'],P['n_4'] = 0.1,0.1,1,1
    
    # Algorithmic delta for modified smooth hardening function
    P['delta']=1e-5
    
    # Calibration Stress
    P['sig_cal']=200E6
    
    # Tolerance for change in MVF during implicit iteration
    P['MVF_tolerance']=1e-8
    
    plot_phase_diagram(P, [0,400E6])
    
        
        