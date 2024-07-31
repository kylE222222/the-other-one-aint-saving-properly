from room import *
from character import *
from item import *
from moveset import *
from names import *
from dialogue import *
import time 
import random
import os


#Room Instantiation
outside = Room("Outside", "The enemy fortress lies ahead.")
supply_room = Room("Supply Room", "A storage space full of equipment.")
cafeteria = Room("Cafeteria", "An area to eat and socialise.")
bathroom = Room("Bathroom", "A place for a momentary break from the action.")
vents = Room("Vents", "Dark and cramped but free of soldiers.")
main_room = Room("Main Room", "The command centre of the base. The way south is blocked by a particularly explodable barrier.")
training_area = Room("Training Area", "A high-intensity training facility used to hone the skills of soldiers.")
data_room = Room("Data Room", "The data centre of the facility and a treasure trove of classified information.")
security_room = Room("Security Room", "Home to the camera and alarm systems that guard the base.")
hidden_room = Room("???", "A dark presence fills the room.")

left_hall_a = Room("Left Hall A", None)
left_hall_b = Room("Left Hall B", None)
left_hall_c = Room("Left Hall C", "A barrier blocks the way to the Main Room")

right_hall_a = Room("Right Hall A", None)
right_hall_b = Room("Right Hall B", None)
right_hall_c = Room("Right Hall C", None)
right_hall_d = Room("Right Hall D", None)


#Room Linking: Left Side (Up to the main room)
left_hall_a.link_room(cafeteria, "north")
left_hall_a.link_room(outside, "south")
left_hall_a.link_room(left_hall_b, "west")

left_hall_b.link_room(left_hall_c, "north")
left_hall_b.link_room(left_hall_a, "east")
left_hall_b.link_room(supply_room, "west")

left_hall_c.link_room(left_hall_b, "south")

cafeteria.link_room(vents, "east")
cafeteria.link_room(left_hall_a, "south")

supply_room.link_room(left_hall_b, "east")


#Room Linking: Right Side (Up to the main room)
right_hall_a.link_room(right_hall_b, "north")
right_hall_a.link_room(outside, "south")
right_hall_a.link_room(bathroom, "west")

right_hall_b.link_room(right_hall_c, "north")
right_hall_b.link_room(training_area, "east")
right_hall_b.link_room(right_hall_a, "south")
right_hall_b.link_room(vents, "west")

right_hall_c.link_room(security_room, "north")
right_hall_c.link_room(right_hall_b, "south")
right_hall_c.link_room(right_hall_d, "west")

right_hall_d.link_room(right_hall_c, "east")
right_hall_d.link_room(main_room, "west")

bathroom.link_room(right_hall_a, "east")

training_area.link_room(right_hall_b, "west")

security_room.link_room(right_hall_c, "south")


#Room Linking: Miscellaneous
outside.link_room(right_hall_a, "north-east")
outside.link_room(left_hall_a, "north-west")

main_room.link_room(data_room, "north")
main_room.link_room(right_hall_d, "north-east")
main_room.link_room(vents, "south-east")

data_room.link_room(main_room, "south")


#Item Instantiation
data_crystal = Item("[DATA CRYSTAL]", "A capsule containg intel on enemy plans and tactics.")
data_room.set_item(data_crystal)
disguise = Item("[DISGUISE]", "Blend in with the opposition.")
supply_room.set_item(disguise)
flashlight = Item("[FLASHLIGHT]", "Light up the surrounding area.")
bomb = Item("[BOMB]", "Explosive!")
security_room.set_item(bomb)
#use bomb in right hall c to open the secret!


#Item Subclass: Weapon
fists = Weapon("[FISTS]", None, 2)
knife = Weapon("[KNIFE]", None, random.randint(3,4))
bat = Weapon("[BAT]", None, random.randint(3,4))
shovel = Weapon("[SHOVEL]", None, random.randint(3,4))
sword = Weapon("[SWORD]", None, random.randint(3,4))


#Item Subclass: Heal
banana = Heal("[BANANA]", "Restores 1 HP", 10)
medkit = Heal("[MEDKIT]", "Restores 5 HP", 10)


#Item Subclass: Support
shield_blocking_time_buff = round(random.uniform(0.1, 0.25),2)
shield = Support("[SHIELD]", "Increases the amount of time the numbers stay on screen by " + str(shield_blocking_time_buff) + "s", "blocking_time", shield_blocking_time_buff) 
lucky_charm_crit_boost = random.randint(1, 10)
lucky_charm = Support("[LUCKY CHARM]", "Provides a crit rate of " + str(lucky_charm_crit_boost) + "%", "crit_rate", lucky_charm_crit_boost)
armour_hp_buff = random.randint(3, 5)
vest = Support("[VEST]", "Increases your max health by " + str(armour_hp_buff), "health", armour_hp_buff)
gloves_dmg_buff = random.randint(1,3)
gloves = Support("[GLOVE]", "Increases your damage by " + str(gloves_dmg_buff), "damage", gloves_dmg_buff)


#Character Instantiation
enemy = Enemy(None, None, None)
security_guard = Enemy("security guard", fists, 20)
security_room.set_character(security_guard)

#tidy this up, maybe have less things
os.system("printf '\033c'") 
player_name = input("Enter your character's name: ")
player = Character(player_name, fists, 20)
player_max_hp = player.get_max_hp()
player_hp = player_max_hp
bag = []


# Pools
weapon_pool = [knife, bat, shovel, sword]
item_pool = [banana, medkit, shield, lucky_charm, vest, gloves, flashlight]
#rooms not included: outside, supply_room, data_room, hidden_room
item_rooms = [cafeteria, bathroom, vents, main_room, training_area, security_room, left_hall_a, left_hall_b, left_hall_c, right_hall_a, right_hall_b, right_hall_c, right_hall_d]

vent_exits = [cafeteria, right_hall_b, main_room]
bomb_rooms = [left_hall_c, main_room]
directions = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
encounterless_rooms = [outside, vents, security_room, hidden_room]

current_room = outside
disguised = False
security_active = True #disable by killing security guard
alarm = False #INTEL STOLEN -> ALARM = true (if security is active)
#for security active, maybe just use isinstance to check if an enemy is in security room
#(only securit guard can be in security room)
force_fight = False #always true when alarm is true


#putting item in room
for room in item_rooms:
    room_item_chance = random.randint(0,1)
    if room_item_chance == 1:
        if len(item_pool) > 0:
            random_item = random.choice(item_pool)
            item_pool.remove(random_item)
            room.set_item(random_item)


#MAIN PROCESS
os.system("printf '\033c'")
print("Hello " + player_name + ".")
print("You have been tasked to steal a valuable asset from an enemy base: the [DATA CRYSTAL].")
print("Navigate through the base to find and steal this [DATA CRYSTAL].")
print("The base is filled with enemies. Do what you must to get past.")
print("Good luck.")
print("\nPress enter to begin")
input('')

#the below works in pycharm but not in github...
"""print("Loading", end = '')
time.sleep(1)
for i in range(0,3):
    print(".", end = '')
    time.sleep(1)"""

#github alternative
loading = "Loading"
for i in range(0,4):
    os.system("printf '\033c'") 
    print(loading)
    loading = loading + "."
    time.sleep(1)


#HIDDEN ROOM BOSS FIGHTT?

while player_hp > 0:
    os.system("printf '\033c'")
    if current_room == vents:
        if "flashlight" in bag:
            print("You light up the vents with your flashlight.")
            vents.link_room(cafeteria, "a")
            vents.link_room(right_hall_b, "b")
            vents.link_room(main_room, "c")
        elif "flashlight" not in bag:
            print("The vents are too dark. You leave at a safe but random exit.")
            current_room = random.choice(vent_exits)
            time.sleep(1)

    if force_fight == True:
        command = "fight"
        force_fight = False
    else:
        #print("\n")
        room_enemy = current_room.get_character() 
        room_item = current_room.get_item() 
        current_room.get_details()
        if room_enemy != None:
            room_enemy.char_describe()
        if room_item != None:
            room_item.item_describe()
        print("\nEnter Help for controls")
        print("\nWhat would you like to do?")
        command = input("").lower()

    if command in current_room.linked_rooms:
        if command == "north" and current_room == right_hall_d:
            print("Are you sure you would like to continue? (You cannot go back)")
            enter_hidden = input("")
            if enter_hidden == "yes":
                in_hidden = True
                break
        else:
            current_room.set_character(None)
            current_room = current_room.move(command)
            print("You move to the " + current_room.get_name())
            time.sleep(2)
            if current_room not in encounterless_rooms:
                encounter_chance = random.randint(0,1) #temp values man
                if alarm == True:
                    encounter_chance = 1
                if encounter_chance == 1:
                    enemy.generate_enemy(get_name_pool(), weapon_pool, random.randint(1,2))
                    current_room.set_character(enemy)
                    room_enemy = current_room.get_character()
                    if disguised == False:
                        os.system("printf '\033c'")
                        print("You are spotted by " + room_enemy.get_name() + ".")
                        force_fight = True
                        #time.sleep(1)

    elif command in directions:
        print("You cannot go that way.")
        #time.sleep(2)


    elif command == "fight":
        if room_enemy != None:
            os.system("printf '\033c'")
            print("You engage in a fight with " + room_enemy.get_name())
            print(room_enemy.get_name() + ": " + random.choice(get_dialogue_pool()) + "\n")
            player_charged = False
            player_blocking = False
            moveset = ["attack", "charge", "block"]
            enemy_charged = False
            enemy_blocking = False
            enemy_max_hp = room_enemy.get_max_hp()
            enemy_hp = enemy_max_hp
            while enemy_hp > 0 and player_hp > 0:
                print("Player HP: " + str(player_hp) + "/" + str(player_max_hp))
                print("Enemy HP: " + str(enemy_hp) + "/" + str(enemy_max_hp))
                print("\nEnter Help for controls\n")
                print("What will you do?")
                fight_action = input().lower()
                #there is +-1 damage spread
                #maybe charged attacks can bypass block
                if fight_action == "attack":
                    if enemy_blocking == True:
                        print(player_name + " attacks but " + room_enemy.get_name() + " blocks the attack.")
                    else:
                        enemy_hp = attack(player_name, player.get_weapon(), player.get_item(), player_charged, enemy_hp)
                elif fight_action == "charge":
                    player_charged = charge(player_name)

                elif fight_action == "block":
                    player_blocking = block(player_name, player.get_item(), "player")

                elif fight_action == "run":
                    random_direction = ""
                    run_success = run(player_name)
                    if run_success == True:
                        while random_direction not in current_room.linked_rooms:
                            random_direction = random.choice(directions)
                        current_room = current_room.move(random_direction)
                        print(player_name + " runs off in a random direction.")
                        break
                        
                elif fight_action == "help":
                    os.system("printf '\033c'")
                    print("Controls")
                    print("-----------------------")
                    print("[Attack] - attack the enemy")
                    print("[Charge] - charge up and attack for a 1.5x damage multiplier. Charging twice in a row will do NOTHING")
                    print("[Block] - block the next enemy attack by entering the 3 digit code that briefly appears (no spaces)(lasts 1 turn)")
                    print("[Run] - attempt to flee from the enemy. If successful, you end up in a random room adjacent to your current room. (25%)")
                    print("-----------------------")
                    print("Press enter to go back.")
                    command = input()
                
                else:
                    fight_action = "help"

                time.sleep(1)
                if fight_action != "help" and enemy_hp > 0:
                    #enemy_charged = False
                    enemy_blocking = False
                    enemy_move = random.choice(moveset)
                    if enemy_move == "attack":
                        if player_blocking == True:
                            print(room_enemy.get_name() + " attacks but " + player_name + " blocks the attack.")
                        else:
                            player_hp = attack(room_enemy.get_name(), room_enemy.get_weapon(), None, enemy_charged, player_hp)
                    elif enemy_move == "charge":
                        enemy_charged = charge(room_enemy.get_name())
                    elif enemy_move == "block": 
                        enemy_blocking = block(room_enemy.get_name(), None, "enemy")
                time.sleep(1)
                #player_charged = False
                player_blocking = False
                os.system("printf '\033c'")
                if player_hp <= 0:
                    print("Game over. You have died.")
                    break

            if enemy_hp <= 0:
                if room_enemy == security_guard:
                    print("The security system has been disabled.")
                    security_active = False
                drop_chance = random.randint(0,1) #temp value (50%)
                if drop_chance == 1:
                    print(room_enemy.get_name() + " drops his " + room_enemy.get_weapon().get_name())
                    os.system("printf '\033c'")
                    print("\nWould you like to replace your current weapon?")
                    print("Current Weapon: ", end = '')
                    player.get_weapon().weapon_describe()
                    print("\nEnemy's Weapon: ", end = '')
                    room_enemy.get_weapon().weapon_describe()
                    take_weapon = input().lower()
                    if take_weapon == "yes":
                        print("You take the " + room_enemy.get_weapon().get_name() + ".")
                        player.set_weapon(room_enemy.get_weapon())
                        current_room.set_item(None)

                    else:
                        print("You leave the weapon behind.")

                print("You defeated " + room_enemy.get_name())
                current_room.set_character(None)

        else:
            print("There is no one to fight here.")

    
    elif command == "use":
        if isinstance(room_item, Heal) or len(bag) > 0:
            print("What would you like to use?")
            if isinstance(room_item, Heal): 
                print("Room item: " + room_item.get_name())
            if len(bag) > 0:
                print("Bag: " + str(bag))
            item_to_use = input().lower()
            if item_to_use == room_item.get_name():
                if player_hp == player.get_max_hp():
                    print("You are already at max health.")
                else:
                    room_item.use_heal(player_name)
                    player_hp += room_item.get_heal_amount()
                    if player_hp > player.get_max_hp():
                        player_hp = player.get_max_hp()
                    room_item.set_item(None)
            elif item_to_use == "bomb":
                if current_room in bomb_rooms:
                    print("Are you sure you would like to use the bomb?")
                    use_bomb = input("").lower()
                    if use_bomb == "yes":
                        print("You explode the barrier. The path is now clear")
                        left_hall_c.link_room(main_room, "north")
                        main_room.link_room(left_hall_c, "south")
                        bag.remove("bomb")
                        left_hall_c.set_description(None)
                        main_room.set_description("The command centre of the base.")
                elif current_room == right_hall_d:
                    print("What are you trying to do? (Would you like to use the bomb?)")
                    use_bomb = input("").lower()
                    if use_bomb == "yes":
                        print("Blowing up the wall reveals a hidden area.")
                        right_hall_d.link_room(hidden_room, "north")
                else:
                    print("You cannot use that here.")
            else: 
                print("You cannot use that item here.")
        else:
            print("There are no items to use.")

   
    elif command == "take":
        if room_item != None:
            if isinstance(room_item, Heal):
                print("You cannot take healing items with you.")

            elif isinstance(room_item, Support):
                os.system("printf '\033c'")
                print("\nWould you like to replace your item?")
                print("Current Item: ", end = '')
                if player.get_item() != None:
                    player.get_item().support_describe()
                else:
                    print("None")
                print("\nRoom Item: ", end = '')
                room_item.support_describe()
                take_item = input().lower()
                if take_item == "yes":
                    if player.get_item() == None:
                        print("You take the " + room_item.get_name() + ".")
                        player.set_item(room_item)
                        current_room.set_item(None)
                    else: 
                        print("You take the " + room_item.get_name() + " and leave the " + player.get_item().get_name() + " behind.")
                        temporary_storage = player.get_item()
                        player.set_item(room_item)
                        current_room.set_item(temporary_storage)
                    if player.get_item().get_buff_type() == "health":
                        player_max_hp = player.get_max_hp() + player.get_item().get_buff_amount()
                else:
                    print("You leave the item on the ground.")

            else:
                print("\nWould you like to take " + room_item.get_name() + "?")
                take_conditional = input().lower()
                if take_conditional == "yes":
                    if room_item == disguise:
                        print("You put on the disguise.")
                        disguised = True
                        current_room.set_item(None)
                    else:
                        print("You take the " + room_item.get_name() + ".")
                        bag.append(room_item.get_name())
                        if room_item == data_crystal and security_active == True:
                            alarm = True
                            print("The alarm has been set off.")
                        current_room.set_item(None)
    
                else:
                    print("You leave the item on the ground.")
        else:
            print("There is nothing to take")

    
    elif command == "menu":
        os.system("printf '\033c'")
        print("Name: " + player.get_name())
        print("HP: " + str(player_hp) + "/" + str(player_max_hp))
        print("Weapon: " + player.get_weapon().get_name())
        if player.get_item() != None:
            print("Item: " + player.get_item().get_name())
        else:
            print("Item: None")
        print("Bag: " + str(bag))
        print("Press enter to go back.")
        command = input()

    
    elif command == "escape":
        if current_room == outside:
            if "data crystal" in bag:
                print("You win.")
                break
            else:
                print("You do not have the data crystal") 
        else:
            print("You cannot escape from here.")


    elif command == "help":
        os.system("printf '\033c'")
        print("Commands")
        print("-----------------------")
        print("[Direction] - if there is a somewhere to move to in that direction, move there.")
        print("[Fight] - engage in a fight with the enemy in the room (if there is one).")
        print("[Use] - use an item in the room.")
        print("[Take] - take the item in the room.")
        print("[Menu] - check your player stats, weapons and items.")
        print("[Escape] - escape from outside when you have the win condition.")
        print("-----------------------")
        print("Press enter to go back.")
        input()


    else:
        print("Invalid Input. Enter 'Help' for a list of commands.")


    time.sleep(2)


if in_hidden == True:
    pass
    #whatever, make a boss fight