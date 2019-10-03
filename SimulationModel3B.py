#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 14:32:03 2019

@author: juliedemeyere
"""

from Model3 import CalculateTravelTime
from Model3 import DistanceCalculator_Move3
from Model3 import DistanceCalculator_Move1
from Model3 import DistanceCalculator_Move2
from MatrixFile import PodMatrixClass
from collections import deque # Use deque because it is really fast
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


Robots_Moving_WS1 = []
WS1JobCycle = []
WS2JobCycle = []
WS3JobCycle = []
WS4JobCycle = []
WS5JobCycle = []


N = 168 # amount of hours. Needs to be greater than 1 for warm up effect
T = 60*60*N # amount of time that the simulation is kept running, in seconds

t = 0

#robots = (['Robot1', 0], ['Robot2', 0], ['Robot3', 0], ['Robot4', 0], ['Robot5', 0], ['Robot6', 0], ['Robot7', 0], ['Robot8', 0], ['Robot9', 0], ['Robot10', 0], ['Robot11', 0], ['Robot12', 0], ['Robot13', 0], ['Robot14', 0])

robots = ('Robot 1', 'Robot 2', 'Robot 3', 'Robot 4', 'Robot 5', 'Robot 6', 'Robot 7', 'Robot 8', 'Robot 9', 'Robot 10', 'Robot 11', 'Robot 12', 'Robot 13', 'Robot 14')
F = 2 # Specify here the amount of robots per workstation to initialize [robot number, arrival at workstation]
ArrivalRate = 31.68 # arrivalrate per hour

LengthBufferQueue = [[],[],[],[],[]]

WS1Delay = [[],[],[]]
WS2Delay = [[],[],[]]
WS3Delay = [[],[],[]]
WS4Delay = [[],[],[]]
WS5Delay = [[],[],[]]

Robots_WS1 = []
Robots_WS2 = []
Robots_WS3 = []
Robots_WS4 = []
Robots_WS5 = []

for i in range(0,F): #[robot#, arrivalat WS, WS, arrivalofjob, storagelocation x, storagelocation y]
    z1 = [robots[i], 0, 1, 0, 0, 0]
    Robots_WS1.append(z1)
    z2 = [robots[i], 0, 2, 0, 0, 0]
    Robots_WS2.append(z2)
    z3 = [robots[i], 0, 3, 0, 0, 0]
    Robots_WS3.append(z3)
    z4 = [robots[i], 0, 4, 0, 0, 0]
    Robots_WS4.append(z4)
    z5 = [robots[i], 0, 5, 0, 0, 0]
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



def Move1ToStorageScheduleArrival(PodMatrix, WS,t):
    x = WS_Xlocation[WS]
    y = WS_Ylocation[WS]
    location = WS_direction[WS]
    Move1 = DistanceCalculator_Move1(x,y, location, PodMatrix)
    Workfloor.MakeOne(Move1[1],Move1[2])
    TravelTime = Move1[0]/1.3
    ArrivalTime = TravelTime + t
    return ArrivalTime, Move1[1], Move1[2], PodMatrix, TravelTime

def Move2Move3DelayTime(PodMatrix, WS,t, x2, y2):
    x = WS_Xlocation[WS]
    y = WS_Ylocation[WS]
    location = WS_direction[WS]
    Move3 = DistanceCalculator_Move3(x,y, location, PodMatrix)
    Workfloor.MakeZero(Move3[1],Move3[2])
    Move2 = DistanceCalculator_Move2(x2,y2, Move3[1], Move3[2])
    Times = CalculateTravelTime(Move2, Move3)
    Time = sum(Times)
    ArrivalTime = Time + t
    return ArrivalTime, PodMatrix, Times[0], Times[1]
    
MovingMove1_WS1 = []
RobotinStorage_WS1 = []
MovingMove23_WS1 = []
WS_1Jobs= [] # arrival times of the jobs awaiting service

MovingMove1_WS2 = []
RobotinStorage_WS2 = []
MovingMove23_WS2 = []
WS_2Jobs= [] # arrival times of the jobs awaiting service

MovingMove1_WS3 = []
RobotinStorage_WS3 = []
MovingMove23_WS3 = []
WS_3Jobs= [] # arrival times of the jobs awaiting service

MovingMove1_WS4 = []
RobotinStorage_WS4 = []
MovingMove23_WS4 = []
WS_4Jobs= [] # arrival times of the jobs awaiting service

MovingMove1_WS5 = []
RobotinStorage_WS5 = []
MovingMove23_WS5 = []
WS_5Jobs= [] # arrival times of the jobs awaiting service

Workfloor = PodMatrixClass()
probability = 85

Workfloor.PodMatrixGenerator(probability) # generates a new podmatrix

PodMatrix = Workfloor.Matrix



WS1IncomingJobArrivalTime = 0
WS2IncomingJobArrivalTime = 0
WS3IncomingJobArrivalTime = 0
WS4IncomingJobArrivalTime = 0
WS5IncomingJobArrivalTime = 0

#def JobScheduler(ArrivalRate, t):
#    seconds = 1/(ArrivalRate/60/60)
#    NextArrival = random.expovariate(1/seconds)
#    ArrivalTime = t + NextArrival
#    print(NextArrival,'ArrivalTime:', ArrivalTime)
#    return ArrivalTime
    
AmountOfJobsArrived = 0    
StartServiceNext_WS1 = 0 # Initialize the service start at WS
StartServiceNext_WS2 = 0
StartServiceNext_WS3 = 0
StartServiceNext_WS4 = 0
StartServiceNext_WS5 = 0

while t < T:
    if len(MovingMove1_WS1) > 0:
        for i in MovingMove1_WS1:
            ArrivalTime = i[1]
            if t >= ArrivalTime: #schedule the arrival of the pods to storage
                AddingEvent = i
                indexnumber = MovingMove1_WS1.index(i)
                MovingMove1_WS1.remove(i)
                RobotinStorage_WS1.append(AddingEvent)
    if len(RobotinStorage_WS1) > 0:    
        if len(WS_1Jobs) > 0:
            earliest = min(WS_1Jobs)
            WS_1Jobs.remove(earliest)
            Robot = RobotinStorage_WS1[0]
            WS = Robot[2]
            RobotinStorage_WS1.pop(0)
            Robot[3] = earliest
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            WS1Delay[1].append(Move23[2])
            WS1Delay[2].append(Move23[3])
            Robot[1] = ArrivalAtWS
            MovingMove23_WS1.append(Robot)
    if  t >= WS1IncomingJobArrivalTime:
        WS_1Jobs.append(WS1IncomingJobArrivalTime)
        AmountOfJobsArrived += 1
        seconds = 1/(ArrivalRate/60/60)
        NextArrival = random.expovariate(1/seconds)
        ArrivalTime = t + NextArrival
        WS1IncomingJobArrivalTime = ArrivalTime
    if len(MovingMove23_WS1) > 0:
        for i in MovingMove23_WS1:
            ArrivalTime = i[1]
            if t >= ArrivalTime:
                AddingEvent = i
                MovingMove23_WS1.remove(i)
                Robots_WS1.append(AddingEvent)
    if len(Robots_WS1) > 0:
        if t >= StartServiceNext_WS1: # starts the service of a new job at WS
            CurrentEvent = Robots_WS1[0]
            WS = CurrentEvent[2]
            QueueWaitingTime_WS1 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS1.append(QueueWaitingTime_WS1)
            TimesStartedService_WS1.append(t)
            Robots_WS1.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS1 = t + PickingTime
            TimeJobFinished_WS1.append(StartServiceNext_WS1)
            AmountofJobsFinished_WS1.append(1)
            WS1picking.append(PickingTime)
            
            Move1= Move1ToStorageScheduleArrival(PodMatrix, WS,t)
            WS1Delay[0].append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS1JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS1.append(CurrentEvent)
            
    #### NUMBER 2 #########       
    if len(MovingMove1_WS2) > 0:
        for i in MovingMove1_WS2:
            ArrivalTime = i[1]
            if t >= ArrivalTime: #schedule the arrival of the pods to storage
                AddingEvent = i
                indexnumber = MovingMove1_WS2.index(i)
                MovingMove1_WS2.remove(i)
                RobotinStorage_WS2.append(AddingEvent)
    if len(RobotinStorage_WS2) > 0:    
        if len(WS_2Jobs) > 0:
            earliest = min(WS_2Jobs)
            WS_2Jobs.remove(earliest)
            Robot = RobotinStorage_WS2[0]
            WS = Robot[2]
            RobotinStorage_WS2.pop(0)
            Robot[3] = earliest
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            WS2Delay[1].append(Move23[2])
            WS2Delay[2].append(Move23[3])
            Robot[1] = ArrivalAtWS
            #print(round(ArrivalAtWS - t,2))
            MovingMove23_WS2.append(Robot)
    if  t >= WS2IncomingJobArrivalTime:
        WS_2Jobs.append(WS2IncomingJobArrivalTime)
        AmountOfJobsArrived += 1
        seconds = 1/(ArrivalRate/60/60)
        NextArrival = random.expovariate(1/seconds)
        ArrivalTime = t + NextArrival
        WS2IncomingJobArrivalTime = ArrivalTime
    if len(MovingMove23_WS2) > 0:
        for i in MovingMove23_WS2:
            ArrivalTime = i[1]
            if t >= ArrivalTime:
                AddingEvent = i
                MovingMove23_WS2.remove(i)
                Robots_WS2.append(AddingEvent)
    if len(Robots_WS2) > 0:
        if t >= StartServiceNext_WS2: # starts the service of a new job at WS
            CurrentEvent = Robots_WS2[0]
            WS = CurrentEvent[2]
            QueueWaitingTime_WS2 = t - CurrentEvent[1] 
            #print(t, CurrentEvent[1], QueueWaitingTime_WS2)
            TimeWaitedInQueue_WS2.append(QueueWaitingTime_WS2)
            TimesStartedService_WS2.append(t)
            Robots_WS2.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS2 = t + PickingTime
            TimeJobFinished_WS2.append(StartServiceNext_WS2)
            AmountofJobsFinished_WS2.append(1)
            WS2picking.append(PickingTime)
            
            Move1= Move1ToStorageScheduleArrival(PodMatrix, WS,t)
            WS2Delay[0].append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS2JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS2.append(CurrentEvent)
            
    
    ###############
    if len(MovingMove1_WS3) > 0:
        for i in MovingMove1_WS3:
            ArrivalTime = i[1]
            if t >= ArrivalTime: #schedule the arrival of the pods to storage
                AddingEvent = i
                indexnumber = MovingMove1_WS3.index(i)
                MovingMove1_WS3.remove(i)
                RobotinStorage_WS3.append(AddingEvent)
    if len(RobotinStorage_WS3) > 0:    
        if len(WS_3Jobs) > 0:
            earliest = min(WS_3Jobs)
            WS_3Jobs.remove(earliest)
            Robot = RobotinStorage_WS3[0]
            WS = Robot[2]
            RobotinStorage_WS3.pop(0)
            Robot[3] = earliest
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            WS3Delay[1].append(Move23[2])
            WS3Delay[2].append(Move23[3])
            Robot[1] = ArrivalAtWS
            MovingMove23_WS3.append(Robot)
    if  t >= WS3IncomingJobArrivalTime:
        WS_3Jobs.append(WS3IncomingJobArrivalTime)
        AmountOfJobsArrived += 1
        seconds = 1/(ArrivalRate/60/60)
        NextArrival = random.expovariate(1/seconds)
        ArrivalTime = t + NextArrival
        WS3IncomingJobArrivalTime = ArrivalTime
    if len(MovingMove23_WS3) > 0:
        for i in MovingMove23_WS3:
            ArrivalTime = i[1]
            if t >= ArrivalTime:
                AddingEvent = i
                MovingMove23_WS3.remove(i)
                Robots_WS3.append(AddingEvent)
    if len(Robots_WS3) > 0:
        if t >= StartServiceNext_WS3: # starts the service of a new job at WS
            CurrentEvent = Robots_WS3[0]
            WS = CurrentEvent[2]
            QueueWaitingTime_WS3 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS3.append(QueueWaitingTime_WS3)
            TimesStartedService_WS3.append(t)
            Robots_WS3.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS3 = t + PickingTime
            TimeJobFinished_WS3.append(StartServiceNext_WS3)
            AmountofJobsFinished_WS3.append(1)
            WS3picking.append(PickingTime)
            
            Move1= Move1ToStorageScheduleArrival(PodMatrix, WS,t)
            WS3Delay[0].append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS3JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS3.append(CurrentEvent)
    ##########
    if len(MovingMove1_WS4) > 0:
        for i in MovingMove1_WS4:
            ArrivalTime = i[1]
            if t >= ArrivalTime: #schedule the arrival of the pods to storage
                AddingEvent = i
                indexnumber = MovingMove1_WS4.index(i)
                MovingMove1_WS4.remove(i)
                RobotinStorage_WS4.append(AddingEvent)
    if len(RobotinStorage_WS4) > 0:    
        if len(WS_4Jobs) > 0:
            earliest = min(WS_4Jobs)
            WS_4Jobs.remove(earliest)
            Robot = RobotinStorage_WS4[0]
            WS = Robot[2]
            RobotinStorage_WS4.pop(0)
            Robot[3] = earliest
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            WS4Delay[1].append(Move23[2])
            WS4Delay[2].append(Move23[3])
            Robot[1] = ArrivalAtWS
            MovingMove23_WS4.append(Robot)
    if  t >= WS4IncomingJobArrivalTime:
        WS_4Jobs.append(WS4IncomingJobArrivalTime)
        AmountOfJobsArrived += 1
        seconds = 1/(ArrivalRate/60/60)
        NextArrival = random.expovariate(1/seconds)
        ArrivalTime = t + NextArrival
        WS4IncomingJobArrivalTime = ArrivalTime
    if len(MovingMove23_WS4) > 0:
        for i in MovingMove23_WS4:
            ArrivalTime = i[1]
            if t >= ArrivalTime:
                AddingEvent = i
                MovingMove23_WS4.remove(i)
                Robots_WS4.append(AddingEvent)
    if len(Robots_WS4) > 0:
        if t >= StartServiceNext_WS4: # starts the service of a new job at WS
            CurrentEvent = Robots_WS4[0]
            WS = CurrentEvent[2]
            QueueWaitingTime_WS4 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS4.append(QueueWaitingTime_WS4)
            TimesStartedService_WS4.append(t)
            Robots_WS4.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS4 = t + PickingTime
            TimeJobFinished_WS4.append(StartServiceNext_WS4)
            AmountofJobsFinished_WS4.append(1)
            WS4picking.append(PickingTime)
            
            Move1= Move1ToStorageScheduleArrival(PodMatrix, WS,t)
            WS4Delay[0].append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS4JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS4.append(CurrentEvent)
    ######
    if len(MovingMove1_WS5) > 0:
        for i in MovingMove1_WS5:
            ArrivalTime = i[1]
            if t >= ArrivalTime: #schedule the arrival of the pods to storage
                AddingEvent = i
                indexnumber = MovingMove1_WS5.index(i)
                MovingMove1_WS5.remove(i)
                RobotinStorage_WS5.append(AddingEvent)
    if len(RobotinStorage_WS5) > 0:    
        if len(WS_5Jobs) > 0:
            earliest = min(WS_5Jobs)
            WS_5Jobs.remove(earliest)
            Robot = RobotinStorage_WS5[0]
            WS = Robot[2]
            RobotinStorage_WS5.pop(0)
            Robot[3] = earliest
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            WS5Delay[1].append(Move23[2])
            WS5Delay[2].append(Move23[3])
            Robot[1] = ArrivalAtWS
            MovingMove23_WS5.append(Robot)
    if  t >= WS5IncomingJobArrivalTime:
        WS_5Jobs.append(WS5IncomingJobArrivalTime)
        AmountOfJobsArrived += 1
        seconds = 1/(ArrivalRate/60/60)
        NextArrival = random.expovariate(1/seconds)
        ArrivalTime = t + NextArrival
        WS5IncomingJobArrivalTime = ArrivalTime
    if len(MovingMove23_WS5) > 0:
        for i in MovingMove23_WS5:
            ArrivalTime = i[1]
            if t >= ArrivalTime:
                AddingEvent = i
                MovingMove23_WS5.remove(i)
                Robots_WS5.append(AddingEvent)
    if len(Robots_WS5) > 0:
        if t >= StartServiceNext_WS5: # starts the service of a new job at WS
            CurrentEvent = Robots_WS5[0]
            WS = CurrentEvent[2]
            QueueWaitingTime_WS5 = t - CurrentEvent[1] 
            TimeWaitedInQueue_WS5.append(QueueWaitingTime_WS5)
            TimesStartedService_WS5.append(t)
            Robots_WS5.pop(0)
            PickingTime = random.expovariate(1/15)
            StartServiceNext_WS5 = t + PickingTime
            TimeJobFinished_WS5.append(StartServiceNext_WS5)
            AmountofJobsFinished_WS5.append(1)
            WS5picking.append(PickingTime)
            
            Move1= Move1ToStorageScheduleArrival(PodMatrix, WS,t)
            WS5Delay[0].append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS5JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS5.append(CurrentEvent)
    
    LengthBufferQueue[0].append(len(WS_1Jobs))
    LengthBufferQueue[1].append(len(WS_2Jobs))
    LengthBufferQueue[2].append(len(WS_3Jobs))
    LengthBufferQueue[3].append(len(WS_4Jobs))
    LengthBufferQueue[4].append(len(WS_5Jobs))
    t = t+1

# In order to eliminate the warm up effect
n = 30

del TimeWaitedInQueue_WS1[:n]
del TimesStartedService_WS1[:n]
del TimeJobFinished_WS1[:n]
del AmountofJobsFinished_WS1[:n]
del OrderCycleTime_WS1[:n]

del TimeWaitedInQueue_WS2[:n]
del TimesStartedService_WS2[:n]
del TimeJobFinished_WS2[:n]
del AmountofJobsFinished_WS2[:n]
del OrderCycleTime_WS2[:n]

del TimeWaitedInQueue_WS3[:n]
del TimesStartedService_WS3[:n]
del TimeJobFinished_WS3[:n]
del AmountofJobsFinished_WS3[:n]
del OrderCycleTime_WS3[:n]

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



UtilizationWS1 = sum(WS1picking)/T
UtilizationWS2 = sum(WS2picking)/T
UtilizationWS3 = sum(WS3picking)/T
UtilizationWS4 = sum(WS4picking)/T
UtilizationWS5 = sum(WS5picking)/T


Lo1 = sum(LengthBufferQueue[0])/len(LengthBufferQueue[0])
Lo2 = sum(LengthBufferQueue[1])/len(LengthBufferQueue[1])
Lo3 = sum(LengthBufferQueue[2])/len(LengthBufferQueue[2])
Lo4 = sum(LengthBufferQueue[3])/len(LengthBufferQueue[3])
Lo5 = sum(LengthBufferQueue[4])/len(LengthBufferQueue[4])

print('#####Workstation 1:######')
AverageWaitingTime1 = sum(TimeWaitedInQueue_WS1)/(max(len(TimeWaitedInQueue_WS1),1))
print('Average Waiting Time in Queue (s) :', round(AverageWaitingTime1,2))
AverageThroughputRate1 = (sum(AmountofJobsFinished_WS1)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',round(AverageThroughputRate1,2))    
AverageOrderCycleTime1 = sum(WS1JobCycle)/(len(WS1JobCycle))
print('Toc (Average order cycle time  (s)):', round(AverageOrderCycleTime1,2))
print('Lo (mean length external order queue):', round(Lo1,2))
print('Pws (Workstation Utilization):', round(UtilizationWS1,2))
print('')
print('#####Workstation 2:######')
AverageWaitingTime2 = sum(TimeWaitedInQueue_WS2)/(max(len(TimeWaitedInQueue_WS2),1))
print('Average Waiting Time in Queue (s) :', round(AverageWaitingTime2,2))
AverageThroughputRate2 = (sum(AmountofJobsFinished_WS2)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',round(AverageThroughputRate2,2))   
AverageOrderCycleTime2 = sum(WS2JobCycle)/(len(WS2JobCycle))
print('Toc (Average order cycle time (s)):', round(AverageOrderCycleTime2,2))
print('Lo (mean length external order queue):', round(Lo2,2))
print('Pws (Workstation Utilization):', round(UtilizationWS2,2))
print('')
print('#####Workstation 3:######')
AverageWaitingTime3 = sum(TimeWaitedInQueue_WS3)/(max(len(TimeWaitedInQueue_WS3),1))
print('Average Waiting Time in Queue (s) :', round(AverageWaitingTime3,2))
AverageThroughputRate3 = (sum(AmountofJobsFinished_WS3)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',round(AverageThroughputRate3,2))   
AverageOrderCycleTime3 = sum(WS3JobCycle)/(len(WS3JobCycle))
print('Toc (Average order cycle time (s)):', round(AverageOrderCycleTime3,2))
print('Lo (mean length external order queue):', round(Lo3,2))
print('Pws (Workstation Utilization):', round(UtilizationWS3,2))
print('')
print('#####Workstation 4:######')
AverageWaitingTime4 = sum(TimeWaitedInQueue_WS4)/(max(len(TimeWaitedInQueue_WS4),1))
print('Average Waiting Time in Queue (s) :', round(AverageWaitingTime4,2))
AverageThroughputRate4 = (sum(AmountofJobsFinished_WS4)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',round(AverageThroughputRate4,2))   
AverageOrderCycleTime4 = sum(WS4JobCycle)/(len(WS4JobCycle))
print('Toc (Average order cycle time (s)):', round(AverageOrderCycleTime4,2))
print('Lo (mean length external order queue):', round(Lo4,2))
print('Pws (Workstation Utilization):', round(UtilizationWS4,2))
print('')
print('#####Workstation 5:######')
AverageWaitingTime5 = sum(TimeWaitedInQueue_WS5)/(max(len(TimeWaitedInQueue_WS5),1))
print('Average Waiting Time in Queue (s) :', round(AverageWaitingTime5,2))
AverageThroughputRate5 = (sum(AmountofJobsFinished_WS5)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',round(AverageThroughputRate5,2))   
AverageOrderCycleTime5 = sum(WS5JobCycle)/(len(WS5JobCycle))
print('Toc (Average order cycle time (s)):', round(AverageOrderCycleTime5,2))
print('Lo (mean length external order queue):', round(Lo5,2))
print('Pws (Workstation Utilization):', round(UtilizationWS5,2))


def AverageDelayTimes(WS):
    workstation = {1:WS1DelayDistances}
    distancelist = workstation[WS]
    Move1list = distancelist[0]
    AverageMove1Time = (sum(Move1list)/len(Move1list))/1.3
    AverageMove2Time = (sum(Move2list)/len(Move2list))/1.3
    Move3list = distancelist[2]
    AverageMove3Time = (sum(Move3list)/len(Move3list))/1.3
    return AverageMove1Time, AverageMove2Time, AverageMove3Time


titles = ['Av. Waiting Time', 'Av. Throughput Rate', 'Av. To', 'Lo', 'Av. Pwc']
pdWS1 = [round(AverageWaitingTime1,2),round(AverageThroughputRate1,2), round(AverageOrderCycleTime1,2),round(Lo1,2), round(UtilizationWS1,2)]
pdWS2 = [round(AverageWaitingTime2,2),round(AverageThroughputRate2,2), round(AverageOrderCycleTime2,2),round(Lo2,2), round(UtilizationWS2,2)]
pdWS3 = [round(AverageWaitingTime3,2),round(AverageThroughputRate3,2), round(AverageOrderCycleTime3,2),round(Lo3,2), round(UtilizationWS3,2)]
pdWS4 = [round(AverageWaitingTime4,2),round(AverageThroughputRate4,2), round(AverageOrderCycleTime4,2),round(Lo4,2), round(UtilizationWS4,2)]
pdWS5 = [round(AverageWaitingTime5,2),round(AverageThroughputRate5,2), round(AverageOrderCycleTime5,2),round(Lo5,2), round(UtilizationWS5,2)]

AverageWT = round((AverageWaitingTime1 + AverageWaitingTime2 + AverageWaitingTime3 + AverageWaitingTime4 + AverageWaitingTime5)/5,2)
AverageTH = round((AverageThroughputRate1+AverageThroughputRate2+AverageThroughputRate3+AverageThroughputRate4+AverageThroughputRate5)/5,2)
AverageCT = round((AverageOrderCycleTime1+AverageOrderCycleTime2+AverageOrderCycleTime3+AverageOrderCycleTime4+AverageOrderCycleTime5)/5,2)
AverageLo = round((Lo1+Lo2+Lo3+Lo4+Lo5)/5,2)
AveragePws = round((UtilizationWS1+UtilizationWS2+UtilizationWS3+UtilizationWS4+UtilizationWS5)/5,2)

avWS = [AverageWT, AverageTH, AverageCT, AverageLo, AveragePws]
A_Results = pd.DataFrame({'PM': titles, 'WS1': pdWS1, 'WS2': pdWS2, 'WS3': pdWS3, 'WS4': pdWS4,'WS5': pdWS5, 'Average': avWS})

A_Results = A_Results.set_index('PM')
#Col1 = ['Av. Waiting Time', 'Av. Throughput Rate']

#col2 = [5, 4]

#Results[0] = Col1
#Results[2] = col2

#Results.set_index('Av. Waiting Time')

#Times1= AverageDelayTimes(1)


#AverageD1 = (Times1[0] + Times2[0] + Times3[0] + Times4[0] + Times5[0])/5


#lent = sum(LengthBufferQueue)/len(LengthBufferQueue)

#print('Workstation Utlizations:',
#      'WS1:',round(UtilizationWS1,2))
#plt.plot(TimesStartedService,TimeWaitedInQueue)
#plt.xlabel('Time')
#plt.ylabel('Time Waited in Queue')

#plt.plot(TimesStartedService,OrderCycleTime)
#plt.xlabel('Time')
#plt.ylabel('OrderCycleTime (s)')# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-

