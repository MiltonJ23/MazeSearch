"""This module is the game module.Containing the implementation of the maze game itself. It will be called with the correct arguments in the main file and ensure the readability of the code."""



from __future__ import annotations
import pygame
import sys
import time
import numpy as np

from Player.player import Player
from MAZE.maze import Maze


class Game:
    def __init__(self, grid_rows: int, grid_cols: int, cell_size: int = 22):
        pygame.init()
        self.grid_rows = grid_rows
        self.grid_cols = grid_cols
        self.cell_size = cell_size

        # matrix produced by Maze has size (2*grid_rows+1, 2*grid_cols+1)
        self.matrix_rows = 2 * grid_rows + 1
        self.matrix_cols = 2 * grid_cols + 1

        self.sidebar_width = 200
        w = self.matrix_cols * self.cell_size + self.sidebar_width
        h = self.matrix_rows * self.cell_size + 0
        self.SCREEN = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Search Algorithms in Maze")

        self.Clock = pygame.time.Clock()
        self.Font = pygame.font.Font(None, 28)
        self.SmallFont = pygame.font.Font(None, 20)

        # Buttons
        left = self.matrix_cols * self.cell_size + 20
        top = 20
        self.btn_regen = pygame.Rect(left, top, 160, 40)
        self.btn_dfs = pygame.Rect(left, top + 60, 160, 40)
        self.btn_bfs = pygame.Rect(left, top + 120, 160, 40)
        self.btn_ga = pygame.Rect(left, top + 180, 160, 40)

        # Button colors requested
        self.color_regen = (200, 200, 200)
        self.color_dfs = (0, 0, 255)       # blue
        self.color_bfs = (0, 255, 255)     # cyan
        self.color_ga = (210, 180, 140)    # light brown / tan

        # Game state
        self.MazeObject: Maze | None = None
        self.MazeMatrix: np.ndarray | None = None
        self.Player: Player | None = None

        # Start / destination are matrix coordinates (row, col)
        self.start = (1, 0)
        self.destination = (self.matrix_rows - 2, self.matrix_cols - 1)

        self.is_game_active = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.win_message = ""

    def new_game(self):
        self.MazeObject = Maze(self.grid_rows, self.grid_cols)
        self.MazeMatrix = self.MazeObject.maze_generator()
        # Player uses (x, y) = (col, row)
        start_row, start_col = self.start
        self.Player = Player(start_col, start_row)
        self.is_game_active = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.win_message = ""

    def draw_text(self, text: str, font, color: tuple[int, int, int], x: float, y: float, center: bool = False):
        textArea = font.render(text, True, color)
        if center:
            rect = textArea.get_rect(center=(x, y))
        else:
            rect = textArea.get_rect(topleft=(x, y))
        self.SCREEN.blit(textArea, rect)

    def draw_grid(self):
        if self.MazeMatrix is None:
            return
        for r in range(self.MazeMatrix.shape[0]):
            for c in range(self.MazeMatrix.shape[1]):
                rect = pygame.Rect(c * self.cell_size, r * self.cell_size, self.cell_size, self.cell_size)
                color = (255, 255, 255) if self.MazeMatrix[r, c] == 0 else (0, 0, 0)
                # start / destination highlight
                if (r, c) == self.start:
                    color = (0, 0, 255)
                elif (r, c) == self.destination:
                    color = (255, 0, 0)
                pygame.draw.rect(self.SCREEN, color, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.btn_regen.collidepoint(event.pos):
                    self.new_game()
                if self.btn_dfs.collidepoint(event.pos):
                    print("DFS button pressed")  # placeholder: call DFS solver
                if self.btn_bfs.collidepoint(event.pos):
                    print("BFS button pressed")  # placeholder: call BFS solver
                if self.btn_ga.collidepoint(event.pos):
                    print("GA button pressed")   # placeholder: call GA solver
            if event.type == pygame.KEYDOWN:
                if not self.is_game_active and self.win_message == "":
                    self.is_game_active = True
                    self.start_time = time.time()
                if self.is_game_active and self.Player is not None and self.MazeMatrix is not None:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        self.Player.move(-1, 0, self.MazeMatrix)
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        self.Player.move(1, 0, self.MazeMatrix)
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.Player.move(0, -1, self.MazeMatrix)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.Player.move(0, 1, self.MazeMatrix)

    def update(self):
        if self.is_game_active:
            self.elapsed_time = time.time() - self.start_time
        if self.Player is not None:
            # check win: player's (row,col) equals destination
            if (self.Player.cor_y, self.Player.cor_x) == self.destination:
                if self.is_game_active:
                    self.is_game_active = False
                    self.win_message = f"You won! Time: {self.elapsed_time:.2f}s"

    def draw_ui(self):
        # sidebar background
        sidebar_rect = pygame.Rect(self.matrix_cols * self.cell_size, 0, self.sidebar_width, self.matrix_rows * self.cell_size)
        pygame.draw.rect(self.SCREEN, (50, 50, 50), sidebar_rect)

        # Buttons
        pygame.draw.rect(self.SCREEN, self.color_regen, self.btn_regen)
        self.draw_text("Regenerate", self.SmallFont, (0, 0, 0), self.btn_regen.left + 10, self.btn_regen.top + 10)

        pygame.draw.rect(self.SCREEN, self.color_dfs, self.btn_dfs)
        self.draw_text("DFS", self.SmallFont, (255, 255, 255), self.btn_dfs.centerx, self.btn_dfs.centery, center=True)

        pygame.draw.rect(self.SCREEN, self.color_bfs, self.btn_bfs)
        self.draw_text("BFS", self.SmallFont, (0, 0, 0), self.btn_bfs.centerx, self.btn_bfs.centery, center=True)

        pygame.draw.rect(self.SCREEN, self.color_ga, self.btn_ga)
        self.draw_text("GA", self.SmallFont, (0, 0, 0), self.btn_ga.centerx, self.btn_ga.centery, center=True)

        # Timer and message
        timer_text = f"Time: {self.elapsed_time:.2f}s"
        self.draw_text(timer_text, self.Font, (255, 255, 255), self.matrix_cols * self.cell_size + 20, self.btn_ga.bottom + 20)
        if self.win_message:
            self.draw_text(self.win_message, self.Font, (0, 255, 0), self.matrix_cols * self.cell_size + 20, self.btn_ga.bottom + 60)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.SCREEN.fill((100, 100, 100))
            self.draw_grid()
            if self.Player is not None:
                self.Player.draw(self.SCREEN, self.cell_size)
            self.draw_ui()
            pygame.display.flip()
            self.Clock.tick(60)
