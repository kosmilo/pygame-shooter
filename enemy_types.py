from npc import NPC


class SnakeEnemy(NPC):
    def __init__(self, game, pos=(2, 2)):
        self.game = game
        super().__init__(game=game, path="resources/sprites/npc/snake/0.png", pos=pos, health=200, attack_dist=2,
                         attack_damage=3, speed=0.03, base_score=100)


class JellyfishEnemy(NPC):
    def __init__(self, game, pos=(2, 2)):
        self.game = game
        super().__init__(game=game, path="resources/sprites/npc/jellyfish/0.png", pos=pos, health=150, attack_dist=2,
                         attack_damage=5, speed=0.02, base_score=90)


class AngelEnemy(NPC):
    def __init__(self, game, pos=(2, 2)):
        self.game = game
        super().__init__(game=game, path="resources/sprites/npc/angel/0.png", pos=pos, health=200, attack_dist=4,
                         attack_damage=7, speed=0.02, base_score=130)
