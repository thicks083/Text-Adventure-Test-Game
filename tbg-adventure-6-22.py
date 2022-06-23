# Text Adventure Python Test
# by Tim Hicks 2022
# 6/22/22 - worked on inventory a bit, still working on consumable, then weapons

import time
import numpy as np
import sys
from random import randint
import unicodedata

# delay printing
def delay_print(s):
    for c in s:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(0.05)

# player class, contains health and damage
class Player:
    def __init__(self, name, healthPoints, attackPower, defense, xp, inventory):
        self.name = name
        self.healthPoints = healthPoints
        self.attackPower = attackPower
        self.defense = defense
        self.xp = xp
        self.inventory = [] # lets make inventory 6 slots
    
    def attack(self, Target):
        #while (self.healthPoints > 0) and (Target.health > 0):
            # determine damage
        Target.healthPoints -= self.attackPower
        currentAttack = int(self.attackPower)
        currentDefense = int(Target.defense)
        print(f"\nYou attack with: ({currentAttack})")
        time.sleep(0.75)
        print(f"{Target.type} defense: ({Target.defense})")
        time.sleep(0.75)
        totalDamage =  currentAttack - currentDefense
        if totalDamage > 0:
            print(f"{Target.type} takes", totalDamage, "damage!")
            time.sleep(0.75)
        elif totalDamage <= 0:
            print(f"Failed to damage {Target.type}")
            time.sleep(0.75)
        print(f"{Target.type} health: ({Target.healthPoints})") 
        time.sleep(0.75)

    def inventoryAdd(self, Target):
        # add item
        # check 6 item limit in inventory
        if len(self.inventory) <= 6:
            self.inventory.append(Target.type)
            print(f"\nYou picked up {Target.type}!")
        else:  
            print(f"\nYou can't hold anymore!")
            
    def lootMonster(self, Target):
        if len(self.inventory) <= 6:
            self.inventory.append(Target.lootDrop)
            print(f"You picked up {Target.lootDrop}!")
        else:  
            print(f"\nYou can't hold anymore!")
        
    def checkInventory(self):
        # check inventory
        print(f"\n ====== INVENTORY ======")
        i = 0
        while i < len(self.inventory):
            #print(f"{len(self.inventory)}")
            print(f"{i+1}: {self.inventory[i]}")
            i += 1
        choice = input("Select number of item to use, or [I] to exit: ")
        if (choice == "1"): 
            self.useHealthPotion(smHealthPotion)
        
    def characterSheet(self):
        print (f"\n ====== CHARACTER SHEET ====== ")
        print(f"Name: {self.name}")
        print(f"Level 1 Adventurer")
        print(f"Current HP: {self.healthPoints}")
        print(f"Attack Power: d6")
        print(f"Defense: {self.defense}")
        print(f"Current XP: {self.xp} / 20")
        
    def search(self):
        # !!!! search the room - should pass through room at later time
        delay_print(f"\nYou look around the room, but it is dark. You hear noises ahead..")
        time.sleep(0.75)
        delay_print(f"\n ...\n")
        time.sleep(0.75)
        delay_print(f'\nThere is an item on the floor. Pick it up? [y/n]:')
        choice = input("\n Selection: ")
        if choice == "y":
            self.inventoryAdd(smHealthPotion)
        
    def moveForward(self):
        # !!!! room
        delay_print(f"\nYou walk forward into the darkness...")
        delay_print(f"\n 'RAAAAAHH...'")
        time.sleep(0.75)
        print("\nA goblin appears!")
        Game.encounter(p1, Goblin)
        # time.sleep(1)
        # print(f"\n[A]ttack or try to [R]un?")
        # choice = input("Enter selection [A/R]: ")
        # if (choice == "a") or (choice == "A"):
            # Game.encounter(p1, Goblin)
            # elif (choice =="r") or (choice=="R") or (choice=="run") or (choice=="Run") or (choice=="RUN"):
                # print(f"\n You try to flee, but there's no way out!!!")
                # print(f"{Target.type} strikes you while you try to flee!!!")
                # Target.attack(self)
        
    def gainXP(self,Target):
        self.xp += Target.xpOut
        print(f"\nYou gain {Target.xpOut} experience!")
        
    def useHealthPotion(self, Target):
        self.healthPoints += Target.healAmt
        print(f"\nYou consumed {Target.type}.")
        print(f"You healed for {Target.healAmt} health!")
        print(f"Your health is now {self.healthPoints}") 

# monster class contains health, attack
class Monster:
    def __init__(self, type, healthPoints, attackPower, defense, xpOut, lootDrop):
        self.type = type
        self.healthPoints = healthPoints
        self.attackPower = attackPower
        self.defense = defense
        self.xpOut = xpOut
        self.lootDrop = lootDrop
        
    def attack(self, Target):
       #while (self.healthPoints > 0) and (Target.health > 0):
            # determine damage
        Target.healthPoints -= self.attackPower
        currentAttack = int(self.attackPower)
        currentDefense = int(Target.defense)
        print(f"\n{self.type} attacks with: ({currentAttack})")
        time.sleep(0.75)
        print(f"Player defense: ({Target.defense})")
        time.sleep(0.75)
        totalDamage =  currentAttack - currentDefense
        if totalDamage > 0:
            print(f"You take", totalDamage, "damage!")
            time.sleep(0.75)
            print(f"Player health: ({Target.healthPoints})") 
            time.sleep(0.75)
        elif totalDamage <= 0:
            print(f"{self.type} failed to damage you!")
            time.sleep(0.75)


class Item:
    def __init__(self, type, effect):
        self.type = type
        self. effect = effect
        
class potion:
    def __init__(self, type, description, healAmt):
        self.type = type
        self.description = description
        self.healAmt = healAmt
        # health potion not working yet
        
class Game:
    #def startScreen(self):
    def intro(self):
        print(f"\nWhat is your name, adventurer?")
        choice = input("Type your name: ")
        p1.name = choice.capitalize()
        delay_print(f"\n {choice.capitalize()}, your adventure awaits...")
        delay_print(f"\n ... ")
        delay_print(f"\n You awake in a dark cave, with no memory of how you got here...\n")
   
    def gameOver(self):
        choice = input(f"\n Gameover. Try again?")
        if (choice ==  "y") or (choice == "Y"):
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:  
            quit()
           
    def ui(self):
        print(f"\nWhat would you like to do?")
        print(f"[M]OVE | [S]EARCH | [C]HARACTER SHEET | [I]NVENTORY ")
        choice = input("Type letter for selection: ")
        if (choice == "c") or (choice == "C"):
            p1.characterSheet()
        elif (choice == "s") or (choice == "S"):
            p1.search()
        elif (choice == "m") or (choice == "M"):
            p1.moveForward()
        elif (choice == "i") or (choice == "I"):
            p1.checkInventory()
        #elif (choice == "h") or (choice == "H"):
        #    Game.helpManual(self)
        else:
            print(f"Invalid selection, try again")
    
    #def helpManual(self):
    #    print(f"\n ===== HELP MANUAL ===== ")
    #    print(f"\n Just litterally type your selection.")
    #    print(f"\n - Tim")
           

    def encounter(self, Target):
        while (self.healthPoints > 0) and (Target.healthPoints > 0):
            # 1st turn
            self.attack(Target)
            #check to see if target has dead
            if Target.healthPoints <= 0:
                print(f"\nEnemy slain!")
                delay_print(f" ... ")   
                time.sleep(1) 
                p1.gainXP(Target)
                p1.lootMonster(Target)
                break
            # 2nd turn
            print(f"\n{Target.type} strikes back!\n")
            Target.attack(self)
            #check if self dead
            if self.healthPoints <= 0:
                print(f"\nYou died!")
                delay_print(f"\n ... ")   
                time.sleep(1)
                Game.gameOver()
                break
            choice = input("\n[A]ttack or try to [R]un?")
            if (choice == "a") or (choice == "A"):
                continue
            elif (choice =="r") or (choice=="R") or (choice=="run") or (choice=="Run") or (choice=="RUN"):
                print(f"\n You try to flee, but there's no way out!!!")
                print(f"{Target.type} strikes you while you try to flee!!!")
                Target.attack(self)
            else:
                break

        
if __name__ == '__main__':
    p1 = Player("", 12, randint(1,6), 2, 0, [0])
    Goblin = Monster("Goblin", 8, randint(1,4), 1, 5, "Small Health Potion")
    Dragon = Monster("Dragon", 100, randint(30,40), 25, 1000, "Rune of Amara")
    #healthPotion = Item("Health Potion", "Heals the user for +5 health.")
    smHealthPotion = potion("Small Health Potion", "Heals user for +5 health.", 5)
    
    Game.intro(p1)
    while (1):  
        #Game.startScreen(p1)
        Game.ui(p1)
   
    
    # delay_print("\nOh shit, now a dragon ...")
    # time.sleep(1)
    # choice = input("\nShoul you attack? [y/n] ")
    # if choice == "y":
        # Game.encounter(p1, Dragon)
        
    # print("\nGoblin attacks you back!")
    # time.sleep(1)
    # Goblin.attack(p1)
    
    # choice = input("\nAttack again [y/n]? ")
    # if choice == "y":
        # p1.attack(Goblin)