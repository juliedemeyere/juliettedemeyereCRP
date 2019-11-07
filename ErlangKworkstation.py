#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:13:04 2019

@author: juliedemeyere
"""

import math
import numpy as np

from numpy.linalg import inv

mew = 1/(44.1 + 33.13 + 45.2)

lambd = 2/30


k = 3

def createarrays(k, lambd, mew):
    zeros = []
    zerolist = []
    for i in range(0,k):
        zeros.append(float(0))
    for i in range(0,k):
        zerolist.append(zeros)
    zeroarray = np.array(zerolist)
    onesarray = zeroarray.copy()
    for i in range(0,k):
        onesarray[i][i] = 1
    Carray = zeroarray.copy()
    for i in range(0,k):
        Carray[i][i] = k*lambd
    for i in range(0, k-1):
        Carray[i][i+1] = -k*lambd
    Barray = zeroarray.copy()
    Barray[k-1][0] = k*lambd
    return zeroarray, onesarray, Carray, Barray
def EquilibriumDistributionErlangK(N, mew, lambd, k):
    mat = createarrays(k, lambd, mew)
    GammaDict = {N:mat[1],N+1:mat[0]}
    MnList = {-1:mat[0]}
    C = mat[2]
    B = mat[3]
    GammaList = [mat[1]]
    Mnarray = mat[0].copy()
    for m in range(0,N+1):
        M= mat[0].copy()
        for i in range(0,k):
            M[i][i] = (N-m)*mew
       # M = np.array([[(N-m)*mew,0,0],[0,(N-m)*mew,0],[0,0,(N-m)*mew]])
        MnList[m] = M
    m = N - 1
    while m >= 0:
        AA_b = MnList[m+1] + C
        AA = np.dot(GammaDict[m+1],AA_b)
        BB = np.dot(GammaDict[m+2], B)
        Comp1 = AA - BB
        Comp2 = inv(MnList[m])
        Gamma = np.dot(Comp1,Comp2)
        GammaDict[m] = Gamma
        GammaList.append(Gamma)
        m -= 1
    
    del GammaDict[N+1]

    sGamma = sum(GammaList[:-1])
    Gamma0 = GammaDict[0]
    Flist = []
    for i in range(0,k):
        Flist.append(Gamma0[i][0])
   # Fa = Gamma0[0][0]
   # Fb = Gamma0[1][0]
   # Fc = Gamma0[2][0]
    for i in range(0,k):
        for m in range(0,k):
            Flist[i] += sGamma[i][m]
     #   Fa += sGamma[0][i]
     #   Fb += sGamma[1][i]
     #   Fc += sGamma[2][i]
    bvalues = [1]    
    for i in range(1,k):
        bvalues.append(0)
    aarray = [Flist]
    for z in range(1,k):
        GammaList = []
        for i in range(0,k):
            GammaList.append(Gamma0[i][z])
        aarray.append(GammaList)
    a = np.array(aarray) 
    #print(a)
    b = np.array(bvalues)
    PNvalues = np.linalg.solve(a, b)
    AllProbabilities = {}
    ProbabilitiesList = []
    for i in range(0, len(GammaDict)):
        Matrix = GammaDict[i]
        Probability = np.dot(PNvalues, Matrix)
        if i == 0:
            P = [Probability[0]]
            for i in range(1,k):
                P.append(0)
            Probability = np.array(P)
        ProbabilitiesList.append(Probability)
        AllProbabilities[i] = Probability
    AllProbabilities[N] = PNvalues
    sumprob = sum(ProbabilitiesList)
    multlist = []
    for i in range(0,k):
        if i == (k-1):
            multlist.append([1])
        else:
            multlist.append([0])
    multiplier = np.array(multlist)
    Throughput = k*lambd*np.dot(sumprob,multiplier)[0]
    print('N=',N,',k=', k, ':',Throughput*60*60*5)

    return GammaDict,'Throughput', MnList, GammaList 

values = [2,3,4,5,10,20,30]
for i in range(len(values)):
    EquilibriumDistributionErlangK(2, mew, lambd, values[i])
print('')
for i in range(len(values)):
    EquilibriumDistributionErlangK(8, mew, lambd, values[i])
print('')
for i in range(len(values)):
    EquilibriumDistributionErlangK(14, mew, lambd, values[i])


a = np.array([[193-416+553,-39+182-175.12874074], [-1240,452]])
b = np.array([1,0])
x = np.linalg.solve(a, b)
a = np.array([[5,8,9], [2,4,6],[7,8,9]])
b = np.array([1,0,1])
x = np.linalg.solve(a, b)