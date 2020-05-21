from .. components import info
import pygame

# load screen of the game. Show game information before game starts

class LoadScreen:
    def __init__(self):
        self.info = info.Info('load_screen')
        self.finished = False
        self.next = 'level'
        self.timer = 0

    def update(self, surface, keys):
        self.draw(surface)
        # enter next state after 2s
        if self.timer == 0:
            self.timer = pygame.time.get_ticks()
        elif pygame.time.get_ticks() - self.timer > 2000:
            self.finished = True
            self.timer = 0

    def draw(self, surface):
        surface.fill((0, 0, 0)) # black
        self.info.draw(surface)