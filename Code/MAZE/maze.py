""" This is the maze moduele. It contains the Maze class and methods to generate and manipulate mazes.The randomized kruskal's algorithm is implemented here in order to generate a sound maze."""

from __future__ import annotations 
import numpy as np 
from typing import List, Tuple



class Maze: 
    def __init__(self:"Maze",rows: int, cols:int)-> None:
        self.grid_rows = rows # I am doing a distinction betweeen the 2x3 defines by the user and the need for other cells to materialize the walls 
        self.grid_columns = cols
        self.rows = (2 * self.grid_rows) + 1 # This is the maze with the walls and open space
        self.cols = (2 * self.grid_columns) + 1 
        self.Matrix = np.ones((self.rows,self.cols)) # Let's initialize the matrix with all walls 
        for r in range(self.grid_rows):
            for c in range(self.grid_columns):
                self.Matrix[2*r + 1, 2*c + 1] = 0
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

    
        parent = list(range(self.grid_columns * self.grid_rows ))
        matrix_rank = [0] * (self.grid_columns * self.grid_rows )
        
        def _find(node :int )-> int:
            if parent[node] == node:
                return node
            parent[node] = _find(parent[node])
            return parent[node]
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
    
        for (node1, node2) in self.edges_list:
            index1 = node1[0] * self.grid_columns + node1[1]
            index2 = node2[0] * self.grid_columns + node2[1]
            if _find(index1) != _find(index2):
                _union(index1, index2)
                r_wall = (node1[0] + node2[0]) + 1
                c_wall = (node1[1] + node2[1]) + 1
                self.Matrix[r_wall, c_wall] = 0
    
        self.Matrix[1][0] = 0  # making sure the start is free 
        self.Matrix[self.rows-2][self.cols-1] = 0
        return self.Matrix 
    
    def edgesListing(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        self.edges_list = []
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                if j + 1 < self.grid_columns:
                    self.edges_list.append( ((i,j), (i, j+1)) )  # Edge in the right position registered
                if i + 1 < self.grid_rows:
                    self.edges_list.append( ((i,j), (i+1, j)) )  # Edge in the downward postion registered | only performed the right and down sides. to avoid duplicates .
        print("Edges List:", self.edges_list) 
        return self.edges_list





