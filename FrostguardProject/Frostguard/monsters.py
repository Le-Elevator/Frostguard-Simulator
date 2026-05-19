# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:51:12 2025

@author: Admin
"""

from .character import Character

import random as r

class NPC(Character):
    
    def __init__(self, name, St, Ge, In, Cha, HP, block, resist, angriff, haltung_max = 3, ranged = False, multiattack = 1, magical = False):
    
        super().__init__(name,
                        HP=HP,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block=block,
                        resist=resist,
                        haltung_max = haltung_max,
                        angriff = angriff)
        
        self.ranged = False
        self.invulnerable = True
        self.multiattack = multiattack
        self.magical = magical
        
    def Attack(self, target):
        for i in range(self.multiattack):
            vorteil = target.advantage()
            if self.magical:    
                target.Resist(self.angriff, vorteil)
            else:
                target.Block(self.angriff, vorteil)
            
        
    def class_block(self, damage, vorteil = 0):
        return damage - self.block - vorteil - self.Dodge()


    def class_resist(self, damage, vorteil = 0):
        return damage - self.resist - vorteil - self.Dodge()





class Goblin(NPC):
    
    def __init__(self, name, HP=3, St = 0, Ge=3, In = 0, Cha = 0, block=1, resist=0, haltung_max = 2):
    
        super().__init__(name,
                        HP=HP,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block=block,
                        resist=resist,
                        angriff = Ge,
                        haltung_max = haltung_max)


    def Attack(self, target):
        vorteil = target.advantage()
        finte = 0
        if self.haltung >= 2 and self.HP > 1 and (r.random() < 0.75 or target.haltung == 0):
            finte += 1
            self.haltung -= 2
        target.Block(self.angriff + finte, vorteil)




class Wolf(NPC):
    
    def __init__(self, name, HP=4, St = 1, Ge=2, In = 0, Cha = 0, block=1, resist=1, angriff = 2, haltung_max = 3):
    
        super().__init__(name,
                        HP=HP,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block=block,
                        resist=resist,
                        angriff = angriff,
                        haltung_max = haltung_max)
    
        self.dodge_cost = 1


    def Attack(self, target):
        vorteil = target.advantage()
        if self.haltung >= 2 and self.HP > 1 and r.random() < 0.75:
            self.haltung -= 1
            vorteil += 1
        target.Block(self.angriff, vorteil = vorteil)
        
        
    
        
    
class Bear(NPC):
    
    def __init__(self, name, HP=13, St = 4, Ge=1, In = 0, Cha = 0, block=2, resist=1, haltung_max = 3):
    
        super().__init__(name,
                        HP=HP,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block=block,
                        resist=resist,
                        angriff = max(St, Ge),
                        haltung_max = haltung_max)

    def turn(self, battle):
        # Regenerate stamina/guard
        if self.regen > 0:
            self.Heal(1)
            self.regen -= 1
            
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)

        n_of_attacks = 1
        if self.haltung >= 2:
            n_of_attacks = 2
            self.haltung -= 2
        
        for i in range(n_of_attacks):
            target = battle.choose_target(self)
            if target is None:
               return
            self.Attack(target)       
