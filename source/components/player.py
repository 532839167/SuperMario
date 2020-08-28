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

        # self.frame_index = 0
        # self.img = self.frames[self.frame_index]
        # self.rect = self.img.get_rect()

    # load player data from json files
    def load_data(self):
        file_name = self.name + '.json'
        file_path = os.path.join('source/data/player', file_name)
        with open(file_path) as f:
            self.player_data = json.load(f)


    def setup_states(self):
        self.state = 'stand'
        self.forward = True # If the figure is moving forward
        self.dead = False
        self.big = False
        self.can_jump = True

    def setup_velocities(self):
        speed = self.player_data['speed']
        self.vx = 0
        self.vy = 0

        self.max_walk_speed = speed['max_walk_speed']
        self.max_run_speed = speed['max_run_speed']
        self.max_y_speed = speed['max_y_velocity']
        self.jump_speed = speed['jump_velocity']
        self.walk_accel = speed['walk_accel']
        self.turn_accel = speed['turn_accel']
        self.run_accel = speed['run_accel']
        self.gravity = C.GRAVITY
        self.anti_gravity = C.ANTI_GRAVITY

        self.max_x_speed = self.max_walk_speed
        self.x_accel = self.walk_accel


    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0
        self.death_timer = 0

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
        self.states_actions(keys)

    def states_actions(self, keys):

        self.can_jump_or_not(keys)

        if self.state == 'stand':
            self.stand(keys)
        elif self.state == 'walk':
            self.walk(keys)
        elif self.state == 'jump':
            self.jump(keys)
        elif self.state == 'fall':
            self.fall(keys)
        elif self.state == 'die':
            self.die(keys)

        if self.forward:
            self.img = self.right_frames[self.frame_index]
        else:
            self.img = self.left_frames[self.frame_index]

    def can_jump_or_not(self, keys):
        if not keys[pygame.K_SPACE]:
            self.can_jump = True

    def stand(self, keys):
        # speed set to 0
        self.frame_index = 0
        self.vx = 0
        self.vy = 0
        if keys[pygame.K_RIGHT]:
            self.forward = True
            self.state = 'walk'
        elif keys[pygame.K_LEFT]:
            self.forward = False
            self.state = 'walk'
        elif keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'     # press space to jump
            self.vy = self.jump_speed

    def walk(self, keys):

        # press s to sprint
        if keys[pygame.K_s]:
            self.max_x_speed = self.max_run_speed
            self.x_accel = self.run_accel
        else:
            self.max_x_speed = self.max_walk_speed
            self.x_accel = self.walk_accel

        if keys[pygame.K_SPACE] and self.can_jump:
            self.state = 'jump'
            self.vy = self.jump_speed

        # [1, 3]
        if self.current_time - self.walking_timer > self.calc_frame_duration():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time

        if keys[pygame.K_RIGHT]:
            self.forward = True
            if self.vx < 0:
                # Mario is moving backwards
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, True)
        elif keys[pygame.K_LEFT]:
            self.forward = False
            if self.vx > 0:
                self.frame_index = 5
                self.x_accel = self.turn_accel
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, False)
        else:
            if self.forward:
                self.vx -= self.x_accel
                if self.vx < 0:
                    self.vx = 0
                    self.state = 'stand'
            else:
                self.vx += self.x_accel
                if self.vx > 0:
                    self.vx = 0
                    self.state = 'stand'

    def jump(self, keys):
        self.frame_index = 4
        self.vy += self.anti_gravity  # 跳起时 y 速度的变化
        self.can_jump = False

        if self.vy >= 0:         # start to fall
            self.state = 'fall'

        # move horizontally while jumping
        if keys[pygame.K_RIGHT]:
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, True)
        elif keys[pygame.K_LEFT]:
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, False)

        if not keys[pygame.K_SPACE]:
            self.state = 'fall'

    def fall(self, keys):
        self.vy = self.calc_vel(self.vy, self.gravity, self.max_y_speed)

        # # fall on the ground
        # if self.rect.bottom > C.GROUNG_HEIGHT:  # Maria is lower than ground level
        #     self.rect.bottom = C.GROUNG_HEIGHT
        #     self.vy = 0
        #     self.state = 'walk'

        # move horizontally while jumping
        if keys[pygame.K_RIGHT]:
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, True)
        elif keys[pygame.K_LEFT]:
            self.vx = self.calc_vel(self.vx, self.x_accel, self.max_x_speed, False)

    def die(self, keys):
        self.rect.y += self.vy
        self.vy += self.anti_gravity

    def set_die(self):
        self.dead = True
        self.vy = self.jump_speed
        self.frame_index = 6
        self.state = 'die'
        self.death_timer = self.current_time

    def calc_vel(self, vel, accel, max_vel, is_positive = True):
        if is_positive:
            return min(vel + accel, max_vel)
        else:
            return max(vel - accel, -max_vel)

    # 根据当前速度计算切换帧的频率（摆臂的频率）
    def calc_frame_duration(self):
        duration = -60 / self.max_run_speed * abs(self.vx) + 80
        return duration