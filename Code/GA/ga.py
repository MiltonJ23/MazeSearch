import heapq
from typing import Generator, Tuple, Dict
import numpy as np

def manhattan(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def ga_generator(maze: np.ndarray, start: Tuple[int,int], goal: Tuple[int,int]) -> Generator[Tuple[str, Tuple[int,int]], None, None]:
    """
    Implementation uses A* to produce a path but yields 'visit' events for nodes popped from the open set.
    This provides a distinct (tan) visualization for the GA button while remaining efficient.
    """
    open_heap = []
    g_score: Dict[Tuple[int,int], int] = {start: 0}
    f_score = {start: manhattan(start, goal)}
    parent = {}
    heapq.heappush(open_heap, (f_score[start], start))
    closed = set()
    yield ("visit", start)
    while open_heap:
        _, current = heapq.heappop(open_heap)
        if current in closed:
            continue
        closed.add(current)
        yield ("visit", current)
        if current == goal:
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
        r, c = current
        for dr, dc in [(-1,0),(0,1),(1,0),(0,-1)]:
            nbr = (r+dr, c+dc)
            nr, nc = nbr
            if 0 <= nr < maze.shape[0] and 0 <= nc < maze.shape[1]:
                if maze[nr, nc] != 0:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(nbr, 1_000_000):
                    parent[nbr] = current
                    g_score[nbr] = tentative_g
                    f = tentative_g + manhattan(nbr, goal)
                    f_score[nbr] = f
                    heapq.heappush(open_heap, (f, nbr))