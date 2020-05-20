import pygame
from .. import constants as C
from . import coin
pygame.font.init()

class Info:
    def __init__(self, state):
        self.state = state
        self.create_caption()
        self.create_info_labels()
        self.coin = coin.FlashingCoin()

    def create_caption(self):
        self.state_captions = []
        if self.state == 'main_menu':
            self.state_captions.append((self.create_label('1  PLAYER  GAME'), (272, 360)))
            self.state_captions.append((self.create_label('2  PLAYER  GAME'), (272, 405)))
            self.state_captions.append((self.create_label('TOP - '), (290, 465)))
            self.state_captions.append((self.create_label('000000'), (400, 465)))


    def create_info_labels(self):
        self.info_labels = []
        self.state_captions.append((self.create_label('MARIO'), (75, 30)))
        self.state_captions.append((self.create_label('WORLD'), (450, 30)))
        self.state_captions.append((self.create_label('TIME'), (625, 30)))
        self.state_captions.append((self.create_label('000000'), (75, 55)))
        self.state_captions.append((self.create_label('x00'), (300, 55)))
        self.state_captions.append((self.create_label('1  -  1'), (480, 55)))

    # 字体 → 文字 → 图片
    def create_label(self, label, size = 40, width_scale = 1.25, height_scale = 1):
        font = pygame.font.SysFont(C.FONT, size)
        # 文字 → 图片
        pic = font.render(label, 1, (225, 225, 225))

        return pic

    def update(self):
        self.coin.update()

    def draw(self, surface):
        for caption in self.state_captions:
            surface.blit(caption[0], caption[1])

        for label in self.info_labels:
            surface.blit(label[0], label[1])

        surface.blit(self.coin.img, self.coin.rect)