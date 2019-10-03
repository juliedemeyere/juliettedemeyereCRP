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

N = 168 # amount of hours. Needs to be greater than 1 for warm up effect
T = 60*60*N # amount of time that the simulation is kept running, in seconds

t = 0

#robots = (['Robot1', 0], ['Robot2', 0], ['Robot3', 0], ['Robot4', 0], ['Robot5', 0], ['Robot6', 0], ['Robot7', 0], ['Robot8', 0], ['Robot9', 0], ['Robot10', 0], ['Robot11', 0], ['Robot12', 0], ['Robot13', 0], ['Robot14', 0])

robots = ('Robot 1', 'Robot 2', 'Robot 3', 'Robot 4', 'Robot 5', 'Robot 6', 'Robot 7', 'Robot 8', 'Robot 9', 'Robot 10', 'Robot 11', 'Robot 12', 'Robot 13', 'Robot 14')
F = 2 # Specify here the amount of robots per workstation to initialize [robot number, arrival at workstation]
ArrivalRate = 31.68 # arrivalrate per hour

LengthBufferQueue = []

WS1DelayDistances = [[],[],[]]
Robots_WS1 = []

for i in range(0,F): #[robot#, arrivalat WS, WS, arrivalofjob, storagelocation x, storagelocation y]
    z1 = [robots[i], 0, 1, 0, 0, 0]
    Robots_WS1.append(z1)


TimeWaitedInQueue_WS1 =[]
TimesStartedService_WS1 = []
TimeJobFinished_WS1 = []
AmountofJobsFinished_WS1 = []
OrderCycleTime_WS1 = []

WS1picking = []

Xlength = 90
Ylength = 37
crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections
aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections

WS_Xlocation = {1:0, 2:17, 3:46, 4:74, 5:90}
WS_Ylocation = {1:19, 2:0, 3:0, 4:0, 5:20}
WS_direction = {1:'West',2:'South', 3:'South',4:'South', 5:'East'}

Delays1WS1 = []
Delays2WS1 = []
Delays3WS1 = []

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
  #  print(Times)
    Time = sum(Times)
    ArrivalTime = Time + t
    #print(ArrivalTime - t)
    return ArrivalTime, PodMatrix, Times[0], Times[1]
    
MovingMove1_WS1 = []
RobotinStorage_WS1 = []

MovingMove23_WS1 = []

Workfloor = PodMatrixClass()
probability = 85

Workfloor.PodMatrixGenerator(probability) # generates a new podmatrix

PodMatrix = Workfloor.Matrix

WS_1Jobs= [] # arrival times of the jobs awaiting service


WS1IncomingJobArrivalTime = 0

def JobScheduler(ArrivalRate, t):
    seconds = 1/(ArrivalRate/60/60)
    NextArrival = random.expovariate(1/seconds)
    ArrivalTime = t + NextArrival
    print(NextArrival,'ArrivalTime:', ArrivalTime)
    return ArrivalTime
    
AmountOfJobsArrived = 0    
StartServiceNext_WS1 = 0 # Initialize the service start at WS

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
            Robot[3] = earliest # denote the arrival time of the job in the system
            Move23 = Move2Move3DelayTime(PodMatrix, WS,t, Robot[4], Robot[5])
            ArrivalAtWS = Move23[0]
            Delays2WS1.append(Move23[2])
            Delays3WS1.append(Move23[3])
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
            Delays1WS1.append(Move1[4])
            CurrentEvent[4] = Move1[1]
            CurrentEvent[5] = Move1[2]
            ArrivalTimeStorage = Move1[0]
            
            CurrentEvent[1] = ArrivalTimeStorage
            
            OrderCycle = t + PickingTime - CurrentEvent[3]
            WS1JobCycle.append(OrderCycle)
            CurrentEvent[3] = 0
            MovingMove1_WS1.append(CurrentEvent)
    LengthBufferQueue.append(len(WS_1Jobs))
    t = t+1

# In order to eliminate the warm up effect
n = 30

del TimeWaitedInQueue_WS1[:n]
del TimesStartedService_WS1[:n]
del TimeJobFinished_WS1[:n]
del AmountofJobsFinished_WS1[:n]
del OrderCycleTime_WS1[:n]

print('##Workstation 1:##')
AverageWaitingTime1 = sum(TimeWaitedInQueue_WS1)/(max(len(TimeWaitedInQueue_WS1),1))
print('Average Waiting Time in Queue (s) :', AverageWaitingTime1)
#Time = (T-30)*60*60
AverageThroughputRate1 = (sum(AmountofJobsFinished_WS1)/(T - 30))*60*60
print('Average Throughput Rate (/hour):',AverageThroughputRate1)    
AverageOrderCycleTime1 = sum(WS1JobCycle)/(len(WS1JobCycle))
print('Average order cycle time (s):', AverageOrderCycleTime1)


def AverageDelayTimes(WS):
    workstation = {1:WS1DelayDistances}
    distancelist = workstation[WS]
    Move1list = distancelist[0]
    AverageMove1Time = (sum(Move1list)/len(Move1list))/1.3
    AverageMove2Time = (sum(Move2list)/len(Move2list))/1.3
    Move3list = distancelist[2]
    AverageMove3Time = (sum(Move3list)/len(Move3list))/1.3
    return AverageMove1Time, AverageMove2Time, AverageMove3Time

#Times1= AverageDelayTimes(1)


#AverageD1 = (Times1[0] + Times2[0] + Times3[0] + Times4[0] + Times5[0])/5
UtilizationWS1 = sum(WS1picking)/T

lent = sum(LengthBufferQueue)/len(LengthBufferQueue)

print('Workstation Utlizations:',
      'WS1:',round(UtilizationWS1,2))
#plt.plot(TimesStartedService,TimeWaitedInQueue)
#plt.xlabel('Time')
#plt.ylabel('Time Waited in Queue')

#plt.plot(TimesStartedService,OrderCycleTime)
#plt.xlabel('Time')
#plt.ylabel('OrderCycleTime (s)')# -*- coding: utf-8 -*-

