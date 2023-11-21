import pygame as pg
import sys
from settings import *
from game import *
from menus import *


# Define game
class Session:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.game_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 50)
        self.title_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 200)

        self.main_menu = MainMenu(self)

        self.run()

    # Get inputs
    def check_events(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            # Quit
            if event.type == pg.QUIT or (
                event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE
            ):
                pg.quit()
                sys.exit()
            # Start a new game
            elif keys[pg.K_s]:
                self.game = Game(self)

    def run(self):
        while True:
            self.check_events()
            self.main_menu.draw_main_menu()

            pg.display.flip()


# Start game
if __name__ == "__main__":
    session = Session()
