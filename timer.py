from game import *


class Timer:
    def __init__(self, game):
        self.game = game
        self.clock = game.clock
        self.timer = TIME_LIMIT_MS
        self.timer_running = True

        self.timer_font = pg.font.SysFont('Comic Sans MS', 30)

    def update(self, dt):
        if self.timer <= 0:
            self.game.game_over()
        if self.timer_running:
            self.timer -= dt

    def draw(self):
        timer_label = self.timer_font.render(str(int(self.timer/1000)), True, 'White')
        self.game.screen.blit(timer_label, (HALF_WIDTH, 0))

