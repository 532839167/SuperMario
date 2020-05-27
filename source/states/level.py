import pygame
from .. components import info
from .. import tools, setup
from .. import constants as C
from .. components import player

class Level:
    def __init__(self):
        self.info = info.Info('level')
        self.finished = False
        self.next = None
        self.set_background()
        self.set_player()

    def set_background(self):
        self.background = setup.GRAPHICS['level_1']
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BACKGROUND_MULTI), int(rect.height * C.BACKGROUND_MULTI)))
        self.background_rect = self.background.get_rect()

    def set_player(self):
        self.player = player.Player('mario')
        self.player.rect.x = 300
        self.player.rect.y = 490

    def update(self, surface, keys):
        self.player.update(keys)
        self.move_player()
        self.draw(surface)

    def move_player(self):
        self.player.rect.x += self.player.vx
        self.player.rect.y += self.player.vy

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.player.img, self.player.rect)
        self.info.draw(surface)