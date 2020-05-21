import pygame
from .. components import info
from .. import tools, setup
from .. import constants as C

class Level:
    def __init__(self):
        self.info = info.Info('level')
        self.finished = False
        self.next = None
        self.set_background()

    def set_background(self):
        self.background = setup.GRAPHICS['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BACKGROUND_MULTI), int(rect.height * C.BACKGROUND_MULTI)))
        self.background_rect = self.background.get_rect()


    def update(self, surface, keys):
        self.draw(surface)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        self.info.draw(surface)