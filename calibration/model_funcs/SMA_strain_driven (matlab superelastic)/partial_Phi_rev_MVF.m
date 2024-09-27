function [ partial_Phi_rev_MVF ] = partial_Phi_rev_MVF( MVF, delta, n3, n4,a1,a2,a3 )
%Solve for the partial derivative of transformation surfade Phi with
%respect to the martensitic volume fraction MVF.
partial_Phi_rev_MVF=1/2*(-(1-MVF+delta)^(n4-2)*n4*MVF+MVF*(MVF+delta)^(n3-2)*n3+(1-MVF+delta)^(n4-2)*delta...
    +(1-MVF+delta)^(n4-2)*n4+(MVF+delta)^(n3-2)*delta)*a2;

end
