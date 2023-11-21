import pygame as pg
from main import *
from button import *


class Menu:
    def __init__(self, session):
        self.game_font = session.game_font
        self.title_font = session.title_font
        self.screen = session.screen


class MainMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)

        self.title_text = self.title_font.render('GAME TITLE', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.info_text = self.game_font.render('Press S to start', False, (200, 200, 200))
        self.info_rect = self.info_text.get_rect(midtop=self.title_rect.midbottom)

        self.hs_title_text = self.game_font.render('high scores', True, (200, 0, 0))
        self.hs_title_rect = self.hs_title_text.get_rect(topleft=self.info_rect.bottomleft)

        self.tutorial_button = Button(self, WIDTH-250, HEIGHT-100, 250, 100, 'tutorial', self.open_tutorial_menu)

        self.settings_button = Button(self, 0, HEIGHT-100, 250, 100, 'settings', self.open_settings_menu)

        self.hs_data = [
            (1, 'player1', 1000),
            (2, 'player2', 900),
            (3, 'player3', 800),
            (4, 'player4', 700),
            (5, 'player5', 600)
        ]

    def draw_main_menu(self):
        self.screen.fill((0, 0, 0))

        self.draw_high_scores()

        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.info_text, self.info_rect)

        self.screen.blit(self.hs_title_text, self.hs_title_rect)

        self.tutorial_button.process()
        self.settings_button.process()

    def draw_high_scores(self):
        for i, (rank, name, score) in enumerate(self.hs_data):
            text = f"{rank}. {name}: {score}"
            score_row_text = self.game_font.render(text, True, (200, 200, 200))

            self.screen.blit(score_row_text, (self.hs_title_rect.bottomleft[0], self.hs_title_rect.bottomleft[1]+i*40))

    def open_tutorial_menu(self):
        print('get away from here! weeeeee')

    def open_settings_menu(self):
        print('settings menu! i choose you!!')
