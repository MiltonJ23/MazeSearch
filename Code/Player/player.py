"""This module implement the player and how he will move inside of the maze"""



from __future__ import annotations 
import pygame 




class Player:
    def __init__(self:"Player", cor_x:int , cor_y:int):
       self.cor_x = cor_x # Those x and y refer to grid coordinates and not pixel coordinates | Careful 
       self.cor_y = cor_y 

    def GetCoordinates(self)-> tuple[int,int]:
       return (self.cor_x, self.cor_y)
    def SetCoordinaates(self, x : int , y:int) -> None:
         self.cor_x = x 
         self.cor_y =y 

    def move(self, dx :int, dy: int , maze_matrix: list[list[int]], grid_rows:int , grid_cols:int)-> None:
       new_x = self.cor_x + dx 
       new_y = self.cor_y + dy 

       # Next we have to ensure that the position is valid , thus checking boudaries 
       if 0 <= new_x < grid_cols and 0 <= new_y < grid_rows:
          if maze_matrix[new_y][new_x] == 0 : 
             self.cor_x = new_x 
             self.cor_y = new_y 
             
    def draw(self, screen:pygame.Surface, cellSize:int)-> None:
       rect = pygame.Rect(self.cor_x * cellSize, self.cor_y * cellSize, cellSize, cellSize)
       pygame.draw.rect(screen, (0, 255, 0), rect)