# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 12:06:09 2025

@author: Admin
"""

import random as r


import matplotlib.pyplot as plt




def s():
    return r.choice([0, 1, 1, 1, 2, 2])


def b():
    return r.choice([1, 1, 2, 2, 2, 3])



def o():
    return r.choice([1, 2, 2, 3, 3, 4])



def Roll(i):
    if i == 0:
        return r.choice([0,1])
    elif i == 1:
        return s()
    elif i == 2:
        return b()
    elif i == 3:
        return s() + s()
    elif i == 4:
        return b() + s()
    elif i == 5:
        return b() + b()
    elif i == 6:
        return b() + s() + s()
    elif i == 7:
        return b() + b() + s()
    elif i == 8:
        return b() + b() + b()
    elif i == 9:
        return 0() + b() + b()
    elif i == 10:
        return o() + o() + b()
    elif i > 10:
        return o() + o() + o()



repetitions = 10000

x = [0, 1, 2, 3, 4, 5, 6, 7]
Result = [0, 0, 0, 0, 0, 0, 0, 0]


for i in range(repetitions):
    
    Knight_HP = 7

    Knight_A = 2

    Knight_B = 3

    Knight_R = 2
    
    Knight_ini = r.random()*8 + 1
    
    Taktik = 2
    

    Goblin_HP = 4

    Goblin_A = 3

    Goblin_B = 1

    Goblin_R = 0
    
    Goblin_ini = r.random()*8 + 3
    
    
    First = Knight_ini >= Goblin_ini

    
    
    
    while (Knight_HP > 0 and Goblin_HP > 0):
        
        if First:
            
            Goblin_HP -= (Roll(Knight_A) - Goblin_B)
        
            if Goblin_HP > 0:
                
                Damage = (Goblin_A - Roll(Knight_B))
                
                if Taktik > 0 and Damage > 0:
                    Damage -= s()
                    Taktik -= 1
                    
                if Damage < 0:
                    Damage = 0
                               
                Knight_HP -= Damage
                
    
        else:
            
            Damage = (Goblin_A - Roll(Knight_B))
            
            if Taktik > 0 and Damage > 0:
                Damage -= s()
                Taktik -= 1
                
            if Damage < 0:
                Damage = 0
            
            Knight_HP -= Damage
            
            if Knight_HP > 0:
                
                Goblin_HP -= (Roll(Knight_A) - Goblin_B)
                
    if Knight_HP < 0:
        Knight_HP = 0
    
    
    Result[Knight_HP] += 1/repetitions*100


plt.bar(x, Result)

plt.show()



