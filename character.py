import random
from enemy_data_pool import *


class Character():

    def __init__(self, character_name, character_weapon, character_max_hp):
        self.name = character_name
        self.weapon = character_weapon
        self.item = None
        self.max_hp = character_max_hp

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_weapon(self):
        return self.weapon
    
    def set_weapon(self, weapon):
        self.weapon = weapon
    
    def get_item(self):
        return self.item
    
    def set_item(self, item):
        self.item = item
    
    def get_max_hp(self):
        return self.max_hp

class Enemy(Character):
    def __init__(self, character_name, character_weapon, character_max_hp, character_rank):
        super().__init__(self, character_name, character_weapon, character_max_hp)
        self.rank = character_rank

    def get_rank(self):
        return self.rank
    
    def enemy_describe(self):
        print(self.rank + " " + self.name + " is here.\n")

    def begin_fight(self):
        print("You engage in a fight with " + self.rank, self.name + ".")
        print(self.name + ": " + random.choice(get_dialogue_pool()) + "\n")

    def generate_enemy(self, weapon_pool):
        self.name = random.choice(get_name_pool())
        self.weapon = random.choice(weapon_pool)
        self.max_hp = random.randint(75, 100)
        self.rank = random.choice(get_rank_pool())