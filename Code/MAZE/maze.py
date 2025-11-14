""" This is the maze moduele. It contains the Maze class and methods to generate and manipulate mazes."""

from __future__ import annotations 
import numpy as np 



class Maze: 
    def __init__(self:"Maze",rows: int, cols:int)-> None:
        self.rows = rows 
        self.cols = cols 
        self.Matrix = np.zeros((rows,cols)) # In this the attribute Matrix is of type ndarray 

    def display_matrix(self) -> None:
        print(self.Matrix)

    def maze_generator(self)-> np.ndarray :
        for i in range(self.rows):
            for k in range(self.cols):
                r = np.random.randint(0,1) # randomly generated number either 0 or 1
                if i==0 and k == 0 :
                    self.Matrix[0][0]= 0 
                else:
                    if r == 0:
                        self.Matrix[i][k] = 0 # Meaning there is a path 
                    else:
                        self.Matrix[i][k] = 1 # this means there is a wall 
        return self.Matrix 
    
    def GetMatrix(self) -> np.ndarray:
        return self.Matrix

    def SetMatrix(self, matrix:np.ndarray) -> None:
        self.Matrix = matrix 

