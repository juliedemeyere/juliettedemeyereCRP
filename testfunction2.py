#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 15:27:47 2019

@author: juliedemeyere
"""



from Model1 import CalculateTravelTime
from Model1 import DistanceCalculator_Move3
from Model1 import DistanceCalculator_Move1
from Model1 import DistanceCalculator_Move2
from collections import deque # Use deque because it is really fast
import random


# Initialize with four robots
Robots_WS = []
Robots_Moving = []
Robots_WS.append(['Robot1', 0]) 
Robots_WS.append(['Robot2', 0]) 
Robots_WS.append(['Robot3', 0]) 
Robots_WS.append(['Robot4', 0])

for i in Robots_WS:
    time = i[1]
    Robots_WS.remove(i)
    print(Robots_WS)
#    print(time)
    
#print(Robots_WS)

print(Robots_WS[0][1])