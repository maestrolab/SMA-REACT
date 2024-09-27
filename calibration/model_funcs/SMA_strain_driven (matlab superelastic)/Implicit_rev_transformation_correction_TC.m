function [ MVF, T, eps_t, E, MVF_r, eps_t_r, sigma, Phi_rev ] = Implicit_rev_transformation_correction_TC( MVF, eps_t, E,MVF_r,eps_t_r,sigma, eps, T, T_0,...
    Phi_rev,P, TP)
% Function to correct for reverse transformation using implicit integration
% scheme
% Input variables are from elastic prediction/ transformation check

% Find initial values for iteration (k=1)
% Transformation Direction for reverse transformation
Lambda = eps_t_r/MVF_r;

% Iterate MVF until its change after an iteration is negligible (less than
% assigned tolerance MVF_tolerance) or until MVF reaches bound of 0

maxiter = 100;
for iter = 1:maxiter
    % Determine the partial derivative of the transformation
    % surface (Phi) with respect to stress
    partial_Phi_rev_sigma_k=-(1+TP.D)*eps_t_r/MVF_r-(1/P.E_M-1/P.E_A)*sigma;
    
    % Determine the partial derivative of transformation surface
    % (Phi) with respect to Martensitic volume fraction
    partial_Phi_rev_MVF_k=partial_Phi_rev_MVF(MVF,P.delta,P.n3,P.n4,TP.a1,TP.a2,TP.a3);
    
    % Determine the partial derivative of transformation surface (Phi) with
    % respect to Temperature
    partial_Phi_rev_T_k=-TP.rho_delta_s0;
    
    % Use partial derivatives and MVF evolution to solve A^t
    A_t=partial_Phi_rev_MVF_k-partial_Phi_rev_sigma_k*E*((1/P.E_M-1/P.E_A)*sigma+Lambda);
    
    % Determine the effective thermodynamic driving force pi^t for reverse
    % transformation
    pi_t_rev=-TP.Y_0_t+TP.D*sigma*eps_t_r/MVF_r;
      
    % Determine the change in MVF and T for the iteration using the linear
    % system of equations
    % 2x2 Matrix 'L' representing the terms requiring the partial
    % derivatives and material properties (x:MVF, T:Temperature)
    L_xx=-partial_Phi_rev_sigma_k*E*((1/P.E_M-1/P.E_A)*sigma+Lambda)+partial_Phi_rev_MVF_k;
    L_xT=-partial_Phi_rev_sigma_k*E*P.alpha+partial_Phi_rev_T_k;
    L_Tx=-T*P.alpha*E*((1/P.E_M-1/P.E_A)*sigma+Lambda)+(-pi_t_rev+TP.rho_delta_s0*T);
    L_TT=P.rho*P.c-T*E*P.alpha^2;
    L= [L_xx, L_xT;
        L_Tx, L_TT];
    % Assign matrix 'B' to the solutions to the system of equations
    % (Transformation surface)
    B=[-Phi_rev; 0];
    % Solve for change in MVF and T
    D=inv(L)*B;
    delta_MVF=D(1,1);
    delta_T=D(2,1);
    
    
    % Hold the MVF value of the previous iteration in case of
    % MVF > 1 correction
    MVF_k=MVF;
    T_k=T;
    % Update MVF and T using the calculated change over the iteration
    MVF=MVF+delta_MVF;
    T=T+delta_T;
    
    % Correct if MVF reaches a bound of 0
    if MVF < 0
        MVF = 0;
        delta_MVF=MVF-MVF_k;
        % Recalculate transformation strain for corrected MVF
        eps_t=eps_t+delta_MVF*Lambda;
        % Recalculate temperature for corrected MVF using the second 
        % equation in the system of equations
        L_Tx=-T_k*P.alpha*E*((1/P.E_M-1/P.E_A)*sigma+Lambda)+(-pi_t_rev+TP.rho_delta_s0*T_k);
        L_TT=P.rho*P.c-T_k*E*P.alpha^2;
        delta_T=-L_Tx*delta_MVF/L_TT;
        T=T_k+delta_T;
        % Youngs Modulus for austenite material
        E=P.E_A;
        % Calculate Stress
        sigma= E*(eps- P.alpha*(T-T_0)-eps_t);
        % Update transformation reversal values to zero
        eps_t_r=0;
        MVF_r=0;
        break
    end
    
    % Update transformation strain using calculated values for change in
    % MVF (delta_MVF) and transformation direction
    eps_t=eps_t+delta_MVF*Lambda;
    % Update value for Young's Modulus and use this value to determine
    % stress (sigma)
    E=(1/P.E_A+MVF*(1/P.E_M-1/P.E_A))^-1;
    sigma= E*(eps- P.alpha*(T-T_0)-eps_t);
    
    % Update transformation surface/output variables for next
    % iteration
    % Update transformation direction
    Lambda = eps_t_r/MVF_r;
    % Update hardening function
    f_rev = .5*TP.a2*(1+(MVF^(1/P.n3)/(MVF+P.delta)^(1/P.n3-1))^P.n3-...
        ((1-MVF)^(1/P.n4)/(1-MVF+P.delta)^(1/P.n4-1))^P.n4)-TP.a3;
    % Update transformation surface
    Phi_rev = -(1+TP.D)*sigma*eps_t_r/MVF_r-.5*(1/P.E_M-1/P.E_A)...
        *sigma^2-TP.rho_delta_s0*T+TP.rho_delta_u0+f_rev-TP.Y_0_t;
    
    % Transformation reversal values remain the same
    if abs(delta_MVF) < P.MVF_tolerance
        break
    end
    
    if iter == maxiter
        error(['ERROR: MAXIMUM NUMBER OF ITERATIONS (', num2str(iter),  ') REACHED IN THE RMA'])
    end
end
end

