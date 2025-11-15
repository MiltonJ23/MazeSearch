"""This module implement the Depth-First algorithm also used to generate a tree or traverse a tree"""
import numpy as np
from typing import Generator, Tuple



def dfs_generator(maze: np.ndarray, start: Tuple[int, int], goal: Tuple[int, int]) -> Generator[Tuple[str, Tuple[int,int]], None, None]:

    stack = [start]
    visited = set()
    parent: dict[Tuple[int,int], Tuple[int,int]] = {}

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        yield ("visit", node)

        if node == goal:
            
            path = []
            cur = goal
            while True:
                path.append(cur)
                if cur == start:
                    break
                cur = parent[cur]
            path.reverse()
            for p in path:
                yield ("path", p)
            return

        r, c = node
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]: 
            nr, nc = r + dr, c + dc
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] == 0 and (nr, nc) not in visited:
                    parent[(nr, nc)] = node
                    stack.append((nr, nc))
                    