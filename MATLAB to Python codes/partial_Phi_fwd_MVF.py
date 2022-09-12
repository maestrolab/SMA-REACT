# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 11:28:10 2022

@author: Tiago
"""


def partial_Phi_fwd_MVF( MVF, delta, n1, n2,a1,a2,a3 ):
    # Solve for the partial derivative of transformation surfade Phi with
    # respect to the martensitic volume fraction MVF.
    partial_Phi_fwd_MVF=-1/2*(-(1-MVF+delta)**(n2-2)*n2*MVF+MVF*(MVF+delta)**(n1-2)*n1+(1-MVF+delta)**(n2-2)*delta+(1-MVF+delta)**(n2-2)*n2+(MVF+delta)**(n1-2)*delta)*a1
    
    return partial_Phi_fwd_MVF
print(partial_Phi_fwd_MVF())
