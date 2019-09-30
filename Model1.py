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

def AisleInformation(y):
    distance = 100
    for aisle in aisles:
        dist = abs(y - aisle)
        if dist < distance:
            distance = dist
            AisleUsed = aisle
    TravelDirection = aislesdict[AisleUsed]
    return AisleUsed, TravelDirection

def HorizontalCoordinate():
    aisles = [6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84]
    while True:
        Coordinate = random.randint(1,89)
        if Coordinate in aisles:
            pass
        else:
            X = Coordinate
            break
    return X

def VerticalCoordinate():
    crossaisles = [2,5,8,11,14,17,20,23,26,29,32,35]
    while True:
        Coordinate = random.randint(1,36)
        if Coordinate in crossaisles:
            pass
        else:
            Y = Coordinate
            break
    return Y 

def XYcoordinatesMove3(PodMatrix):
    aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] 
    crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] 
    while True:
        YCoordinate = random.randint(1,36)
        XCoordinate = random.randint(1,89)
        PodValue = PodMatrix[YCoordinate][XCoordinate]
        if PodValue == 0:
            pass
        else:
            Y = YCoordinate
            X = XCoordinate
            break
    PodMatrix[Y][X] = 0
    return X, Y, PodMatrix
    
def XYcoordinatesMove1(PodMatrix):
    aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] 
    crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] 
    while True:
        while True:
            XCoordinate = random.randint(1,89)
            if XCoordinate in crossaisles:
                pass
            else:
                X = XCoordinate
                break
        while True:
            YCoordinate = random.randint(1,36)
            if YCoordinate in aisles:
                pass
            else:
                Y = YCoordinate
                break
        PodValue = PodMatrix[YCoordinate][XCoordinate]
        if PodValue == 1:
            pass
        else:
            Y = YCoordinate
            X = XCoordinate
            break
    PodMatrix[Y][X] = 1
    return X, Y, PodMatrix
    
' Case 1: WS east/west and first aisle it passes is in direction  east/west'
' Case 2: WS east/west and first aisle it passes is in direction  west/east'
' Case 3: WS north/south and first cross section it passes is in direction  north/south'
' Case 4: WS north/south and first cross section it passes is in direction south/north'



def DistanceCalculator_Move3(Xws,Yws, Location, PodMatrix): # Coordinates of WS, location (east/west/south/north)      

    Move3 = XYcoordinatesMove3(PodMatrix)
    x = Move3[0]
    y = Move3[1]
    PodMatrix = Move3[2]
    AisleTravelDirection = AisleInformation(y)[1]
    if Location == 'West' or Location == 'East':
        if Location == AisleTravelDirection:
            Case = 1
            D = Case1CalculateDistance(x,y, Xws, Yws)
        else:
            Case = 2
            D = Case2CalculateDistance(x,y,Xws,Yws)
    elif Location == 'North' or Location == 'South':
        CrossAisleDirection = FindClosestCrossAisle(x,y)[0]
        if Location == CrossAisleDirection:
            Case = 3
            D = Case3CalculateDistance(x,y,Xws,Yws, Location)
        else:
            Case = 4
            D = Case4CalculateDistance(x,y,Xws,Yws, Location)

    return D, x,y, PodMatrix
                
def DistanceCalculator_Move1(Xws,Yws, Location, PodMatrix):
 #   x = HorizontalCoordinate() # initialize coordinates
 #   y = VerticalCoordinate()
    Move1 = XYcoordinatesMove1(PodMatrix)
    x = Move1[0]
    y = Move1[1]
    PodMatrix = Move1[2]
    AisleTraveldirectionPOD = AisleInformation(y)[1]
    AisleTravelDirectionWS = AisleInformation(Yws)[1]
    if Location == 'West' or Location == 'East': 
        if AisleTraveldirectionPOD != Location:
            Case = 1
            D = Case1CalculateDistance(x,y, Xws, Yws)
        else:
            Case = 2
            D = Case2CalculateDistance(x,y, Xws, Yws)
    elif Location == 'North' or Location == 'South':
        CrossAisleDirection  = FindClosestCrossAisle(x,y)[0]
        if Location != CrossAisleDirection:
            Case = 3
            D = Case3CalculateDistance(x,y,Xws,Yws, Location)
        else:
            Case = 4
            D = Case4CalculateDistance(x,y,Xws,Yws, Location)
   # print('MOVE 1. Coordinates:(', x, y,')', 'Case:', Case, ',Distance:', D, 'TravelDirection WS:', AisleTravelDirectionWS,'TravelDirection POD:', AisleTraveldirectionPOD )
    return D, x, y
        
def DistanceCalculator_Move2(x1,y1, x3, y3): #simply the manhattan distance between two points
    D = abs(x1-x3) + abs(y1-y3)
  #  print('(',x1,',',y1,') to (',x3,',',y3,'))')
  #  print('MOVE 2: Distance', D)
    return D
    
        
def Case1CalculateDistance(x,y, Xws, Yws): #Location pod (x,y), Location WS(Xx,Yy)
    u = 1 
    if Yws <= y: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
        DeltaLeWs = 2
    else:
        DeltaLeWs = 0
    D = u + abs(x - Xws) + abs(y - Yws) + DeltaLeWs
    return D
    
def FindClosestCrossAisle(x, y):
    aisle = AisleInformation(y)
    TravelDirection = aisle[1]
    distance = 100
    for m in crossaisles:
        dist = abs(m-x)
        if dist < distance:
            distance = dist
            Index= crossaisles.index(m)
            ClosestIntersection = m
    if TravelDirection == 'East':
        if ClosestIntersection > x:
            Xintersection = ClosestIntersection
        else:
            Xintersection = crossaisles[ Index + 1]
    elif TravelDirection == 'West':
        if ClosestIntersection < x:
            Xintersection = ClosestIntersection
        else:
            Xintersection = crossaisles[ Index - 1]
    CrossAisleDirection = crossaislesdict[Xintersection]
    return CrossAisleDirection, Xintersection
    

def Case2CalculateDistance(x,y,Xws,Yws): #the closest cross section that will be travelled to
    aisle = AisleInformation(y)
    print(aisle, 'aisle')
    Yintersection = aisle[0]
    TravelDirection = aisle[1]
    distance = 100
    for m in crossaisles:
        dist = abs(m-x)
        if dist < distance:
            distance = dist
            Index= crossaisles.index(m)
            ClosestIntersection = m
    if TravelDirection == 'East':
        if ClosestIntersection > x:
            Xintersection = ClosestIntersection
        else:
            Xintersection = crossaisles[ Index + 1]
    elif TravelDirection == 'West':
        if ClosestIntersection < x:
            Xintersection = ClosestIntersection
        else:
            Xintersection = crossaisles[ Index - 1]
    if crossaislesdict[Xintersection] == 'North':
        if Yintersection == 35: #if Yintersection is already the bottom then it will need to travel downwards
            Ysi = 32
        else:
            Ysi = Yintersection + 3
    else:
        if Yintersection == 2: # if Yintersection is already the bottom then it will need to travel upwards
            Ysi = 5
        else:
            Ysi = Yintersection - 3
    Xsi = Xintersection
    u = 1
    w = 5
    l = 2
    DcaSi = abs(x - Xintersection)
    DleSi = 2*u + DcaSi + l
    if Yws <= y: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
        DeltaLeWs = 2
    else:
        DeltaLeWs = 0
    D = u + DleSi + abs(Xsi - Xws) + abs(Ysi - Yws) + DeltaLeWs
  #  print('DleSi:', DleSi, ',Xsi:', Xsi, ',Xws:', Xws, ',Ysi', Ysi, ',Yws:', Yws, ',DeltaLeWs:', DeltaLeWs)
    return D
    

def Case3CalculateDistance(x,y,Xws,Yws, Location):
    u = 1
    Xsi = FindClosestCrossAisle(x,y)[1]
    if Location == 'North':
        if Xws <= x: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
            DeltaLeWs = 2
        else:
            DeltaLeWs = 0
    elif Location == 'South':
        if Xws <= x: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
            DeltaLeWs = 0
        else:
            DeltaLeWs = 2
    DleSi = abs(Xsi - x)
    D = u + DleSi  + abs(Xsi - Xws) + abs(y - Yws) + DeltaLeWs
    return D

def Case4CalculateDistance(x,y,Xws,Yws, Location):
    u = 1
    w = 5
    l = 2
    Xsi = FindClosestCrossAisle(x,y)[1]
    dCaLe = abs(x-Xsi)
    if Location == 'North':
        if Xws <= x: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
            DeltaLeWs = 2
        else:
            DeltaLeWs = 0
    elif Location == 'South':
        if Xws <= x: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
            DeltaLeWs = 0
        else:
            DeltaLeWs = 2
    D1 = u + dCaLe + w + u + abs((x - dCaLe - w - u) - Xws) + abs(y -Yws) + DeltaLeWs
    D2 = u + dCaLe + 2*l + w + 3*u + abs((x - dCaLe + w + u) - Xws) + abs(y - Yws) + DeltaLeWs
    D = min(D1, D2)
    return D 

def CalculateTravelTime(Move1, Move2, Move3):
    D1 = Move1[0]
    D2 = Move2
    D3 = Move3[0]
    T1 = D1/1.3
    T2 = D2/1.3
    T3 = D3/1.3
    return T1,T2,T3

#Move3 = DistanceCalculator_Move3(46,0, 'South')
#Move1 = DistanceCalculator_Move1(46,0, 'South')
#Move2 = DistanceCalculator_Move2(Move1[1],Move1[2], Move3[1], Move3[2])

#CalculateTravelTime(Move1, Move2, Move3)











    
