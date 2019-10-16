#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 14:19:40 2019

@author: juliedemeyere
"""
import math


mew = 1/(44.1 + 33.13 + 45.2)
#mew = (1/44.1 +  1/33.13 +  1/45.2)
lambd = 1/15
N = 14

def PiOCalculator(N, mew, lambd):
    Pi0Components = []
    for m in range(0,N+1):
        PiX = (math.factorial(N)*(mew/lambd)**m)/(math.factorial(N-m))
        Pi0Components.append(PiX)
    sumComponents = sum(Pi0Components)
    Pi0 = 1/sumComponents
    return Pi0

Pi0 = PiOCalculator(N, mew, lambd)

Throughput_second = lambd - lambd*Pi0

Throughput_hour = Throughput_second*60*60

TotalThroughput_hour = Throughput_hour*5


me2 = (1/44.1 +  1/33.13 +  1/45.2)