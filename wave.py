from game import *


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
        self.wave_list = [Wave(game, [NPC(game, pos=(8, 3)), NPC(game, pos=(9, 5))]),
                          Wave(game, [NPC(game, pos=(8, 3)), NPC(game, pos=(5, 4))])]

        self.object_handler = game.object_handler
        self.current_wave_index = 0
        self.timer = game.timer

        self.start_wave()

    def update(self):
        if len(self.object_handler.npc_list) < 1:
            self.current_wave_index += 1
            self.timer.timer_running = False
            self.start_wave()
            
    def start_wave(self):
        if self.current_wave_index < len(self.wave_list):
            self.wave_list[self.current_wave_index].spawn_enemies()
            self.timer.timer_running = True
        else:
            self.game.game_over()
