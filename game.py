import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *
from crosshair import *

# Define game
class Game:
    def __init__(self, session):
        self.session = session
        self.screen = session.screen
        self.clock = session.clock
        self.delta_time = session.delta_time
        self.new_game()
        self.running = True
        self.run()

    def new_game(self):
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.sound = Sound(self)
        self.pathfinding = Pathfinding(self)
        self.crosshair = Crosshair(self)

    def update(self):
        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.crosshair.update()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)

        pg.display.set_caption(f"fps: {self.clock.get_fps() :.1f}")

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()
        self.crosshair.draw()
        # self.map.draw()
        # self.player.draw()

    # Get inputs
    def check_events(self):
        for event in pg.event.get():
            # Quit
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            # Shoot
            self.player.single_fire_event(event)

    # Game loop
    def run(self):
        while self.running:
            self.check_events()
            self.update()
            self.draw()
            if len(self.object_handler.npc_list) < 1:
                self.running = False