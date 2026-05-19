# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 09:32:00 2025

@author: Admin
"""


import sys
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from Frostguard.power import KämpferP, ZaubererP, BerserkerP, KlerikerP
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
adan = KämpferP('Adan', 2, 0, 1, 1, 'Verteidiger', level = 2, upgrades = ['HP', 'block', 'stärke'])
konrad = KämpferP('Konrad', 2, 1, 0, 1, 'Krieger', beidhändig = True, shield = False, level = 2, upgrades = ['stärke', 'HP', 'block'])
grandulf = ZaubererP('Grandulf', 0, 2, 1, 1, 'Evoker', level = 2, upgrades = ['HP', 'block', 'intelligenz'])
björn = BerserkerP('Björn', 2, 2, 0, 0, 'Juggernaut', level = 2, upgrades = ['stärke', 'HP', 'block'])
marcon = KlerikerP('Marcon', 2, 0, 0, 2, 'Paladin', beidhändig = True, shield = False, level = 2, upgrades = ['stärke', 'HP', 'block'])






#%%


heroes = [konrad, björn, adan, marcon]

monsters = [goblin1, goblin2, goblin3, goblin4]

battle = Battle(heroes, monsters)


#%%

iterations = 2

x = [np.linspace(0, hero.HP_max, hero.HP_max + 1) for hero in heroes]

y = [np.zeros(hero.HP_max + 1) for hero in heroes]

effective_HP = [[] for hero in heroes]
effective_dmg = [[] for hero in heroes]

lethality = np.zeros(len(heroes)+1)


for i in range(iterations):

    #print('____________New Battle__________________')
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
    
    while any(char.HP > 0 and char.regen == 0 for char in heroes) and any(char.HP > 0 for char in monsters):     

        for char in turn_order:
            battle.run_turn(char)
            
        Counter += 1
    
    
    i = 0
    
    # Show Hero HP after fight
    for hero in heroes:
        y[i][hero.HP] += 100/iterations
        i += 1
    
    survived = 0
    
    for hero in heroes:
        survived += hero.is_alive()
    
    lethality[survived] += 100/(iterations*len(heroes))
    
    
    excess_HP = 0
    excess_dmg = 0
    i = 0
    for hero in heroes:
        if i == 3:
            break
        
        effective_HP[i].append(hero.effective_HP) 
        effective_dmg[i].append(hero.effective_dmg/(Counter))
        
        excess_HP += hero.excess_HP
        excess_dmg += hero.excess_dmg
        
        i += 1
    
    effective_HP[3].append(marcon.effective_HP + excess_HP)
    effective_dmg[3].append(hero.effective_dmg/(Counter) + excess_dmg/(Counter))


# =============================================================================
# for i, hero in enumerate(heroes):
#     plt.figure()        # new figure for each hero
#     plt.bar(x[i], y[i])
#     plt.title(hero.name)
#     plt.show()          # show this figure before next one
# 
# =============================================================================



# =============================================================================
# plt.figure()
# plt.bar([4, 3, 2, 1, 0], lethality)
# plt.title('Lethality')
# =============================================================================



power = [[], [], [], []]

for i in range(4):
    for j in range(len(effective_HP[0])):
        power[i].append(effective_HP[i][j] * effective_dmg[i][j])

for i in range(4):
        
    dmg = pd.Series(effective_dmg[i])
    
    # Plot histogram with density curve
    plt.figure(figsize=(8, 5))
    
    # Histogram    
    plt.hist(dmg, bins=10, density=True, alpha=0.6, color="skyblue", edgecolor="black")
    plt.title(f"Effective Damage of {heroes[i].name}")
    plt.xlabel("Damage")
    plt.ylabel("%")
    plt.show()
    
    hp = pd.Series(effective_HP[i])
    
    # Plot histogram with density curve
    plt.figure(figsize=(8, 5))
    
    # Histogram    
    plt.hist(hp, bins=10, density=True, alpha=0.6, color="skyblue", edgecolor="black")
    plt.title(f"Effective HP of {heroes[i].name}")
    plt.xlabel("HP")
    plt.ylabel("%")
    plt.show()
    
    p = pd.Series(power[i])
    
    # Plot histogram with density curve
    plt.figure(figsize=(8, 5))
    
    # Histogram    
    plt.hist(p, bins=10, density=True, alpha=0.6, color="skyblue", edgecolor="black")
    plt.title(f"Power of {heroes[i].name}")
    plt.xlabel("Power")
    plt.ylabel("%")
    plt.show()
