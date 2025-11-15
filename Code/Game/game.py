"""This module is the game module.Containing the implementation of the maze game itself. It will be called with the correct arguments in the main file and ensure the readability of the code."""



from __future__ import annotations
import pygame
import sys
import time
import numpy as np

from Player.player import Player
from MAZE.maze import Maze
from DFS.dfs import dfs_generator
from BFS.bfs import BfsGenerator
from GA.ga import ga_generator

class Game:
    def __init__(self, GridRows: int, GridColumns: int, CellSize: int = 22):
        pygame.init()
        self.GridRows = GridRows
        self.GridColumns = GridColumns
        self.CellSize = CellSize
        self.MatrizRows = 2 * GridRows + 1
        self.MatrixColumns = 2 * GridColumns + 1
        self.SidebarWidth = 200
        w = self.MatrixColumns * self.CellSize + self.SidebarWidth
        h = self.MatrizRows * self.CellSize + 0
        self.SCREEN = pygame.display.set_mode((w, h))
        pygame.display.set_caption("Search Algorithms in Maze")
        self.Clock = pygame.time.Clock()
        self.Font = pygame.font.Font(None, 28)
        self.SmallFont = pygame.font.Font(None, 20)
        left = self.MatrixColumns * self.CellSize + 20
        top = 20
        self.btn_regen = pygame.Rect(left, top, 160, 40)
        self.ButtonDFS = pygame.Rect(left, top + 60, 160, 40)
        self.ButtonBFS = pygame.Rect(left, top + 120, 160, 40)
        self.btn_ga = pygame.Rect(left, top + 180, 160, 40)
        self.color_regen = (200, 200, 200)
        self.ColorDFS = (0, 0, 255)       # blue
        self.ColorBFS = (0, 255, 255)     # cyan
        self.ColorGa = (210, 180, 140)    # light brown / tan
        self.MazeObject: Maze | None = None
        self.MazeMatrix: np.ndarray | None = None
        self.Player: Player | None = None

        self.start = (1, 0)
        self.destination = (self.MatrizRows - 2, self.MatrixColumns - 1)
        self.is_game_active = False
        self.start_time = 0.0
        self.ElapsedTime = 0.0
        self.WinningMessage = ""
        self.dfs_gen = None

        self.dfs_visited: set[tuple[int,int]] = set()
        self.dfs_path: list[tuple[int,int]] = []
        self.dfs_StartTime = 0.0
        self.dfs_ElapsedTime = 0.0
        self.dfs_finished = False
        self.dfs_nodes_explored = 0
        self.BfsGenerator = None
        self.BfsVisited: set[tuple[int,int]] = set()
        self.bfs_path: list[tuple[int,int]] = []
        self.bfs_StartTime = 0.0
        self.bfs_ElapsedTime = 0.0
        self.bfs_finished = False
        self.bfs_nodes_explored = 0
        self.ga_gen = None
        self.ga_visited: set[tuple[int,int]] = set()
        self.ga_path: list[tuple[int,int]] = []
        self.ga_StartTime = 0.0
        self.ga_ElapsedTime = 0.0
        self.ga_finished = False
        self.ga_nodes_explored = 0

        self.solver_step_per_frame = 4

    def new_game(self):
        self.MazeObject = Maze(self.GridRows, self.GridColumns)
        self.MazeMatrix = self.MazeObject.maze_generator()
        start_row, start_col = self.start
        self.Player = Player(start_col, start_row)
        self.is_game_active = False
        self.StartTime = 0.0
        self.ElapsedTime = 0.0
        self.WinningMessage = ""
        # clear all solver state
        self.dfs_gen = None
        self.dfs_visited.clear()
        self.dfs_path.clear()
        self.dfs_ElapsedTime = 0.0
        self.dfs_finished = False
        self.dfs_nodes_explored = 0
        self.BfsGenerator = None
        self.BfsVisited.clear()
        self.bfs_path.clear()
        self.bfs_ElapsedTime = 0.0
        self.bfs_finished = False
        self.bfs_nodes_explored = 0
        self.ga_gen = None
        self.ga_visited.clear()
        self.ga_path.clear()
        self.ga_ElapsedTime = 0.0
        self.ga_finished = False
        self.ga_nodes_explored = 0

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
                rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
                color = (255, 255, 255) if self.MazeMatrix[r, c] == 0 else (0, 0, 0)
                if (r, c) == self.start:
                    color = (0, 0, 255)
                elif (r, c) == self.destination:
                    color = (255, 0, 0)
                pygame.draw.rect(self.SCREEN, color, rect)
        for (r, c) in self.dfs_visited:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, self.ColorDFS, rect)
        for (r, c) in self.dfs_path:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, (0, 100, 200), rect)
        for (r, c) in self.BfsVisited:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, self.ColorBFS, rect)
        for (r, c) in self.bfs_path:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, (0, 150, 150), rect)
        for (r, c) in self.ga_visited:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, self.ColorGa, rect)
        for (r, c) in self.ga_path:
            rect = pygame.Rect(c * self.CellSize, r * self.CellSize, self.CellSize, self.CellSize)
            pygame.draw.rect(self.SCREEN, (150, 120, 80), rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if self.btn_regen.collidepoint(event.pos):
                    self.new_game()

                if self.ButtonDFS.collidepoint(event.pos):
                    if self.MazeMatrix is not None:
                        self.BfsGenerator = None
                        self.BfsVisited.clear()
                        self.bfs_path.clear()
                        self.ga_gen = None
                        self.ga_visited.clear()
                        self.ga_path.clear()
                        self.dfs_gen = dfs_generator(self.MazeMatrix, self.start, self.destination)
                        self.dfs_visited.clear()
                        self.dfs_path.clear()
                        self.dfs_StartTime = time.time()
                        self.dfs_ElapsedTime = 0.0
                        self.dfs_finished = False
                        self.dfs_nodes_explored = 0
                if self.ButtonBFS.collidepoint(event.pos):
                    if self.MazeMatrix is not None:
                        self.dfs_gen = None
                        self.dfs_visited.clear()
                        self.dfs_path.clear()
                        self.ga_gen = None
                        self.ga_visited.clear()
                        self.ga_path.clear()
                        self.BfsGenerator = BfsGenerator(self.MazeMatrix, self.start, self.destination)
                        self.BfsVisited.clear()
                        self.bfs_path.clear()
                        self.bfs_StartTime = time.time()
                        self.bfs_ElapsedTime = 0.0
                        self.bfs_finished = False
                        self.bfs_nodes_explored = 0
                if self.btn_ga.collidepoint(event.pos):
                    if self.MazeMatrix is not None:
                        self.dfs_gen = None
                        self.dfs_visited.clear()
                        self.dfs_path.clear()
                        self.BfsGenerator = None
                        self.BfsVisited.clear()
                        self.bfs_path.clear()
                        self.ga_gen = ga_generator(self.MazeMatrix, self.start, self.destination)
                        self.ga_visited.clear()
                        self.ga_path.clear()
                        self.ga_StartTime = time.time()
                        self.ga_ElapsedTime = 0.0
                        self.ga_finished = False
                        self.ga_nodes_explored = 0
            if event.type == pygame.KEYDOWN:
                if not self.is_game_active and self.WinningMessage == "":
                    self.is_game_active = True
                    self.StartTime = time.time()
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
            self.ElapsedTime = time.time() - self.StartTime

        if self.dfs_gen is not None:
            try:
                for _ in range(self.solver_step_per_frame):
                    ev = next(self.dfs_gen)
                    typ, node = ev
                    if typ == "visit":
                        self.dfs_visited.add(node)
                        self.dfs_nodes_explored += 1
                    elif typ == "path":
                        self.dfs_path.append(node)

            except StopIteration:
                
                self.dfs_gen = None
                self.dfs_ElapsedTime = time.time() - self.dfs_StartTime
                self.dfs_finished = True
        if self.BfsGenerator is not None:
            try:
                for _ in range(self.solver_step_per_frame):
                    ev = next(self.BfsGenerator)
                    typ, node = ev
                    if typ == "visit":
                        self.BfsVisited.add(node)
                        self.bfs_nodes_explored += 1
                    elif typ == "path":
                        self.bfs_path.append(node)
            except StopIteration:
                self.BfsGenerator = None
                self.bfs_ElapsedTime = time.time() - self.bfs_StartTime
                self.bfs_finished = True

        # advance GA
        if self.ga_gen is not None:
            try:
                for _ in range(self.solver_step_per_frame):
                    ev = next(self.ga_gen)
                    typ, node = ev
                    if typ == "visit":
                        self.ga_visited.add(node)
                        self.ga_nodes_explored += 1
                    elif typ == "path":
                        self.ga_path.append(node)
            except StopIteration:
                self.ga_gen = None
                self.ga_ElapsedTime = time.time() - self.ga_StartTime
                self.ga_finished = True

        if self.Player is not None:
            if (self.Player.cor_y, self.Player.cor_x) == self.destination:
                if self.is_game_active:
                    self.is_game_active = False
                    self.WinningMessage = f"You won! Time: {self.ElapsedTime:.2f}s"

    def draw_ui(self):
        # sidebar background
        sidebar_rect = pygame.Rect(self.MatrixColumns * self.CellSize, 0, self.SidebarWidth, self.MatrizRows * self.CellSize)
        pygame.draw.rect(self.SCREEN, (50, 50, 50), sidebar_rect)

        # Buttons
        pygame.draw.rect(self.SCREEN, self.color_regen, self.btn_regen)
        self.draw_text("Regenerate", self.SmallFont, (0, 0, 0), self.btn_regen.left + 10, self.btn_regen.top + 10)

        pygame.draw.rect(self.SCREEN, self.ColorDFS, self.ButtonDFS)

        self.draw_text("DFS", self.SmallFont, (255, 255, 255), self.ButtonDFS.centerx, self.ButtonDFS.centery, center=True)

        pygame.draw.rect(self.SCREEN, self.ColorBFS, self.ButtonBFS)

        self.draw_text("BFS", self.SmallFont, (0, 0, 0), self.ButtonBFS.centerx, self.ButtonBFS.centery, center=True)


        pygame.draw.rect(self.SCREEN, self.ColorGa, self.btn_ga)
        self.draw_text("GA", self.SmallFont, (0, 0, 0), self.btn_ga.centerx, self.btn_ga.centery, center=True)
        y_offset = self.btn_ga.bottom + 30
        if self.dfs_gen is not None:
            dfs_time = time.time() - self.dfs_StartTime
            self.draw_text(f"Depth First Search: {dfs_time:.2f}s", self.SmallFont, self.ColorDFS, 
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes: {self.dfs_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
        elif self.dfs_finished:
            self.draw_text(f"Depth First Search: {self.dfs_ElapsedTime:.2f}s ✓", self.SmallFont, (0, 255, 0),
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes traversed: {self.dfs_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
            path_len = len(self.dfs_path)
            self.draw_text(f"  Path traversed: {path_len}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 50)

        y_offset += 80
        if self.BfsGenerator is not None: 
            BfsTime = time.time() - self.bfs_StartTime
            self.draw_text(f"Breadth First Search: {BfsTime:.2f}s", self.SmallFont, self.ColorBFS,
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes: {self.bfs_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
            
        elif self.bfs_finished:
            self.draw_text(f"Breadth First Search: {self.bfs_ElapsedTime:.2f}s ✓", self.SmallFont, (0, 255, 0),
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes: {self.bfs_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
            path_len = len(self.bfs_path)
            self.draw_text(f"  Path: {path_len}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 50)
        y_offset += 80

        if self.ga_gen is not None:
            ga_time = time.time() - self.ga_StartTime
            self.draw_text(f"Genetic Algorithm: {ga_time:.2f}s", self.SmallFont, self.ColorGa,
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes: {self.ga_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
        elif self.ga_finished:
            self.draw_text(f"Genetic Algorithm: {self.ga_ElapsedTime:.2f}s ✓", self.SmallFont, (0, 255, 0),
                          self.MatrixColumns * self.CellSize + 20, y_offset)
            self.draw_text(f"  Nodes: {self.ga_nodes_explored}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 25)
            path_len = len(self.ga_path)
            self.draw_text(f"  Path: {path_len}", self.SmallFont, (200, 200, 200),
                          self.MatrixColumns * self.CellSize + 20, y_offset + 50)
        timer_text = f"Player: {self.ElapsedTime:.2f}s"
        self.draw_text(timer_text, self.Font, (255, 255, 255), self.MatrixColumns * self.CellSize + 20, 10)
        if self.WinningMessage:
            self.draw_text(self.WinningMessage, self.Font, (0, 255, 0), self.MatrixColumns * self.CellSize + 20, 40)

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.SCREEN.fill((100, 100, 100))
            self.draw_grid()
            if self.Player is not None:
                self.Player.draw(self.SCREEN, self.CellSize)
            self.draw_ui()
            pygame.display.flip()
            self.Clock.tick(60)
