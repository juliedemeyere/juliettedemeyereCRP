#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 13:07:58 2019

@author: juliedemeyere
"""

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
from function import cox
from function import coxMean
from MatrixFile import PodMatrixClass
from collections import deque # Use deque because it is really fast
import random
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import sem, t
from scipy import mean

"The purpose of this simulation is to be run multiple times in order to generate a confidence interval"

"Start the Simulation by altering how many hours it should be run for (N)"
"and by altering which table number from the Paper should be mimicked "
"(in terms of number of robots and arrival rate)"
def RunSimulation(TableNumber, nrRuns, k, b1):
    N =  1# amount of hours. Needs to be greater than 1 for warm up effect
    T = 60*60*N # amount of time that the simulation is kept running, in seconds
    "Closedloop and general delay below can be switched on and off to simulate different aspects, as described below"
    closedloop = 1 # if the simulation should simulate a closed loop then put 1
    generaldelay = 0 # this switch can be turned on if using the average delay times instead of the simulation of the movement of the pod locations
    t = 0
    mu = 15
  #  TableNumber = 2 # write in the table from the paper you want to replicate
    if TableNumber == 2:
        F = 2
        ArrivalRate = 31.68
    elif TableNumber == 3:
        F = 2
        ArrivalRate = 14.40
    elif TableNumber == 4:
        F = 8
        ArrivalRate = 126.72
    elif TableNumber == 5:
        F = 8
        ArrivalRate = 57.60
    elif TableNumber == 6:
        F = 14
        ArrivalRate = 221.76
    elif TableNumber == 7:
        F = 14
        ArrivalRate = 100.80
    
    
    Xlength = 89
    Ylength = 36
    crossaisles = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84] # relevant for x intersections
    aisles = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35] # relevant for y intersections
    
    "Initialize the Locations of the WorkStations"
    WS_Xlocation = {1:0, 2:17, 3:46, 4:74, 5:90}
    WS_Ylocation = {1:19, 2:0, 3:0, 4:0, 5:20}
    WS_direction = {1:'West',2:'South', 3:'South',4:'South', 5:'East'}
    
    "Initialize the Pod location matrix on the workfloor"
    Workfloor = PodMatrixClass()
    probability = 85
    
    Workfloor.PodMatrixGenerator(probability) # generates a new podmatrix
    
    PodMatrix = Workfloor.Matrix
    
    
    def Move1ToStorageScheduleArrival(WS,t, generaldelay):
        if generaldelay == 0:
            PodMatrix = Workfloor.Matrix
            x = WS_Xlocation[WS]
            y = WS_Ylocation[WS]
            location = WS_direction[WS]
            Move1 = DistanceCalculator_Move1(x,y, location, PodMatrix)
            Workfloor.MakeOne(Move1[1],Move1[2])
            TravelTime = (Move1[0]+1)/1.3
            ArrivalTime = TravelTime + t
        else:
            TravelTime = np.random.exponential(44.1)
            ArrivalTime = TravelTime + t
            Move1 = [0,0,0]
        return ArrivalTime, Move1[1], Move1[2], 'nothing', TravelTime
    
    def Move2Move3DelayTime(WS,t, x2, y2, generaldelay):
        if generaldelay == 0:
            PodMatrix = Workfloor.Matrix
            x = WS_Xlocation[WS]
            y = WS_Ylocation[WS]
            location = WS_direction[WS]
            Move3 = DistanceCalculator_Move3(x,y, location, PodMatrix)
            Workfloor.MakeZero(Move3[1],Move3[2])
            Move2 = DistanceCalculator_Move2(x2,y2, Move3[1], Move3[2])
            Times = CalculateTravelTime(Move2, Move3)
            Time = sum(Times)
            ArrivalTime = Time + t
        else:
            TravelTime = np.random.exponential(33.13) + np.random.exponential(45.2)
            ArrivalTime = TravelTime + t
            Times = [33.13,45.2]
        return ArrivalTime, 'nothing', Times[0], Times[1]
    
    "Initialize the first robots, all located at the WorkStation"
    robots = ('Robot 1', 'Robot 2', 'Robot 3', 'Robot 4', 'Robot 5', 'Robot 6', 'Robot 7', 'Robot 8', 'Robot 9', 'Robot 10', 'Robot 11', 'Robot 12', 'Robot 13', 'Robot 14')
    Robots_at_WS = {1:[],2:[],3:[],4:[],5:[]}
    for i in range(0,F): #[robot#, arrivalat WS, WS, arrivalofjob, storagelocation x, storagelocation y]
        z1 = [robots[i], 0, 1, 0, 0, 0]
        Robots_at_WS[1].append(z1)
        z2 = [robots[i], 0, 2, 0, 0, 0]
        Robots_at_WS[2].append(z2)
        z3 = [robots[i], 0, 3, 0, 0, 0]
        Robots_at_WS[3].append(z3)
        z4 = [robots[i], 0, 4, 0, 0, 0]
        Robots_at_WS[4].append(z4)
        z5 = [robots[i], 0, 5, 0, 0, 0]
        Robots_at_WS[5].append(z5)
       
    "Initialization lists and values"
    JobCycle = {1:[],2:[],3:[],4:[],5:[]}
    WSDelay = {1:[[],[],[]],2:[[],[],[]],3:[[],[],[]],4:[[],[],[]],5:[[],[],[]]}
    MovingMove1 = {1:[],2:[],3:[],4:[],5:[]}
    RobotinStorage = {1:[],2:[],3:[],4:[],5:[]}
    MovingMove23 ={1:[],2:[],3:[],4:[],5:[]}
    Jobs_at_SyncStation = {1:[],2:[],3:[],4:[],5:[]} # used to be WS_1Jobs, arrival times of the jobs awaiting service
    TimeWaitedInQueue = {1:[],2:[],3:[],4:[],5:[]}
    TimesStartedService = {1:[],2:[],3:[],4:[],5:[]}
    TimeJobFinished = {1:[],2:[],3:[],4:[],5:[]}
    AmountofJobsFinished = {1:[],2:[],3:[],4:[],5:[]}
    PickingTimes = {1:[],2:[],3:[],4:[],5:[]} # used to be WS1picking
    IncomingJobArrivalTime = {1:0,2:0,3:0,4:0,5:0} # used to be WS2IncomingJobArrivalTime 
    AmountOfJobsArrived = 0    
    StartServiceNextJobAtWS = {1:0,2:0,3:0,4:0,5:0} # Initialize the service start at WS, used to be StartServiceNext_WS1
    LengthQueue_at_WS = {1:[],2:[],3:[],4:[],5:[]} # used to be QueueWS1
    LengthBufferQueue = {1:[],2:[],3:[],4:[],5:[]}
    
    "Will run for t amount of time and repeat the code every second"
    while t < T:
        for WS in range(1,6):
            "Schedules the arrival of new jobs at the synchronization station"
            if closedloop == 0:
                if  t >= IncomingJobArrivalTime[WS]: # jobscheduler
                    Jobs_at_SyncStation[WS].append(IncomingJobArrivalTime[WS])
                    AmountOfJobsArrived += 1
                    seconds = 1/(ArrivalRate/60/60)
                    NextArrivalJob = np.random.exponential(seconds)
                    ArrivalTime_NewJob = t + NextArrivalJob
                    IncomingJobArrivalTime[WS] = ArrivalTime_NewJob
            "Stores the Robot into the arrival location when it has reached its arrival time"
            if len(MovingMove1[WS]) > 0:
                for i in MovingMove1[WS]:
                    ArrivalTime_RobotAtStorage = i[1]
                    if t >= ArrivalTime_RobotAtStorage: #schedule the arrival of the pods to storage
                        AddingEvent_ArrivalAtStorage = i
                        #indexnumber = MovingMove1[WS].index(i)
                        MovingMove1[WS].remove(i)
                        RobotinStorage[WS].append(AddingEvent_ArrivalAtStorage)
            
            "Assigns a job to a robot if there is a robot at the storage location as well as a job at the SyncStation"          
            if len(RobotinStorage[WS]) > 0:    
                if len(Jobs_at_SyncStation[WS]) > 0 or closedloop == 1:
                    if closedloop == 0:
                        earliest = min(Jobs_at_SyncStation[WS])
                        Jobs_at_SyncStation[WS].remove(earliest)
                    else:
                        earliest = t
                    #Jobs_at_SyncStation[WS].remove(earliest)
                    Robot_StartsMove23 = RobotinStorage[WS][0]
                    WS = Robot_StartsMove23[2]
                    RobotinStorage[WS].pop(0)
                    Robot_StartsMove23[3] = earliest
                    Move23 = Move2Move3DelayTime(WS,t, Robot_StartsMove23[4], Robot_StartsMove23[5], generaldelay)
                    ArrivalAtWS = Move23[0]
                    WSDelay[WS][1].append(Move23[2])
                    WSDelay[WS][2].append(Move23[3])
                    Robot_StartsMove23[1] = ArrivalAtWS
                    MovingMove23[WS].append(Robot_StartsMove23)
                    
            "Places robots at the workstation when it has finished moves 2 and move 3"
            if len(MovingMove23[WS]) > 0:
                for i in MovingMove23[WS]:
                    ArrivalTime_RobotAtWS = i[1]
                    if t >= ArrivalTime_RobotAtWS:
                        AddingEvent_RobotAtWS = i
                        MovingMove23[WS].remove(i)
                        Robots_at_WS[WS].append(AddingEvent_RobotAtWS)
        
            "Carries out and schedules the service of the picking at the workstation and sends the finished job off on Move 1"
            if len(Robots_at_WS[WS]) > 0:
                if t >= StartServiceNextJobAtWS[WS]: # starts the service of a new job at WS
                    Robot_ServiceAtWS = Robots_at_WS[WS][0]
                    WS = Robot_ServiceAtWS[2]
                    QueueWaitingTime = t - Robot_ServiceAtWS[1] 
                    TimeWaitedInQueue[WS].append(QueueWaitingTime)
                    TimesStartedService[WS].append(t)
                    Robots_at_WS[WS].pop(0)
                    #PickingTime = random.expovariate(1/15)
                    #PickingTime = cox(b1,k,mu)
                    PickingTime = coxMean(b1,k,15)
                    #PickingTime = np.random.exponential(15)
                    
                    StartServiceNextJobAtWS[WS] = t + PickingTime
                    TimeJobFinished[WS].append(StartServiceNextJobAtWS[WS])
                    AmountofJobsFinished[WS].append(1)
                    PickingTimes[WS].append(PickingTime)
                    
                    Move1= Move1ToStorageScheduleArrival(WS,StartServiceNextJobAtWS[WS], generaldelay)
                    WSDelay[WS][0].append(Move1[4])
                    Robot_ServiceAtWS[4] = Move1[1]
                    Robot_ServiceAtWS[5] = Move1[2]
                    ArrivalTimeStorage = Move1[0]
                    
                    Robot_ServiceAtWS[1] = ArrivalTimeStorage
                    
                    OrderCycle = t + PickingTime - Robot_ServiceAtWS[3]
                    JobCycle[WS].append(OrderCycle)
                    Robot_ServiceAtWS[3] = 0
                    MovingMove1[WS].append(Robot_ServiceAtWS)
                    
         
            LengthBufferQueue[WS].append(len(Jobs_at_SyncStation[WS]))
            LengthQueue_at_WS[WS].append(len(Robots_at_WS[WS]))
    
        t = t+1
    
    
    
    
    
    
    
    
    "The lists and values below are created in order to record the performance measurements"
    UtilizationWS = {1:sum(PickingTimes[1])/T,2:sum(PickingTimes[2])/T,3:sum(PickingTimes[3])/T,4:sum(PickingTimes[4])/T,5:sum(PickingTimes[5])/T}
    
    
    Lo1 = sum(LengthBufferQueue[1])/max(len(LengthBufferQueue[1]),1)
    Lo2 = sum(LengthBufferQueue[2])/max(len(LengthBufferQueue[2]),1)
    Lo3 = sum(LengthBufferQueue[3])/max(len(LengthBufferQueue[3]),1)
    Lo4 = sum(LengthBufferQueue[4])/max(len(LengthBufferQueue[4]),1)
    Lo5 = sum(LengthBufferQueue[5])/max(len(LengthBufferQueue[5]),1)
    
    
    WS1RobotAverageBusyTimes = (sum(WSDelay[1][0]) + sum(WSDelay[1][1]) + sum(WSDelay[1][2]) + sum(PickingTimes[1]) + sum(TimeWaitedInQueue[1]))/F
    WS2RobotAverageBusyTimes = (sum(WSDelay[2][0]) + sum(WSDelay[2][1]) + sum(WSDelay[2][2]) + sum(PickingTimes[2]) + sum(TimeWaitedInQueue[2]))/F
    WS3RobotAverageBusyTimes = (sum(WSDelay[3][0]) + sum(WSDelay[3][1]) + sum(WSDelay[3][2]) + sum(PickingTimes[3]) + sum(TimeWaitedInQueue[3]))/F
    WS4RobotAverageBusyTimes = (sum(WSDelay[4][0]) + sum(WSDelay[4][1]) + sum(WSDelay[4][2]) + sum(PickingTimes[4]) + sum(TimeWaitedInQueue[4]))/F
    WS5RobotAverageBusyTimes = (sum(WSDelay[5][0]) + sum(WSDelay[5][1]) + sum(WSDelay[5][2]) + sum(PickingTimes[5]) + sum(TimeWaitedInQueue[5]))/F
    
    WS1RobotBusy = WS1RobotAverageBusyTimes/T
    WS2RobotBusy = WS2RobotAverageBusyTimes/T
    WS3RobotBusy = WS3RobotAverageBusyTimes/T
    WS4RobotBusy = WS4RobotAverageBusyTimes/T
    WS5RobotBusy = WS5RobotAverageBusyTimes/T
    
    avBusy = round((WS1RobotBusy + WS2RobotBusy+WS3RobotBusy+WS4RobotBusy + WS5RobotBusy)/5,2)
    
    AverageWaitingTimes = []
    AverageThroughPutRate = []
    AverageOrderCycleTime = []
    AverageExternalOrder = []
    Utilization = []
    for i in range(1,6):
        AvWaitingTime = round(sum(TimeWaitedInQueue[i])/max(len(TimeWaitedInQueue[i]),1),2)
        AverageWaitingTimes.append(AvWaitingTime)
        AvTH = round((sum(AmountofJobsFinished[i])/T)*60*60,2)
        AverageThroughPutRate.append(AvTH)
        AvCT = round(sum(JobCycle[i])/max(len(JobCycle[i]),1),2)
        AverageOrderCycleTime.append(AvCT)
        AvLo = round(sum(LengthBufferQueue[i])/max(len(LengthBufferQueue[i]),1),2)
        AverageExternalOrder.append(AvLo)
        Ut = sum(PickingTimes[i])/T
        Utilization.append(Ut)
  #  print(AverageThroughPutRate)
    Th1 = AverageThroughPutRate[0]
    Th2 = AverageThroughPutRate[1]
    Th3 = AverageThroughPutRate[2]
    Th4 = AverageThroughPutRate[3]
    Th5 = AverageThroughPutRate[4]
    TotalThroughPut = sum(AverageThroughPutRate)
    if TableNumber == 2:
        B= 206.1
        C= 0.52
        D= 0.13
        E= 0.64
        PaperTotalThroughPut = 245.1
    elif TableNumber == 3:
        B= 154.4
        C= 0.03
        D= 0.06
        E= 0.29
        PaperTotalThroughPut = 245.1
    elif TableNumber == 4:
        B= 173.3
        C= 0.51
        D= 0.53
        E= 0.69
        PaperTotalThroughPut = 871.6
    elif TableNumber == 5:
        B= 150.4
        C= 0.00
        D= 0.24
        E= 0.30
        PaperTotalThroughPut = 871.6
    elif TableNumber == 6:
        B= 412.7 
        C= 12.63
        D= 0.92
        E= 0.91
        PaperTotalThroughPut = 1165.2
    elif TableNumber == 7:
        B= 156.6
        C= 0
        D= 0.42
        E= 0.31
        PaperTotalThroughPut = 1165.2
    Comparison = ['NA', 'NA', B, C, D, E]
    comparedtotitle = 'Sim. Results Table' + str(TableNumber)
    
    titles = ['Av. Waiting Time', 'Av. Throughput Rate', 'Av. To', 'Lo', 'Pwc', 'Pr']
    
    Workstations = ['WS1', 'WS2','WS3','WS4','WS5', 'Average', 'PAPER Results Table' + str(TableNumber)]
    AverageWT = round((sum(AverageWaitingTimes)/len(AverageWaitingTimes)),2)
    AverageTH = round((sum(AverageThroughPutRate)/len(AverageThroughPutRate)),2)
    AverageCT = round((sum(AverageOrderCycleTime)/len(AverageOrderCycleTime)),2)
    AverageLo = round((sum(AverageExternalOrder)/len(AverageExternalOrder)),2)
    AveragePws = round((sum(Utilization)/len(Utilization)),2)
    
    AverageWaitingTimes.append(AverageWT)
    AverageWaitingTimes.append(Comparison[0])
    AverageThroughPutRate.append(AverageTH)
    AverageThroughPutRate.append(Comparison[1])
    AverageOrderCycleTime.append(AverageCT)
    AverageOrderCycleTime.append(Comparison[2])
    AverageExternalOrder.append(AverageLo)
    AverageExternalOrder.append(Comparison[3])
    Utilization.append(AveragePws)
    Utilization.append(Comparison[4])
    Pr = [WS1RobotBusy, WS2RobotBusy, WS3RobotBusy, WS4RobotBusy, WS5RobotBusy, avBusy,Comparison[5]]
    A_PerformanceMeasurements = pd.DataFrame({'Workstations':Workstations, 'WaitingTime WS Queue': AverageWaitingTimes, 'Throughput (/h)':AverageThroughPutRate,
                               'Cycle Time (s)':AverageOrderCycleTime, 'Lo':AverageExternalOrder, 'Pwc':Utilization, 'Pr':Pr})
    
    DWS1 = sum(WSDelay[1][0])/(len(WSDelay[1][0]))+sum(WSDelay[1][1])/(len(WSDelay[1][1])) + sum(WSDelay[1][2])/(len(WSDelay[1][2]))
    DWS2 = sum(WSDelay[2][0])/(len(WSDelay[2][0]))+sum(WSDelay[2][1])/(len(WSDelay[2][1])) + sum(WSDelay[2][2])/(len(WSDelay[2][2]))
    DWS3 = sum(WSDelay[3][0])/(len(WSDelay[3][0]))+sum(WSDelay[3][1])/(len(WSDelay[3][1])) + sum(WSDelay[3][2])/(len(WSDelay[3][2]))
    DWS4 = sum(WSDelay[4][0])/(len(WSDelay[4][0]))+sum(WSDelay[4][1])/(len(WSDelay[4][1])) + sum(WSDelay[4][2])/(len(WSDelay[4][2]))
    DWS5 = sum(WSDelay[5][0])/(len(WSDelay[5][0]))+sum(WSDelay[5][1])/(len(WSDelay[5][1])) + sum(WSDelay[5][2])/(len(WSDelay[5][2]))
  
    
    
   # print(sum(WSDelay[1][0])/(len(WSDelay[1][0]))+sum(WSDelay[1][1])/(len(WSDelay[1][1])) + sum(WSDelay[1][2])/(len(WSDelay[1][2])))
    
    
    AvDelayMove1 = (sum(WSDelay[1][0]) + sum(WSDelay[2][0]) + sum(WSDelay[3][0]) + sum(WSDelay[4][0]) + sum(WSDelay[5][0]))/(len(WSDelay[1][0]) + len(WSDelay[2][0]) +len(WSDelay[3][0]) + len(WSDelay[4][0]) + len(WSDelay[5][0]))

    AvDelayMove2 = (sum(WSDelay[1][1]) + sum(WSDelay[2][1]) + sum(WSDelay[3][1]) + sum(WSDelay[4][1]) + sum(WSDelay[5][1]))/(len(WSDelay[1][1]) + len(WSDelay[2][1]) +len(WSDelay[3][1]) + len(WSDelay[4][1]) + len(WSDelay[5][1]))

    AvDelayMove3 = (sum(WSDelay[1][2]) + sum(WSDelay[2][2]) + sum(WSDelay[3][2]) + sum(WSDelay[4][2]) + sum(WSDelay[5][2]))/(len(WSDelay[1][2]) + len(WSDelay[2][2]) +len(WSDelay[3][2]) + len(WSDelay[4][2]) + len(WSDelay[5][2]))
    print('run #', nrRuns, 'completed')
    return Th1, Th2, Th3, Th4, Th5, DWS1, DWS2, DWS3, DWS4, DWS5


def GenerateResults(TableNumber,k, b1):
    nrRuns = 10
    Th1 = []
    Th2 = []
    Th3 = []
    Th4 = []
    Th5 = []
    DWS1 = []
    DWS2 = []
    DWS3 = []
    DWS4 = []
    DWS5 = []
    for i in range(0,nrRuns):
        SimulationResults = RunSimulation(TableNumber, i, k, b1)
        Th1.append(SimulationResults[0])
        Th2.append(SimulationResults[1])
        Th3.append(SimulationResults[2])
        Th4.append(SimulationResults[3])
        Th5.append(SimulationResults[4])
        DWS1.append(SimulationResults[5])
        DWS2.append(SimulationResults[6])
        DWS3.append(SimulationResults[7])
        DWS4.append(SimulationResults[8])
        DWS5.append(SimulationResults[9])
    
    Confidence = 0.95
    n = len(DWS1)
    mD1 = mean(DWS1)
    std_err = sem(DWS1)
    h = std_err * t.ppf((1 + Confidence) / 2, n - 1)
    CI_D1 = (round(mD1-h,2),round(mD1+h,2))
    
    n = len(DWS2)
    mD2 = mean(DWS2)
    std_err = sem(DWS2)
    h = std_err * t.ppf((1 + Confidence) / 2, n - 1)
    CI_D2 = (round(mD2-h,2),round(mD2+h,2))
    
    n = len(DWS3)
    mD3 = mean(DWS3)
    std_err = sem(DWS3)
    h = std_err * t.ppf((1 + Confidence) / 2, n - 1)
    CI_D3 = (round(mD3-h,2),round(mD3+h,2))
    
    n = len(DWS4)
    mD4 = mean(DWS4)
    std_err = sem(DWS4)
    h = std_err * t.ppf((1 + Confidence) / 2, n - 1)
    CI_D4 = (round(mD4-h,2),round(mD4+h,2))
    
    n = len(DWS5)
    mD5 = mean(DWS5)
    std_err = sem(DWS5)
    h = std_err * t.ppf((1 + Confidence) / 2, n - 1)
    CI_D5 = (round(mD5-h,2),round(mD5+h,2))
    
    if TableNumber == 2:
        N = 2
    elif TableNumber == 4:
        N = 8
    else:
        N = 14
    print(N, 'k:', k, 'b:', b1)
    #return mTH, CI_TH, mD1, CI_D1, mD2, CI_D2, mD3, CI_D3, PickingTimes
    return mean(Th1), mean(Th2), mean(Th3), mean(Th4), mean(Th5), mean(DWS1), mean(DWS2), mean(DWS3), mean(DWS4), mean(DWS5), CI_D1, CI_D2, CI_D3, CI_D4, CI_D5



ResultsData = pd.DataFrame(columns=['N', 'k', 'b', 'TH1', 'TH2','TH3', 'TH4','TH5','avDelay1', 'avDelay2','avDelay3', 'avDelay4','avDelay5','CIdelay1','CIdelay2','CIdelay3','CIdelay4','CIdelay5'])
#b1values = [1,0.8,0.6,0]
b1values = [1]
values = [2,3,4,5,10]
for s in range(len(b1values)):
    b = b1values[s]
    for i in range(len(values)):
        print(values[i])
        Re = GenerateResults(2,values[i], b)
        Res = pd.DataFrame([[2, values[i], b, Re[0],Re[1],Re[2],Re[3],Re[4],Re[5],Re[6],Re[7],Re[8],Re[9],Re[10],Re[11], Re[12],Re[13],Re[14]]], columns=['N', 'k', 'b', 'TH1', 'TH2','TH3', 'TH4','TH5','avDelay1', 'avDelay2','avDelay3', 'avDelay4','avDelay5','CIdelay1','CIdelay2','CIdelay3','CIdelay4','CIdelay5'])
        ResultsData = ResultsData.append(Res,ignore_index=True)
    for i in range(len(values)):
        Re = GenerateResults(4,values[i], b)
        Res = pd.DataFrame([[8, values[i], b, Re[0],Re[1],Re[2],Re[3],Re[4],Re[5],Re[6],Re[7],Re[8],Re[9],Re[10],Re[11], Re[12],Re[13],Re[14]]], columns=['N', 'k', 'b', 'TH1', 'TH2','TH3', 'TH4','TH5','avDelay1', 'avDelay2','avDelay3', 'avDelay4','avDelay5','CIdelay1','CIdelay2','CIdelay3','CIdelay4','CIdelay5'])
        ResultsData = ResultsData.append(Res,ignore_index=True)
    for i in range(len(values)):
        Re = GenerateResults(6,values[i], b)
        Res = pd.DataFrame([[14, values[i], b, Re[0],Re[1],Re[2],Re[3],Re[4],Re[5],Re[6],Re[7],Re[8],Re[9],Re[10],Re[11], Re[12],Re[13],Re[14]]], columns=['N', 'k', 'b', 'TH1', 'TH2','TH3', 'TH4','TH5','avDelay1', 'avDelay2','avDelay3', 'avDelay4','avDelay5','CIdelay1','CIdelay2','CIdelay3','CIdelay4','CIdelay5'])
        ResultsData = ResultsData.append(Res,ignore_index=True)


