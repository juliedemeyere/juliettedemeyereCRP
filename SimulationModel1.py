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
import matplotlib.pyplot as plt


# Initialize with four robots
Robots_WS = []
Robots_Moving = []


N = 12 # amount of hours. Needs to be greater than 1 for warm up effect
T = 60*60*N # amount of time that the simulation is kept running, in seconds

t = 0

robots = (['Robot1', 0], ['Robot2', 0], ['Robot3', 0], ['Robot4', 0], ['Robot5', 0], ['Robot6', 0], ['Robot7', 0], ['Robot8', 0], ['Robot9', 0], ['Robot10', 0], ['Robot11', 0], ['Robot12', 0], ['Robot13', 0], ['Robot14', 0])

F = 8 # Specify here the amount of robots per workstation to initialize [robot number, arrival at workstation]


Robots_WS = []
for i in range(0,F):
    m = robots[i]
    Robots_WS .append(m)


TimeWaitedInQueue =[]
TimesStartedService = []
TimeJobFinished = []
AmountofJobsFinished = []
OrderCycleTime = []

Xlength = 90
Ylength = 37
crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections
aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections
def ZeroOrOneGenerator(probability):
    value = random.randint(1,101)
    if value <= probability:
        n = 1
    else:
        n = 0
    return n

def PodMatrixGenerator(probability):
    matrix = []
    for i in range(Ylength+1):
        aislerow = []
        if i in aisles:
            for x in range(Xlength+1):
                aislerow.append(0)
        else:
            for x in range(Xlength+1):
                if x in crossaisles:
                    aislerow.append(0)
                else:
                    m = ZeroOrOneGenerator(probability)
                    aislerow.append(m)
        matrix.append(aislerow)
    return matrix

def GenerateRobotDelay(PodMatrix):
    Move3 = DistanceCalculator_Move3(46,0, 'South', PodMatrix)
    PodMatrix = Move3[3]
    Move1 = DistanceCalculator_Move1(46,0, 'South', PodMatrix)
    Move2 = DistanceCalculator_Move2(Move1[1],Move1[2], Move3[1], Move3[2])
    Times = CalculateTravelTime(Move1, Move2, Move3)
    Time = sum(Times)
    return Time, PodMatrix

PodMatrix = PodMatrixGenerator(85) # initialize all pod positions
while t < T:
    for i in Robots_Moving:
        ArrivalTime = i[1]
        if t >= ArrivalTime: # schedule the arrival of the pods
            AddingEvent = i
            indexnumber = Robots_Moving.index(i)
            Robots_Moving.remove(i)
            Robots_WS.append(AddingEvent)
    if len(Robots_WS) > 0:
        CurrentEvent = Robots_WS[0]
        QueueWaitingTime = t - CurrentEvent[1] 
        TimeWaitedInQueue.append(QueueWaitingTime)
        TimesStartedService.append(t)
        Robots_WS.pop(0)
        PickingTime = random.expovariate(15)
        t += PickingTime
        TimeJobFinished.append(t)
        AmountofJobsFinished.append(1)
    
        DT = GenerateRobotDelay(PodMatrix)
        DelayTime = DT[0]
        PodMatrix = DT[1]
        ReturnTime = t + DelayTime
        CurrentEvent[1] = ReturnTime
        Robots_Moving.append(CurrentEvent)
        OrderCycleTimeJob = QueueWaitingTime + PickingTime + DelayTime
        OrderCycleTime.append(OrderCycleTimeJob)

    t = t+1

# In order to eliminate the warm up effect
n = 30
del TimeWaitedInQueue[:n]
del TimesStartedService[:n]
del TimeJobFinished[:n]
del AmountofJobsFinished[:n]
del OrderCycleTime[:n]
    
AverageWaitingTime = sum(TimeWaitedInQueue)/len(TimeWaitedInQueue)
print('Average Waiting Time in Queue (s) :', AverageWaitingTime)

AverageThroughputRate = sum(AmountofJobsFinished)/(T - 30)*60*60
print('Average Throughput Rate (/hour):',AverageThroughputRate)    

AverageOrderCycleTime = sum(OrderCycleTime)/len(OrderCycleTime)
print('Average order cycle time (s):', AverageOrderCycleTime)

#plt.plot(TimesStartedService,TimeWaitedInQueue)
#plt.xlabel('Time')
#plt.ylabel('Time Waited in Queue')

#plt.plot(TimesStartedService,OrderCycleTime)
#plt.xlabel('Time')
#plt.ylabel('OrderCycleTime (s)')