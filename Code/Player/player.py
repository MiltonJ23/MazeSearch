"""This module implement the player and how he will move inside of the maze"""



from __future__ import annotations 
import pygame 




class Player:
    def __init__(self, cor_x: int, cor_y: int):
        # cor_x, cor_y are matrix coordinates (col, row)
        self.cor_x = cor_x
        self.cor_y = cor_y

    def GetCoordinates(self) -> tuple[int, int]:
        return (self.cor_x, self.cor_y)

    def SetCoordinaates(self, x: int, y: int) -> None:
        self.cor_x = x
        self.cor_y = y

    def move(self, dx: int, dy: int, maze_matrix) -> None:
        new_x = self.cor_x + dx
        new_y = self.cor_y + dy
        max_rows = maze_matrix.shape[0]
        max_cols = maze_matrix.shape[1]
        if 0 <= new_x < max_cols and 0 <= new_y < max_rows:
            # maze_matrix uses 0 for free cells
            if maze_matrix[new_y][new_x] == 0:
                self.cor_x = new_x
                self.cor_y = new_y

    def draw(self, screen: pygame.Surface, cellSize: int) -> None:
        rect = pygame.Rect(self.cor_x * cellSize, self.cor_y * cellSize, cellSize, cellSize)
        pygame.draw.rect(screen, (0, 255, 0), rect)