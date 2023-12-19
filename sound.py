import pygame as pg


class Sound:
    def __init__(self, session):
        self.session = session
        pg.mixer.init()
        self.path = 'resources/sound/'

        self.weapon = pg.mixer.Sound(self.path + 'blaster.wav')
        self.button_click = pg.mixer.Sound(self.path + 'Bluezone_BC0268_switch_button_click_small_005.wav')
        self.key_pressed = pg.mixer.Sound(self.path + 'Wall_Light_Double_Switch_Off-004.wav')
        self.alien_attack = pg.mixer.Sound(self.path + 'Alien_Damage_1__calicrazed.com.wav')
        self.game_over = pg.mixer.Sound(self.path + 'Bluezone_BC0267_cinematic_texture_007.wav')
        self.game_over.set_volume(0.5)

        pg.mixer.music.load(self.path + 'Bluezone_BC0255_ambience_texture_004.wav')
