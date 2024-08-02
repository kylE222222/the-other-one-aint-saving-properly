class Item():

    def __init__(self, item_name, item_description):
        self.name = item_name
        self.description = item_description

    def get_name(self):
        return self.name
    
    def get_description(self):
        return self.description
    
    def item_describe(self): 
        text = "A " + self.name + " is here - " + self.description + "\n"
        if self.name == "Data Crystal":
            text = text.replace("A", "The")
        print(text)
    

class Weapon(Item):
    
    def __init__(self, item_name, item_description, damage):
        super().__init__(item_name, item_description)
        self.damage = damage
    
    def get_damage(self):
        return self.damage

    def weapon_describe(self):
        print(self.name)
        print("Damage: " + str(self.damage))


class Heal(Item):
    
    def __init__(self, item_name, item_description, heal_amount):
        super().__init__(item_name, item_description)
        self.heal_amount = heal_amount
    
    def get_heal_amount(self):
        return self.heal_amount

    def use_heal(self, name):
        print(name + " uses the " + self.name + " and restores " + str(self.heal_amount) + " HP.")


class Support(Item):
    def __init__(self, item_name, item_description, buff_type, buff_amount):
        super().__init__(item_name, item_description)
        self.buff_type = buff_type
        self.buff_amount = buff_amount

    def get_buff_type(self):
        return self.buff_type
    
    def get_buff_amount(self):
        return self.buff_amount
    
    def support_describe(self):
        print(self.name)
        print(self.description)