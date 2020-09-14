import pygame
from .. components import info
from .. import tools, setup
from .. import constants as C
from .. components import player, stuff, brick, box, enemy
import os, json

class Level:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = 'game_over'
        self.info = info.Info('level', self.game_info)
        self.load_map_data()
        self.set_background()
        self.set_start_position()
        self.set_player()
        self.set_ground_items()
        self.set_bricks_n_boxes()
        self.set_enemies()
        self.set_checkpoints()

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

    def set_ground_items(self):
        self.ground_items_group = pygame.sprite.Group()
        for name in ['ground', 'pipe', 'step']:
            for item in self.map_data[name]:
                self.ground_items_group.add(stuff.Item(item['x'], item['y'], item['width'], item['height'], name))

    def set_bricks_n_boxes(self):
        self.brick_group = pygame.sprite.Group()
        self.box_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.powerup_group = pygame.sprite.Group()

        if 'brick' in self.map_data:
            for brick_data in self.map_data['brick']:
                x, y = brick_data['x'], brick_data['y']
                brick_type = brick_data['type']
                if brick_type == 0:
                    if 'brick_num' in brick_data:
                        # batch bricks
                        pass
                    else:
                        self.brick_group.add(brick.Brick(x, y, brick_type, None))
                elif brick_type == 1:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.coin_group))
                else:
                    self.brick_group.add(brick.Brick(x, y, brick_type, self.powerup_group))

        if 'box' in self.map_data:
            for box_data in self.map_data['box']:
                x, y = box_data['x'], box_data['y']
                box_type = box_data['type']

                if box_type == 1:
                    self.box_group.add(box.Box(x, y, box_type, self.coin_group))
                else:
                    self.box_group.add(box.Box(x, y, box_type, self.powerup_group))

    def set_enemies(self):
        self.dead_enemy_group = pygame.sprite.Group()
        self.koopa_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.enemy_group_dict = {}
        for enemy_group_data in self.map_data['enemy']:
            group = pygame.sprite.Group()
            for enemy_group_id, enemy_list in enemy_group_data.items():
                for enemy_data in enemy_list:
                    group.add(enemy.create_enemy(enemy_data))
                self.enemy_group_dict[enemy_group_id] = group

    def set_checkpoints(self):
        self.checkpoint_group = pygame.sprite.Group()
        for item in self.map_data['checkpoint']:
            x, y, w, h = item['x'], item['y'], item['width'], item['height']
            checkpoint_type = item['type']
            enemy_groupid = item.get('enemy_groupid')
            self.checkpoint_group.add(stuff.Checkpoint(x, y, w, h, checkpoint_type, enemy_groupid))

    def update(self, surface, keys):
        self.current_time = pygame.time.get_ticks()
        self.player.update(keys)

        if self.player.dead:
            if self.current_time - self.player.death_timer > 3000:
                # dead over 3 seconds, finish game
                self.finished = True
                self.update_game_info()
        else:
            self.move_player()
            self.check_checkpoints()
            self.check_die()
            self.update_game_window()
            self.info.update()
            self.brick_group.update()
            self.box_group.update()
            self.enemy_group.update(self)
            self.dead_enemy_group.update(self)
            self.koopa_group.update(self)
            self.coin_group.update()
            self.powerup_group.update(self)

        self.draw(surface)

    def move_player(self):
        self.player.rect.x += self.player.vx

        # 让 Mario 不能超过地图的末尾
        if self.player.rect.x < self.start_x:
             self.player.rect.x = self.start_x
        elif self.player.rect.right > self.end_x:
            self.player.rect.right = self.end_x
        self.check_x_collisions()

        # if self.player.rect.x > C.SCREEN_W - 16*C.PLAYER_MULTI:
        #     self.player.rect.x = C.SCREEN_W - 16*C.PLAYER_MULTI
        # y direction
        if not self.player.dead:
            self.player.rect.y += self.player.vy
            self.check_y_collisions()

    def check_x_collisions(self):
        check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided = pygame.sprite.spritecollideany(self.player, check_group)
        # ground_items != null
        if collided:
            self.adjust_player_x(collided)

        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)
        if enemy:
            self.player.set_die()

        koopa = pygame.sprite.spritecollideany(self.player, self.koopa_group)
        if koopa:
            if self.player.rect.x < koopa.rect.x:
                koopa.vx = 10
                koopa.rect.x += 40
                koopa.direction = 1
            else:
                koopa.vx = -10
                koopa.rect.x += -40
                koopa.direction = 0
            koopa.state = 'slide'

        powerup = pygame.sprite.spritecollideany(self.player, self.powerup_group)
        if powerup:
            powerup.kill()
            if powerup.name == 'mushroom':
                self.player.state = 'small2big'

    def check_y_collisions(self):
        # check_group = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        ground_item = pygame.sprite.spritecollideany(self.player, self.ground_items_group)
        brick = pygame.sprite.spritecollideany(self.player, self.brick_group)
        box = pygame.sprite.spritecollideany(self.player, self.box_group)
        enemy = pygame.sprite.spritecollideany(self.player, self.enemy_group)

        # collided = pygame.sprite.spritecollideany(self.player, check_group)
        # # ground_items != null
        # if collided:
        #     self.adjust_player_y(collided)
        if brick and box:
            distance_to_brick = abs(self.player.rect.centerx - brick.rect.centerx)
            distance_to_box = abs(self.player.rect.centerx - box.rect.centerx)
            if distance_to_brick > distance_to_box:
                brick = None
            else:
                box = None

        if ground_item:
            self.adjust_player_y(ground_item)
        elif brick:
            self.adjust_player_y(brick)
        elif box:
            self.adjust_player_y(box)
        elif enemy:
            self.enemy_group.remove(enemy)
            if enemy.name == 'koopa':
                self.koopa_group.add(enemy)
            else:
                self.dead_enemy_group.add(enemy)
            if self.player.vy < 0:
                death = 'bumped'
            else:
                death = 'trampled'
                self.player.state = 'jump'
                self.player.rect.bottom = enemy.rect.top
                self.player.vy = self.player.jump_speed * 0.8
            enemy.set_die(death)

        self.check_fall(self.player)

    def adjust_player_x(self, sprite):
        # hit item from left
        if self.player.rect.x < sprite.rect.x:
            self.player.rect.right = sprite.rect.left
        else:
            # hit item from right
            self.player.rect.left = sprite.rect.right

        self.player.vx = 0

    def adjust_player_y(self, sprite):
        # hit item from top
        if self.player.rect.bottom < sprite.rect.bottom:
            self.player.vy = 0
            self.player.rect.bottom = sprite.rect.top
            self.player.state = 'walk'
        else:
            # hit item from underneath
            self.player.vy = 7 # bounce back
            self.player.rect.top = sprite.rect.bottom
            self.player.state = 'fall'

            if sprite.name == 'box':
                if sprite.state == 'rest':
                    sprite.get_bumped()

            if sprite.name == 'brick':
                if sprite.state == 'rest':
                    sprite.get_bumped()

    def check_fall(self, sprite):
        sprite.rect.y += 1
        check = pygame.sprite.Group(self.ground_items_group, self.brick_group, self.box_group)
        collided = pygame.sprite.spritecollideany(sprite, check)
        if not collided and sprite.state != 'jump':
            sprite.state = 'fall'
        sprite.rect.y -= 1

    def update_game_window(self):
        # When mario moves to the 1/3 of the screen, move background
        pos = self.game_window.x + self.game_window.width / 3
        if self.player.vx > 0 and self.player.rect.centerx > pos and self.game_window.right < self.end_x:
            self.game_window.x += self.player.vx
            self.start_x = self.game_window.x

    def draw(self, surface):
        self.game_scene.blit(self.background, self.game_window, self.game_window)
        self.game_scene.blit(self.player.img, self.player.rect)
        self.powerup_group.draw(self.game_scene)
        self.brick_group.draw(self.game_scene)
        self.box_group.draw(self.game_scene)
        self.enemy_group.draw(self.game_scene)
        self.dead_enemy_group.draw(self.game_scene)
        self.koopa_group.draw(self.game_scene)
        self.coin_group.draw(self.game_scene)


        surface.blit(self.game_scene, (0, 0), self.game_window)
        self.info.draw(surface)

    def check_checkpoints(self):
        checkpoint = pygame.sprite.spritecollideany(self.player, self.checkpoint_group)
        if checkpoint:
            if checkpoint.checkpoint_type == 0:
                self.enemy_group.add(self.enemy_group_dict[str(checkpoint.enemy_groupid)])
            checkpoint.kill() # once a checkpoint is passed, it get killed

    def check_die(self):
        if self.player.rect.y > C.SCREEN_H:
            # if mario drop out of the screen, die
            self.player.set_die()

    def update_game_info(self):
        if self.player.dead:
            self.game_info['lives'] -= 1
        if self.game_info['lives'] == 0:
            self.next = 'game_over'
        else:
            self.next = 'load_screen'