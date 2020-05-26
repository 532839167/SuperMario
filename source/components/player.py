import pygame
from .. import tools, setup
from .. import constants as C
import json
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.load_data()
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

        self.frame_index = 0
        self.img = self.frames[self.frame_index]
        self.rect = self.img.get_rect()

    # load player data from json files
    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)


    def setup_states(self):
        self.state = 'walk'
        self.forward = True # If the figure is moving forward
        self.dead = False
        self.big = False

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.vx = 0
        self.vy = 0

        self.max_walk_speed = speed['max_walk_speed']
        self.max_run_speed = speed['max_run_vel']
        self.max_y_speed = speed['max_y_velocity']
        self.jump_speed = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.turn_accel = speed['turn_accel']
        self.run_accel = speed['run_accel']
        self.gravity = C.GRAVITY

        self.max_x_speed = self.max_walk_speed
        self.x_accel = self.walk_accel


    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0

    def load_images(self):
        figure = setup.GRAPHICS['mario_bros']
        frame_rects = self.player_data['image_frames']

        self.right_small_normal_frames = []
        self.right_big_normal_frames = []
        self.right_big_fire_frames = []
        self.left_small_normal_frames = []
        self.left_big_normal_frames = []
        self.left_big_fire_frames = []

        self.small_normal_frames = [self.right_small_normal_frames, self.left_small_normal_frames]
        self.big_normal_frames = [self.right_big_normal_frames, self.left_big_normal_frames]
        self.big_fire_frames = [self.right_big_fire_frames, self.left_big_fire_frames]

        self.all_frames = [self.right_small_normal_frames, self.right_big_normal_frames, self.right_big_fire_frames, self.left_small_normal_frames, self.left_big_normal_frames, self.left_big_fire_frames]

        # default frames
        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames

        for group, group_frame_rects in frame_rects.items():
            for frame_rect in group_frame_rects:
                right_img = tools.get_image(figure, frame_rect['x'], frame_rect['y'], frame_rect['width'], frame_rect['height'], (0, 0, 0), C.PLAYER_MULTI)
                left_img = pygame.transform.flip(right_img, True, False)

                if group == 'right_small_normal':
                    self.right_small_normal_frames.append(right_img)
                    self.left_small_normal_frames.append(left_img)
                if group == 'right_big_normal':
                    self.right_big_normal_frames.append(right_img)
                    self.left_big_normal_frames.append(left_img)
                if group == 'right_big_fire':
                    self.right_big_fire_frames.append(right_img)
                    self.left_big_fire_frames.append(left_img)

        # self.frames.append(tools.get_image(figure, 178, 32, 12, 16, (0, 0, 0), C.BACKGROUND_MULTI))

        self.frame_index = 0
        self.frames = self.right_frames
        self.img = self.frames[self.frame_index]
        self.rect = self.img.get_rect()

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            self.state = 'walk'
            self.vx = 5
            self.vy = 0
            self.frames = self.right_frames
        if keys[pygame.K_LEFT]:
            self.state = 'walk'
            self.vx = -5
            self.vy = 0
            self.frames = self.left_frames

        # jump
        if keys[pygame.K_SPACE]:
            self.state = 'jump'
            self.vy = -5

        # change picture every 100ms
        if self.state == 'walk':
            if self.current_time - self.walking_timer > 100:
                self.walking_timer = self.current_time
                self.frame_index += 1
                self.frame_index %= 4
        if self.state == 'jump':
            self.frame_index = 4
        self.img = self.frames[self.frame_index]