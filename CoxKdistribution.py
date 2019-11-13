#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 15:42:43 2019

@author: juliedemeyere
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 21:13:04 2019

@author: juliedemeyere
"""

import math
import numpy as np

from numpy.linalg import inv

mew = 1/(122.83)

lambd = 2/30


def createarrays(k, lambd, mew,b):
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
    Carray[0][0] = b*k*lambd +(1-b)*k*lambd
    Carray[0][1] = b*Carray[0][1]
   # print('Carray:',Carray)
    Barray = zeroarray.copy()
    Barray[k-1][0] = k*lambd
    Barray[0][0] = (1-b)*k*lambd
    return zeroarray, onesarray, Carray, Barray

def EquilibriumDistributionCoxK(N, mew, lambd, k, b):
    mat = createarrays(k, lambd, mew,b)
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
        MnList[m] = M
   # print(MnList)
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
    print('sumGamma:',sGamma)
    Gamma0 = GammaDict[0]
    print('Gamma0:',Gamma0)
    Flist = []
    for i in range(0,k):
        Flist.append(Gamma0[i][0])
    for i in range(0,k):
        for m in range(0,k):
            Flist[i] += sGamma[i][m]
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
    q = np.array(bvalues)
    PNvalues = np.linalg.solve(a, q)
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
    multfirstlist = [[1]]
    for i in range(1,k):
        multfirstlist.append([0])
    m1multiplier = np.array(multfirstlist)
   # print(np.dot(sumprob,m1multiplier))
    multiplier = np.array(multlist)
    #coxarrival = (1-b)*lambd + b*k*lambd
    #print(b)
    #Throughput = coxarrival*np.dot(sumprob,multiplier)[0]
    #Th1 = lambd*np.dot(sumprob,multiplier)[0]
    #Th2 = (1-b)*lambd*np.dot(sumprob,m1multiplier)[0]
    #print(AllProbabilities)
    #Throughput = Th1 + Th2
    #print(Th1*60*60*5, Th2*60*60*5)
    Throughput = k*lambd*np.dot(sumprob,multiplier)[0]
    #print(AllProbabilities)
    print('N=',N,',k=', k, ':',Throughput*60*60*5)

    return GammaDict,'Throughput', MnList, GammaList 
#b = 0.8
#Analytical_N2_k2_b08 = EquilibriumDistributionCoxK(2, mew, lambd, 2,0.8)
#EquilibriumDistributionCoxK(2, mew, lambd, 2,2)

EquilibriumDistributionCoxK(2, mew, lambd, 2,0.8)
#EquilibriumDistributionCoxK(8, mew, lambd, 2,0)
#EquilibriumDistributionCoxK(14, mew, lambd, 2,0)


def PrintValues(b, mew, lambd):
    print('######### b =', b,'###########')
    values = [2,3,4,5,10]
    values = [2]
   # values = [2,5]
    for i in range(len(values)):
        EquilibriumDistributionCoxK(2, mew, lambd, values[i],b)
    print('')
    for i in range(len(values)):
        EquilibriumDistributionCoxK(8, mew, lambd, values[i],b)
    print('')
    for i in range(len(values)):
        EquilibriumDistributionCoxK(14, mew, lambd, values[i],b)
#PrintValues(1,mew,lambd)        
#PrintValues(0.8,mew,lambd)
#PrintValues(0.6,mew,lambd)
#PrintValues(0,mew,lambd)
