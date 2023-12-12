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

        self.menu_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 50)
        self.title_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 200)
        self.ui_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 40)

        self.current_menu = 'main_menu'
        self.menus = {
            'main_menu': MainMenu(self),
            'settings': SettingsMenu(self),
            'tutorial': TutorialMenu(self),
            'empty': Menu(self)
        }

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

    def run(self):
        while True:
            self.check_events()
            self.menus[self.current_menu].draw_menu()

            pg.display.flip()

    def start_game(self):
        self.game = Game(self)
        self.menus.update({'game_over': GameOverMenu(self)})

    def change_current_menu(self, new_menu):
        self.current_menu = new_menu


# Start game
if __name__ == "__main__":
    session = Session()
