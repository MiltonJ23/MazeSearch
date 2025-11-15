import pygame, sys 
from pygame.locals import *  # type: ignore
from Game.game import Game




if __name__ == "__main__":
    # Taille du labyrinthe en cellules "logiques"
    GRID_ROWS = 10
    GRID_COLS = 14
    CELL_SIZE = 22

    game = Game(GRID_ROWS, GRID_COLS, CELL_SIZE)
    game.new_game()
    game.run()