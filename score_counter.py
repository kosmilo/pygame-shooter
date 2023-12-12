import pygame as pg
from game import *


class ScoreCounter:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.score_counter = 0
        self.score_font = game.session.game_font

    @staticmethod
    def calculate_multiplier():
        time_in_10s_of_seconds = round(pg.time.get_ticks() / 1000, -1)
        # multiplier is 1% of every 10 seconds left combined
        # e.g. if there is 160 seconds left it's 1.6
        multiplier = 0.01 * (300 - time_in_10s_of_seconds)
        return multiplier

    def increase_score(self, amount):
        self.score_counter += int(round(amount * self.calculate_multiplier(), 0))

    def get_score(self):
        return self.score_counter

    def draw(self):
        score_counter_text = self.score_font.render('score: ' + str(self.score_counter), False, (200, 0, 0))
        self.game.screen.blit(score_counter_text, (20, 20))
