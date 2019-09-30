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
from MatrixFile import PodMatrixClass
from collections import deque # Use deque because it is really fast
import random
import matplotlib.pyplot as plt


# Initialize with four robots
Robots_Moving_WS1 = []
Robots_Moving_WS2 = []
Robots_Moving_WS3 = []
Robots_Moving_WS4 = []
Robots_Moving_WS5 = []


N = 12 # amount of hours. Needs to be greater than 1 for warm up effect
T = 60*60*N # amount of time that the simulation is kept running, in seconds

t = 0

#robots = (['Robot1', 0], ['Robot2', 0], ['Robot3', 0], ['Robot4', 0], ['Robot5', 0], ['Robot6', 0], ['Robot7', 0], ['Robot8', 0], ['Robot9', 0], ['Robot10', 0], ['Robot11', 0], ['Robot12', 0], ['Robot13', 0], ['Robot14', 0])

robots = ('Robot 1', 'Robot 2', 'Robot 3', 'Robot 4', 'Robot 5', 'Robot 6', 'Robot 7', 'Robot 8', 'Robot 9', 'Robot 10', 'Robot 11', 'Robot 12', 'Robot 13', 'Robot 14')
F = 8 # Specify here the amount of robots per workstation to initialize [robot number, arrival at workstation]


Robots_WS1 = []
Robots_WS2 = []
Robots_WS3 = []
Robots_WS4 = []
Robots_WS5 = []
for i in range(0,F):
    z1 = [robots[i], 0, 1]
    Robots_WS1.append(z1)
    z2 = [robots[i], 0, 2]
    Robots_WS2.append(z2)
    z3 = [robots[i], 0, 3]
    Robots_WS3.append(z3)
    z4 = [robots[i], 0, 4]
    Robots_WS4.append(z4)
    z5 = [robots[i], 0, 5]
    Robots_WS1.append(z5)


TimeWaitedInQueue_WS1 =[]
TimesStartedService_WS1 = []
TimeJobFinished_WS1 = []
AmountofJobsFinished_WS1 = []
OrderCycleTime_WS1 = []

TimeWaitedInQueue_WS2 =[]
TimesStartedService_WS2 = []
TimeJobFinished_WS2 = []
AmountofJobsFinished_WS2 = []
OrderCycleTime_WS2 = []

TimeWaitedInQueue_WS3 =[]
TimesStartedService_WS3 = []
TimeJobFinished_WS3 = []
AmountofJobsFinished_WS3 = []
OrderCycleTime_WS3 = []

TimeWaitedInQueue_WS4 =[]
TimesStartedService_WS4 = []
TimeJobFinished_WS4 = []
AmountofJobsFinished_WS4 = []
OrderCycleTime_WS4 = []

TimeWaitedInQueue_WS5 =[]
TimesStartedService_WS5 = []
TimeJobFinished_WS5 = []
AmountofJobsFinished_WS5 = []
OrderCycleTime_WS5 = []

Xlength = 90
Ylength = 37
crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections
aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections
#def ZeroOrOneGenerator(probability):
#    value = random.randint(1,101)
#    if value <= probability:
#        n = 1
#    else:
#        n = 0
#    return n

#def PodMatrixGenerator(probability):
#    matrix = []
#    for i in range(Ylength+1):
#        aislerow = []
#        if i in aisles:
#            for x in range(Xlength+1):
#                aislerow.append(0)
#        else:
#            for x in range(Xlength+1):
#                if x in crossaisles:
#                    aislerow.append(0)
#                else:
#                    m = ZeroOrOneGenerator(probability)
#                    aislerow.append(m)
#        matrix.append(aislerow)
#    return matrix

WS_Xlocation = {1:0, 2:17, 3:46, 4:74, 5:90}
WS_Ylocation = {1:19, 2:0, 3:0, 4:0, 5:20}
WS_direction = {1:'West',2:'South', 3:'South',4:'South', 5:'East'}

def GenerateRobotDelay(PodMatrix, WS):
    x = WS_Xlocation[WS]
    y = WS_Ylocation[WS]
    location = WS_direction[WS]
    Move3 = DistanceCalculator_Move3(x,y, location, PodMatrix)
  #  PodMatrix[Move3[2]][Move3[1]] = 0
    Workfloor.MakeZero(Move3[1],Move3[2])
  #  print(PodMatrix[Move3[2]][Move3[1]])
    Move1 = DistanceCalculator_Move1(x,y, location, PodMatrix)
    Workfloor.MakeOne(Move1[1],Move1[2])
    Move2 = DistanceCalculator_Move2(Move1[1],Move1[2], Move3[1], Move3[2])
    Times = CalculateTravelTime(Move1, Move2, Move3)
    Time = sum(Times)
    return Time, PodMatrix


Workfloor = PodMatrixClass()
probability = 90

Workfloor.PodMatrixGenerator(probability) # generates a new podmatrix

PodMatrix = Workfloor.Matrix
print(len(PodMatrix))

Workfloor.MakeZero(1,2)

Workfloor.MakeOne(1,3)


newmatrix = Workfloor.Matrix

#PodMatrix = PodMatrixGenerator(85) # initialize all pod positions
#PodMatrixOriginal = PodMatrix.copy()
StartServiceNext_WS1 = 0 # Initialize the service start at WS
StartServiceNext_WS2 = 0
StartServiceNext_WS3 = 0
StartServiceNext_WS4 = 0
StartServiceNext_WS5 = 0
third = int(0.9*T)
twothird = int(0.66*T)

while t < T:
    if len(Robots_Moving_WS1) > 0:
        for i in Robots_Moving_WS1:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS1.index(i)
                Robots_Moving_WS1.remove(i)
                Robots_WS1.append(AddingEvent)
    if len(Robots_Moving_WS3):
        for i in Robots_Moving_WS3:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS3.index(i)
                Robots_Moving_WS3.remove(i)
                Robots_WS3.append(AddingEvent)
    if len(Robots_WS1) > 0:
        if t >= StartServiceNext_WS1:
            WS = 1
            CurrentEvent = Robots_WS1[0]
            QueueWaitingTime_WS1 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS1.append(QueueWaitingTime_WS1)
            TimesStartedService_WS1.append(t)
            Robots_WS1.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS1 = t + PickingTime
            TimeJobFinished_WS1.append(StartServiceNext_WS1)
            AmountofJobsFinished_WS1.append(1)
        
            DT = GenerateRobotDelay(PodMatrix, WS)
            DelayTime = DT[0]
   #         PodMatrix = DT[1]
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS1.append(CurrentEvent)
            OrderCycleTimeJob_WS1 = QueueWaitingTime_WS1 + PickingTime + DelayTime
            OrderCycleTime_WS1.append(OrderCycleTimeJob_WS1)
    if len(Robots_WS3) > 0:
        if t > StartServiceNext_WS3:
            WS = 3
            CurrentEvent = Robots_WS3[0]
            QueueWaitingTime_WS3 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS3.append(QueueWaitingTime_WS3)
            TimesStartedService_WS3.append(t)
            Robots_WS3.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS3 = t + PickingTime
            TimeJobFinished_WS3.append(StartServiceNext_WS3)
            AmountofJobsFinished_WS3.append(1)
        
            DT = GenerateRobotDelay(PodMatrix, WS)
            DelayTime = DT[0]
  #          PodMatrix = DT[1]
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS3.append(CurrentEvent)
            OrderCycleTimeJob_WS3 = QueueWaitingTime_WS3 + PickingTime + DelayTime
            OrderCycleTime_WS3.append(OrderCycleTimeJob_WS3)
#    if t == third:
#        Pmat1 = PodMatrix
#    if t == twothird:
#        Pmat2 = PodMatrix
        
 #   print(PodMatrix[4])
    t = t+1
#counter = 0
#noncounter = 0
#for i in range(0,len(PodMatrix)):
 #   print(Pmat1[i], Pmat2[i])
#    if PodMatrix[i] == PodMatrixOriginal[i]:
#        noncounter += 1
#    else:
#        counter += 1
#print(counter, noncounter)
        
#        print('sisisi')
#    else:
#        print('no')
  #  print(i)

# In order to eliminate the warm up effect
n = 30
del TimeWaitedInQueue_WS3[:n]
del TimesStartedService_WS3[:n]
del TimeJobFinished_WS3[:n]
del AmountofJobsFinished_WS3[:n]
del OrderCycleTime_WS3[:n]

del TimeWaitedInQueue_WS1[:n]
del TimesStartedService_WS1[:n]
del TimeJobFinished_WS1[:n]
del AmountofJobsFinished_WS1[:n]
del OrderCycleTime_WS1[:n]

print('##Workstation 1:##')
AverageWaitingTime = sum(TimeWaitedInQueue_WS1)/len(TimeWaitedInQueue_WS1)
print('Average Waiting Time in Queue (s) :', AverageWaitingTime)

AverageThroughputRate = sum(AmountofJobsFinished_WS1)/(T - 30)*60*60
print('Average Throughput Rate (/hour):',AverageThroughputRate)    

AverageOrderCycleTime = sum(OrderCycleTime_WS1)/len(OrderCycleTime_WS1)
print('Average order cycle time (s):', AverageOrderCycleTime)

print('##Workstation 3:##')
AverageWaitingTime = sum(TimeWaitedInQueue_WS3)/len(TimeWaitedInQueue_WS3)
print('Average Waiting Time in Queue (s) :', AverageWaitingTime)

AverageThroughputRate = sum(AmountofJobsFinished_WS3)/(T - 30)*60*60
print('Average Throughput Rate (/hour):',AverageThroughputRate)    

AverageOrderCycleTime = sum(OrderCycleTime_WS3)/len(OrderCycleTime_WS3)
print('Average order cycle time (s):', AverageOrderCycleTime)

#plt.plot(TimesStartedService,TimeWaitedInQueue)
#plt.xlabel('Time')
#plt.ylabel('Time Waited in Queue')

#plt.plot(TimesStartedService,OrderCycleTime)
#plt.xlabel('Time')
#plt.ylabel('OrderCycleTime (s)')