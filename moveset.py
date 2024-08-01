import time
import random
import os


def attack(name, weapon, item, charged, enemy_hp):
    critical_hit = False
    total_damage = weapon.get_damage() + random.randint(-2, 2)
    if charged == True:
        total_damage *= 1.5
    if item != None:
        if item.get_buff_type() == "damage":
            total_damage += item.get_buff_amount()
        elif item.get_buff_type() == "crit_rate":
            critical_hit_chance = random.randint(1, 100)
            if critical_hit_chance <= item.get_buff_amount():
                critical_hit = True
                total_damage *= 2
    enemy_hp -= total_damage
    print(name + " attacks with " + weapon.get_name() + " and deals " + str(total_damage) + " damage.")
    if critical_hit == True: 
        print(" Critical hit!")
    return enemy_hp


def charge(name):
    print(name + " charges up their next attack.")
    return True


def block(name, item, user):
    if user == "player":
        number_combination = ""
        os.system("printf '\033c'")
        min = 1
        max = 3
        for i in range(0,3):
            number_generated = random.randint(min,max)
            number_combination += str(number_generated)
            print(number_generated)
            time.sleep(0.2)
            if item != None:
                if item.get_buff_type() == "blocking_time":
                    time.sleep(item.get_buff_amount())
            os.system("printf '\033c'")
            min += 3
            max += 3
        combination_input = input()
        if combination_input == number_combination:
            print(name + " puts up their guard")
            return True
        else:
            print(name + " spaces out")
    else:
        print(name + " puts up their guard")
        return True


def run(name):
    run_chance = random.randint(1,4)
    print(name + " attempts to run away..")
    time.sleep(1)
    if run_chance == 1:
        return True
    else:
        print("..but fails")