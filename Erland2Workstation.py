#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 14:20:53 2019

@author: juliedemeyere
"""
import math
import numpy as np

from numpy.linalg import inv

mew = 1/(44.1 + 33.13 + 45.2)
#mew = 1/(44.1 + 33.13 + 45.2)

#mew = 29.4
lambd = 2/30
#lambd = 120


def EquilibriumDistribution(N, mew, lambd):
    GammaDict = {N:np.array([[1, 0], [0, 1]]),N+1:np.array([[0, 0], [0, 0]])}
    MnList = {-1:np.array([[0,0],[0,0]])}
    Ae = np.array([[1,-1],[-1,1]])
    Be = np.array([[0,0],[1,0]])
    C = np.array([[2*lambd,-2*lambd],[0,2*lambd]])
    B = np.array([[0,0],[2*lambd,0]])
    GammaList = [np.array([[1, 0], [0, 1]])]
    for m in range(0,N+1):
        M = np.array([[(N-m)*mew,0],[0,(N-m)*mew]])
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
   # print(Gamma0)
   # print(sGamma)
    Fa = sGamma[0][0] + sGamma[0][1] + Gamma0[0][0]
    Fb = sGamma[1][0] + sGamma[1][1] + Gamma0[1][0] 
    PiD = -Gamma0[1][1]/Gamma0[0][1]
    pb = Fa*PiD + Fb
    PiB = 1/pb
    PiA = PiD*PiB
    PNvalues = [PiA, PiB]
   # print(PNvalues)
    AllProbabilities = {}
    ProbabilitiesList = []
    for i in range(0, len(GammaDict)):
        Matrix = GammaDict[i]
        Probability = np.dot(PNvalues, Matrix)
        if i == 0:
            Probability = np.array([Probability[0], 0])
        AllProbabilities[i] = Probability
        ProbabilitiesList.append(Probability)
    AllProbabilities[N] = PNvalues
    sumprob = sum(ProbabilitiesList)
    multiplier = np.array([[0],[1]])
    Throughput = 2*lambd*np.dot(sumprob, multiplier)[0]

    return GammaDict,Throughput, MnList, GammaList 


mew2 =  1/(44.1 + 33.13 + 45.2)
lambd2  = 1/15
def PiOCalculator(N, mew, lambd):
    Pi0Components = []
    for m in range(0,N+1):
        PiX = (math.factorial(N)*(mew/lambd)**m)/(math.factorial(N-m))
        Pi0Components.append(PiX)
    sumComponents = sum(Pi0Components)
    Pi0 = 1/sumComponents
    Throughput_second = lambd - lambd*Pi0
    Throughput_hour = Throughput_second*60*60
    TotalThroughput_hour = Throughput_hour*5
    return round(Throughput_hour,2),round(TotalThroughput_hour,2), Pi0Components


EquilibriumDistribution4 = EquilibriumDistribution(4, mew, lambd)
print('N=4 Throughput')
print('Erlang2 TH:', round(EquilibriumDistribution4[1],6), 'units per second 1 WS')
print('Erlang2 TH:', round(EquilibriumDistribution4[1]*60*60*5,6), 'units per hour 5 WS')
print('Exponential TH:', PiOCalculator(4, mew2, lambd2)[1], 'units per hour 5 WS')
print('% difference erlang2/exponential:', round(100-(EquilibriumDistribution4[1]*60*60*5/PiOCalculator(4, mew2, lambd2)[1])*100,2),'%')

print('')
EquilibriumDistribution2 = EquilibriumDistribution(2, mew, lambd)
print('N=2 Throughput')
print('Erlang2 TH:', round(EquilibriumDistribution2[1],6), 'units per second 1 WS')
print('Erlang2 TH:', round(EquilibriumDistribution2[1]*60*60*5,6), 'units per hour 5 WS')
print('Exponential TH:', PiOCalculator(2, mew2, lambd2)[1], 'units per hour 5 WS')
print('Theoretical (paper) TH: 245.1 units per hour 5 WS')
print('% difference erlang2/exponential:', round(100-(EquilibriumDistribution2[1]*60*60*5/PiOCalculator(2,mew2, lambd2)[1])*100,2),'%')


print('')
EquilibriumDistribution8 = EquilibriumDistribution(8, mew, lambd)
print('N=8 Throughput')
print('Erlang2 TH:', round(EquilibriumDistribution8[1],6), 'units per second 1 WS')
print('Erlang2 TH:', round(EquilibriumDistribution8[1]*60*60*5,6), 'units per hour 5 WS')
print('Exponential TH:', PiOCalculator(8, mew2, lambd2)[1], 'units per hour 5 WS')
print('% difference erlang2/exponential:', round(100-(EquilibriumDistribution8[1]*60*60*5/PiOCalculator(8, mew2, lambd2)[1])*100,2),'%')

print('Theoretical (paper) TH: 876 units per hour 5 WS')

print('')
EquilibriumDistribution14 = EquilibriumDistribution(14, mew, lambd)
print('N=14 Throughput')
print('Erlang2 TH:', round(EquilibriumDistribution14[1],6), 'units per second 1 WS')
print('Erlang2 TH:', round(EquilibriumDistribution14[1]*60*60*5,6), 'units per hour 5 WS')
print('Exponential TH:', PiOCalculator(14, mew2, lambd2)[1], 'units per hour 5 WS')
print('Theoretical (paper) TH: 1165.2 units per hour 5 WS')
print('% difference erlang2/exponential:', round(100-(EquilibriumDistribution14[1]*60*60*5/PiOCalculator(14, mew2, lambd2)[1])*100,2),'%')


