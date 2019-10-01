#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:32:03 2019

@author: juliedemeyere
"""

from Model2 import CalculateTravelTime
#from Model2 import DistanceCalculator_Move3
#from Model2 import DistanceCalculator_Move1
#from Model2 import DistanceCalculator_Move2
#from MatrixFile import PodMatrixClass
from collections import deque # Use deque because it is really fast
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


# Initialize with four robots
Robots_Moving_WS1 = []
Robots_Moving_WS2 = []
Robots_Moving_WS3 = []
Robots_Moving_WS4 = []
Robots_Moving_WS5 = []


N = 168 # amount of hours. Needs to be greater than 1 for warm up effect
T = 60*60*N # amount of time that the simulation is kept running, in seconds

t = 0

#robots = (['Robot1', 0], ['Robot2', 0], ['Robot3', 0], ['Robot4', 0], ['Robot5', 0], ['Robot6', 0], ['Robot7', 0], ['Robot8', 0], ['Robot9', 0], ['Robot10', 0], ['Robot11', 0], ['Robot12', 0], ['Robot13', 0], ['Robot14', 0])

robots = ('Robot 1', 'Robot 2', 'Robot 3', 'Robot 4', 'Robot 5', 'Robot 6', 'Robot 7', 'Robot 8', 'Robot 9', 'Robot 10', 'Robot 11', 'Robot 12', 'Robot 13', 'Robot 14')
F = 14 # Specify here the amount of robots per workstation to initialize [robot number, arrival at workstation]

WS1DelayDistances = [[],[],[]]
WS2DelayDistances = [[],[],[]]
WS3DelayDistances = [[],[],[]]
WS4DelayDistances = [[],[],[]]
WS5DelayDistances = [[],[],[]]

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
    Robots_WS5.append(z5)


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

WS1picking = []
WS2picking = []
WS3picking = []
WS4picking = []
WS5picking = []


Xlength = 90
Ylength = 37
crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections
aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections

WS_Xlocation = {1:0, 2:17, 3:46, 4:74, 5:90}
WS_Ylocation = {1:19, 2:0, 3:0, 4:0, 5:20}
WS_direction = {1:'West',2:'South', 3:'South',4:'South', 5:'East'}

def GenerateRobotDelay(WS):
    Times = CalculateTravelTime(F)
    Time = sum(Times)
    return Time




#PodMatrix = PodMatrixGenerator(85) # initialize all pod positions
#PodMatrixOriginal = PodMatrix.copy()
StartServiceNext_WS1 = 0 # Initialize the service start at WS
StartServiceNext_WS2 = 0
StartServiceNext_WS3 = 0
StartServiceNext_WS4 = 0
StartServiceNext_WS5 = 0

while t < T:
    if len(Robots_Moving_WS1) > 0:
        for i in Robots_Moving_WS1:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS1.index(i)
                Robots_Moving_WS1.remove(i)
                Robots_WS1.append(AddingEvent)
    if len(Robots_Moving_WS2) > 0:
        for i in Robots_Moving_WS2:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS2.index(i)
                Robots_Moving_WS2.remove(i)
                Robots_WS2.append(AddingEvent)
    if len(Robots_Moving_WS3):
        for i in Robots_Moving_WS3:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS3.index(i)
                Robots_Moving_WS3.remove(i)
                Robots_WS3.append(AddingEvent)
    if len(Robots_Moving_WS4) > 0:
        for i in Robots_Moving_WS4:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS4.index(i)
                Robots_Moving_WS4.remove(i)
                Robots_WS4.append(AddingEvent)
    if len(Robots_Moving_WS5) > 0:
        for i in Robots_Moving_WS5:
            ArrivalTime = i[1]
            if t >= ArrivalTime: # schedule the arrival of the pods
                AddingEvent = i
                indexnumber = Robots_Moving_WS5.index(i)
                Robots_Moving_WS5.remove(i)
                Robots_WS5.append(AddingEvent)
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
            WS1picking.append(PickingTime)
        
            DT = GenerateRobotDelay(WS)
            DelayTime = DT
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS1.append(CurrentEvent)
            OrderCycleTimeJob_WS1 = QueueWaitingTime_WS1 + PickingTime + DelayTime
            OrderCycleTime_WS1.append(OrderCycleTimeJob_WS1)
    if len(Robots_WS2) > 0:
        if t >= StartServiceNext_WS2:
            WS = 2
            CurrentEvent = Robots_WS2[0]
            QueueWaitingTime_WS2 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS2.append(QueueWaitingTime_WS2)
            TimesStartedService_WS2.append(t)
            Robots_WS2.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS2 = t + PickingTime
            TimeJobFinished_WS2.append(StartServiceNext_WS2)
            AmountofJobsFinished_WS2.append(1)
            WS2picking.append(PickingTime)
        
            DT = GenerateRobotDelay(WS)
            DelayTime = DT
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS2.append(CurrentEvent)
            OrderCycleTimeJob_WS2 = QueueWaitingTime_WS2 + PickingTime + DelayTime
            OrderCycleTime_WS2.append(OrderCycleTimeJob_WS2)
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
            WS3picking.append(PickingTime)
        
            DT = GenerateRobotDelay(WS)
            DelayTime = DT
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS3.append(CurrentEvent)
            OrderCycleTimeJob_WS3 = QueueWaitingTime_WS3 + PickingTime + DelayTime
            OrderCycleTime_WS3.append(OrderCycleTimeJob_WS3)
    if len(Robots_WS4) > 0:
        if t > StartServiceNext_WS4:
            WS = 4
            CurrentEvent = Robots_WS4[0]
            QueueWaitingTime_WS4 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS4.append(QueueWaitingTime_WS4)
            TimesStartedService_WS4.append(t)
            Robots_WS4.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS4 = t + PickingTime
            TimeJobFinished_WS4.append(StartServiceNext_WS4)
            AmountofJobsFinished_WS4.append(1)
            WS4picking.append(PickingTime)
        
            DT = GenerateRobotDelay(WS)
            DelayTime = DT
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS4.append(CurrentEvent)
            OrderCycleTimeJob_WS4 = QueueWaitingTime_WS4 + PickingTime + DelayTime
            OrderCycleTime_WS4.append(OrderCycleTimeJob_WS4)
    if len(Robots_WS5) > 0:
        if t > StartServiceNext_WS5:
            WS = 5
            CurrentEvent = Robots_WS5[0]
            QueueWaitingTime_WS5 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS5.append(QueueWaitingTime_WS5)
            TimesStartedService_WS5.append(t)
            Robots_WS5.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS5 = t + PickingTime
            TimeJobFinished_WS5.append(StartServiceNext_WS5)
            AmountofJobsFinished_WS5.append(1)
            WS5picking.append(PickingTime)
        
            DT = GenerateRobotDelay(WS)
            DelayTime = DT
            ReturnTime = t + DelayTime
            CurrentEvent[1] = ReturnTime
            Robots_Moving_WS5.append(CurrentEvent)
            OrderCycleTimeJob_WS5 = QueueWaitingTime_WS5 + PickingTime + DelayTime
            OrderCycleTime_WS5.append(OrderCycleTimeJob_WS5)
    t = t+1

# In order to eliminate the warm up effect
n = 30
del TimeWaitedInQueue_WS3[:n]
del TimesStartedService_WS3[:n]
del TimeJobFinished_WS3[:n]
del AmountofJobsFinished_WS3[:n]
del OrderCycleTime_WS3[:n]

del TimeWaitedInQueue_WS2[:n]
del TimesStartedService_WS2[:n]
del TimeJobFinished_WS2[:n]
del AmountofJobsFinished_WS2[:n]
del OrderCycleTime_WS2[:n]

del TimeWaitedInQueue_WS1[:n]
del TimesStartedService_WS1[:n]
del TimeJobFinished_WS1[:n]
del AmountofJobsFinished_WS1[:n]
del OrderCycleTime_WS1[:n]

del TimeWaitedInQueue_WS4[:n]
del TimesStartedService_WS4[:n]
del TimeJobFinished_WS4[:n]
del AmountofJobsFinished_WS4[:n]
del OrderCycleTime_WS4[:n]

del TimeWaitedInQueue_WS5[:n]
del TimesStartedService_WS5[:n]
del TimeJobFinished_WS5[:n]
del AmountofJobsFinished_WS5[:n]
del OrderCycleTime_WS5[:n]

#print('##Workstation 1:##')
AverageWaitingTime1 = sum(TimeWaitedInQueue_WS1)/len(TimeWaitedInQueue_WS1)
#print('Average Waiting Time in Queue (s) :', AverageWaitingTime1)
AverageThroughputRate1 = sum(AmountofJobsFinished_WS1)/(T - 30)*60*60
#print('Average Throughput Rate (/hour):',AverageThroughputRate1)    
AverageOrderCycleTime1 = sum(OrderCycleTime_WS1)/len(OrderCycleTime_WS1)
#print('Average order cycle time (s):', AverageOrderCycleTime1)

#print('##Workstation 2:##')
AverageWaitingTime2 = sum(TimeWaitedInQueue_WS2)/len(TimeWaitedInQueue_WS2)
#print('Average Waiting Time in Queue (s) :', AverageWaitingTime2)
AverageThroughputRate2 = sum(AmountofJobsFinished_WS2)/(T - 30)*60*60
#print('Average Throughput Rate (/hour):',AverageThroughputRate2)    
AverageOrderCycleTime2 = sum(OrderCycleTime_WS2)/len(OrderCycleTime_WS2)
#print('Average order cycle time (s):', AverageOrderCycleTime2)

#print('##Workstation 3:##')
AverageWaitingTime3 = sum(TimeWaitedInQueue_WS3)/len(TimeWaitedInQueue_WS3)
#print('Average Waiting Time in Queue (s) :', AverageWaitingTime3)
AverageThroughputRate3 = sum(AmountofJobsFinished_WS3)/(T - 30)*60*60
#print('Average Throughput Rate (/hour):',AverageThroughputRate3)    
AverageOrderCycleTime3 = sum(OrderCycleTime_WS3)/len(OrderCycleTime_WS3)
#print('Average order cycle time (s):', AverageOrderCycleTime3)

#print('##Workstation 4:##')
AverageWaitingTime4 = sum(TimeWaitedInQueue_WS4)/len(TimeWaitedInQueue_WS4)
#print('Average Waiting Time in Queue (s) :', AverageWaitingTime4)
AverageThroughputRate4 = sum(AmountofJobsFinished_WS4)/(T - 30)*60*60
#print('Average Throughput Rate (/hour):',AverageThroughputRate4)    
AverageOrderCycleTime4 = sum(OrderCycleTime_WS4)/len(OrderCycleTime_WS4)
#print('Average order cycle time (s):', AverageOrderCycleTime4)

#print('##Workstation 5:##')
AverageWaitingTime5 = sum(TimeWaitedInQueue_WS5)/len(TimeWaitedInQueue_WS5)
#print('Average Waiting Time in Queue (s) :', AverageWaitingTime5)
AverageThroughputRate5 = sum(AmountofJobsFinished_WS5)/(T - 30)*60*60
#print('Average Throughput Rate (/hour):',AverageThroughputRate5)    
AverageOrderCycleTime5 = sum(OrderCycleTime_WS5)/len(OrderCycleTime_WS5)
#print('Average order cycle time (s):', AverageOrderCycleTime5)

#print('#######################')
print('Average all Workstations')
AverageWaitingTime = (AverageWaitingTime1+AverageWaitingTime2+AverageWaitingTime3+AverageWaitingTime4+AverageWaitingTime5)/5
print('Average Waiting Time in Queue (s) :', AverageWaitingTime)
AverageThroughputRate = (AverageThroughputRate1+AverageThroughputRate2+AverageThroughputRate3+AverageThroughputRate4+AverageThroughputRate5)/5
print('Average Throughput Rate (/hour):',AverageThroughputRate)    
AverageOrderCycleTime = (AverageOrderCycleTime1+AverageOrderCycleTime2+AverageOrderCycleTime3+AverageOrderCycleTime4+AverageOrderCycleTime5)/5
print('Average order cycle time (s):', AverageOrderCycleTime)
print('For an overview of all results per workstation view the panda "Results"')

def AverageDelayTimes(WS):
    workstation = {1:WS1DelayDistances,2:WS2DelayDistances, 3:WS3DelayDistances, 4:WS4DelayDistances, 5:WS5DelayDistances }
    distancelist = workstation[WS]
    Move1list = distancelist[0]
    AverageMove1Time = (sum(Move1list)/len(Move1list))/1.3
    Move2list = distancelist[1]
    AverageMove2Time = (sum(Move2list)/len(Move2list))/1.3
    Move3list = distancelist[2]
    AverageMove3Time = (sum(Move3list)/len(Move3list))/1.3
    return AverageMove1Time, AverageMove2Time, AverageMove3Time

#Times1= AverageDelayTimes(1)
#Times2= AverageDelayTimes(2)
#Times3= AverageDelayTimes(3)
#Times4= AverageDelayTimes(4)
#Times5= AverageDelayTimes(5)

#AverageD1 = (Times1[0] + Times2[0] + Times3[0] + Times4[0] + Times5[0])/5
#AverageD2 = (Times1[1] + Times2[1] + Times3[1] + Times4[1] + Times5[1])/5
#AverageD3 = (Times1[2] + Times2[2] + Times3[2] + Times4[2] + Times5[2])/5

UtilizationWS1 = sum(WS1picking)/T
UtilizationWS2 = sum(WS2picking)/T
UtilizationWS3 = sum(WS3picking)/T
UtilizationWS4 = sum(WS4picking)/T
UtilizationWS5 = sum(WS5picking)/T


Results = pd.DataFrame(np.array([[(0,19), AverageWaitingTime1, AverageThroughputRate1, AverageOrderCycleTime1], 
                                 [(17,0), AverageWaitingTime2, AverageThroughputRate2, AverageOrderCycleTime2],
                                 [(46,0), AverageWaitingTime3, AverageThroughputRate3, AverageOrderCycleTime3],
                                 [(74,0), AverageWaitingTime4, AverageThroughputRate4, AverageOrderCycleTime4],
                                 [(90,20), AverageWaitingTime5, AverageThroughputRate5, AverageOrderCycleTime5],
                                 ['Average', AverageWaitingTime, AverageThroughputRate, AverageOrderCycleTime]]),
                       columns=['Coordinates', 'Queue Time (s)', 'Throughput Rate (/hour)', 'Order Cycle Time (s)'])

TotalThroughPut = AverageThroughputRate1 + AverageThroughputRate2 + AverageThroughputRate3 + AverageThroughputRate4 + AverageThroughputRate5
print('Total Throughput all Workstations (/hour)', TotalThroughPut)

print('Workstation Utlizations:',
      'WS1:',round(UtilizationWS1,2),
      'WS2:',round(UtilizationWS2,2),
      'WS3:',round(UtilizationWS3,2),
      'WS4:',round(UtilizationWS4,2),
      'WS5:',round(UtilizationWS5,2))
#plt.plot(TimesStartedService,TimeWaitedInQueue)
#plt.xlabel('Time')
#plt.ylabel('Time Waited in Queue')

#plt.plot(TimesStartedService,OrderCycleTime)
#plt.xlabel('Time')
#plt.ylabel('OrderCycleTime (s)')