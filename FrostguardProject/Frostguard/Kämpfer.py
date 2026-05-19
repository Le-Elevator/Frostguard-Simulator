# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 23:38:03 2025

@author: Admin
"""

from character import PC, Roll, s, b, o

class Kämpfer(PC):
    def __init__(self, name, St, Ge, In, Cha, subclass='None', beidhändig=False, shield=True, can_dodge=False):

        if beidhändig and shield:
            print(f"{name} can't use two-handed weapon and shield")
            shield = False

        super().__init__(
            name=name,
            St=St,
            Ge=Ge,
            In=In,
            Cha=Cha,
            HP=5,
            block=2 + shield - can_dodge,
            resist=2 + shield - can_dodge,
            angriff=max(St + beidhändig, Ge),
            haltung_max=3,
            subclass=subclass,
            taunt=3 + 2 * (subclass == 'Verteidiger'),
            can_dodge=can_dodge
        )
        
        self.taktik = 2
        self.taktik_dice = 1
        

    def Attack(self, target):
        if self.shield and self.haltung > 2:
            self.Shield_Bash(target)
        vorteil = 0
        if target.haltung == 0:
            vorteil = 1
        damage = Roll(self.angriff + vorteil - target.Dodge())
        if self.subclass == 'Krieger' and self.taktik > 0 and (target.HP + target.block == damage + 1 or damage + 2):
            damage += s()
            self.taktik -= 1
        target.Block(damage)
    
    
    def Block(self, damage, vorteil = 0):
        damage -= Roll(self.block - vorteil)
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage = max(damage - s(), 0)
            self.taktik -= 1
        self.HP = max(0, self.HP - max(0, damage))


    def Resist(self, damage, vorteil = 0):
        damage -= Roll(self.resist - vorteil)
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage -= Roll(self.taktik_dice)
            self.taktik -= 1
        self.HP = max(0, self.HP - max(0, damage))
    
    
    def Shield_Bash(self, target):
        self.haltung -= 1
        if Roll(self.angriff) > target.block:
            target.haltung = max(0, target.haltung -1)

    
    def Subclasses(self):
        print('Possible subclasses:')
        print('Verteidiger')
        print('Krieger')
