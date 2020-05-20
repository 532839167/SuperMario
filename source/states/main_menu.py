import pygame
from .. import setup
from .. import tools
from .. import constants as C
from .. components import info


class MainMenu:
    def __init__(self):
        self.setup_background()
        self.setup_player()
        self.setup_cursor()
        self.info = info.Info('main_menu')


    def setup_background(self):
        self.background = setup.GRAPHICS['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(self.background_rect.width * C.BACKGROUND_MULTI), int(self.background_rect.height * C.BACKGROUND_MULTI)))

        # current view box
        self.view = setup.SCREEN.get_rect()

        # main menu banner
        # coordinate: (1, 60), width: 716, height: 88, base color: 255, 0, 220
        self.banner = tools.get_image(setup.GRAPHICS['title_screen'], 1, 60, 176, 88, (255, 0, 220), C.BACKGROUND_MULTI)


    def setup_player(self):
        # the player: coordinate: (178, 32), width: 12, height: 16, base color: 0, 0, 0
        self.figure = tools.get_image(setup.GRAPHICS['mario_bros'], 178, 32, 12, 16, (0, 0, 0), C.BACKGROUND_MULTI)

    def setup_cursor(self):
        self.cursor = tools.get_image(setup.GRAPHICS['item_objects'], 25, 160, 8, 8, (0, 0, 0), C.BACKGROUND_MULTI)

    def update(self, surface):
        surface.blit(self.background, self.view)
        surface.blit(self.banner, (170, 100))
        surface.blit(self.figure, (110, 490))
        surface.blit(self.cursor, (220, 360))

        self.info.update()
        self.info.draw(surface)