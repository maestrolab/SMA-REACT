function [ partial_Hcur_sigma ] = partial_Hcur_sigma( sigma, sigma_crit, k, Hsat, Hmin )
% Function to solve for the partial derivative of the current
% transformation strain (Hcur) with respect to sigma (stress)

%first solve for the partial derivative of abs(sigma) with respect to sigma
if sigma > 0
    partial_abssigma = 1;
elseif sigma < 0
    partial_abssigma = -1;
else
    partial_abssigma = 0;
end

%Solve for partial derivative of current transformation strain
if abs(sigma) <= sigma_crit
    partial_Hcur_sigma = 0;
else
    partial_Hcur_sigma = k*(Hsat-Hmin)*exp(-k*(abs(sigma)-sigma_crit))*partial_abssigma;
end
end

