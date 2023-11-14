import pygame as pg
import sys
from settings import *
from game import *

# Define game
class Session:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1

        self.game_font = pg.font.SysFont('Comic Sans MS', 30)
        self.info_text = self.game_font.render('Press S to start', False, (200, 200, 200))

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

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.info_text, (0,0))
        pg.display.flip()


    def run(self):
        while True:
            self.check_events()
            self.draw_menu()

# Start game
if __name__ == "__main__":
    session = Session()
