""" This is the maze moduele. It contains the Maze class and methods to generate and manipulate mazes.The randomized kruskal's algorithm is implemented here in order to generate a sound maze."""

from __future__ import annotations 
import numpy as np 
from typing import List, Tuple



class Maze: 
    def __init__(self:"Maze",rows: int, cols:int)-> None:
        self.rows = rows 
        self.cols = cols 
        self.Matrix = np.ones((rows,cols)) # Let's initialize the matrix with all walls 
        self.edges_list:list[tuple[tuple[int,int],tuple[int,int]]] = []

    def display_matrix(self) -> None:
        print(self.Matrix)

    def GetMatrix(self) -> np.ndarray:
        return self.Matrix

    def SetMatrix(self, matrix:np.ndarray) -> None:
        self.Matrix = matrix 


    def maze_generator(self)-> np.ndarray :
        # The matrix is already initialized with walls, now let's initialize the edge list 
        self.edges_list = self.edgesListing()
        np.random.shuffle(self.edges_list) # let's randomize the list of edges 

        # 
        matrix_degree = self.cols * self.rows 
        parent = list(range(matrix_degree))
        matrix_rank = [0] * matrix_degree

        def _index(cell: Tuple[int,int])-> int:
            row,col = cell
            return row*self.cols + col
        
        def _find(node :int )-> int:
            while parent[node] != node:
                parent[node] = parent[parent[node]]
                node = parent[node]
            return node
        def _union(nd1:int , nd2:int)-> None:
            rnd1 = _find(nd1)
            rnd2 = _find(nd2) 
            if rnd1 == rnd2 :
                return 
            if matrix_rank[rnd1] < matrix_rank[rnd2]:
                parent[rnd1] = rnd2 
            elif matrix_rank[rnd1] > matrix_rank[rnd2]:
                parent[rnd2] = rnd1 
            else :
                parent[rnd2] = rnd1 
                matrix_rank[rnd1] += 1
        
        for (node1,node2) in self.edges_list:
            index1 = _index(node1)
            index2 = _index(node2)
            if _find(index1) != _find(index2):
                row1,col1 = node1 
                row2,col2 = node2 
                self.Matrix[row1,col1] = 0 
                self.Matrix[row2,col2] = 0 
                _union(index1,index2)
        self.Matrix[0][0] = 0 # making sure the start is free 
        self.Matrix[self.rows-1][self.cols-1] = 0
        return self.Matrix 
    
    def edgesListing(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        self.edges_list = []
        for i in range(self.rows):
            for j in range(self.cols):
                if j + 1 < self.cols:
                    self.edges_list.append( ((i,j), (i, j+1)) )  # Edge right
                if i + 1 < self.rows:
                    self.edges_list.append( ((i,j), (i+1, j)) )  # Edge down | only performed the right and down sides. to avoid duplicates .
        return self.edges_list






