import pygame as pg
from main import *
from button import Button, InputField


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

        self.title_text = self.title_font.render('DAGON', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.hs_title_text = self.menu_font.render('high scores', True, (200, 0, 0))
        self.hs_title_rect = self.hs_title_text.get_rect(midtop=self.title_rect.midbottom)

        self.tutorial_button = Button(self, WIDTH-250, HEIGHT-450, 250, 100, 'tutorial', self.open_tutorial_menu, True)
        self.settings_button = Button(self, 0, HEIGHT-450, 250, 100, 'settings', self.open_settings_menu, True)
        self.start_game_button = Button(self, WIDTH/2-350/2, HEIGHT-250, 350, 100, 'start game', self.session.start_game, True)


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

        self.return_button = Button(self, WIDTH/2-250/2, HEIGHT-450, 250, 100, 'return', self.open_main_menu, True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_text, self.title_rect)

        self.return_button.process()


class TutorialMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)

        self.title_text = self.title_font.render('TUTORIAL', True, (200, 0, 0))
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.return_button = Button(self, WIDTH/2-250/2, HEIGHT-450, 250, 100, 'return', self.open_main_menu, True)

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.title_text, self.title_rect)

        self.return_button.process()


class GameOverMenu(Menu):
    def __init__(self, session):
        Menu.__init__(self, session)
        pg.mouse.set_visible(True)
        self.score_counter = session.game.score_counter
        self.score = self.score_counter.get_score()

        self.title_text = self.title_font.render('GAME OVER', True, 'Red')
        self.title_rect = self.title_text.get_rect(midtop=self.screen.get_rect().midtop)

        self.score_text = self.menu_font.render('your score: {}'.format(self.score), True, 'White')
        self.score_rect = self.score_text.get_rect(midtop=self.title_rect.midbottom)

        self.return_button = Button(self, WIDTH/2-250/2, HEIGHT-150, 250, 100, 'return', self.open_main_menu, True)

        self.playername_input = InputField(self, WIDTH/2-400/2, HEIGHT-600, 400, 100, 'insert name')

        self.name_too_long = False
        self.name_too_long_text = self.menu_font.render('name should be max 3 characters', True, 'Red')
        self.name_too_long_rect = self.name_too_long_text.get_rect(midbottom=self.playername_input.get_rect().midtop)

        self.save_score_button = Button(self, WIDTH/2-350/2, HEIGHT-450, 350, 100, 'save score', self.send_score_to_db_link, False)

        self.score_saved = False
        self.score_saved_text = self.menu_font.render('saved!', True, 'White')
        self.score_saved_rect = self.score_saved_text.get_rect(midtop=self.save_score_button.get_rect().midbottom)

    def draw_menu(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.title_text, self.title_rect)
        self.screen.blit(self.score_text, self.score_rect)
        if self.name_too_long:
            self.screen.blit(self.name_too_long_text, self.name_too_long_rect)
        if self.score_saved:
            self.screen.blit(self.score_saved_text, self.score_saved_rect)

        self.return_button.process()
        self.save_score_button.process()
        self.playername_input.process()

    def send_score_to_db_link(self):
        playername_text = self.playername_input.get_user_text()
        if playername_text == '':
            self.session.db_link.save_score_into_db("NUL", self.score)
            self.name_too_long = False
        elif len(playername_text) > 3:
            self.name_too_long = True
        else:
            self.session.db_link.save_score_into_db(playername_text, self.score)
            self.name_too_long = False
            self.score_saved = True

