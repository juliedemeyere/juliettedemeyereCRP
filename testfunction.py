#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:10:04 2019

@author: juliedemeyere
"""

aisles = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35] # relevant for y intersections

aislesdict = {2:'East', 5:'West', 8:'East', 11:'West', 14:'East', 17:'West', 20:'East', 23:'West', 26:'East', 29:'West', 32:'East', 35:'West'}

crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections

crossaislesdict = {0 :'North', 6:'South', 12:'North', 18:'South', 24:'North', 30:'South', 36:'North', 42:'South', 48:'North', 54:'South', 60:'North', 66:'South', 72:'North', 78:'South', 84:'North', 90:'South'}

x = 32
y = 12
distance = 100

#TravelDirection = 'East'

for m in crossaisles:
 #   print(m)
    dist = abs(m-x)
    if dist < distance:
        distance = dist
        Index= crossaisles.index(m)
        ClosestIntersection = m
if TravelDirection == 'East':
    if ClosestIntersection > x:
        Intersection = ClosestIntersection
    else:
        Intersection = crossaisles[ Index + 1]

def AisleInformation(y):
    distance = 100
    for aisle in aisles:
        dist = abs(y - aisle)
        if dist < distance:
            distance = dist
            AisleUsed = aisle
    TravelDirection = aislesdict[AisleUsed]
    return AisleUsed, TravelDirection

def Case2CalculateDistance(x,y,Xws,Yws): #the closest cross section that will be travelled to
    aisle = AisleUsed(y)
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
    if TravelDirection == 'West':
        if ClosestIntersection < x:
            XintersectionClosest = ClosestIntersection
        else:
            Xintersection = crossaisles[ Index - 1]
    print(Xintersection, Yintersection)
    if crossaislesdict[Xintersection] == 'North':
        Ysi = Yintersection + 2
    else:
        Ysi = Yintersection - 2
    Xsi = Xintersection
    u = 1
    w = 5
    l = 2
    DcaSi = abs(Yintersection - y) # Not specified what this is? Assuming this is true
    DleSi = 2*u + DcaSi + w + l
    if Yws <= y: # INCOMPLETE detour because of not entirely specified reasons in the paper. Needs to be adjusted
        DeltaLeWs = 2
    else:
        DeltaLeWs = 0
    D = u + DleSi + abs(Xsi - Xws) + abs(Ysi - Yws) + DeltaLeWs
    

def EastTravelDistanceWS():
    WScoordinates = [0,17]
    #Generate a location of pod that needs to be picked up
    x = HorizontalCoordinate()  
    y = VerticalCoordinate()  
    PodCoordinate = [x,y]
    right = [4,6,10,12,16,18,22,24,28,30,34,36]
    if y in right:
        TravelDirection = 'East'
        Case = 1
    else:
        TravelDirection = 'West'
        Case = 2
    
    u = 1
    Xle = x
    Xws = WScoordinates[0]
    Yle = y
    Yws = WScoordinates[1]
    if Yws >= Yle:
        LeWs = 2
    else:
        LeWs = 0
    
    if Case == 1:
        D = u + abs(Xle - Xws) + abs(Yle-Yws) + LeWs
        
    elif Case == 2:
        if x in Xspot1:
            dCaLe = 4
        if x in Xspot2:
            dCaLe = 3
        if x in Xspot3:
            dCaLe = 2
        if x in Xspot4:
            dCaLe = 1
        if x in Xspot5:
            dCaLe = 0
        dLeSi = 2+ 5 + 2 + dCaLe
#        D = u + dLeSi + abs(Xsi - Xws) + abs(Ysi-Yws) + LeWs
y = EastTravelDistanceWS()
crossaisles = []
m = 6
while m < 90:
    crossaisles.append(m)
    m +=6
print(crossaisles)

CrossSectionTravelingTo(32,12)

#print(AisleUsed(10), 'AISLE')
#print(distance)
#print(Index, 'Index', ClosestIntersection, 'closestintersection', Intersection)
