#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 16:12:12 2019

@author: juliedemeyere
"""
import random
import numpy as np

#print(random.expovariate(1/15))

lists = []
def cox(b1=1,k=3,mu=15):
    u = (np.random.uniform(0,1) < b1)
    x = np.random.exponential(mu,k)
    if u:
        return x[0]
    return sum(x)
#
#lists2 = []
#for i in range(0,1000):
#    y = cox()
#    m = random.expovariate(1/15)
#    lists.append(y)
#    lists2.append(m)

#m = np.random.exponential(15)
#print(m)
#print(sum(lists)/len(lists))
#print(sum(lists2)/len(lists2))