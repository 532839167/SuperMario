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
        self.finished = False # If the main menu is finished (enter the game)
        self.next = 'load_screen' # After finishing main menu, the game is loaded


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
        self.cursor = pygame.sprite.Sprite()
        self.cursor.img = tools.get_image(setup.GRAPHICS['item_objects'], 25, 160, 8, 8, (0, 0, 0), C.BACKGROUND_MULTI)
        rect = self.cursor.img.get_rect()
        rect.x, rect.y = (220, 360)
        self.cursor.rect = rect
        # initialize the state of cursor
        self.cursor.state = '1P'

    def update_cursor(self, keys):
        if keys[pygame.K_UP]:
            self.cursor.state = '1P'
            self.cursor.rect.y = 360
        elif keys[pygame.K_DOWN]:
            self.cursor.state = '2P'
            self.cursor.rect.y = 405
        elif keys[pygame.K_RETURN]:
            # press enter then load the game scene
            if self.cursor.state == '1P':
                self.finished = True
            elif self.cursor.state == '2P':
                self.finished = True


    def update(self, surface, keys):

        self.update_cursor(keys)

        surface.blit(self.background, self.view)
        surface.blit(self.banner, (170, 100))
        surface.blit(self.figure, (110, 490))
        # surface.blit(self.cursor.img, (220, 360))
        surface.blit(self.cursor.img, self.cursor.rect)

        self.info.update()
        self.info.draw(surface)