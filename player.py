from settings import *
import pygame as pg
import math


class HealthBar:
    def __init__(self, player):
        self.player = player
        self.max_health = player.health
        self.width = 100  
        self.height = 10  
        self.health_bar_color = (0, 255, 0)  
        self.border_color = (255, 255, 255)  

    def update(self):
        health_percentage = max(0, self.player.health / self.max_health)
        self.width = int(health_percentage * 100)

    def draw(self, screen):
         x = (screen.get_width() - self.width) // 2
         y = 10
         
         pg.draw.rect(screen, self.health_bar_color, (x, y, self.width, self.height))
         pg.draw.rect(screen, self.border_color, (x, y, 100, self.height), 2)

        
class Player:
    def __init__(self, game):
        self.game = game
        pg.mouse.set_visible(False)
        self.x, self.y = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.shot = False
        self.health = 40

        self.target_positions = [((2, 2), (2, 4), (5, 4), (5, 6)),
                                 ((7, 6), (10, 6)),
                                 ((6, 6), (6, 4))]
        self.cur_point_in = 0  # current point index
        self.cur_track_in = 0  # current track index
        self.wait_tracker = 0
        
        self.moving = False
        self.auto_rotate = True  # camera rotation use mouse or automate

        # Set to avoid errors
        self.rel = 0
        
        self.health_bar = HealthBar(self)

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
        if self.cur_track_in < len(self.target_positions):
            if self.cur_point_in < len(self.target_positions[self.cur_track_in]):
                next_coords = self.target_positions[self.cur_track_in][self.cur_point_in]
                if next_coords == 'stop':
                    self.pause_movement_for_seconds(5)
                else:
                    self.decide_direction(next_coords)
                    if self.calculate_distance_to_next_pos() < 0.05:
                        print('move to next coords')
                        self.cur_point_in += 1
            else:
                print('cur point in not in target positions cur track')
                self.moving = False
                self.cur_track_in += 1
                self.cur_point_in = 0
                self.game.wave_manager.start_wave()

    def pause_movement_for_seconds(self, wait_seconds):
        wait_milliseconds = wait_seconds * 1000
        self.wait_tracker += self.game.delta_time
        if self.wait_tracker > wait_milliseconds:
            self.wait_tracker = 0
            self.cur_point_in += 1

    def calculate_distance_to_next_pos(self):
        cur_x, cur_y = self.pos
        new_x, new_y = self.target_positions[self.cur_track_in][self.cur_point_in]

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
        self.health_bar.draw(self.game.screen)

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * MOUSE_SENSITIVITY * self.game.delta_time

    def auto_rotate_camera(self):
        if self.game.object_handler.npc_list:
            avg_npc_pos = (
                sum(npc.map_pos[0] for npc in self.game.object_handler.npc_list) / len(self.game.object_handler.npc_list),
                sum(npc.map_pos[1] for npc in self.game.object_handler.npc_list) / len(self.game.object_handler.npc_list)
            )

            angle_to_avg_npc = math.atan2(avg_npc_pos[1] - self.y, avg_npc_pos[0] - self.x)

            smoothing_factor = 0.1

            angle_difference = (angle_to_avg_npc - self.angle + math.pi) % (2 * math.pi) - math.pi
            self.angle += angle_difference * smoothing_factor

    def update(self):
        # self.movement()
        if self.moving:
            self.move_to_target_positions()
            
        # CAMERA UPDATE
        # Check if "k" is pressed
        # keys = pg.key.get_pressed()
        # if keys[pg.K_k]:
            # self.auto_rotate = not self.auto_rotate  # Change rotation automatically

        # Update Camera angle
        if self.auto_rotate:
            self.auto_rotate_camera()
        else:
            self.mouse_control()
            
        self.health_bar.update()

    @property
    def pos(self):
        return self.x, self.y

    @property
    def map_pos(self):
        return int(self.x), int(self.y)
