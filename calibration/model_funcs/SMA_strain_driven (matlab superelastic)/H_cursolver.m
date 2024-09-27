function [ H_cur ] = H_cursolver( sigma, sigma_crit, k, H_min, H_sat)
% Function to determine the current transformation strain H^cur using
% inputs for stress, critical stress, k, Hsat and Hmin

if abs(sigma) <= sigma_crit
    H_cur=H_min;
else
    H_cur = H_min + (H_sat - H_min)*(1-exp(-k*(abs(sigma)-sigma_crit)));
end
end

