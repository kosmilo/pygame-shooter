import pygame as pg
from game import *


class ScoreCounter:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen

        self.score_counter = 0

        self.score_font = pg.font.SysFont('Comic Sans MS', 30)

    @staticmethod
    def calculate_multiplier():
        time_in_seconds = pg.time.get_ticks() / 1000
        multiplier = 0.01 * (300 - time_in_seconds)
        return multiplier

    def increase_score(self, amount):
        self.score_counter += int(round(amount * self.calculate_multiplier(), -1))

    def reset_score(self):
        self.score_counter = 0

    def draw(self):
        score_counter_text = self.score_font.render(str(self.score_counter), False, (0, 0, 0))
        self.game.screen.blit(score_counter_text, (0, 0))


