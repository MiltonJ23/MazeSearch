import pygame, sys 
from pygame.locals import * 


pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((799,599)) # Let's dfine the size of the window 

background = pygame.color.Color(43,233,23) # defining a color for the background 

while True:
    surface.fill(background)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(30)