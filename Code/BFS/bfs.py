"""This module is the BFS implementation for finding the most optimal path from the start and the end of the maze"""
from collections import deque
from typing import Generator, Tuple
import numpy as np

def BfsGenerator(maze: np.ndarray, start: Tuple[int,int], goal: Tuple[int,int]) -> Generator[Tuple[str, Tuple[int,int]], None, None]:
    FrontierQueue  = deque([start])
    VisitedNode = set([start])
    ParentNode = {}
    yield ("visit", start) # yield the start as visited 
    while FrontierQueue:
        node = FrontierQueue.popleft()
        if node == goal:
            # reconstruct path
            MazePath = []
            cur = goal
            while True:
                MazePath.append(cur)
                if cur == start:
                    break
                cur = ParentNode[cur]
            MazePath.reverse()
            for node in MazePath:
                yield ("path", node) # yield each cell in the path 
            return
        r, c = node
        for dr, dc in [(-1,0),(0,1),(1,0),(0,-1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] == 0 and (nr, nc) not in VisitedNode:
                    VisitedNode.add((nr, nc))
                    ParentNode[(nr, nc)] = node
                    FrontierQueue.append((nr, nc))
                    yield ("visit", (nr, nc))