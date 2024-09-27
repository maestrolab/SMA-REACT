function [ sigma, T, eps_t, MVF, H_cur, Phi_fwd, Phi_rev, chck ] = Elastic_Transformation_check_RI_TC( P, TP, eps, eps_prev,t, t_prev, T_prev, T0, sigma_prev, Phi_fwd_prev, Phi_rev_prev, E, MVF, eps_t, eps_t_r, MVF_r )
% Function to return elastic prediction and check for transformation using
% scaled elastic projections (transformation surface rate-informed)

% Returns chck=1 for forward transformation, 2 for reverse transformation 
% and 0 for no transformation

% Predict change in stress and temperature using system of equations
% obtained from linearization of stress and conservation of energy
% equations
% q: Body heat source/sink (for circular cross section)
q=  - 4*P.h/P.d*(T_prev-T0);
% Evaluate the change in strain and time over the step
delta_eps=eps-eps_prev;
delta_t=t-t_prev;
% Define matrix 'A' representing 2x2 matrix in linearized stress and energy
% equations
A= [1, E*P.alpha;
    T_prev*P.alpha, P.rho*P.c];
% Evaluate change in stress and temperature ('C' is a dummy vector for the
% change in stress and temperature)
C= inv(A)*[E*delta_eps; (q+P.rho*P.r)*delta_t];
delta_sigma=C(1,1);
delta_T=C(2,1);

% Use the increments in stress and temperature to calculate the current
% value of each
sigma=sigma_prev+delta_sigma;
T=T_prev+delta_T;

% Solve for current transformational strain  
H_cur=H_cursolver(sigma,P.sig_crit,P.k,P.H_min,P.H_sat);

% Solve for hardening functions 
f_fwd = .5*TP.a1*(1+MVF^P.n1-(1-MVF)^P.n2)+TP.a3;
f_rev = .5*TP.a2*(1+MVF^P.n3-(1-MVF)^P.n4)-TP.a3;

% Solve for the forward transformation surface
Phi_fwd = (1-TP.D)*abs(sigma)*H_cur+.5*(1/P.E_M-1/P.E_A)*sigma^2+...
    TP.rho_delta_s0*T-TP.rho_delta_u0-f_fwd-TP.Y_0_t;

% Solve for the reverse transformation surface
Phi_rev=0;
if MVF_r == 0
    % Reverse transformation strain remains zero if Martensitic Strain at
    % transformation reversal is zero
else
    Phi_rev = -(1+TP.D)*sigma*eps_t_r/MVF_r-.5*(1/P.E_M-1/P.E_A)...
        *sigma^2-TP.rho_delta_s0*T+TP.rho_delta_u0+f_rev-TP.Y_0_t;
end

% Find the scaled projections of strain, temperature (and the scaled change
% (delta) in these values
% s: scaling factor
s = 0.001;
scaled_d_eps = s*(eps - eps_prev);
scaled_d_T = s*(T - T_prev);
scaled_T = scaled_d_T + T_prev;

% Find the scaled projection of stress using scaled projections for strain
% and temperature
scaled_d_sigma= E*((eps_prev+scaled_d_eps) - P.alpha*(scaled_T - T0) - eps_t) - sigma_prev;
scaled_sigma= scaled_d_sigma + sigma_prev;

% Calculate the scaled projections for forward and reverse transformation
% surface
% Calculate the current transformational strain for these scaled values
% (required to find the transformation surfaces)
scaled_H_cur = H_cursolver(scaled_sigma,P.sig_crit,P.k,P.H_min,P.H_sat);
% Forward transformation surface for scaled values
scaled_Phi_fwd = (1-TP.D)*abs(scaled_sigma)*scaled_H_cur+.5*(1/P.E_M-1/P.E_A)*scaled_sigma^2+...
    TP.rho_delta_s0*scaled_T - TP.rho_delta_u0 - f_fwd - TP.Y_0_t;
% Reverse transformation surface for scaled values
scaled_Phi_rev=0;
if MVF_r == 0
else
    scaled_Phi_rev = -(1+TP.D)*scaled_sigma*eps_t_r/MVF_r - .5*(1/P.E_M-1/P.E_A)...
        *scaled_sigma^2 - TP.rho_delta_s0*scaled_T + TP.rho_delta_u0+f_rev-TP.Y_0_t;
end

% Check for transformation
% Determine change in transformation surface from the previous value to the
% scaled projection
scaled_d_Phi_fwd = scaled_Phi_fwd - Phi_fwd_prev;
scaled_d_Phi_rev = scaled_Phi_rev - Phi_rev_prev;

% Forward Transformation Check
if scaled_d_Phi_fwd > 0 && scaled_d_Phi_rev <= 0
    if Phi_fwd > 0 && MVF < 1
        % Forward transformation
        chck = 1;
    else 
        % No transformation
        chck = 0;
    end
% Reverse transformation check    
elseif scaled_d_Phi_rev > 0 && scaled_d_Phi_fwd <= 0
    if Phi_rev > 0 && MVF > 0
        % Reverse transformation
        chck = 2;
    else
        %No transformation
        chck = 0;
    end
    
elseif scaled_d_Phi_rev <= 0 && scaled_d_Phi_fwd <=0
    % No transformation
    chck = 0;
    
elseif scaled_d_Phi_fwd > 0 && scaled_d_Phi_rev > 0
    if Phi_fwd <= 0 && Phi_rev <=0
        %No transformation
        chck = 0;
    elseif Phi_fwd > 0 && Phi_rev <= 0
        % Check for forward transformation
        if Phi_fwd > 0 && MVF < 1
            % Forward transformation
            chck = 1;
        else 
            % No transformation
            chck = 0;
        end
    elseif Phi_rev > 0 && Phi_fwd <= 0
        % Check for reverse transformation
        if Phi_rev > 0 && MVF > 0
            % Reverse transformation
            chck = 2;
        else
            %No transformation
            chck = 0;
        end
    % If both transformation surfaces are greater than zero, check which one
    % has the higher rate of change
    elseif Phi_fwd > 0 && Phi_rev > 0
        if scaled_d_Phi_fwd > scaled_d_Phi_rev
            % Check for forward transformation
            if Phi_fwd > 0 && MVF < 1
                % Forward transformation
                chck = 1;
            else 
                % No transformation
                chck = 0;
            end
        else
            % Check for reverse transformation
            if Phi_rev > 0 && MVF > 0
                % Reverse transformation
                chck = 2;
            else
                %No transformation
                chck = 0;
            end
        end
    end
end

end


