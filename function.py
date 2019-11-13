#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:12:12 2019

@author: juliedemeyere
"""
import random
import numpy as np
from scipy.stats import gamma
import scipy.stats
from scipy import mean
#print(random.expovariate(1/15))

lists = []
#cox(b1=1,k=3,mu=15)
def coxOLD(b1,k,mu):
    u = (np.random.uniform(0,1) < b1)
    # mu should be l
    x = np.random.exponential(mu,k)
    if u:
        return x[0]
    return sum(x)

def coxMeanOLD(b1,k,mean):
    return coxOLD(b1,k,(k*(1-b1)-1)/mean)

def coxMean(b1,k,mean):
    return cox(b1,k,1/((1+b1*(k-1))/mean))

def cox(b1,k,mu):
    u = (np.random.uniform(0,1) < b1)
    x = np.random.exponential(mu,k)
    if u:
        return sum(x)
    else:
        return x[0]

#print(coxMean(0.8,3,15))


def TestCox():
    mlist = []
    meanlist = []
    for i in range(0,100):
        var = coxMean(0.8,3,15)
        mlist.append(var)
        me = 1/((1+0.8*(3-1))/15)
        meanlist.append(me)
    print(mean(mlist))
    print(mean(meanlist))
    print(mlist)
TestCox()

def ErlangDist():
    data_gamma = gamma.rvs(a=  1, size=10000)
    #p = scipy.stats.erlang(1/2)
    listgamma = []
    f = np.random.gamma(2,15)
    b = np.random.exponential(15,3)
    shape, scale = 3., 2.  # mean=4, std=2*sqrt(2)
    for r in range(0, 1000):
        s = np.random.gamma(shape, scale, 1)
        listgamma.append(s)
   # print(mean(listgamma))
#ErlangDist()