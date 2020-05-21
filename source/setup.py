import pygame
from . import constants as C
from . import tools

# initialize game panel
pygame.init()
SCREEN = pygame.display.set_mode((C.SCREEN_W, C.SCREEN_H))
pygame.display.set_caption("Super Mario! ")

GRAPHICS = tools.load_graphics('resources/graphics')