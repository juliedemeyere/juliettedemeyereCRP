#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:44:27 2019

@author: juliedemeyere
"""
import math
#n = 3


mud = 29.4
lambd = 240


N = 14

Nabove = 1 + (1/lambd)*(1/mud)
Nbelow = 1 + (1/lambd)*(1/mud) + (1/(lambd**2))*(1/(2*mud**2))

Th = Nabove/Nbelow


def ThroughPutCalculator(N):
    AllNValues = []
    for n in range(0,N+1):
        #GwGd = (1/(lambd**n))*(1/(math.factorial(n)*mud**n))
        Gw = 1/(lambd**n)
        Gd = (1/(math.factorial(n)*mud**n))
        GwGd = Gw*Gd
        AllNValues.append(GwGd)
    Nabove = sum(AllNValues[:N])
    Nbelow = sum(AllNValues)
    Throughput = Nabove/Nbelow
#    print(AllNValues[:N])
#    print(AllNValues)
#    print(Throughput)
    print('Throughput:',Throughput)
    return(Throughput)
    
ThroughPutCalculator(N)



#Kvalues = []
#for n in range(1,15):
#    sumD = []
#    sumW = []
#    for g in range(1,n+1):
#        Dprobability = 1/((1/(MUd**g))*(1/(math.factorial(g))))
#        Wprobability = 1/(lambd**g)
#        sumD.append(Dprobability)
#        sumW.append(Wprobability)
#    PyD = sum(sumD)
#    PyW = sum(sumW)
#    
#    K = PyD*PyW
#    Kvalues.append(K)
    
#Throughput2 = (Kvalues[0]/Kvalues[1])
#Throughput8 = Kvalues[6]/Kvalues[7]
#Throughput14 = Kvalues[12]/Kvalues[13]


mew = 1/(44.1 + 33.13 + 45.2)
lam = 1/15
#ze8 = mew*8/lam
#ze2 = mew*2/lam
#ze14 = mew*14/lam



#Dvalues = []
#for n in range(1,15):
#    sumD = []
#    for g in range(1,n+1):
        #Dprobability = 1/((1/(MUd**g))*(1/(math.factorial(g))))
#        Dprobability = 1/(lambd**g)
#        sumD.append(Dprobability)
#    PyD = sum(sumD)
#    D = 1/(PyD)
#    Dvalues.append(D)
    
#v2 = Dvalues[0]/(Dvalues[0]+Dvalues[1])
#v8 = sum(Dvalues[:6])/sum(Dvalues[:7])
#v14 = sum(Dvalues[:12])/sum(Dvalues[:13])

#sumpartd = 0
#sud = []
#for i in range(1,100):
#    z = 1/((1/(MUd**i))*(1/(math.factorial(i))))
#    sumpartd += z
    
#sumpartw = 0
#for t in range(1,100):
#    m = 1/(lambd**t)
#    sumpartw += m

#Pw0 = 1/(1 + sumpartw)
#Pd0 = 1/(1 + sumpartd)

