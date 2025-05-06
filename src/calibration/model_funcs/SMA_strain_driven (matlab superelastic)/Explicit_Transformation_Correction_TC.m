function [ MVF, T, eps_t, E, MVF_r, eps_t_r, sigma, Phi_fwd, Phi_rev ] = Explicit_Transformation_Correction_TC( P, TP, chck,MVF, eps_t, E,MVF_r,eps_t_r,sigma, H_cur,eps, T, T_0, Phi_fwd, Phi_rev )
% Function to return the outputs for Martensitic volume ftaction, stress,
% transformation strain, Young's modulus, etc. using explicit integration
% scheme
% Input variables are from elastic prediction

% Return elastic predictions if no transformation is occuring
if chck == 0;
 
% Forward Transformation correction    
elseif chck ==1;
    [ MVF, T, eps_t, E, MVF_r, eps_t_r, sigma, Phi_fwd ] = Explicit_fwd_transformation_correction_TC( MVF, eps_t, sigma, H_cur,eps, T, T_0,P,TP );
    
% Reverse Transformation correction    
elseif chck == 2;
    [ MVF, T, eps_t, E, MVF_r, eps_t_r, sigma, Phi_rev ] = Explicit_rev_transformation_correction_TC( MVF, eps_t, MVF_r,eps_t_r,sigma, eps, T, T_0,P, TP );
end
end

