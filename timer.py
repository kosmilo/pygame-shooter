from game import *


class Timer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.clock = game.clock

        self.timer = TIME_LIMIT_MS
        self.timer_running = True

        self.timer_font = game.session.ui_font

    def update(self, dt):
        if self.timer <= 0:
            self.game.game_over()
        if self.timer_running:
            self.timer -= dt

    def draw(self):
        timer_label = self.timer_font.render('time: {}'.format(int(self.timer/1000)), False, (200, 0, 0))
        timer_rect = timer_label.get_rect(topright=self.screen.get_rect().topright)
        self.screen.blit(timer_label, timer_rect)

