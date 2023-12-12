from sprite_object import *
from npc import *

# Keeps track of objects in runtime
class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.npc_sprite_path = 'resources/sprites/npc/'
        self.static_sprite_path = 'resources/sprites/static/'
        self.anim_sprite_path = 'resources/sprites/animated_sprites/'
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        # Objects
        add_sprite(Candlebra(game, pos=(2, 2)))
        add_sprite(Torch(game, pos=(2, 3)))

        # NPCs
        add_npc(NPC(game, path="resources/sprites/npc/jellyfish/0.png", pos=(8, 5), scale=2, attack_dist=3, health=100, attack_damage=6))
        add_npc(NPC(game, path="resources/sprites/npc/jellyfish/0.png", pos=(9, 4), attack_dist=2, speed=0.02))
        add_npc(NPC(game, path="resources/sprites/npc/jellyfish/0.png", pos=(8, 4), attack_dist=1, health=150, attack_damage=4))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)