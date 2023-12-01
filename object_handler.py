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
        add_npc(NPC(game, pos=(64, 3)))  #8,3
        add_npc(NPC(game, pos=(64, 5)))  #9,5
        add_npc(NPC(game, pos=(64, 4)))  #9,4
        add_npc(NPC(game, path="resources/sprites/npc/snake/0.png", pos=(64, 4), attack_dist=2, health=150, attack_damage=4)) #8,4

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}
        [sprite.update() for sprite in self.sprite_list]
        [npc.update() for npc in self.npc_list]

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)