function [ eps, MVF, eps_t, E, MVF_r, eps_t_r ] = Full_Model_stress( T, sigma, P, elastic_check, integration_scheme)
% Function to run the One Dimensional, strain-driven, implicit integration
% scheme

% Current transformation strain at calibration stress
H_cur_cal = H_cursolver(P.sig_cal, P.sig_crit,P.k,P.H_min,P.H_sat);

% Partial Derivative of H_cur at calibration stress (dH_cur)
dH_cur=partial_Hcur_sigma(P.sig_cal,P.sig_crit,P.k,P.H_sat,P.H_min);

% Transformation Parameters (structure: TP)
TP.rho_delta_s0 = (-2*(P.C_M*P.C_A)*(H_cur_cal+P.sig_cal*dH_cur+P.sig_cal*(1/P.E_M-1/P.E_A)))/(P.C_M+P.C_A);
TP.D = ((P.C_M-P.C_A)*(H_cur_cal+P.sig_cal*dH_cur+P.sig_cal*(1/P.E_M-1/P.E_A)))/((P.C_M+P.C_A)*(H_cur_cal+...
    P.sig_cal*dH_cur));
TP.a1 = TP.rho_delta_s0*(P.M_f-P.M_s);
TP.a2 = TP.rho_delta_s0*(P.A_s-P.A_f);
TP.a3 = -TP.a1/4*(1+1/(P.n1+1)-1/(P.n2+1))+TP.a2/4*(1+1/(P.n3+1)-1/(P.n4+1));
TP.rho_delta_u0 = TP.rho_delta_s0/2*(P.M_s+P.A_f);
TP.Y_0_t = TP.rho_delta_s0/2*(P.M_s-P.A_f)-TP.a3;

%--------------------------------------------------------------------------
% GENERATION OF MEMORY ARRAYS
%--------------------------------------------------------------------------

% Arrays of output variables
% H_cur: Current maximum transformational strain
H_cur = zeros((size(T,1)),1);
% eps_t: Transformational Strain
eps_t = zeros((size(T,1)),1);
% eps: Strain
eps = zeros((size(T,1)),1);
% MVF: Martensitic Volume Fraction
MVF = zeros((size(T,1)),1);
% E: Youngs Modulus
E = zeros((size(T,1)),1);
% eps_t_r: transformational strain at transformation reversal
eps_t_r = zeros((size(T,1)),1);
% MVF_r: Martensic Strain at transformation reversal
MVF_r = zeros((size(T,1)),1);
%Phi_fwd: Forward transformation surface
Phi_fwd = zeros((size(T,1)),1);
%Phi_rev: Reverse transformation surface
Phi_rev = zeros((size(T,1)),1);

% Initialize outputs
H_cur(1,1) = H_cursolver(sigma(1,1),P.sig_crit,P.k,P.H_min,P.H_sat);
eps_t(1,1) = H_cur(1,1);
eps(1,1) = H_cur(1,1) + sigma(1,1)/P.E_M;
MVF(1,1) = 1.;
E(1,1)=P.E_M;

% Array for number of iterations required for each load step
increments = zeros((size(T,1)),1);
for i = 2:size(T,1)
    increments(i,1)=0;
    % Initialize Output Variables
    MVF(i,1)=MVF(i-1,1);
    eps_t(i,1)=eps_t(i-1,1);
    E(i,1)=E(i-1,1);
    MVF_r(i,1)=MVF_r(i-1,1);
    eps_t_r(i,1)=eps_t_r(i-1,1);
    
    % Elastic prediction and transformation Check
    % Determine user input for transformation check
    if strcmpi(elastic_check,'No') || strcmpi(elastic_check,'N')
        % Non-transformation surface rate-informed selected
        [ eps(i,1), eps_t(i,1), MVF(i,1), H_cur(i,1), Phi_fwd(i,1), Phi_rev(i,1), chck ] = ...
            Elastic_Transformation_check_stress( P, TP, sigma(i,1), eps(i-1,1), T(i,1), T(i-1,1), T(1,1), sigma(i-1,1), Phi_fwd(i-1,1), Phi_rev(i-1,1), E(i,1), MVF(i,1), eps_t(i,1), eps_t_r(i,1), MVF_r(i,1) );
    
    elseif strcmpi(elastic_check,'Yes') || strcmpi(elastic_check,'Y')
        % Transformation surface rate-informed selected
        [ eps(i,1), eps_t(i,1), MVF(i,1), H_cur(i,1), Phi_fwd(i,1), Phi_rev(i,1), chck ] = ...
            Elastic_Transformation_check_RI_stress(P, TP, sigma(i,1), eps(i-1,1), T(i,1), T(i-1,1), T(1,1), sigma(i-1,1), Phi_fwd(i-1,1), Phi_rev(i-1,1), E(i,1), MVF(i,1), eps_t(i,1), eps_t_r(i,1), MVF_r(i,1) );
    
    else
        % Display error if neither Yes or No are selected
        disp('Please input "No" or "Yes" for Elastic Prediction: Transformation Surface Rate-informed');
        break
    end
    
    % Determine User input for transformation correction
    if strcmpi(integration_scheme,'explicit') || strcmpi(integration_scheme,'E')
        % Explicit integration scheme selected
        % Display error if n1,n2,n3, or n4 are not equal to 1
        if P.n1 ~= 1 || P.n2 ~=1 || P.n3 ~= 1 || P.n4 ~= 1
            h = msgbox('Smoothness parameters must be changed to 1 for explicit integration scheme.', 'Error','error');
            break
        end
        % Call function to return output variables for explicit correction
        [ MVF(i,1), eps_t(i,1), E(i,1), MVF_r(i,1), eps_t_r(i,1), eps(i,1), Phi_fwd(i,1), Phi_rev(i,1) ] = ...
            Explicit_Transformation_Correction_stress(P, TP, chck,...
            MVF(i,1),eps_t(i,1),E(i,1),MVF_r(i,1),eps_t_r(i,1),sigma(i,1), H_cur(i,1),eps(i,1), T(i,1), T(1,1), Phi_fwd(i,1), Phi_rev(i,1) );
    elseif strcmpi(integration_scheme,'implicit') || strcmpi(integration_scheme,'I')
        % Implicit integration scheme selected
        % Call function to return output variables for explicit correction
        [ MVF(i,1), eps_t(i,1), E(i,1), MVF_r(i,1), eps_t_r(i,1), eps(i,1), Phi_fwd(i,1), Phi_rev(i,1) ] = ...
            Implicit_Transformation_Correction_stress(P, TP, chck,...
            MVF(i,1),eps_t(i,1),E(i,1),MVF_r(i,1),eps_t_r(i,1),sigma(i,1), H_cur(i,1),eps(i,1), T(i,1), T(1,1), Phi_fwd(i,1), Phi_rev(i,1) );
    else
        % Display error if neither Implicit or Explicit are selected
        disp('Please input "Implicit" or "Explicit" for integration scheme');
    end


end

disp(eps)
disp(MVF)
disp(eps_t)
disp(E)
disp(MVF_r)
disp(eps_t_r )

end



% P.alpha =3
% P.sig_cal=2
% P.sig_crit=5
% P.k=20
% P.H_min=12
% P.H_sat=30
% P.C_M=14
% P.C_A=15
% P.E_M=23
% P.E_A=20
% P.M_f=22
% P.M_s=19
% P.A_s=31
% P.A_f=25
% P.n1=3
% P.n2=7
% P.n3=9
% P.n4=4
% 
% T = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16],[17,18,19,20]]
% elastic_check = 'No'
% sigma = [[5,10,15,32,45],[20,25,30,345,76],[35,40,45,12,5],[55,60,65,34,56],[1,2,3,5,6]]
% integration_scheme = 'implicit'
