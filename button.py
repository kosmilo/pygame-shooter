import pygame as pg
from main import *


class Button:

    # when making a new button: make sure to include its button.process() in an update loop like you would a blit()
    # otherwise the button won't render or work
    def __init__(self, menu, x, y, width, height, button_text='Button', onclick_function=None, one_press=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = onclick_function
        self.one_press = one_press
        self.already_pressed = False
        self.game_font = menu.game_font
        self.screen = menu.screen

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': 'Red',
            'pressed': 'Gray',
        }

        self.button_surface = pg.Surface((self.width, self.height))
        self.button_rect = pg.Rect((x, y), (self.width, self.height))

        self.button_surf = self.game_font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pg.mouse.get_pos()

        self.button_surface.fill(self.fill_colors['normal'])

        # handle hovering and pressing button
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                if self.one_press:
                    self.onclick_function()
                elif not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
            else:
                self.already_pressed = False

        self.button_surface.blit(self.button_surf, [
            self.button_rect.width/2 - self.button_surf.get_rect().width/2,
            self.button_rect.height/2 - self.button_surf.get_rect().height/2
        ])

        self.screen.blit(self.button_surface, self.button_rect)


