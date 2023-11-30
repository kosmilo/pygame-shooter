from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, game):
        self.game = game
        pg.mouse.set_visible(False)
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = 10000

        self.target_positions = [(6, 6), (12, 6), 'stop', (5, 6), 'stop', (8, 4), (1, 1)]
        self.current_point_index = 0
        self.wait_tracker = 0

        # Set to avoid errors
        self.rel = 0

    def check_game_over(self):
        if self.health < 1:
            print('GAME OVER')

    def get_damage(self, damage):
        self.health -= damage
        self.check_game_over()

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.shot and not self.game.weapon.reloading:
                # self.game.sound.weapon.play()
                self.shot = True
                self.game.weapon.reloading = True

    def movement(self):
        # Calc angle and speed
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        self.check_wall_collision(dx, dy)

        self.angle %= math.tau

    def move_in_direction(self, direction):
        dx, dy = 0, 0
        speed = PLAYER_SPEED * self.game.delta_time
        # sin(0) is always 0, cos(0) is always 1
        speed_sin = speed * 0
        speed_cos = speed * 1

        if direction == 'pos_x':
            dx += speed_cos
            dy += speed_sin
        elif direction == 'neg_x':
            dx += -speed_cos
            dy += -speed_sin
        elif direction == 'pos_y':
            dx += -speed_sin
            dy += speed_cos
        elif direction == 'neg_y':
            dx += speed_sin
            dy += -speed_cos

        self.check_wall_collision(dx, dy)

    def decide_direction(self, coords):
        new_x, new_y = coords
        cur_x, cur_y = self.pos

        if new_x - cur_x > 0.01:
            self.move_in_direction('pos_x')
        elif new_x - cur_x < -0.01:
            self.move_in_direction('neg_x')

        if new_y - cur_y > 0.01:
            self.move_in_direction('pos_y')
        elif new_y - cur_y < -0.01:
            self.move_in_direction('neg_y')

    def move_to_target_positions(self):
        if self.current_point_index < len(self.target_positions):
            next_coords = self.target_positions[self.current_point_index]
            if next_coords == 'stop':
                self.pause_movement_for_seconds(5)
            else:
                self.decide_direction(next_coords)
                if self.calculate_distance_to_next_pos() < 0.05:
                    self.current_point_index += 1

    def pause_movement_for_seconds(self, wait_seconds):
        wait_milliseconds = wait_seconds * 1000
        self.wait_tracker += self.game.clock.get_time()
        if self.wait_tracker > wait_milliseconds:
            self.wait_tracker = 0
            self.current_point_index += 1

    def calculate_distance_to_next_pos(self):
        cur_x, cur_y = self.pos
        new_x, new_y = self.target_positions[self.current_point_index]
        distance = math.sqrt((cur_x - new_x)**2 + (cur_y - new_y)**2)
        return distance

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map

    def check_wall_collision(self, dx, dy):
        scale = PLAYER_SIZE / self.game.delta_time
        if self.check_wall(int(self.x + dx * scale), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy * scale)):
            self.y += dy

    def draw(self):
        # pg.draw.line(self.game.screen, 'yellow', (self.x * 100, self.y * 100),
        #             (self.x * 100 + WIDTH * math.cos(self.angle),
        #              self.y * 100 + WIDTH * math.sin(self.angle)), 2)
        # pg.draw.circle(self.game.screen, "green", (self.x * 100, self.y * 100), 15)
        pass

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def update(self):
        self.movement()
        # self.move_to_target_positions()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
