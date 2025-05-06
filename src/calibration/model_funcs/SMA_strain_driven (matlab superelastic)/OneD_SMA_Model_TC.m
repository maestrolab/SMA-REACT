
% Initializing environment
clear all; close all; clc

%--------------------------------------------------------------------------
% INPUTS
%--------------------------------------------------------------------------

% Maximum Number of increments n per loading step
n = 100; 

% INPUT:
% Temperature and time at the start and at the ends of each loading step
% Linear increments strain and temperature loading step assumed
t_inp = [0; 20; 40]; %s

eps_inp = [0; .08; 0];


% MATERIAL PARAMETERS (Structure: P)
% Young's Modulus for Austenite and Martensite 
P.E_A = 55E9;
P.E_M = 46E9;

% Transformation temperatures (M:Martensite, A:
% Austenite), (s:start,f:final)
P.M_s = -28+273.15;
P.M_f = -43+273.15;
P.A_s = -3+273.15;
P.A_f = 7+273.15;

% Slopes of transformation boundarings into austenite (C_A) and
% martensite (C_M) at Calibration Stress 
P.C_A = 7.4E6;
P.C_M = 7.4e6;

% Maximum and minimum transformation strain
P.H_min = 0.056;
P.H_sat = 0.056;

P.k = 1e3;
P.sig_crit = 0;

%Energy Coefficients
% Coefficient of thermal expansion
P.alpha = 10E-6;
% Mass density
P.rho=6500; %kg/m^3
% Specific Heat
P.c=400;
% Heat convection coefficient
P.h=0;
% Specific heat source/sink term
P.r=0;
% Ambient Temperature (Initial Temperature??)
T_ambient=298.15; %K
% Model Geometry
% d: Diameter of considered 1D model
P.d = 1e-3;

% Smoothness hardening parameters 
P.n1 = .8;
P.n2 = .8;
P.n3 = .8;
P.n4 = .8;

% Algorithmic delta for modified smooth hardening function
P.delta=1e-5;

% Calibration Stress
P.sig_cal=200E6;

% Tolerance for change in MVF during implicit iteration
P.MVF_tolerance=1e-8;

% Generate strain and time states at each increment
% t: time
for i = 1:(size(t_inp,1)-1)
    if i == 1
        t = linspace(t_inp(i), t_inp(i+1), n)';
    else     
        t = [t; linspace(t_inp(i), t_inp(i+1),n)'];
    end
end

% eps: Strain
for i = 1:(size(eps_inp,1)-1)
    if i == 1
        eps = linspace(eps_inp(i), eps_inp(i+1), n)';
    else     
        eps = [eps; linspace(eps_inp(i), eps_inp(i+1),n)'];
    end
end

% Elastic Prediction Check
% prompt = {'Will the Elastic Prediction Check be Transformation Surface Rate-informed or not (Y/N)?'};
% dlg_title = '1D SMA Model Elastic Prediction Check';
% num_lines = 1;
% defaultans = {'N','hsv'};
% elastic_check = inputdlg(prompt,dlg_title,num_lines,defaultans);
elastic_check = 'Y';

[sigma,MVF,T,eps_t,E,MVF_r,eps_t_r ] = Full_Model_TC( t, eps, P, elastic_check, T_ambient );

figure(1)
box on 
plot(eps,sigma/1E6,'b','LineWidth',1.5)
xlabel('Strain')
ylabel('Stress (MPa)')
title('One D SMA Models')
set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
set(gca,'XMinorTick','on','YMinorTick','on')
set(gca,'ticklength',3*get(gca,'ticklength'))

figure(2)
box on 
plot(T,eps,'b','LineWidth',1.5)
xlabel('Temperature (K)')
ylabel('Strain')
title('One D SMA Models T vs. \epsilon')
set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
set(gca,'XMinorTick','on','YMinorTick','on')
set(gca,'ticklength',3*get(gca,'ticklength'))

figure(3)
box on 
plot(T,sigma/1E6,'b','LineWidth',1.5)
xlabel('Temperature (K)')
ylabel('Stress (MPa)')
title('One D SMA Models T vs. \sigma')
set(gca,'FontName','Times New Roman','fontsize', 20,'linewidth',1.15)
set(gca,'XMinorTick','on','YMinorTick','on')
set(gca,'ticklength',3*get(gca,'ticklength'))