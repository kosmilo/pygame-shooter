import pygame as pg
from main import *


class Button:

    # when making a new button: make sure to include its button.process() in an update loop like you would a blit()
    # otherwise the button won't render or work
    def __init__(self, menu, x, y, width, height, button_text='Button', onclick_function=None, multiple_presses=False):
        self.menu = menu
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = onclick_function
        self.multiple_presses = multiple_presses
        self.already_pressed = False
        self.menu_font = menu.menu_font
        self.screen = menu.screen

        self.fill_colors = {
            'normal': '#ffffff',
            'hover': 'Red',
            'pressed': 'Gray',
        }

        self.button_surface = pg.Surface((self.width, self.height))
        self.button_rect = pg.Rect((x, y), (self.width, self.height))

        self.button_surf = self.menu_font.render(button_text, True, (20, 20, 20))

    def process(self):
        mouse_pos = pg.mouse.get_pos()

        self.button_surface.fill(self.fill_colors['normal'])

        # handle hovering and pressing button
        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                if self.multiple_presses:
                    self.onclick_function()
                    self.play_button_sound()
                elif not self.already_pressed:
                    self.onclick_function()
                    self.already_pressed = True
                    self.play_button_sound()

        self.draw_button()

    def play_button_sound(self):
        self.menu.session.sound.button_click.play()

    def draw_button(self):
        self.button_surface.blit(self.button_surf, [
            self.button_rect.width / 2 - self.button_surf.get_rect().width / 2,
            self.button_rect.height / 2 - self.button_surf.get_rect().height / 2
        ])

        self.screen.blit(self.button_surface, self.button_rect)

    def get_rect(self):
        return self.button_rect


class InputField(Button):
    def __init__(self, menu, x, y, width, height, box_text='input'):
        Button.__init__(self, menu, x, y, width, height, box_text)
        self.take_player_input = False
        self.user_text = ''

    def clickable(self):
        mouse_pos = pg.mouse.get_pos()
        self.button_surface.fill(self.fill_colors['normal'])

        if self.button_rect.collidepoint(mouse_pos):
            self.button_surface.fill(self.fill_colors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.button_surface.fill(self.fill_colors['pressed'])
                self.take_player_input = True
                self.play_button_sound()

    def detect_and_handle_input(self):
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                self.play_key_pressed_sound()
                if event.key == pg.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                elif event.key == pg.K_RETURN:
                    self.take_player_input = False
                else:
                    self.user_text += event.unicode

    def process(self):
        self.clickable()
        if self.take_player_input:
            self.button_surface.fill(self.fill_colors['hover'])
            self.detect_and_handle_input()
        self.draw_input_field()

    def get_user_text(self):
        return self.user_text

    def draw_input_field(self):
        input_text = self.menu_font.render('insert name', True, (20, 20, 20))
        if not self.user_text == '':
            input_text = self.menu_font.render(self.user_text, True, (20, 20, 20))
        self.button_surface.blit(input_text, [
            self.button_rect.width / 2 - input_text.get_rect().width / 2,
            self.button_rect.height / 2 - input_text.get_rect().height / 2
        ])

        self.screen.blit(self.button_surface, self.button_rect)

    def play_key_pressed_sound(self):
        self.menu.session.sound.key_pressed.play()


