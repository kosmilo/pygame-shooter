import pygame as pg

class Wave:
    def __init__(self, game, max_time, enemies):
        self.game = game
        self.max_time = max_time
        self.start_time = pg.time.get_ticks()
        self.spawn_cooldown = 4000
        self.last_spawn = self.start_time
        self.enemies_spawned = 0
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
        elif time_now - self.last_spawn > self.spawn_cooldown and len(self.enemies) > 0:
            self.game.object_handler.add_npc(self.enemies[0])
            self.enemies.remove(self.enemies[0])
            self.last_spawn = pg.time.get_ticks()
            self.enemies_spawned += 1

            # Shorten spawn cooldown every 3 enemies
            if self.enemies_spawned % 3 == 0 and self.spawn_cooldown > 400:
                self.spawn_cooldown -= 75
                print('Shortened spawn cooldown')


    # Stop wave when all enemies are dead 
    def check_enemy_count(self):
        if len(self.game.object_handler.npc_list) < 1 and len(self.enemies) < 1:
            print('no enemies, stopping wave')
            self.isFinished = True