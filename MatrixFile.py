import numpy as np

from collections import deque
from math import sqrt
import matplotlib.pyplot as plt
import random


def ZeroOrOneGenerator(probability):
    value = random.randint(1,101)
    if value <= probability:
        n = 1
    else:
        n = 0
    return n

class PodMatrixClass:
   
    def __init__(self):     # Whenever we add something here we want to keep track off we should also reset it after warmup
        self.Matrix = []
       # self.probability = 90
            
    
    def PodMatrixGenerator(self, probability):
        Xlength = 90
        Ylength = 37
        crossaisles = [0, 6, 12, 18, 24, 30, 36, 42, 48, 54, 60, 66, 72, 78, 84, 90] # relevant for x intersections
        aisles = [0, 2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35, 37] # relevant for y intersections
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
                      #  value = random.randint(1,101)
                      #  if value <= probability:
                      #      K = 1
                      #  else:
                       #     K = 0
                        m = ZeroOrOneGenerator(probability)
                        aislerow.append(m)
            matrix.append(aislerow)
        self.Matrix = matrix
    
    def MakeZero(self,x,y):
        f = self.Matrix[y][x]
        before = f
        self.Matrix[y][x] = 0
    
    def MakeOne(self,x,y):
        f = self.Matrix[y][x]
        before = f
        self.Matrix[y][x] = 7
