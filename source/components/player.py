import pygame
from .. import tools, setup
from .. import constants as C

class Player(pygame.sprite.Sprite):
    def __init__(self, name):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.setup_states()
        self.setup_velocities()
        self.setup_timers()
        self.load_images()

        self.frame_index = 0
        self.img = self.frames[self.frame_index]
        self.rect = self.img.get_rect()

    def setup_states(self):
        self.forward = True # If the figure is moving forward
        self.dead = False
        self.big = False

    def setup_velocities(self):
        self.vx = 0
        self.vy = 0

    def setup_timers(self):
        self.walking_timer = 0
        self.transition_timer = 0

    def load_images(self):
        figure = setup.GRAPHICS['mario_bros']

        self.right_frames = []
        self.left_frames = []
        self.up_frames = []
        self.down_frames = []

        frame_rects = [(178, 32, 12, 16), (80, 32, 15, 16), (96, 32, 16, 16), (112, 32, 16, 16)]

        for r in frame_rects:
            right_img = tools.get_image(figure, *r, (0, 0, 0), C.BACKGROUND_MULTI)
            left_img = pygame.transform.flip(right_img, True, False)
            up_img = pygame.transform.rotate(right_img, 90)
            down_img = pygame.transform.rotate(right_img, -90)
            # add img to the list
            self.right_frames.append(right_img)
            self.left_frames.append(left_img)
            self.up_frames.append(up_img)
            self.down_frames.append(down_img)

        # self.frames.append(tools.get_image(figure, 178, 32, 12, 16, (0, 0, 0), C.BACKGROUND_MULTI))

        self.frame_index = 0
        self.frames = self.right_frames
        self.img = self.frames[self.frame_index]
        self.rect = self.img.get_rect()

    def update(self, keys):
        self.current_time = pygame.time.get_ticks()
        if keys[pygame.K_RIGHT]:
            self.vx = 5
            self.vy = 0
            self.frames = self.right_frames
        if keys[pygame.K_LEFT]:
            self.vx = -5
            self.vy = 0
            self.frames = self.left_frames
        if keys[pygame.K_UP]:
            self.vx = 0
            self.vy = -5
            self.frames = self.up_frames
        if keys[pygame.K_DOWN]:
            self.vx = 0
            self.vy = 5
            self.frames = self.down_frames

        # change picture every 100ms
        if self.current_time - self.walking_timer > 100:
            self.walking_timer = self.current_time
            self.frame_index += 1
            self.frame_index %= 4
        self.img = self.frames[self.frame_index]