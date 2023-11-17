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

        self.game_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 50)
        self.title_font = pg.font.Font('resources/fonts/vermin_vibes_1989.ttf', 200)

        self.title_text = self.title_font.render('GAME TITLE', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.info_text = self.game_font.render('Press S to start', False, (200, 200, 200))
        self.info_rect = self.info_text.get_rect(midtop=self.title_rect.midbottom)

        self.hs_data = [
            (1, 'player1', 1000),
            (2, 'player2', 900),
            (3, 'player3', 800),
            (4, 'player4', 700),
            (5, 'player5', 600)
        ]

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

    def draw_high_scores(self):
        hs_title_text = self.game_font.render('high scores', True, (200, 0, 0))
        hs_title_rect = hs_title_text.get_rect(topleft=self.info_rect.bottomleft)
        self.screen.blit(hs_title_text, hs_title_rect)

        for i, (rank, name, score) in enumerate(self.hs_data):
            text = f"{rank}. {name}: {score}"
            score_row_text = self.game_font.render(text, True, (200, 200, 200))

            self.screen.blit(score_row_text, (hs_title_rect.bottomleft[0], hs_title_rect.bottomleft[1]+i*40))

    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))

        self.draw_high_scores()

        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.info_text, self.info_rect)
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.draw_main_menu()


# Start game
if __name__ == "__main__":
    session = Session()
