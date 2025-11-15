""" This is the maze moduele. It contains the Maze class and methods to generate and manipulate mazes.The randomized kruskal's algorithm is implemented here in order to generate a sound maze."""

from __future__ import annotations 
import numpy as np 
from typing import List, Tuple
import pygame
import sys
import time

# --- (This is your original Maze class, unchanged) ---

class Maze: 
    def __init__(self:"Maze",rows: int, cols:int)-> None:
        self.grid_rows = rows 
        self.grid_columns = cols
        self.rows = (2 * self.grid_rows) + 1 # This is the maze with the walls and open space
        self.cols = (2 * self.grid_columns) + 1 
        self.Matrix = np.ones((self.rows,self.cols)) # Let's initialize the matrix with all walls 
        
        # --- FIX 1 ---
        # Carve out the cells (paths, 0)
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

        # --- FIX 2 ---
        # DSU must be sized for the number of cells, not the whole grid
        num_cells = self.grid_rows * self.grid_columns
        parent = list(range(num_cells))
        matrix_rank = [0] * num_cells
        
        def _find(node :int )-> int:
            if parent[node] == node:
                return node
            parent[node] = _find(parent[node]) # Path compression
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
                
                # --- FIX 3 ---
                # Calculate the (r, c) of the wall *between* the cells
                r_wall = (node1[0] + node2[0]) + 1
                c_wall = (node1[1] + node2[1]) + 1
                self.Matrix[r_wall, c_wall] = 0 # Use (r, c) indexing
                
        self.Matrix[1, 0] = 0 # making sure the start is free 
        self.Matrix[self.rows - 2, self.cols - 1] = 0 # and the end is free
        return self.Matrix 
    
    def edgesListing(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        self.edges_list = []
        for i in range(self.grid_rows):
            for j in range(self.grid_columns):
                if j + 1 < self.grid_columns:
                    self.edges_list.append( ((i,j), (i, j+1)) )  # Edge in the right position registered
                if i + 1 < self.grid_rows:
                    self.edges_list.append( ((i,j), (i+1, j)) )  # Edge in the downward postion registered | only performed the right and down sides. to avoid duplicates .
        # print("Edges List:", self.edges_list) # Commented out for cleaner game output
        return self.edges_list

def test():
    # This will create a 5x5 *cell* maze, on an 11x11 grid
    rm : Maze = Maze(5, 5) 
    # print("--- Initial Grid (Cells pre-carved) ---") # Commented out
    # rm.display_matrix() # Commented out
    
    # Generate the maze
    rm.SetMatrix(rm.maze_generator())
    
    # print("\n--- Final Maze ---") # Commented out
    # rm.display_matrix() # Commented out

# test() # We will call the new Pygame main function instead


# --- (NEW PYGAME CODE STARTS HERE) ---

# --- Constants ---
MAZE_CELL_ROWS = 15
MAZE_CELL_COLS = 15
CELL_SIZE = 25

# Calculate "thick" grid dimensions
GRID_ROWS = (2 * MAZE_CELL_ROWS) + 1
GRID_COLS = (2 * MAZE_CELL_COLS) + 1

# Screen dimensions
SCREEN_WIDTH = GRID_COLS * CELL_SIZE
SCREEN_HEIGHT = GRID_ROWS * CELL_SIZE + 100 # Add 100 pixels for UI

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Button
BUTTON_RECT = pygame.Rect(50, SCREEN_HEIGHT - 75, 220, 50)


class Player:
    def __init__(self, x, y):
        # x and y are GRID coordinates, not pixel coordinates
        self.x = x
        self.y = y

    def move(self, dx, dy, maze_matrix):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Check boundaries
        if 0 <= new_x < GRID_COLS and 0 <= new_y < GRID_ROWS:
            # Check for wall collision (1 is a wall, 0 is a path)
            if maze_matrix[new_y, new_x] == 0:
                self.x = new_x
                self.y = new_y

    def draw(self, screen):
        rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Maze Runner")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.small_font = pygame.font.Font(None, 30)
        
        self.start_pos = (1, 0) # (row, col)
        self.end_pos = (GRID_ROWS - 2, GRID_COLS - 1) # (row, col)
        
        self.maze_obj = None
        self.maze_matrix = None
        self.player = None
        
        self.game_active = False
        self.start_time = 0
        self.elapsed_time = 0
        self.win_message = ""
        
        self.new_game()

    def new_game(self):
        # Generate a new maze
        self.maze_obj = Maze(MAZE_CELL_ROWS, MAZE_CELL_COLS)
        self.maze_matrix = self.maze_obj.maze_generator()
        
        # Reset player to start position
        # Player(x, y) maps to (col, row)
        self.player = Player(self.start_pos[1], self.start_pos[0])
        
        # Reset timer and game state
        self.game_active = False
        self.start_time = 0
        self.elapsed_time = 0
        self.win_message = ""

    def draw_text(self, text, font, color, x, y, center=True):
        text_surface = font.render(text, True, color)
        if center:
            text_rect = text_surface.get_rect(center=(x, y))
        else:
            text_rect = text_surface.get_rect(topleft=(x, y))
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        for r in range(GRID_ROWS):
            for c in range(GRID_COLS):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                
                color = WHITE # Default for paths (0)
                if self.maze_matrix[r, c] == 1:
                    color = BLACK # Walls
                
                # Color start and end
                if (r, c) == self.start_pos:
                    color = BLUE
                elif (r, c) == self.end_pos:
                    color = RED
                    
                pygame.draw.rect(self.screen, color, rect)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if BUTTON_RECT.collidepoint(event.pos):
                    self.new_game()
            
            if event.type == pygame.KEYDOWN:
                # Start timer on first move
                if not self.game_active and self.win_message == "":
                    self.game_active = True
                    self.start_time = time.time()
                
                # Player movement
                if self.game_active:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.player.move(-1, 0, self.maze_matrix)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.player.move(1, 0, self.maze_matrix)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.move(0, -1, self.maze_matrix)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.move(0, 1, self.maze_matrix)

    def update(self):
        # Update timer
        if self.game_active:
            self.elapsed_time = time.time() - self.start_time
        
        # Check for win condition
        if (self.player.y, self.player.x) == self.end_pos:
            if self.game_active:
                self.game_active = False # Stop the game and timer
                self.win_message = f"You won! Time: {self.elapsed_time:.2f}s"

    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw maze and player
        self.draw_grid()
        self.player.draw(self.screen)
        
        # --- Draw UI Panel ---
        ui_panel_rect = pygame.Rect(0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100)
        pygame.draw.rect(self.screen, DARK_GRAY, ui_panel_rect)
        
        # Draw Button
        pygame.draw.rect(self.screen, GRAY, BUTTON_RECT)
        self.draw_text("Regenerate Maze", self.small_font, BLACK, BUTTON_RECT.centerx, BUTTON_RECT.centery)
        
        # Draw Timer
        timer_text = f"Time: {self.elapsed_time:.2f}s"
        self.draw_text(timer_text, self.font, WHITE, SCREEN_WIDTH - 150, SCREEN_HEIGHT - 50)
        
        # Draw Win Message if won
        if self.win_message:
            self.draw_text(self.win_message, self.font, GREEN, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            
        pygame.display.flip()

def main():
    game = Game()
    game.run()

if __name__ == "__main__":
    main()