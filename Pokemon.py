#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from collections import namedtuple
import random

# Class that handles scanning of Pokemon and Moves, First team to attack, forming teams (randomly), and opponent AI
class Pokemon:
    def scanPokes(fileName):
        # Dictionary of Pokemon
        pokeData = {}
        reader = open(fileName, "r")
        # Skip header row
        firstLine = reader.readline()
        
        # Scan in Pokemon data
        for line in reader:
            strList = line.split(",")
    
            pokeName = strList[0] #Pokemon name
            pokeType = strList[1] #Pokemon type
            hp = strList[2] #Pokemon hp
            attack = strList[3] #Pokemon attack
            defense = strList[4] #Pokemon defense
    
            strList = line.split("[")
            movesList = strList[1]
            movesList = movesList.split("]")
            moves = movesList[0] #Pokemon moves
            movesList = moves.split("'")
            # If only 1 move is available (Magikarp)
            if len(movesList) == 3:
                move1 = movesList[1]
                move2 = movesList[1]
                move3 = movesList[1]
                move4 = movesList[1]
                move5 = movesList[1]
            # Parse each move
            else:
                move1 = movesList[1]
                move2 = movesList[3]
                move3 = movesList[5]
                move4 = movesList[7]
                move5 = movesList[9]
    
            # Tuple of 'named' Pokemon traits
            traits = namedtuple('pokeTraits', ['type', 'hp', 'attack', 'defense', 'm1', 'm2', 'm3', 'm4', 'm5'])
            pokeTraits = traits(pokeType, hp, attack, defense, move1, move2, move3, move4, move5)
    
            # Append dictionary new Pokemon
            pokeData[pokeName] = pokeTraits
        reader.close()
        return pokeData
    def scanMoves(fileName):
        # Dictionary of Moves
        moveData = {}
        reader = open(fileName, "r")
        # Skip header row
        firstLine = reader.readline()
        
        # Scan in Move data
        for line in reader:
            strList = line.split(",")
    
            moveName = strList[0] #Move name
            moveType = strList[1] #Move type
            power = strList[5] #Move power
    
            # Tuple of 'named' move traits
            traits = namedtuple('moveTraits',['type', 'power'])
            moveTraits = traits(moveType, power)
    
            # Append dictionary new Move
            moveData[moveName] = moveTraits
        reader.close()
        return moveData
    def getTeams(pokeData):
        # Randomly choose Pokemon (no repeats)
        chosenMons = random.sample(list(pokeData.keys()), 6)
        return chosenMons
    def coinFlip():
        # Random Team to attack first
        first = random.choice([0,1])
        return first
    def oppAI():
        # Opponent AI, randomly chooses from Pokemon's available moves
        chosenMove = random.choice([1,2,3,4,5])
        return chosenMove

