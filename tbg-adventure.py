# Text Adventure Python Test
# by Tim Hicks 2022
# 6/24/22 - fixed up encounter/combat rounds

import time
import numpy as np
import sys
import random
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
    def __init__(self, name, healthPoints, attackPower, defense, xp, inventory, weapon, castLightFlag):
    # Attack = d6
    # Defense
    # Luck
    # Dodge
        self.name = name
        self.healthPoints = healthPoints
        self.attackPower = attackPower
        self.defense = defense
        self.xp = xp
        self.inventory = [] # lets make inventory 6 slots
        # weapons
        self.weapon = weapon
        #self.spells = [] # spell book
        self.castLightFlag = 0
    
    def attack(self, Target):
        #while (self.healthPoints > 0) and (Target.health > 0):
            # determine damage
        if self.weapon.damage == "d6":
            currentAttackRoll = Game.rollD6()
        elif self.weapon.damage == "d4":
            currentAttackRoll = Game.rollD4()
        delay_print(f"({self.name}) attack roll: {currentAttackRoll}")
        time.sleep(.3)
        if currentAttackRoll == 6:
            delay_print(f" -- Critical hit!")
            Target.healthPoints -= currentAttackRoll
            print (f"\n({Target.type}) health: {Target.healthPoints}")
        elif currentAttackRoll < 6 and currentAttackRoll > 0:
            delay_print(f"\n({Target.type}) defense: {Target.defense}")
            time.sleep(.3)
            totalDamage = currentAttackRoll - Target.defense
            if totalDamage > 0:
                Target.healthPoints -= totalDamage
                delay_print(f"\nDamage dealt to ({Target.type}): {totalDamage}!")
                time.sleep(.3)
                print (f"\n({Target.type}) health: {Target.healthPoints}")
            elif totalDamage <= 0:
                delay_print(f"\n({Target.type}) defended your attack! No damage!")
                time.sleep(.3)
        elif currentAttackRoll >= 0:
            delay_print(f"You missed!")

    def inventoryAdd(self, Target):
        # add item
        # check 6 item limit in inventory
        if len(self.inventory) <= 6:
            self.inventory.append(Target.type)
            print(f"\nYou picked up {Target.type}!")
        else:  
            print(f"\nYou can't hold anymore!")

    def castLight(self):
        print(f"Casting [Light]!")
        Room.Light(self)
        self.castLightFlag += 1
            
    def equipWeapon(self, Target):
        # equip the weapon
        self.weapon = Target
            
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
    
    def checkSpellbook(self):
        print(f"\n ===== SPELLBOOK =====")
        print(f"\n [Light] - cast an intense burst of light, illuminating the area")
        #print(f"\n [Fear] - afflict the target with fear")
        
    def characterSheet(self):
        print (f"\n ====== CHARACTER SHEET ====== ")
        print(f"Name: {self.name}")
        print(f"Level 1 Adventurer")
        print(f"Current HP: {self.healthPoints}")
        print(f"Attack Power: d6")
        print(f"Defense: {self.defense}")
        print(f"Current XP: {self.xp} / 20")
        
    # def search(self):
        #!!!! search the room - should pass through room at later time
        # delay_print(f'\nThere is an item on the floor. Pick it up? [y/n]:')
        # choice = input("\n Selection: ")
        # if choice == "y":
            # self.inventoryAdd(smHealthPotion)
        
    #def moveForward(self):
        # !!!! room
        #delay_print(f"\nYou walk forward into the darkness...")
        #delay_print(f"\n 'RAAAAAHH...'")
        #time.sleep(0.75)
        #print("\nA goblin appears!")
        #Game.initEncounter(p1, Goblin)
        
    def gainXP(self,Target):
        self.xp += Target.xpOut
        print(f"\nYou gain {Target.xpOut} experience!")
        
    def useHealthPotion(self, Target):
        if p1.checkHealthUse() == 1:
            self.healthPoints += Target.healAmt
            print(f"\nYou consumed {Target.type}.")
            print(f"You healed for {Target.healAmt} health!")
            print(f"Your health is now {self.healthPoints}") 
            self.inventory.remove(Target.type)
        elif p1.checkHealthUse() == 0:
            print(f"\nCan't use that item - you are at max health already!")
        
    def checkHealthUse(self):
        if (self.healthPoints < 12):
            return 1
        elif (self.healthPoints >= 12):
            return 0
            
    def checkIsDead(self):
         if self.healthPoints <= 0:
                print(f"\nYou died!")
                delay_print(f"\n ... ")   
                time.sleep(1)
                Game.gameOver()

# monster class contains health, attack
class Monster:
    def __init__(self, type, healthPoints, attackPower, defense, xpOut, lootDrop, weapon, talk):
        self.type = type
        self.healthPoints = healthPoints
        self.attackPower = attackPower
        self.defense = defense
        self.xpOut = xpOut
        self.lootDrop = lootDrop
        self.weapon = weapon
        self.talk = talk
        
    def attack(self, Target):
       #while (self.healthPoints > 0) and (Target.health > 0):
            # determine damage
        if self.weapon.damage == "d6":
            currentAttackRoll = Game.rollD6()
        elif self.weapon.damage == "d4":
            currentAttackRoll = Game.rollD4()
        delay_print(f"({self.type}) attack roll: {currentAttackRoll}")
        time.sleep(.3)
        if currentAttackRoll == 4:
            delay_print(f"  -- Critical hit!")
            Target.healthPoints -= currentAttackRoll
            delay_print(f"\n({Target.name}) health: {Target.healthPoints}")
        elif currentAttackRoll < 4 and currentAttackRoll > 0:
            delay_print(f"\n({Target.name}) defense: {Target.defense}")
            time.sleep(.3)
            totalDamage = currentAttackRoll - Target.defense
            if totalDamage > 0:
                Target.healthPoints -= totalDamage
                delay_print(f"\nDamage dealt to ({Target.name}): {totalDamage}")
                time.sleep(.3)
                delay_print(f"\n({Target.name}) health: {Target.healthPoints}")
            elif totalDamage <= 0:
                delay_print(f"\n({Target.name}) defended ({self.type}) attack!")
                time.sleep(.3)
        elif currentAttackRoll >= 0:
            delay_print(f"\n{self.type} missed!")
            time.sleep(.3)
            
    def checkIsDead(self):
         if self.healthPoints <= 0:
                print(f"\n\n{self.type} has been slain!")
                delay_print(f"\n ... ")
                time.sleep(1)
                self.lootDrop(self)
                
    def lootDropFx():
        #lootDrop = ["{self.weapon}"]
        print(f"{self.type} dropped {self.weapon}")
        

class Item:
    def __init__(self, type, effect):
        self.type = type
        self.effect = effect
        
class Weapon:
    def __init__(self, type, description, damage, cost):
        self.type = type
        self.description = description
        self.damage = damage
        self.cost = cost
        
class potion:
    def __init__(self, type, description, healAmt):
        self.type = type
        self.description = description
        self.healAmt = healAmt
        # health potion not working yet
#class Room:
#    def __init__(self, search, listen)
#        self.search = search
#        self.listen = listen
# game
class Game:
        
    def rollD4():
        return random.randint(1,4)
    
    def rollD6():
        return random.randint(1,6) 
    
    def rollD8():
        print.random.randint(1,8)
    
    def rollD10():
        print.random.randint(1,10)
        
    #def startScreen(self):
    def intro(self):
        print(f"\n <intro skipped>")
        # print(f"\nWhat is your name, adventurer?")
        choice = input("Type your name: ")
        p1.name = choice.capitalize()
        
    def gameOver(self):
        choice = input(f"\n Gameover. Try again?")
        if (choice ==  "y") or (choice == "Y"):
            os.execl(sys.executable, sys.executable, *sys.argv)
        else:  
            quit()
           
    def ui(self):
        print(f"\nWhat would you like to do?")
        print(f"[C]HARACTER SHEET | [I]NVENTORY | [S]PELLBOOK")
        print(f"Or type /command (type /help for list of commands)")
        choice = input("Type selection: ")
        if (choice == "c") or (choice == "C"):
            p1.characterSheet()
        elif (choice == "i") or (choice == "I"):
            p1.checkInventory()
        elif (choice == "s") or (choice == "S"):
            p1.checkSpellbook()
        elif (choice == "/command") or (choice == "/COMMAND"):
            print(f"Type /help for list of /commands")
        elif (choice == "/help") or (choice == "/HELP"):
            print(f"\nRecognized commands: ")
            #print(f"/forward - move forward")
            print(f"/search - search the area")
            print(f"/listen - listen to your surroundings for notable sounds")
            #print(f"/hide - hide behind cover or in the darkness")
            print(f"/cast - cast a spell from your spellbook")
            print(f"/talk <target> - attempt to talk to a target")
            print(f"/rest - rest for a few hours")
            print(f"/sit - sit down")
            #print(f"/shout - shout loudly")
            print(f"/dance - break out into dance <not recommended during dangerous encounters>")
            print(f"\n")
        elif (choice == "/search") or (choice == "/SEARCH"):
            Room.search(self)
        elif (choice == "/listen") or (choice == "/LISTEN"):
            Room.listen(self)
        elif (choice == "/sit") or (choice == "/SIT"):
            Room.sit(self)
        elif (choice == "/dance") or (choice == "/DANCE"):
            Room.dance(self)
        elif (choice == "/talk") or (choice == "/TALK"):
            Room.talk(self)
        elif (choice == "/rest") or (choice == "/REST"):
            Room.rest(self)
        elif (choice == "/cast") or (choice == "/CAST"):
            choice = input(f"Cast [Light]? [y/n]: ")
            if choice == "y":
                p1.castLight()
        #elif (choice == "h") or (choice == "H"):
        #    Game.helpManual(self)
        else:
            print(f"Invalid selection, try again")

    def initEncounter(self, Target):
        while (self.healthPoints > 0 and Target.healthPoints > 0):
            choice = input(f"\n[A]ttack or attempt to [R]un: ")
            if choice == "a" or choice =="A":
                Game.round(self, Target)
            choice = input(f"\n[A]ttack again, or attempt to [R]un: ")
            if choice == "a" or choice == "A":
                Game.round(self, Target)
       
    def round(self, Target):
        print("\n")
        self.attack(Target)
        # target is dead check
        # target health print
        time.sleep(.3)
        if (Target.healthPoints > 0):
            time.sleep(0.85)
            print(f"\n{Target.type} strikes back!\n")
            time.sleep(0.85)
            Target.attack(self)
            #self is dead check
            #get back to prompt
        elif (Target.healthPoints <= 0):
             delay_print(f"\n({Target.type}) has been slain!")
             Target.lootDropFx()
            
class Room:
    def search(self):
        if p1.castLightFlag < 1:
            delay_print(f"\nIt is too dark to search in here. Perhaps if there was a way to light the area ...")
        elif p1.castLightFlag >= 1:
            delay_print(f"\nIt is dark, but you recall when you cast list there was small stone was by your feet...")   
            delay_print(f"\nPick up the stone? [y/n]: ")
        delay_print("\n")
        
    def listen(self):
        delay_print(f"\nYou listen closely - you can hear the shuffling and grumbling of a creature about 20 feet ahead ...")
        delay_print("\n")

    def sit(self):
        delay_print(f"\nYou sit down on the cold, gravel floor. It is slightly damp and not at all comfortable ...")
        delay_print("\n")

    def dance(self):   
        delay_print(f"\nIn the darkness you do the 'Griddy'. Let's hope the shuffling of your clothes doesn't attract any near by creatures ...")
        delay_print("\n")

    def talk(self):
        if p1.castLightFlag < 1:
            delay_print(f"\nYou are alone - you have nobody to talk to ...")
        elif p1.castLightFlag >= 1:
            delay_print(f"\nDo you want to try talking to the goblin in the distance? [y/n]: ")
        delay_print("\n")

    def rest(self):
        delay_print(f"\nYou lay on the cold, damp gravel floor and close your eyes but you can't seem to rest.. It's just not the ideal spot.")
        delay_print("\n")

    def Light(self):
        if p1.castLightFlag < 1:
            delay_print(f"\nAs the room illuminates you see clearly that you are indeed in a dank cave.")
            delay_print(f"\nThe walls surround you closely,")
            delay_print(f"\nand down a narrow passage ahead you see the back of a goblin, shuffling ...")
            delay_print(f"\nThe burst of light startles the goblin - ")
            delay_print(f"\nit is alert now, but does not know where the light came from. The goblin stands in place, on guard.")
            delay_print(f"\nYou also notice a small stone by your feet")
            delay_print(f"\nThe light flickers out, darkness returns ...")
            delay_print(f"\n")
        elif p1.castLightFlag >= 1:
            print(f"\nAre you sure you want to cast light again?")
        
        
if __name__ == '__main__':
    p1 = Player("", 12, randint(1,6), 2, 0, [0], "", 0)
    #room1 = Room("The room is too dark to see. Need a way to light the area", "You can hear a creature moving about 20 feet ahead of you.")
    roughDagger = Weapon("Rough Dagger", "A rough dagger of PRIMITIVE quality.", "d4", 1)
    ironSword = Weapon("Iron Sword", "An iron sword of ROUGH quality.", "d6", 2)
    Goblin = Monster("Goblin", 8, randint(1,4), 1, 5, "Small Health Potion", roughDagger, "The goblin shrieks at you. Seems he does not want to talk.")
    #healthPotion = Item("Health Potion", "Heals the user for +5 health.")
    smHealthPotion = potion("Small Health Potion", "Heals user for +5 health.", 5)
    
    Game.intro(p1)
    # initialize p1 with starting weapon
    #p1.inventoryAdd(ironSword)
    #p1.equipWeapon(ironSword)
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