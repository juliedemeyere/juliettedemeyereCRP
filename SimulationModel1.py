#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:32:03 2019

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

T = 1000 # amount of time that the simulation is kept running, in seconds

t = 0

Robots_WS.append(['Robot1', 0]) 
Robots_WS.append(['Robot2', 0]) 
Robots_WS.append(['Robot3', 0]) 
Robots_WS.append(['Robot4', 0]) # [Robot number, arrival at WorkStation]
TimeWaitedInQueue =[]



def GenerateRobotDelay():
    Move3 = DistanceCalculator_Move3(46,0, 'South')
    Move1 = DistanceCalculator_Move1(46,0, 'South')
    Move2 = DistanceCalculator_Move2(Move1[1],Move1[2], Move3[1], Move3[2])
    Times = CalculateTravelTime(Move1, Move2, Move3)
    Time = sum(Times)
    return Time

while t < T:
    for i in Robots_Moving:
        ArrivalTime = i[1]
     #   print(ArrivalTime)
        if t >= ArrivalTime:
            AddingEvent = i
            indexnumber = Robots_Moving.index(i)
            Robots_Moving.remove(i)
            Robots_WS.append(AddingEvent)
    if len(Robots_WS) > 0:
        CurrentEvent = Robots_WS[0]
        QueueWaitingTime = t - CurrentEvent[1] 
        TimeWaitedInQueue.append(QueueWaitingTime)
        Robots_WS.pop(0)
        PickingTime = random.expovariate(15)
        t += PickingTime
    
        DelayTime = GenerateRobotDelay()
        ReturnTime = t + DelayTime
        CurrentEvent[1] = ReturnTime
        Robots_Moving.append(CurrentEvent)

    t = t+1
    
    