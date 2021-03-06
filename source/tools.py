import pygame
import random
import os

class Game:

    def __init__(self, states, inital_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.keys = pygame.key.get_pressed()
        self.states = states
        self.state = self.states[inital_state]

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state =self.state.next
            self.state.finished = False
            self.state = self.states[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.keys)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.keys = pygame.key.get_pressed()
                elif event.type == pygame.KEYUP:
                    self.keys = pygame.key.get_pressed()

            self.update()

            pygame.display.update()
            self.clock.tick(60)

# load all graphics in a dictionary
def load_graphics(path, accept = ( '.jpg', '.png', '.bmp', '.gif')):
    graphics = {}
    for p in os.listdir(path):
        # split file names in two part: name + extension
        name, ext = os.path.splitext(p)

        # if extension is in accept
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, p))
            # convert image format
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics

# get figures in an image
# x, y: coordinates of the figure
# w, h: size of the figure
# color: base color // scale: resize scale
def get_image(source_pic, x, y, w, h, color, scale):
    # create a new image with width = w, height = h
    img = pygame.Surface((w, h))
    # from position (0, 0), draw figure (x, y, w, h) in source picture
    img.blit(source_pic, (0, 0), (x, y, w, h))
    # cut figure
    img.set_colorkey(color)
    # resize
    img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img
