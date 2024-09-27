function [ partial_Phi_fwd_t_sigma ] = partial_Phi_fwd_sigma( sigma, Hcur, D, partial_H_cur_sigma, E_M, E_A )
% Solve the partial derivative of forward Transformation Surface (Phi_t) 
% with respect to stress (sigma)

if sigma < 0
    partial_Phi_fwd_t_sigma=-(1-D)*Hcur+(1-D)*abs(sigma)*partial_H_cur_sigma+...
        (1/E_M-1/E_A)*sigma;
elseif sigma > 0
    partial_Phi_fwd_t_sigma=(1-D)*Hcur+(1-D)*abs(sigma)*partial_H_cur_sigma+...
        (1/E_M-1/E_A)*sigma;
else
    partial_Phi_fwd_t_sigma=0;
end

end

