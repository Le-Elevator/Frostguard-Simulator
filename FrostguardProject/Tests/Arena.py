# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:54:04 2025

@author: Admin
"""

import matplotlib.pyplot as plt
import numpy as np
from fontTools.ttLib.tables.C_P_A_L_ import Color

from Frostguard.pc import Kämpfer, Zauberer, Berserker, Kleriker
from Frostguard.monsters import Goblin, Wolf, Bear
from Frostguard.battle import Battle


# Create Goblins
goblin1 = Goblin('Goblin1')
goblin2 = Goblin('Goblin2')
goblin3 = Goblin('Goblin3')
goblin4 = Goblin('Goblin4')
goblin5 = Goblin('Goblin5')
goblin6 = Goblin('Goblin6')


# Create Wolves
wolf1 = Wolf('Wolf1')
wolf2 = Wolf('Wolf2')
wolf3 = Wolf('Wolf3')
wolf4 = Wolf('Wolf4')


# Create Bear
bear = Bear('Bear')


# Create Fighters
adan = Kämpfer('Adan', 2, 0, 1, 1, 'Verteidiger', upgrades = ['HP'])
konrad = Kämpfer('Konrad', 2, 1, 0, 1, 'Krieger', beidhändig = True, shield = False, upgrades = ['stärke'])
grandulf = Zauberer('Grandulf', 0, 2, 1, 1, 'Evoker', upgrades = ['HP'], spells = [])
bjorn = Berserker('Bjorn', 2, 2, 0, 0, 'Juggernaut', upgrades = ['stärke'])
marcon = Kleriker('Marcon', 2, 0, 0, 2, 'Paladin', beidhändig = False, shield = True, upgrades = ['stärke'])






#%%

# Determine Heroes
heroes = [bjorn, grandulf, marcon]

# Determine Adversaries
monsters = [goblin1, goblin2, goblin3]

# Initiate Battle
battle = Battle(heroes, monsters)


#%%

# Number of Fights Simulated
iterations = 1000

# Create Counter of left HP after the Encounter for every Hero in Heroes
x = [np.linspace(0, hero.HP_max, hero.HP_max + 1) for hero in heroes]
y = [np.zeros(hero.HP_max + 1) for hero in heroes]
lethality = np.zeros(len(heroes)+1)

# Run Simulations
for i in range(iterations):

    # Reset Heroes and Monsters to their starting conditions
    for hero in heroes:
        hero.reset()
        
    for monster in monsters:
        monster.reset()


    # Roll initiatives
    initiative_order = [(char.Initiative(), char) for char in heroes + monsters]
    
    # Sort descending
    initiative_order.sort(reverse=True, key=lambda x: x[0])
    turn_order = [char for _, char in initiative_order]
    
    # Roundcounter
    Counter = 0

    # As long as there are Fighters left in both Teams (including regen that can heal Heroes from their death), simulate a combat round
    while any(char.HP > 0 or char.regen != 0 for char in heroes) and any(char.HP > 0 for char in monsters):

        # Characters act in their initiative determined order
        for char in turn_order:
            battle.run_turn(char)

        # Increase Round Counter by 1
        Counter += 1
    
    # Tracker for Heroes current HP
    i = 0
    
    # Organize Hero HP after fight
    for hero in heroes:
        # Save weight of left HP in percent of occurences
        y[i][hero.HP] += 100/iterations
        i += 1


    # Calculate Lethality by counting how many Characters survived
    survived = 0
    for hero in heroes:
        survived += hero.is_alive()

    # Save Contribution of current Lethality in percentile weight
    lethality[survived] += 100/iterations
    
    

# Plot Left HP of Heroes
for i, hero in enumerate(heroes):
    plt.figure()        # new figure for each hero
    plt.bar(x[i], y[i])
    plt.title(hero.name)
    plt.show()          # show this figure before next one


# Calculate Average Lethality
lethality_avg = 0
i = 0
for occurence in lethality:
    lethality_avg += lethality[i] * i/100
    i += 1
lethality_avg = len(lethality) - lethality_avg -1


# Plot lethality
plt.figure()
plt.bar([3, 2, 1, 0], lethality)
plt.plot((lethality_avg, lethality_avg),(0, max(lethality)), color = '#ff0000')
plt.title('Lethality')
plt.show()


