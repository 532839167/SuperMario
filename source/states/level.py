import pygame
from .. components import info
from .. import tools, setup
from .. import constants as C
from .. components import player
import os, json

class Level:
    def __init__(self):
        self.info = info.Info('level')
        self.load_map_data()
        self.finished = False
        self.next = None
        self.set_background()
        self.set_start_position()
        self.set_player()

    def set_background(self):
        self.image_name = self.map_data['image_name']
        self.background = setup.GRAPHICS[self.image_name]
        rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background, (int(rect.width * C.BACKGROUND_MULTI), int(rect.height * C.BACKGROUND_MULTI)))
        self.background_rect = self.background.get_rect()

        # The moving game window
        self.game_window = setup.SCREEN.get_rect()
        self.game_scene = pygame.Surface((self.background_rect.width, self.background_rect.height))

    def set_player(self):
        self.player = player.Player('mario')
        self.player.rect.x = self.game_window.x + self.player_x # 窗口的x坐标加上 player 的相对x坐标
        self.player.rect.bottom = self.player_y

    def load_map_data(self):
        file_name = 'level_1.json'
        file_path = os.path.join('source/data/maps', file_name)
        with open(file_path) as f:
            self.map_data = json.load(f)

    def set_start_position(self):
        self.positions = []
        for data in self.map_data['maps']:
            self.positions.append((data['start_x'], data['end_x'], data['player_x'], data['player_y']))
        self.start_x, self.end_x, self.player_x, self.player_y = self.positions[0]

    def update(self, surface, keys):
        self.player.update(keys)
        self.move_player()
        self.update_game_window()
        self.draw(surface)

    def move_player(self):
        self.player.rect.x += self.player.vx

        # 让 Mario 不能超过地图的末尾
        if self.player.rect.x < self.start_x:
             self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        # if self.player.rect.x > C.SCREEN_W - 16*C.PLAYER_MULTI:
        #     self.player.rect.x = C.SCREEN_W - 16*C.PLAYER_MULTI
        self.player.rect.y += self.player.vy

    def update_game_window(self):
        # When mario moves to the 1/3 of the screen, move background
        pos = self.game_window.x + self.game_window.width / 3
        if self.player.vx > 0 and self.player.rect.centerx > pos and self.game_window.right < self.end_x:
            self.game_window.x += self.player.vx
            self.start_x = self.game_window.x


    def draw(self, surface):
        self.game_scene.blit(self.background, self.game_window, self.game_window)
        self.game_scene.blit(self.player.img, self.player.rect)
        surface.blit(self.game_scene, (0, 0), self.game_window)
        self.info.draw(surface)