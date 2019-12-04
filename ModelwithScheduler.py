#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 15:50:01 2019

@author: juliedemeyere
"""

import math
import numpy as np
from numpy.linalg import inv
from sympy import Matrix, S, linsolve, symbols
from sympy.solvers.solveset import nonlinsolve
import math




from sympy import *


mew = 1/4


lambd = 1/2

x = 1/8

from sympy import *



def Solver(mew,lambd,x):
    d11, d12, d13, d21, d22, d23, d31, d32, d33= symbols('d11, d12, d13, d21, d22, d23, d31, d32, d33', real=True)
    D = np.array([[d11,d12,d13],[d21,d22,d23],[d31,d32,d33]])
    C = np.array([[0.,2*mew,0.],[0.,0.,mew],[0.,0.,0.]])
    A = np.array([[x + 2*mew, 0., 0.],[-lambd, x+lambd+mew, 0.],[0., -lambd, lambd+x]])
    B = np.array([[x,0.,0.],[0.,x,0.],[0.,0.,x]])
    Dsquared = np.dot(D,D)
    p1 = np.dot(Dsquared, C)
    p2 = np.dot(D, A)
    M= p1 - p2 + B
    eq1 = M[0][0]
    eq2 = M[0][1]
    eq3 = M[0][2]
    eq4 = M[1][0]
    eq5 = M[1][1]
    eq6 = M[1][2]
    eq7 = M[2][0]
    eq8 = M[2][1]
    eq9 = M[2][2]
    
    solver = nsolve((eq1,eq2,eq3,eq4,eq5, eq6, eq7,eq8, eq9),(d11, d12, d13, d21, d22, d23, d31, d32, d33),(0,0,0,0,0,0,0,0,0))
    DMatrix = np.array([[solver[0],solver[1], solver[2]],[solver[3],solver[4], solver[5]],[solver[6],solver[7], solver[8]]])
    return DMatrix

def adjustC1(C1):
    C1 = C1.copy()
    C1[0][0] = 0
    C1[1][0] = 0
    C1[2][0] = 0
    return C1

def adjustC2(C2):
    C2 = C2.copy()
    C2[0][0] = 0
    C2[1][0] = 0
    C2[2][0] = 0
    C2[0][1] = 0
    C2[1][1] = 0
    C2[2][1] = 0
    return C2
    

    
def EquilibriumDistribution(mew, lambd, x):
    N = 2 # amount of robots
    Mi = Solver(mew,lambd,x)
    M = Mi.copy()
    A = np.array([[x + N*mew, 0., 0.],[-lambd, x+lambd+(N-1)*mew, 0.],[0., -lambd, lambd+x]])
    B = np.array([[x,0.,0.],[0.,x,0.],[0.,0.,x]])
    C = np.array([[0.,N*mew,0.],[0.,0.,(N-1)*mew],[0.,0.,0.]])
    Z = np.array([[0,0,0],[0,lambd,0],[0,0,0]])
    
    I = np.array([[1,0,0],[0,1,0],[0,0,1]])
    
    Pi = np.array(I-M)
    actual = np.array([[float(Pi[0][0]),float(Pi[0][1]),float(Pi[0][2])],[float(Pi[1][0]),float(Pi[1][1]),float(Pi[1][2])],[float(Pi[2][0]),float(Pi[2][1]),float(Pi[2][2])]])
    P = inv(actual)
    C1o = np.dot(C, inv(A-Z-C))

    C1 = adjustC1(C1o)
    C2o = np.dot(C1, inv(B))
    C2 = adjustC2(C2o)
    T = C1 + C2 + P
    a = T[0][0] + T[0][1] + T[0][2]
    b = T[1][0] + T[1][1] + T[1][2]
    c = T[2][0] + T[2][1] + T[2][2]
    
    eq0= [a,b,c]
    eq1 = [C1o[0][0],C1o[1][0], C1o[2][0]]
    eq2 = [C2o[0][0],C2o[1][0], C2o[2][0]]
    eq3 = [C2o[0][1],C2o[1][1], C2o[2][1]]
    RHS = np.array([1,0,0])

    LHS = np.array([eq0, eq1, eq3])

    P0value = np.linalg.solve(LHS, RHS)
    print(P0value)
    
    zps = np.dot(M,M)
    Mspec = M
    Pi0Dict = {0:P0value}
    for n in range(1,2):
        Pi0Dict[n] = np.dot(P0value, Mspec)
        Mspec = np.dot(Mspec,M)
#    print('')
#    print(Pi0Dict)



Solve = EquilibriumDistribution(mew,lambd,x)


