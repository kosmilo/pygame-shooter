from game import *
from enemy_types import JellyfishEnemy, AngelEnemy, SnakeEnemy


class Wave:
    def __init__(self, game, enemy_list):
        self.game = game
        self.enemy_list = enemy_list
        self.object_handler = game.object_handler

    def spawn_enemies(self):
        for enemy in self.enemy_list:
            self.object_handler.add_npc(enemy)


class WaveManager:
    def __init__(self, game):
        self.game = game
        self.wave_list = [
            Wave(game, [SnakeEnemy(game, pos=(3, 5)), JellyfishEnemy(game, pos=(4, 3))]),
            Wave(game, [JellyfishEnemy(game, pos=(10, 6))]),
            Wave(game, [SnakeEnemy(game, pos=(11, 9)), AngelEnemy(game, pos=(12, 9)), JellyfishEnemy(game, pos=(10, 9))]),
            Wave(game, [SnakeEnemy(game, pos=(6, 1)), JellyfishEnemy(game, pos=(7, 2)), JellyfishEnemy(game, pos=(6, 1))])
                          ]

        self.object_handler = game.object_handler
        self.current_wave_index = 0
        self.timer = game.timer
        self.wave_running = True

        self.start_wave()

    def update(self):
        if self.wave_running:
            if len(self.object_handler.npc_list) < 1:
                print('wave over')
                self.timer.timer_running = False
                self.wave_running = False
                self.current_wave_index += 1
                self.game.player.moving = True

    def start_wave(self):
        print('trying to start new wave')
        if self.current_wave_index < len(self.wave_list):
            print('started  new wave')
            self.wave_running = True
            self.wave_list[self.current_wave_index].spawn_enemies()
            self.timer.timer_running = True
        else:
            print('waves over, ending game')
            self.game.game_over()
