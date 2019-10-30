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
#mew = 29.4
lambd = 1/30
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
       # print(m, GammaDict[m+1])
    #    print('Mntheoretical:',MnList[m+1])
     #   print('Ctheoretical:', C)
     #   print('AA_b', AA_b)
        m -= 1
    sumG = sum(GammaList)
    ii = np.array([[1],[1]])
    P = np.dot(sumG, ii)
    bottom = (1-((GammaDict[0][0][1])/(GammaDict[0][1][1]))*(P[1]/P[0]))
    Pna = (1/P[0])/bottom
    Pnb = ((GammaDict[0][0][1])/(GammaDict[0][1][1]))*Pna
    ProbabilityDict = {}
    Pn = np.array([[Pna[0], Pnb[0]]])
    
    for i in range(0,len(GammaDict)-1):
        GammaMatrix = GammaDict[i]
        Prob = np.dot(Pn, GammaMatrix)
        ProbabilityDict[i] = Prob

    ThroughputSumList = []
    for i in range(1, len(ProbabilityDict)):
        Prob = ProbabilityDict[i][0]
        PibProb = Prob[1]
        Component = PibProb*lambd
        ThroughputSumList.append(Component)
    Throughput = sum(ThroughputSumList)

    GammaNm1 = GammaDict[N-2]
    f = np.dot(Pn, GammaNm1)
    
    del GammaDict[N+1]
    P4value = [0.0000337763, 0.0000196332]
    for i in range(len(GammaDict)):
       # print(i,GammaDict[i])
        Matrix = GammaDict[i]
        Probability = np.dot(P4value, Matrix)
        print(i, Probability)
    return GammaDict, sumG, MnList , ProbabilityDict

Me = EquilibriumDistribution(4, mew, lambd)
GammaValues = Me[0]
#print(GammaValues)
Sums = Me[1]
MnList = Me[2]
Probabilities = Me[3]
#print('')
#print(Probabilities)
#print(Probabilities)
y = Probabilities[2][0]
m = Matrixes[1]
#print(m*y)
#f = np.dot[y,m]
#print(y)

sumlist = []
for i in range(0,N):
    Mat = Matrixes[i]
    P = Probabilities[2][0]
    numb = np.dot(P,Mat)
    sumlist.append(numb)

II = np.array([[1],[1]])
Msum = sum(sumlist)
Multiplied = np.dot(Msum, II)

multiplier = np.array([[1],[1]])
calc = np.dot(Sums, multiplier)
#print(calc)

K1 = np.array([[[(0)*mew,0],[0,(0)*mew]]]) 
K11 = np.array([[[(2-1)*mew,0],[0,(2-1)*mew]]]) 
C = np.array([[2*lambd, -2*lambd],[0,2*lambd]])
K3 = K1 + C
K4 = inv(K11)
K5 = np.dot(K3[0],K4[0])
#print('Mn', K1)
#print('C', C)
#print('Mn-1', K11)
#print('M+C',K3)
#print(K4)
#print(K5)




M0 = np.dot(Probabilities[0][0],MnList[0])
#print(M0)
Bs = np.array([[0,0],[2*mew,0]])
M1 = np.dot(Probabilities[1][0], Bs)
#print(M1)


def PiOCalculator(N, mew, lambd):
    Pi0Components = []
    for m in range(0,N+1):
        PiX = (math.factorial(N)*(mew/(2*lambd))**m)/(math.factorial(N-m))
        Pi0Components.append(PiX)
    sumComponents = sum(Pi0Components)
    Pi0 = 1/sumComponents
    Throughput_second = lambd - lambd*Pi0
    Throughput_hour = Throughput_second*60*60
    TotalThroughput_hour = Throughput_hour*5
    return round(Throughput_hour,2),round(TotalThroughput_hour,2), Pi0Components

Pi02 = PiOCalculator(2, mew, lambd)
Pi08 = PiOCalculator(8, mew, lambd)
Pi014 = PiOCalculator(14, mew, lambd)

Throughput2Robots = Pi02[1]
Throughput8Robots = Pi08[1]
Throughput14Robots = Pi014[1]

#print('total throughput 2 robots:', Throughput2Robots)
#print('total throughput 8 robots:', Throughput8Robots)
#print('total throughput 14 robots:', Throughput14Robots)

import numpy as np

a = np.array([[1., 2.], [3., 4.]])
ainv = inv(a)
#print(a)
#print('')
#print(ainv)

N = 3
#note: the matrix is row stochastic.
#A markov chain transition will correspond to left multiplying by a row vector.
Q = np.array([
    [.95, .05, 0., 0.],
    [0., 0.9, 0.09, 0.01],
    [0., 0.05, 0.9, 0.05],
    [0.8, 0., 0.05, 0.15]])
    
Y = np.array([
    [0., N*mew , 0.],
    [lambd, 0., (N-1)*mew],
    [0., lambd, 0.]])
    
G = np.array([
    [0, N*mew , 0, 0],
    [lambd, 0, (N-1)*mew, 0],
    [0, lambd, 0,(N-2)*mew],
    [0,0,lambd,0]])

#print(G)


N = 3
M = np.array([
        [2*lambd + (N-1)*mew, -2*lambd],
        [0, 2*lambd + (N-1)*mew]])

#print(M)
Minv = inv(M)
#print('')
#print(Minv)
F = N*mew*M
#print('')
#print(F)

def PiCalculator(N,mew,lambd):
    components = [N*mew]
    PiMultiplications = [N*mew]
    for n in range(1,N+1):
        PiXpart =  np.array([[(2*lambd + (N-n)*mew), -2*lambd],
                            [0, (2*lambd + (N-n)*mew)]])
        PiXpartinv = inv(PiXpart)
        components.append(PiXpartinv)
        Coefficient = np.dot(PiMultiplications[-1],PiXpartinv)
        PiMultiplications.append(Coefficient)
    return components,  PiMultiplications
 
def PiCalculatorNumber2(N,mew,lambd):
    components = []
    Mcomponents = []
    for m in range(0,N):
        PiXpartA = np.array([[2*lambd + (N-(m+1))*mew, -2*lambd],[0, 2*lambd + (N-(m+1))*mew]])
        PiXpartBp = np.array([[(N-m)*mew, 0],[0,(N-m)*mew]])
        PiXpartB = inv(PiXpartBp)
        PiXpart = np.dot(PiXpartA,PiXpartB)
        components.append(PiXpart)

    length = len(components)-1
    Mcomponents.append(components[length])
    length = length - 1
    while length >-1:
        Probability = np.dot(Mcomponents[-1], components[length])
        Mcomponents.append(Probability)
        length = length - 1
    PiMalmost = np.array([[1,0],[0,1]]) + sum(Mcomponents)
    PiM = inv(PiMalmost)
    Pi0 = np.dot(PiM, Mcomponents[-1])
    Mcomponents2 = []
    for i in Mcomponents:
        comp = np.dot(PiM, i)
        Mcomponents2.append(comp)
    Mcomponents2.append(PiM)
    return components, Mcomponents, Pi0, Mcomponents2
        
z = PiCalculatorNumber2(2,mew,lambd)
z8 = PiCalculatorNumber2(8,mew,lambd)
z14 = PiCalculatorNumber2(14,mew,lambd)

#print('Pi0 for N=2:')
#print(z[2])
#print('')
#print(np.array([[1,0],[0,1]]) - z[2])

#print('')
#print('Pi0 for N=8:')
#print(z8[2])
#print('')
#print(np.array([[1,0],[0,1]]) - z8[2])

#print('')
#print('Pi0 for N=14:')
#print(z14[2])
#print('')
#print('')
#print(np.array([[1,0],[0,1]]) - z14[2])

K = z8[3]
#print('sum K:')
#print(sum(K))
#print(np.array([[1,0],[0,1]]))


lambdamatrix = np.array([[lambd,0],[0,lambd]])
secondcomponent = np.array([[1,0],[0,1]]) - Pi0
Throughput = np.dot(lambdamatrix , secondcomponent)
Th60 = 60*60*Throughput

lambdamatrix8 = np.array([[lambd,0],[0,lambd]])
secondcomponent8 = np.array([[1,0],[0,1]]) - z8[2]
Throughput8 = np.dot(lambdamatrix8 , secondcomponent8)
Th860 = 60*60*Throughput8

lambdamatrix14 = np.array([[lambd,0],[0,lambd]])
secondcomponent14 = np.array([[1,0],[0,1]]) - z14[2]
Throughput14 = np.dot(lambdamatrix14 , secondcomponent14)
Th1460 = 60*60*Throughput14
#print('')
#print('Throughput  N = 2:')
#print(Th60)
#print('')
#print('Throughput  N = 8:')
#print(Th860)
#print('')
#print('Throughput  N = 14:')
#print(Th1460)

matr = np.array([[0,0],[0,0]])


matrixA = np.array([[1,2],[3,4]])
matrixB = np.array([[5,6],[7,8]])

mat = np.dot(matrixB,matrixA)
mat2 = np.dot(matrixA, mat)
mat3 = np.dot(matrixA, matrixB)
mat4 = np.dot(mat3, matrixA)
#print('')
#print(mat2)
#print('')
#print(mat4)




I = np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1]])
    
Ab = np.array([
        [1,2,3],
        [4,5,6],
        [8,4,2]]) 
    
I2 = np.array([2,2,2])
II = np.array([[1],[1],[1]])
Ar = np.array([
        [5,4,3],
        [2,1,7],
        [8,9,2]])
S = np.array([[2],[4],[6]])
S1 = np.array([3,5,8])
f = np.dot(Ab, S)
#print(f)