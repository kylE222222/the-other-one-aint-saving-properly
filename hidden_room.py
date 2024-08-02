from room import *
from character import *
from item import *
from moveset import *
from enemy_data_pool import *
import time 
import random
import os


def display(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.05)
    user_input = input("\n")
    return user_input


def hidden_room_sequence():
    display("You enter ████.")
    display("The room behind you has disappeared.")
    display("You're in a pitch-black void.")
    display("...")
    display("You run into an.. enemy..?")
    os.system("printf '\033c'")
    display("You engage in a fight with RWQFSFASXC.")
    player_fight_action = ""
    while player_fight_action != "run":
        print("Player HP: ???/???")
        print("RWQFSFASXC's HP: 56E2CD8/V9apyCxS")
        print("\nEnter Help for Controls")
        print("\nWhat will you do?")
        player_fight_action = input().lower()
        os.system("printf '\033c'")
        if player_fight_action == "help":
            print("₵Ø₦₮ⱤØⱠ₴")
            print("-----------------------")
            print("[ⱤɄ₦] -")
            print("[ⱤɄ₦] -")
            print("[ⱤɄ₦] -")
            print("[Run] - attempt to run from the fight. If successful, you will enter a random adjacent room.")
            print("-----------------------")
            print("█████ █████ ██ ₲Ø ฿₳₵₭.")
            input()
        elif player_fight_action == "run":
            print("ɎØɄ ⱤɄ₦ ₣ⱤØ₥ ł₮...")
            time.sleep(2)
        else:
            print("Y O U  C A N ' T.")
            time.sleep(1)
            print("RWQFSFASXC uses 0̴̣̀̓̔1̴̼̱͖̝̗͉̦̞̘̑̿̆̋̉̅̄̎1̵̨͎̻̜̹͕̳̮̜̑̇ͅ0̶͍͓̄͑͐͜0̸̢̧͙̼̱̼̤̱̗̑̃̋́̕0̸̪̫̗̬̿̇͐̾͌͂̚̚͘ͅͅ0̵̡̭͍͚̮̜̬͇̏̈́̾̈̽̿1̸̥͋̽͂̆̐̕ ̷̣̲͙̺̼̥̝̘͍̐̋͛͑͂̽̏̇̚͝0̴̢̡̱̦̟͓̀̏̚1̵̞̱̞̺̩̫̜̗̙̭̋̿̐̔̋́̈́͂1̷͕̬̻̣̘̲͉̲͙͐̈́̉̂̔̈́̄̅͝͝1̷͍͌̌̄0̸͓͗̂̾̊̔̃͠͝͝1̸͕̺͖̓0̷͖͖̬͉̞̖̮̍̓̃͑̾̅̔̿̚͜͠ͅ0̴̜̭͔̹͙̀̉̐͆̈́̋̇͜ ̵̞̻͋̇̔̈́͝0̷̭̻̣̮͕̭͇͔͌̄͌̈́͂̃͊̓͝͝ͅ1̷͚̳̩̺̲̭̘͚͔̑̀́̀͌̂̿͜͝1̸̧̲̥͚̮̝̮͉̉́̔ͅ0̶͉̣̀̃̐͒̕1̴͎͖̓̈͑̋̇͆͛̆̉0̴̪͛̅̓̊́̊̚1̵̛̦͉͚̖́̒̓̉ͅ1̶̞̺̓̆̆̿̈́̿͌")
            time.sleep(2)
        os.system("printf '\033c'")
    display("Where are you now?")
    display("You have no choice but to continue moving forward.")
    display("...")
    display("There's something in the distance.")
    display("It's a room.")
    display("You see someone sitting at their desk.")
    os.system("printf '\033c'") 
    display("???: Oh, hello.")
    display("???: What are you doing here?")
    display("???: How did you even get here? This place is out of bounds.")
    display("???: ...")
    display("???: I see. ")
    display("???: So you broke my game, huh?")
    display("???: Then you are a threat.")
    display("???: ɎØɄ ₥Ʉ₴₮ ฿Ɇ ɆӾ₮ɆⱤ₥ł₦₳₮ɆĐ.")


def hidden_room_fight(player, player_max_hp, enemy):
    enemy_hp = enemy.get_max_hp()
    player_charged = False
    display("You engage in a fight with " + enemy.get_rank() + " " + enemy.get_name() + ".")
    while enemy_hp > 0:
        print("Player HP: ???" + "/" + str(player_max_hp))
        print(enemy.get_rank(), enemy.get_name() + "'s HP: " + str(enemy_hp) + "/" + str(enemy.get_max_hp()))
        print("\nEnter Help for Controls")
        print("\nWhat will you do?")
        player_fight_action = input().lower()
        os.system("printf '\033c'") 
        if player_fight_action == "attack":
            enemy_hp = attack(player.get_name(), player.get_weapon(), player.get_item(), player_charged, enemy_hp)
            player_charged = False
        elif player_fight_action == "charge":
            player_charged = charge(player.get_name())
        elif player_fight_action == "block":
            block(player.get_name(), None, player.get_item(), "player")
        elif player_fight_action == "run":
           print("There's nowhere to run to.")
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
            player_fight_action = "move fail"
        if enemy_hp > 0:
            if player_fight_action == "move fail":
                print("Game Developer Kyle: " + random.choice(get_dev_move_fail_dialogue_pool()))
                time.sleep(2)
            print("Game Developer Kyle attacks.")
            time.sleep(1)
            print("The attack phases through " + player.get_name() + ".")
            time.sleep(2)
            print("Game Developer Kyle: " + random.choice(get_dev_dialogue_pool()))
            time.sleep(2)
        os.system("printf '\033c'")
    time.sleep(2)
    display("Game Developer Kyle: Impossible...")
    display("You defeated Game Developer Kyle!")
    display("He drops a note on the ground.")
    read_note = ""
    while read_note != "yes":
        read_note = display("Read the note?")
        os.system("printf '\033c'")
        if read_note != "yes":
            print("READ IT")
            time.sleep(2)
            os.system("printf '\033c'")
    display("You read the note.")
    display("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    display("What's that supposed to mean?")
    display("The End...?")
