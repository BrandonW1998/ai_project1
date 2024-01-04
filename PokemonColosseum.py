#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import Pokemon
from collections import namedtuple
import random

# Calculate damage given attacker, defender, and move
def calcDmg(pokeA, pokeD, move):
    p = int(moveData[move].power) #Move power
    a = int(pokeData[pokeA].attack) #Attacker's attack stat
    d = int(pokeData[pokeD].defense) #Defender's defense stat
    aType = pokeData[pokeA].type #Attacker's type
    dType = pokeData[pokeD].type #Defender's type
    mType = moveData[move].type #Move type
    r = random.choice([0.5, 0.6, 0.7, 0.8, 0.9, 1.0]) #Random value
    stab = 1.0 #Same Type Attack Bonus
    te = 1.0 #Type Effectiveness
    
    # If Attacker/Move are same type, increase STAB value
    if (aType == mType):
        stab = 1.5
    
    # Check effectiveness of Move vs. Defender
    # If move is fire
    if (mType == "Fire"):
        # Not very effective vs. fire and water
        if (dType == "Fire" or dType == "Water"):
            print("It's not very effective!")
            te = 0.5
        # Super effective vs. grass
        elif(dType == "Grass"):
            print("It's super effective!!!")
            te = 2.0
    elif (mType == "Water"):
        if (dType == "Water" or dType == "Grass"):
            print("It's not very effective!")
            te = 0.5
        elif(dType == "Fire"):
            print("It's super effective!!!")
            te = 2.0
    elif (mType == "Electric"):
        if (dType == "Electric" or dType == "Grass"):
            print("It's not very effective!")
            te = 0.5
        elif(dType == "Water"):
            print("It's super effective!!!")
            te = 2.0
    elif (mType == "Grass"):
        if (dType == "Fire" or dType == "Grass"):
            print("It's not very effective!")
            te = 0.5
        elif(dType == "Water"):
            print("It's super effective!!!")
            te = 2.0
    damage = (p * a / d * stab * te * r) # (Power*Attack/Defense*STAB*TypeEffectiveness*Random)
    damage = int(damage) #Truncate result
    return damage

# Main thread
# Pokemon Colosseum: A Pokemon battle simulator

# Initialize Pokemon Data
pokeData = Pokemon.Pokemon.scanPokes("pokemon-data.csv")
# Initialize Move Data
moveData = Pokemon.Pokemon.scanMoves("moves-data.csv")

# Prompt and scan player name
print("Welcome to the Colosseum!\n")
playerName = input("Enter your name: ")
print("")

# Pick random set of Pokemon for each team
chosenMons = Pokemon.Pokemon.getTeams(pokeData)
pQueue = [] #Player's Pokemon Queue
cQueue = [] #Computer's Pokemon Queue
# Add picked Pokemon to queues
pQueue.append(chosenMons[0])
pQueue.append(chosenMons[1])
pQueue.append(chosenMons[2])
cQueue.append(chosenMons[3])
cQueue.append(chosenMons[4])
cQueue.append(chosenMons[5])

# Display each Pokemon team
print("Team Rocket enters the Colosseum with " + cQueue[0] + ", " + cQueue[1] + ", and " + cQueue[2] + "\n")
print("Team", playerName, "enters the Colosseum with " + pQueue[0] + ", " + pQueue[1] + ", and " + pQueue[2] + "\n")

# Decide whos turn is first
turn = Pokemon.Pokemon.coinFlip()
# 0 = CPU
if turn == 0:
    firstPlay = "Rocket"
# 1 = Player
else:
    firstPlay = playerName

# Display team that will attack first
print("The coin flip goes up... And the first to attack is Team " + firstPlay + "!\n")
print("Fight!!!\n")

currOpp = cQueue.pop(0) #Current CPU Pokemon
currOppHp = int(pokeData[currOpp].hp) #Current CPU Pokemon HP
currPoke = pQueue.pop(0) #Current Player Pokemon
currPokeHp = int(pokeData[currPoke].hp) #Current Player Pokemon HP
mUseFlags = [False, False, False, False, False] #Flag for move usage

# Run game logic, until end of game is reached
while True:
    # CPU turn
    if turn == 0:
        # Run CPU's AI (random) to pick move
        chosenMove = Pokemon.Pokemon.oppAI()
        # Assign opponent's attack
        if chosenMove == 1:
            oppAttack = pokeData[currOpp].m1
        elif chosenMove == 2:
            oppAttack = pokeData[currOpp].m2
        elif chosenMove == 3:
            oppAttack = pokeData[currOpp].m3
        elif chosenMove == 4:
            oppAttack = pokeData[currOpp].m4
        elif chosenMove == 5:
            oppAttack = pokeData[currOpp].m5
        # Display opponent's attack
        print("Team Rocket's " + currOpp + " used " + oppAttack + " on " + currPoke + "!\n")
        # Calculate damage to Player Pokemon
        damage = calcDmg(currOpp, currPoke, oppAttack)
        print(currPoke + " took " + str(damage) + " damage!\n")
        # Update HP
        currPokeHp -= damage
        # If Pokemon fainted
        if currPokeHp <= 0:
            print(currPoke + " fainted...\n")
            # If Pokemon available in queue, send next Pokemon
            if len(pQueue) > 0:
                currPoke = pQueue.pop(0)
                currPokeHp = int(pokeData[currPoke].hp)
                # Reset Move Usage
                mUseFlags = [False, False, False, False, False]
                print("Team " + playerName + " sent out " + currPoke + "!\n")
            # If no Pokemon remaining, lose game
            else:
                print("Team " + playerName + " has no remaining Pokemon...\n")
                print("You Lose!")
                break
        # If Pokemon didn't faint
        else:
            print("Now " + currPoke + " has " + str(currPokeHp) + " HP and " + currOpp + " has " + str(currOppHp) + "HP\n")
        # Alternate turn
        turn = 1
    # Player turn
    else:
        movePicked = False #Flag for checking valid move
        while movePicked == False:
            # Display list of available moves
            print("Choose a move for " + currPoke + ":")
            for x in range(5):
                if mUseFlags[x] == False:
                    print(str(x+1) + ". " + pokeData[currPoke][x+4])
                else:
                    print(str(x+1) + ". " + pokeData[currPoke][x+4] + " (N/A)")
            chosenMove = input("Team " + playerName + "'s choice is ")
            print("")
            
            # Validate/Assign player move choice
            if chosenMove == "1" and mUseFlags[0] == False:
                chosenMove = pokeData[currPoke].m1
                movePicked = True
                mUseFlags[0] = True
            elif chosenMove == "2" and mUseFlags[1] == False:
                chosenMove = pokeData[currPoke].m2
                movePicked = True
                mUseFlags[1] = True
            elif chosenMove == "3" and mUseFlags[2] == False:
                chosenMove = pokeData[currPoke].m3
                movePicked = True
                mUseFlags[2] = True
            elif chosenMove == "4" and mUseFlags[3] == False:
                chosenMove = pokeData[currPoke].m4
                movePicked = True
                mUseFlags[3] = True
            elif chosenMove == "5" and mUseFlags[4] == False:
                chosenMove = pokeData[currPoke].m5
                movePicked = True
                mUseFlags[4] = True
            else:
                print("Invalid choice\n")
        
        print("Team " + playerName + "'s " + currPoke + " used " + chosenMove + " on " + currOpp + "!\n")
        damage = calcDmg(currPoke, currOpp, chosenMove)
        print(currOpp + " took " + str(damage) + " damage!\n")
        currOppHp -= damage
        if currOppHp <= 0:
            print(currOpp + " fainted...\n")
            if len(cQueue) > 0:
                currOpp = cQueue.pop(0)
                currOppHp = int(pokeData[currOpp].hp)
                print("Team Rocket sent out " + currOpp + "!\n")
            else:
                print("Team Rocket has no remaining Pokemon...\n")
                print("You Win!")
                break
        else:
            print("Now " + currPoke + " has " + str(currPokeHp) + " HP and " + currOpp + " has " + str(currOppHp) + "HP\n")
        turn = 0

