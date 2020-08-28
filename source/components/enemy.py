import pygame
from .. import tools, setup
from .. import constants as C

def create_enemy(enemy_data):
    enemy_type = enemy_data['type']
    x, y_bottom, direction, color = enemy_data['x'], enemy_data['y'], enemy_data['direction'], enemy_data['color']

    if enemy_type == 0:
        enemy = Goomba(x, y_bottom, direction, "goomba", color)
    elif enemy_type == 1:
        enemy = Koopa(x, y_bottom, direction, "koopa", color)

    return enemy

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y_bottom, direction, name, frame_rects):
        pygame.sprite.Sprite.__init__(self)
        self.direction = direction
        self.name = name
        self.frame_index = 0
        self.left_frames = []
        self.right_frames = []

        self.load_frames(frame_rects)
        self.frames = self.left_frames if self.direction == 0 else self.right_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y_bottom

        self.timer = 0
        self.vx = -1 * C.ENEMY_SPEED if self.direction == 0 else C.ENEMY_SPEED
        self.vy = 0
        self.gravity = C.GRAVITY
        self.state = 'walk'

    def load_frames(self, frame_rects):
        for frame_rect in frame_rects:
            left_frame = tools.get_image(setup.GRAPHICS['enemies'], *frame_rect, (0, 0, 0), C.ENEMY_MULTI)
            right_frame = pygame.transform.flip(left_frame, True, False)
            self.left_frames.append(left_frame)
            self.right_frames.append(right_frame)

    def update(self, level):
        self.current_time = pygame.time.get_ticks()
        self.states_actions()
        self.update_position(level)

    def states_actions(self):

        if self.state == 'walk':
            self.walk()
        elif self.state == 'fall':
            self.fall()
        elif self.state == 'die':
            self.die()
        elif self.state == 'trampled':
            self.trampled()
        elif self.state == 'slide':
            self.slide()

        if self.direction:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]

    def walk(self):
        if self.current_time - self.timer > 125:
            self.frame_index = (self.frame_index + 1) % 2
            self.image = self.frames[self.frame_index]
            self.timer = self.current_time

    def fall(self):
        if self.vy < 10:
            self.vy += self.gravity

    def die(self):
        self.rect.x += self.vx
        self.rect.y += self.vy
        self.vy += self.gravity
        if self.rect.y > C.SCREEN_H:
            self.kill()

    def trampled(self):
        pass

    def slide(self):
        pass

    def update_position(self, level):
        self.rect.x += self.vx
        self.check_x_collisions(level)
        self.rect.y += self.vy
        if self.state != 'die':
            self.check_y_collisions(level)

    def check_x_collisions(self, level):
        collided = pygame.sprite.spritecollideany(self, level.ground_items_group)
        if collided:
            # change direction
            # self.direction = 1 if self.direction == 0 else 0
            if self.direction: # right
                self.direction = 0
                self.rect.right = collided.rect.left
            else:
                self.direction = 1
                self.rect.left = collided.rect.right
            self.vx *= -1

    def check_y_collisions(self, level):
        obstacles = pygame.sprite.Group(level.ground_items_group, level.brick_group, level.box_group)
        collided = pygame.sprite.spritecollideany(self, obstacles)
        if collided:
            if self.rect.top < collided.rect.top:
                self.rect.bottom = collided.rect.top
                self.vy = 0
                self.state = 'walk'

        level.check_fall(self)

    def set_die(self, death):
        self.death_timer = self.current_time
        if death == 'bumped':
            self.vy = -8
            self.gravity = 0.6
            self.state = 'die'
            self.frame_index = 0
        elif death == 'trumpled':
            self.state = 'trumpled'


class Goomba(Enemy):
    def __init__(self, x, y_bottom, direction, name, color):
        bright_frame_rects = [(0, 16, 16, 16), (16, 16, 16, 16), (32, 16, 16, 16)]
        dark_frame_rects = [(0, 48, 16, 16), (16, 48, 16, 16), (32, 48, 16, 16)]

        if not color:
            # default is bright
            frame_rects = bright_frame_rects
        else:
            frame_rects = dark_frame_rects

        Enemy.__init__(self, x, y_bottom, direction, name, frame_rects)

    def trampled(self):
        self.vx = 0
        # self.frame_index = 2
        if self.death_timer == 0:
            self.death_timer = self.current_time
        if self.current_time - self.death_timer > 500:
            self.kill()

class Koopa(Enemy):
    def __init__(self, x, y_bottom, direction, name, color):
        bright_frame_rects = [(96, 9, 16, 22), (112, 9, 16, 22), (160, 9, 16, 22)]
        dark_frame_rects = [(96, 72, 16, 22), (112, 72, 16, 22), (160, 72, 16, 22)]

        if not color:
            # default is bright
            frame_rects = bright_frame_rects
        else:
            frame_rects = dark_frame_rects

        Enemy.__init__(self, x, y_bottom, direction, name, frame_rects)

        def trampled(self):
            self.vx = 0
            # self.frame_index = 2

        def slide(self):
            pass