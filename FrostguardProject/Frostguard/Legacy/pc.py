# -*- coding: utf-8 -*-
"""
Created on Tue Sep  9 13:45:25 2025

@author: Admin
"""

import random as r

#Ergebnisse von Wurf mit Würfeln

def s():
    return r.choice([0, 1, 1, 1, 2, 2])

def b():
    return r.choice([1, 1, 2, 2, 2, 3])

def o():
    return r.choice([1, 2, 2, 3, 3, 4])



#Allgemeines Wurfergebnis basierend auf 
def Roll(Rang):
    mapping = {
        0: lambda: r.choice([0, 1]),
        1: s,
        2: b,
        3: lambda: s() + s(),
        4: lambda: b() + s(),
        5: lambda: b() + b(),
        6: lambda: b() + s() + s(),
        7: lambda: b() + b() + s(),
        8: lambda: b() + b() + b(),
        9: lambda: o() + b() + b(), 
        10: lambda: o() + o() + b(),
    }
    
    # For i > 10, use a default
    if Rang > 10:
        return o() + o() + o()
    
    # Get function from dict and call it
    return mapping[Rang]()










class Kämpfer:
    
    
    def __init__(self, name, St, Ge, Kon, In, Wei, Cha, subclass, beidhändig = False):
        
        self.name = name
        
        #Stats bestimmen
        self.stärke = St
        
        self.geschicklichkeit = Ge
        
        self.konstitution = Kon
        
        self.intelligenz = In
        
        self.weisheit = Wei
        
        self.charimsa = Cha
        
        
        #Werte errechnen
        self.HP = 5 + Kon
        
        self.HP_max = 5 + Kon
    
        self.angriff = max(St + beidhändig, Ge)
    
        self.block = 2 + (not beidhändig)
    
        self.resist = 2 + (not beidhändig)
    
        self.haltung = 3
        
        self.haltung_max = 3
        
        self.haltung_reg = 1
    
        self.Ini = Ge
        
        self.taunt = 3 + 2 * (subclass == 'Verteidiger')
    
    
        self.taktik = 2
        
        self.subclass = subclass
    

            
            
    
    def Turn(self, heroes, monsters):
        if not self.is_alive():
            return
        
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)
        
        for monster in monsters:
            if monster.is_alive():
                self.Attack(monster)
                break

    


    def Attack(self, target):
        if self.subclass == 'Verteidiger' and self.haltung > 2 and target.haltung > 0:
            self.Shield_Bash(target)
        vorteil = 0
        if target.haltung == 0:
            vorteil = 1
        damage = Roll(self.angriff + vorteil - target.Dodge())
        if self.subclass == 'Krieger' and self.taktik > 0 and (target.HP + target.block == damage + 1 or damage + 2):
            damage += s()
            self.taktik -= 1
            
                
        target.Block(damage)
            
    
    
    
    
    def Block(self, damage, reduced = 0):
        
        damage -= Roll(self.block - reduced)
        
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage = max(damage - s(), 0)
            self.taktik -= 1
        
        self.HP = max(0, self.HP - max(0, damage))

        

    def Resist(self, damage):
        
        damage -= Roll(self.resist)
        
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage -= s()
            self.taktik -= 1

            
        self.HP = max(0, self.HP - max(0, damage))

            
            
    
    
    def Heal(self, amount):
        if amount<=0:
            return
        
        self.haltung = self.haltung * self.is_alive()
        
        self.HP = min(self.HP + amount, self.HP_max)
        
    
        
    def Initiative(self):
        return self.Ini + r.random()*12
        
    
    
    def Shield_Bash(self, target):
        self.haltung -= 2
        if Roll(self.angriff) > target.block:
            target.haltung = max (0, target.haltung -2)

    
    
    def is_alive(self):
        
        return self.HP > 0
        
    
    
    def Dodge(self):
        return False



class Zauberer:
    
    
    def __init__(self, name, St, Ge, Kon, In, Wei, Cha, subclass, beidhändig = False):
        
        self.name = name
        
        #Stats bestimmen
        self.stärke = St
        
        self.geschicklichkeit = Ge
        
        self.konstitution = Kon
        
        self.intelligenz = In
        
        self.weisheit = Wei
        
        self.charimsa = Cha
        
        
        #Werte errechnen
        self.HP = 4 + Kon
        
        self.HP_max = 4 + Kon
    
        self.angriff = In
    
        self.block = 0 + 1 * (subclass == 'Spellblade')
    
        self.resist = 1 
    
        self.haltung = 3
        
        self.haltung_max = 3
        
        self.haltung_reg = 1
    
        self.Ini = Ge
        
        self.taunt = 2 + 2 * (subclass == 'Spellblade')
        
        self.dodge = 2 - 1 * (subclass == 'Spellblade')
        
        
        
        self.spellcost = 1 - 1 * (subclass == 'Spellblade')
    
        self.channelcost = 2 - 1 * (subclass == 'Evoker')
   
        self.subclass = subclass
    
            
            
            
    
    def Turn(self, heroes, monsters):
        if not self.is_alive():
            return
        
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)
        
        for monster in monsters:
            if monster.is_alive():
                self.Attack(monster)
                break

    


    def Attack(self, target):
        vorteil = 0
        if self.haltung == 0:
            self.haltung = self.haltung_max
            return
        self.haltung -= self.spellcost
        
        if target.haltung == 0:
            vorteil = 1
        if (self.haltung > self.channelcost and self.HP < 3) or (self.haltung >= self.channelcost and self.HP > 3):
            vorteil += 1
            self.haltung -= self.channelcost

        damage = Roll(self.angriff + vorteil - target.Dodge())

        if self.subclass == 'Spellblade' and target.resist > target.block:
            target.Block(damage)
            return
            
        target.Resist(damage)
            
    
    
    
    
    def Block(self, damage, reduced = 0):   
        damage -= Roll(self.resist + self.Dodge()- reduced)     
        self.HP = max(0, self.HP - damage)

        

    def Resist(self, damage):
        damage -= Roll(self.resist + self.Dodge())
        self.HP = max(0, self.HP - damage)
        
    
    
    
    def Heal(self, amount):
        if amount<=0:
            return
        
        self.Haltung = self.Haltung * self.is_alive()
            
        self.HP = min(self.HP + amount, self.HP_max)
        
    
        
    def Initiative(self):
        return self.Ini + r.random()*12
        

    
    
    def is_alive(self):
        
        return self.HP > 0
        
    
    
    def Dodge(self):
        if self.haltung > 1:
            self.haltung -= 2
            #print(f"{self.name} Dodged!")
            return True
        else:
            return False


