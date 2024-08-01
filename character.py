import random


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
    
    def char_describe(self):
        print("\nRoom Character:")
        print(self.name + " is here.")

    def generate_enemy(self, name_pool, weapon_pool, enemy_max_hp):
        self.name = random.choice(name_pool)
        self.weapon = random.choice(weapon_pool)
        self.max_hp = enemy_max_hp