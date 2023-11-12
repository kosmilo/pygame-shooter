import pygame as pg
from settings import *

class Crosshair:
    def __init__(self, game):
        self.game = game
        self.pos = self.x, self.y = HALF_WIDTH, HALF_HEIGHT
        self.width, self.height = 10, 10
        print('Crosshair init, ', self.pos)

    def draw(self):
        pg.draw.rect(self.game.screen, 'red', [(self.x - self.width / 2), (self.y - self.height / 2), self.width, self.height], 2)