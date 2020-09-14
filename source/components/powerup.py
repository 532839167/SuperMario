import pygame
from .. import setup, tools
from .. import constants as C

def create_powerup(center_x, center_y, type):
    # create powerups based on type and mario state
    return Mushroom(center_x, center_y)

class Powerup(pygame.sprite.Sprite):
    def __init__(self, center_x, center_y, frame_rects):
        pygame.sprite.Sprite.__init__(self)

        self.frames = []
        self.frame_index = 0
        for frame_rect in frame_rects:
            self.frames.append(tools.get_image(setup.GRAPHICS['item_objects'], *frame_rect, (0, 0, 0), 2.5))
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = center_x
        self.rect.centery = center_y
        self.origin_y = center_y - self.rect.height/2

        self.vx = 0
        self.direction = 1 # facing right
        self.vy = -1
        self.gravity = 1
        self.max_vy = 8

    def update_position(self, level):
        self.rect.x += self.vx
        self.check_x_collisions(level)
        self.rect.y += self.vy
        self.check_y_collisions(level)

        # kill if out of screen
        if self.rect.x < 0 or self.rect.y > C.SCREEN_H:
            self.kill()

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

class Mushroom(Powerup):
    def __init__(self, center_x, center_y):
        Powerup.__init__(self, center_x, center_y, [(0, 0, 16, 16)])
        self.vx = 2
        self.state = 'grow'
        self.name = 'mushroom'

    def update(self, level):
        if self.state == 'grow':
            self.rect.y += self.vy
            if self.rect.bottom < self.origin_y:
                self.state = 'walk'
        elif self.state == 'walk':
            pass
        elif self.state == 'fall':
            if self.vy < self.max_vy:
                self.vy += self.gravity

        if self.state != 'grow':
            self.update_position(level)

class LifeMushroom(Powerup):
    pass

class Fireball(Powerup):
    pass

class Star(Powerup):
    pass
