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
     

Matrix = PodMatrixGenerator(85)

def XYcoordinatesMove3(PodMatrix):
    aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] 
    crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] 
    while True:
        YCoordinate = random.randint(1,36)
        XCoordinate = random.randint(1,89)
        PodValue = PodMatrix[YCoordinate][XCoordinate]
        print(PodValue)
        if PodValue == 0:
            pass
        else:
            Y = YCoordinate
            X = XCoordinate
            break
    #PodMatrix[Y][X] = 0
    
    return X, Y

XY = XYcoordinatesMove3(Matrix)

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
    return X, Y

print(XY)
XY2 = XYcoordinatesMove1(Matrix)
print(XY2)
if XY2[0] in crossaisles:
    print('ERROR x')
if XY2[1] in aisles:
    print('ERROR y')
      
#aislerow = []
#for x in range(Xlength):
#    if x in crossaisles:
#        aislerow.append(0)
#    else:
#        m = ZeroOrOneGenerator(85)
#        aislerow.append(m)

#zerooptions = 90-16      
#print(sum(aislerow))

#percentagefilled = (sum(aislerow))/zerooptions

#print(percentagefilled)