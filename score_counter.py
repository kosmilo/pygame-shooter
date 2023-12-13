import pygame as pg
from game import *
from settings import *


class ScoreCounter:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.timer = game.timer

        self.score_counter = 0
        self.score_font = game.session.ui_font

    def calculate_multiplier(self):
        time_in_ms = self.timer.timer
        # divide by 1000 to convert ms to seconds, then divide by 100 to get 1% for the multiplier
        multiplier = time_in_ms / 1000 / 100
        return multiplier

    def increase_score(self, amount):
        # add 200 for base
        self.score_counter += int(amount * self.calculate_multiplier() + 200)

    def get_score(self):
        return self.score_counter

    def draw(self):
        score_counter_text = self.score_font.render('score: ' + str(self.score_counter), False, (200, 0, 0))
        self.game.screen.blit(score_counter_text, (5, 0))
