import pygame as pg
from main import *
from button import *


class Menu:
    def __init__(self, session):
        self.session = session
        self.menu_font = session.menu_font
        self.title_font = session.title_font
        self.screen = session.screen

    def draw_menu(self):
        self.screen.fill((0, 0, 0))

    def open_tutorial_menu(self):
        self.session.change_current_menu('tutorial')

    def open_settings_menu(self):
        self.session.change_current_menu('settings')

    def open_main_menu(self):
        self.session.change_current_menu('main_menu')
        self.session.menus['main_menu'].update_high_scores()


class MainMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)

        self.title_text = self.title_font.render('GAME TITLE', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.hs_title_text = self.menu_font.render('high scores', True, (200, 0, 0))
        self.hs_title_rect = self.hs_title_text.get_rect(midtop=self.title_rect.midbottom)

        self.tutorial_button = Button(self, WIDTH-250, HEIGHT-100, 250, 100, 'tutorial', self.open_tutorial_menu)
        self.settings_button = Button(self, 0, HEIGHT-100, 250, 100, 'settings', self.open_settings_menu)
        self.start_game_button = Button(self, WIDTH/2-350/2, HEIGHT-100, 350, 100, 'start game', self.session.start_game)


        self.db_data = self.session.db_link.get_top5_scores_from_db()

    def draw_menu(self):
        self.screen.fill((0, 0, 0))

        self.draw_high_scores()

        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.hs_title_text, self.hs_title_rect)

        self.tutorial_button.process()
        self.settings_button.process()
        self.start_game_button.process()

    def draw_high_scores(self):
        for i, (name, score) in enumerate(self.db_data):
            text = f"{i+1}. {name}: {score}"
            score_row_text = self.menu_font.render(text, True, (200, 200, 200))

            self.screen.blit(score_row_text, (self.hs_title_rect.bottomleft[0], self.hs_title_rect.bottomleft[1]+i*40))

    def update_high_scores(self):
        self.db_data = self.session.db_link.get_top5_scores_from_db()


class SettingsMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)

        self.title_text = self.title_font.render('SETTINGS', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.return_button = Button(self, WIDTH-250, HEIGHT-100, 250, 100, 'return', self.open_main_menu, True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_text, self.title_rect)

        self.return_button.process()


class TutorialMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)

        self.title_text = self.title_font.render('TUTORIAL', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.return_button = Button(self, 0, HEIGHT-100, 250, 100, 'return', self.open_main_menu, True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_text, self.title_rect)

        self.return_button.process()


class GameOverMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)
        self.score_counter = session.game.score_counter
        self.score = self.score_counter.get_score()

        self.title_text = self.title_font.render('GAME OVER', True, 'Red')
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.score_text = self.menu_font.render('your score: {}'.format(self.score), True, 'White')
        self.score_rect = self.score_text.get_rect(midtop=self.title_rect.midbottom)

        self.return_button = Button(self, WIDTH/2-250/2, HEIGHT-100, 250, 100, 'return', self.open_main_menu, True)

        self.send_score_to_db_link()

    def draw_menu(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.score_text, self.score_rect)

        self.return_button.process()

    def send_score_to_db_link(self):
        self.session.db_link.save_score_into_db("000", self.score)
