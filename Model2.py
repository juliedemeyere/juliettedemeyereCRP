#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 20:03:33 2019

@author: juliedemeyere
"""
import random

aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections

aislesdict = {0: 'West', 2:'East', 5:'West', 8:'East', 11:'West', 14:'East', 17:'West', 20:'East', 23:'West', 26:'East', 29:'West', 32:'East', 35:'West', 37:'East'}

crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections

crossaislesdict = {0 :'North', 6:'South', 12:'North', 18:'South', 24:'North', 30:'South', 36:'North', 42:'South', 48:'North', 54:'South', 60:'North', 66:'South', 72:'North', 78:'South', 84:'North', 90:'South'}


def CalculateTravelTime(robots):
  #  D1 = Move1[0]
  #  D2 = Move2
    #D3 = Move3[0]
    robotdelaysT1 = {2:42.8078,8:42.827,14:42.78}
    robotdelaysT2 ={2:32.33,8:32.26,14:32.21}
    robotdelaysT3 ={2:43.78,8:43.68,14:43.69}
    T1 = random.expovariate(1/robotdelaysT1[robots])
    T2 = random.expovariate(1/robotdelaysT2[robots])
    T3 = random.expovariate(1/robotdelaysT3[robots])
 #   T1 = D1/1.3+1
 #   T2 = D2/1.3+1
 #   T3 = D3/1.3+1
    
    
    return T1,T2,T3











    
