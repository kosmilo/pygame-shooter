import pygame as pg

class Wave:
    def __init__(self, game, max_time, enemies):
        self.game = game
        self.max_time = max_time
        self.start_time = pg.time.get_ticks()
        self.spawn_cooldown = 35
        self.last_spawn = self.start_time - self.spawn_cooldown
        self.enemies = enemies
        self.isFinished = False

    def update(self):
        self.check_time()
        self.check_enemy_count()

    def check_time(self):
        time_now = pg.time.get_ticks()
        # Check wave time
        if time_now - self.start_time > self.max_time:
            print('WAVE ON OVERTIME, IMPLIMENT ENDING THE WAVE EARLY!!')
        #spawn enemies
        elif time_now - self.last_spawn > self.last_spawn and len(self.enemies) > 0:
            self.game.object_handler.add_npc(self.enemies[0])
            self.enemies.remove(self.enemies[0])
            self.last_spawn = time_now
            print('IMPLIMENT SPAWN ENEMY')

    def check_enemy_count(self):
        if len(self.game.object_handler.npc_list) < 1 and len(self.enemies) < 1:
            self.isFinished = True