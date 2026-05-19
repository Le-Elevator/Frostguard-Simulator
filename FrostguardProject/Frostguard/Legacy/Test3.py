# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 15:39:34 2025

@author: Admin
"""

import sys
import matplotlib.pyplot as plt

sys.path.append(r"C:/Users/Admin/Documents/Frostguard")

from monsters import Goblin
from pc import Kämpfer




x = [0, 1, 2, 3, 4, 5, 6, 7]
konrad_hp = [0, 0, 0, 0, 0, 0, 0, 0]
adan_hp = [0, 0, 0, 0, 0, 0, 0, 0]


iterations = 10000

for i in range(iterations):
    
    
    # Create a Fighter
    adan = Kämpfer('Adan', 2, 1, 2, 1, 0, 1, 'Verteidiger')
    konrad = Kämpfer('Konrad', 0, 2, 2, 1, 1, 1, 'Krieger', beidhändig = True)
    
    
    # Roll initiatives
    initiative_order = [
        (adan.Initiative(), adan),
        (konrad.Initiative(), konrad),

    ]
    
    # Sort descending
    initiative_order.sort(reverse=True, key=lambda x: x[0])
    turn_order = [char for _, char in initiative_order]
    
# =============================================================================
#     print("Initiative order:")
#     for char in turn_order:
#         print(f"{char.name} (HP: {char.HP})")
#     
#     print("\n--- Battle Start ---\n")
# =============================================================================
    
    Counter = 1
    
    while konrad.HP > 0 and adan.HP > 0:
            
# =============================================================================
#         print(f"\n--- Round {Counter} ---\n")
# =============================================================================
        
        for char in turn_order:
            if not char.is_alive():
                continue  # Skip dead characters
        
            # Determine target
            if char.name == "Adan":
                target = konrad
            else:
                target = adan
    
            char.Attack(target)  

            
        Counter += 1
    
        
    
    
    
    
    # =============================================================================
    # print('Adan: ' + str(adan.HP))
    # =============================================================================
    
    
    konrad_hp[konrad.HP] += 1/iterations
    adan_hp[adan.HP] += 1/iterations
    
    
plt.subplots()
plt.bar([item -0.2 for item in x],konrad_hp, width=0.4)
plt.bar([item +0.2 for item in x], adan_hp, width = 0.4)



