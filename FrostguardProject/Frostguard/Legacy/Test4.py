# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 13:53:55 2025

@author: Admin
"""

import sys
import matplotlib.pyplot as plt

sys.path.append(r"C:/Users/Admin/Documents/Frostguard")

from character import Kämpfer, Goblin, Wolf, Zauberer, Battle


x = [0, 1, 2, 3, 4, 5, 6, 7]
y = [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]

lethality = [0, 0, 0, 0]

iterations = 10000

for i in range(iterations):

   
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
    
    
    # Create Fighters
    adan = Kämpfer('Adan', 2, 1, 1, 0, 'Verteidiger')
    konrad = Kämpfer('Konrad', 0, 2, 1, 1, 'Krieger', beidhändig = True, shield = False, can_dodge = True)
    grandulf = Zauberer('Grandulf', 0, 2, 2, 1, 'Evoker')
    
    
    heroes = [adan, konrad, grandulf]
    
    monsters = [goblin1, goblin2, goblin3]
    
    
    battle = Battle(heroes, monsters)
    
    # Roll initiatives
    initiative_order = [(char.Initiative(), char) for char in heroes + monsters]
    
    # Sort descending
    initiative_order.sort(reverse=True, key=lambda x: x[0])
    turn_order = [char for _, char in initiative_order]
    
    # Roundcounter    
    Counter = 1
    
    while any(char.HP > 0 for char in heroes) and any(char.HP > 0 for char in monsters):     

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
    
    lethality[survived] += 100/iterations

for i, hero in enumerate(heroes):
    plt.figure()        # new figure for each hero
    plt.bar(x, y[i])
    plt.title(hero.name)
    plt.show()          # show this figure before next one


plt.figure()
plt.bar([3, 2, 1, 0], lethality)
plt.title('Lethality')