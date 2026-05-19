# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 13:24:11 2025

@author: Admin
"""

import random as r



class Goblin:
    
    def __init__(self, name):
    
        self.name = name
    
        self.HP = 3
    
        self.angriff = 3
    
        self.block = 1
    
        self.resist = 0
    
        self.haltung = 2
        
        self.haltung_max = 2
        
        self.haltung_reg = 1
    
        self.Ini = 3
        
    
    def Turn(self, heroes, monsters):
        if not self.is_alive():
            return
        
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)
        
        target = r.choices(heroes, weights=[hero.taunt for hero in heroes], k=1)[0] 
        
        self.Attack(target)


    def Attack(self, target):
        finte = 0
        if self.haltung >= 2 and self.HP > 1 and r.random() < 0.75:
            self.haltung -=2
            finte = 1
        
        target.Block(self.angriff + finte)
        
    
    def Block(self, Damage):
        self.HP -= max(0, Damage - self.block)
        if self.HP < 0:
            self.HP = 0
        
        
    def Resist(self, Damage):
        self.HP -= max(0, Damage - self.resist)
        if self.HP < 0:
            self.HP = 0
        
    
    def Initiative(self):
        return self.Ini + r.random()*12
    
        
    def is_alive(self):
        return self.HP > 0
        
    
    def Dodge(self):
        if self.haltung >= 2:
            self.haltung -= 2
            return True
        else:
            return False





class Wolf:
    
    def __init__(self, name):
    
        self.name = name
    
        self.HP = 3
    
        self.angriff = 2
    
        self.block = 1
    
        self.resist = 1
    
        self.haltung = 3
        
        self.haltung_max = 3
        
        self.haltung_reg = 1
    
        self.Ini = 2
        
    
    def Turn(self, heroes, monsters):
        if not self.is_alive():
            return
        
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)
        
        target = r.choices(heroes, weights=[hero.taunt for hero in heroes], k=1)[0]
        
        self.Attack(target)


    def Attack(self, target):
        rudel_angriff = 0
        if self.haltung >= 2 and self.HP > 1 and r.random() < 0.75:
            self.haltung -= 1
            rudel_angriff = 1
        
        target.Block(self.angriff, reduced = rudel_angriff)
        
        
    def Block(self, Damage):
        self.HP = max(0, self.HP - max(0, Damage - self.block))

        
        
    def Resist(self, Damage):
        self.HP = max(0, self.HP - max(0, Damage - self.resist))
        
    
    def Initiative(self):
        return self.Ini + r.random()*12
    
        
    def is_alive(self):
        return self.HP > 0
        
    
    def Dodge(self):
        if self.haltung > 0:
            self.haltung -= 1
            return True
        else:
            return False
    
