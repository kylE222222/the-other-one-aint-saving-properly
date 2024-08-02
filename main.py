from room import *
from character import *
from item import *
from moveset import *
from enemy_data_pool import *
from hidden_room import *
import time 
import random
import os


#Room Instantiation
outdoors = Room("The Outdoors", "The enemy base lies ahead.")
supply_room = Room("The Supply Room", "A storage space full of equipment.")
cafeteria = Room("The Cafeteria", "An area to eat and socialise.")
bathroom = Room("The Bathroom", "A place for a momentary break from the action.")
vents = Room("The Vents", "Dark and cramped.")
main_room = Room("The Main Room", "The command centre of the base. The way south is blocked by a particularly explodable barrier.")
training_area = Room("The Training Area", "A high-intensity training facility used to hone the skills of soldiers.")
data_room = Room("The Data Room", "The data centre of the facility and a treasure trove of classified information.")
security_room = Room("The Security Room", "Home to the camera and alarm systems that guard the base.")
hidden_room = Room("████", None)

left_hall_a = Room("Left Hall A", None)
left_hall_b = Room("Left Hall B", None)
left_hall_c = Room("Left Hall C", "A particularly explodable barrier blocks the way north.")

right_hall_a = Room("Right Hall A", None)
right_hall_b = Room("Right Hall B", None)
right_hall_c = Room("Right Hall C", None)
right_hall_d = Room("Right Hall D", None)


#Room Linking: Left Side (Up to Main Room)
left_hall_a.link_room(cafeteria, "north")
left_hall_a.link_room(outdoors, "south")
left_hall_a.link_room(left_hall_b, "west")

left_hall_b.link_room(left_hall_c, "north")
left_hall_b.link_room(left_hall_a, "east")
left_hall_b.link_room(supply_room, "west")

left_hall_c.link_room(left_hall_b, "south")

cafeteria.link_room(vents, "east")
cafeteria.link_room(left_hall_a, "south")

supply_room.link_room(left_hall_b, "east")

#Room Linking: Right Side (Up to Main Room)
right_hall_a.link_room(right_hall_b, "north")
right_hall_a.link_room(outdoors, "south")
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
outdoors.link_room(right_hall_a, "north-east")
outdoors.link_room(left_hall_a, "north-west")

main_room.link_room(data_room, "north")
main_room.link_room(right_hall_d, "east")
main_room.link_room(vents, "south-east")

data_room.link_room(main_room, "south")


#Lists Relevant to Certain/All Rooms
directions = ["north", "north-east", "east", "south-east", "south", "south-west", "west", "north-west"]
vent_exits = [cafeteria, right_hall_b, main_room]
encounterless_rooms = [outdoors, vents, security_room, hidden_room]


#Item Instantiation
data_crystal = Item("Data Crystal", "A capsule containg intel on enemy plans and tactics.")
disguise = Item("Disguise", "Blend in with the opposition.")
flashlight = Item("Flashlight", "Light up the surrounding area.")
bomb = Item("Bomb", "Explosive!")

#Item Subclass: Weapon
baton = Weapon("Baton", None, 10)
knife = Weapon("Knife", None, random.randint(15, 18))
bat = Weapon("Bat", None, random.randint(20, 22))
shovel = Weapon("Shovel", None, random.randint(25, 28))
sword = Weapon("Sword", None, random.randint(30, 32))

#Item Subclass: Heal
banana = Heal("Banana", "Restores 50 HP.", 50)
medkit = Heal("Medkit", "Restores 150 HP.", 150)

#Item Subclass: Support
shield_blocking_time_buff = round(random.uniform(0.1, 0.25),2)
shield = Support("Shield", "Increases number visibility time by " + str(shield_blocking_time_buff) + "s when blocking.", "blocking_time", shield_blocking_time_buff) 
lucky_charm_crit_boost = random.randint(10, 20)
lucky_charm = Support("Lucky Charm", "Provides a critical hit (2x damage) rate of " + str(lucky_charm_crit_boost) + "%", "crit_rate.", lucky_charm_crit_boost)
combat_vest_hp_buff = random.randint(50, 75)
combat_vest = Support("Combat Vest", "Increases max health by " + str(combat_vest_hp_buff) + ".", "health", combat_vest_hp_buff)
tactical_glove_dmg_buff = random.randint(8, 12)
tactical_glove = Support("Tactical Glove", "Increases damage by " + str(tactical_glove_dmg_buff) + ".", "damage", tactical_glove_dmg_buff)


#Placing Items into Rooms
#Set Spawn Locations
data_room.set_item(data_crystal)
supply_room.set_item(disguise)
security_room.set_item(bomb)

#Randomised Spawn Locations
#This list contains all the rooms that can contain random items. The following are not included: outdoors, supply_room, data_room, security_room and hidden_room.
item_rooms = [cafeteria, bathroom, vents, main_room, training_area, left_hall_a, left_hall_b, left_hall_c, right_hall_a, right_hall_b, right_hall_c, right_hall_d]
#This list contains all the items that have a chance to spawn.
item_pool = [flashlight, banana, medkit, shield, lucky_charm, combat_vest, tactical_glove]
for room in item_rooms:
    room_item_chance = random.randint(0,1)
    if room_item_chance == 1:
        room.set_item(random.choice(item_pool))


#Character Instantiation (and Other Things Relevant to the Object)
enemy = Enemy(None, None, None, None)
weapon_pool = [knife, bat, shovel, sword]
moveset = ["attack", "charge", "block"]

security_guard = Enemy("Mike", knife, 125, "Security Guard")
security_room.set_character(security_guard)
security_active = True
alarm = False

game_dev = Enemy("Kyle", None, 150, "Game Developer")

player = Character(None, baton, 250)
player_max_hp = player.get_max_hp()
player_hp = player_max_hp
bag = []
current_room = outdoors
disguised = False
force_fight = False


#MAIN PROCESS
os.system("printf '\033c'")
player_name = input("Enter your character's name: ")
player.set_name(player_name)

os.system("printf '\033c'")
print("Hello " + player.get_name() + ".")
print("You have been tasked to steal a valuable asset from an enemy base: the Data Crystal.")
print("Navigate through the base to find and steal it.")
print("Good luck.")
print("(Hint: Questions are answered with 'Yes' or 'No')")
print("\nPress Enter to Begin")
input('')

loading = "Loading"
for i in range(0,4):
    os.system("printf '\033c'") 
    print(loading)
    loading = loading + "."
    time.sleep(1)

while player_hp > 0:
    os.system("printf '\033c'")
    if current_room == vents and "flashlight" not in bag:
        print("The vents are too dark. You get out at a random exit.")
        current_room = random.choice(vent_exits)
        time.sleep(2)
        os.system("printf '\033c'")

    if force_fight == True:
        command = "fight"
        force_fight = False
    else:
        room_enemy = current_room.get_character() 
        room_item = current_room.get_item() 
        current_room.get_details()
        if room_enemy != None:
            room_enemy.enemy_describe()
        if room_item != None:
            room_item.item_describe()
        print("Enter Help for Controls\n")
        print("What would you like to do?")
        command = input("").lower()
        os.system("printf '\033c'")

    if command == "north" and current_room == right_hall_d and command in current_room.linked_rooms:
        print("Are you sure you would like to continue? (You cannot go back)")
        enter_hidden = input("").lower()
        os.system("printf '\033c'")
        if enter_hidden == "yes":
            current_room = hidden_room
            hidden_room_sequence()
            os.system("printf '\033c'")
            hidden_room_fight(player, player_max_hp, game_dev)
            break

    elif command in current_room.linked_rooms:
        current_room.set_character(None)
        current_room = current_room.move(command)
        time.sleep(2)
        if current_room not in encounterless_rooms:
            enemy_chance = random.randint(0,1)
            if alarm == True:
                enemy_chance = 1
            if enemy_chance == 1:
                enemy.generate_enemy(weapon_pool)
                current_room.set_character(enemy)
                room_enemy = current_room.get_character()
                if disguised == False:
                    os.system("printf '\033c'")
                    print("You are spotted by " + room_enemy.get_rank() + " " + room_enemy.get_name() + ".")
                    force_fight = True
                    time.sleep(2)

    elif command in directions:
        print("You cannot go that way.")
        time.sleep(2)

    elif command == "fight":
        if room_enemy != None:
            room_enemy.begin_fight()
            player_charged = False
            player_blocking = False
            enemy_charged = False
            enemy_blocking = False
            enemy_hp = room_enemy.get_max_hp()
            while enemy_hp > 0 and player_hp > 0:
                print("Your HP: " + str(player_hp) + "/" + str(player_max_hp))
                print(room_enemy.get_rank(), room_enemy.get_name() + "'s HP: " + str(enemy_hp) + "/" + str(room_enemy.get_max_hp()))
                print("\nEnter Help for Controls")
                print("\nWhat will you do?")
                player_fight_action = input().lower()
                os.system("printf '\033c'")
                player_blocking = False
                if player_fight_action == "attack":
                    if enemy_blocking == True:
                        print(player.get_name() + "'s attack is blocked by " + room_enemy.get_rank() + " " + room_enemy.get_name())
                    else:
                        enemy_hp = attack(player.get_name(), player.get_weapon(), player.get_item(), player_charged, enemy_hp)
                    player_charged = False
                elif player_fight_action == "charge":
                    player_charged = charge(player.get_name(), None)
                elif player_fight_action == "block":
                    player_blocking = block(player.get_name(), None, player.get_item(), "player")
                elif player_fight_action == "run":
                    run_success = run(player.get_name())
                    if run_success == True:
                        random_direction = random.choice(directions)
                        while random_direction not in current_room.linked_rooms:
                            random_direction = random.choice(directions)
                        current_room = current_room.linked_rooms[random_direction]
                        print(player.get_name() + " runs off in a random direction.")
                        break 
                elif player_fight_action == "help":
                    print("Controls")
                    print("-----------------------")
                    print("[Attack] - strike the enemy with your weapon.")
                    print("[Charge] - charge up your next attack to deal 1.5x damage.")
                    print("[Block] - successfully enter the 3 numbers shown to block the enemy's attack.")
                    print("[Run] - attempt to run from the fight. If successful, you will enter a random adjacent room.")
                    print("-----------------------")
                    print("Press enter to go back.")
                    input()
                else:
                    print("Invalid Input. Enter 'Help' for a list of commands.")
                    player_fight_action = "help"
                if player_fight_action != "help" and enemy_hp > 0:
                    enemy_blocking = False
                    time.sleep(1)
                    enemy_fight_action = random.choice(moveset)
                    if enemy_fight_action == "attack":
                        if player_blocking == True:
                            print(room_enemy.get_rank() + " " + room_enemy.get_name() + "'s attack is blocked by " + player.get_name()) 
                        else:
                            player_hp = attack(room_enemy.get_name(), room_enemy.get_weapon(), None, enemy_charged, player_hp)
                        enemy_charged = False
                    elif enemy_fight_action == "charge":
                        enemy_charged = charge(room_enemy.get_name(), room_enemy.get_rank())
                    elif enemy_fight_action == "block": 
                        enemy_blocking = block(room_enemy.get_name(), room_enemy.get_rank(), None, "enemy")   
                time.sleep(2)
                os.system("printf '\033c'")
                if player_hp <= 0:
                    print("Game over. You have died.")
                    break
                if enemy_hp <= 0:
                    print("You defeated " + room_enemy.get_rank() + " " + room_enemy.get_name() + ".")
                    if room_enemy == security_guard:
                        print("The security system has been disabled.")
                        security_active = False
                        if alarm == True:
                            print("...but the enemies are already aware of your presence.")
                    time.sleep(2)
                    os.system("printf '\033c'")
                    drop_chance = random.randint(0,1)
                    if drop_chance == 1:
                        print(room_enemy.get_rank() + " " + room_enemy.get_name() + " drops his " + room_enemy.get_weapon().get_name() + ".")
                        print("Would you like to replace your current weapon?")
                        print("Current Weapon: ", end = '')
                        player.get_weapon().weapon_describe()
                        print("\nDropped Weapon: ", end = '')
                        room_enemy.get_weapon().weapon_describe()
                        take_weapon = input().lower()
                        os.system("printf '\033c'")
                        if take_weapon == "yes":
                            print("You take the " + room_enemy.get_weapon().get_name() + ".\n")
                            player.set_weapon(room_enemy.get_weapon())

                        else:
                            print("You leave the weapon behind.\n")
                    current_room.set_character(None)
                    print("You recover 25 HP for winning the fight.")
                    player_hp += 25
        else:
            print("There is no one to fight here.")
        time.sleep(2)

    elif command == "use":
        if isinstance(room_item, Heal) or len(bag) > 0:
            os.system("printf '\033c'")
            print("What would you like to use?")
            if isinstance(room_item, Heal): 
                print("Room item: " + room_item.get_name())
            if len(bag) > 0:
                print("Bag: " + str(bag))
            item_to_use = input().capitalize()
            os.system("printf '\033c'")
            if item_to_use in bag:
                if item_to_use == "Bomb":
                    if current_room == left_hall_c or current_room == main_room:
                        print("Are you sure you want to use the Bomb?")
                        use_bomb = input("").lower()
                        os.system("printf '\033c'")
                        if use_bomb == "yes":
                            print("You blow up the barrier. The path is now clear")
                            left_hall_c.link_room(main_room, "north")
                            left_hall_c.set_description(None)
                            main_room.link_room(left_hall_c, "south")
                            main_room.set_description("The command centre of the base.")
                            bag.remove("Bomb")
                        else:
                            print("You put the Bomb back in your bag.")
                    elif current_room == right_hall_d:
                        print("What are you trying to do? (Would you like to use the Bomb?)")
                        use_bomb = input("").lower()
                        os.system("printf '\033c'")
                        if use_bomb == "yes":
                            print("What have you done?")
                            right_hall_d.link_room(hidden_room, "north")
                        else:
                            print("You put the Bomb back in your bag.")
                else:
                    print("You cannot use that item here.")
            elif isinstance(room_item, Heal):
                if item_to_use == room_item.get_name():
                    print("Are you sure you want to use the " + room_item.get_name() + "?")
                    use_heal = input().lower()
                    if use_heal == "yes":
                        if player_hp == player.max_hp:
                            print("You are already at max health.")
                        else:
                            room_item.use_heal(player.get_name())
                            player_hp += room_item.get_heal_amount()
                            if player_hp > player_max_hp:
                                player_hp = player_max_hp
                            current_room.set_item(None)
            else:
                print("That item is not here.")
        else:
            print("There are no items to use.")
        time.sleep(2)

   
    elif command == "take":
        if room_item != None:
            if isinstance(room_item, Heal):
                print("You cannot take heals with you.")
            elif isinstance(room_item, Support):
                print("Would you like to replace your item?")
                print("Current Item: ", end = '')
                if player.get_item() != None:
                    player.get_item().support_describe()
                else:
                    print("None")
                print("\nRoom Item: ", end = '')
                room_item.support_describe()
                take_item = input().lower()
                os.system("printf '\033c'")
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
                print("Would you like to take " + room_item.get_name() + "?")
                take_conditional = input().lower()
                os.system("printf '\033c'")
                if take_conditional == "yes":
                    if room_item == disguise:
                        print("You put on the disguise. Enemies will no longer attack you.")
                        disguised = True
                    elif room_item == flashlight:
                        vents.link_room(cafeteria, "west")
                        vents.link_room(right_hall_b, "east")
                        vents.link_room(main_room, "north-west")
                        print("You take the flashlight. You can now choose where to exit from in the vents.")
                    else:
                        print("You take the " + room_item.get_name() + ".")
                        if room_item == data_crystal and security_active == True:
                            alarm = True
                            print("The alarm has been set off. A disguise will no longer fool enemies.")
                            if "disguise" in bag:
                                disguised = False
                    bag.append(room_item.get_name())
                    current_room.set_item(None)
                else:
                    print("You leave the item on the ground.")

        else:
            print("There is nothing to take.")
        time.sleep(2)

    
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
        print("\nPress enter to go back.")
        input()


    elif command == "escape":
        os.system("printf '\033c'")
        if current_room == outdoors and "Data Crystal" in bag:
            print("You successfully steal the Data Crystal and escape. You win!")
            print("You feel that you have missed out on something important.")
            print("(Hint: Use the Bomb at Right Hall D)")
            break
        if "Data Crystal" in bag:
            print("Get outdoors to escape.")
        elif current_room == outdoors:
            print("Get the Data Crystal to escape.")
        else:
            print("You can't escape yet.")
        time.sleep(2)


    elif command == "help":
        print("Commands")
        print("-----------------------")
        print("[Direction] - move in the specified direction to a nearby room.")
        print("[Fight] - engage in a fight with the enemy in the room.")
        print("[Use] - use an item in the room or in your bag.")
        print("[Take] - take the item in the room.")
        print("[Menu] - check your player stats, weapons and items.")
        print("[Escape] - escape the enemy base once you have the data crystal and are outdoors.")
        print("-----------------------")
        print("Press enter to go back.")
        input()


    else:
        print("Invalid Input. Enter 'Help' for a list of commands.")
        time.sleep(2)

 