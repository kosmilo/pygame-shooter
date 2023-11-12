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

    def aim_control(self):
        mx, my = pg.mouse.get_pos()
        self.pos = self.x, self.y = mx, my

    def update(self):
        self.aim_control()