# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 12:14:36 2025

@author: Admin
"""


from .pc import Berserker, Kämpfer, Kleriker, Zauberer
from .dice import Roll, s, b, o
        


        
class BerserkerP(Berserker):
    def __init__(self, name, St, Ge, In, Cha, subclass='None', beidhändig=True, shield=False, upgrades = [], level = 1):

        if beidhändig and shield:
            print(f"{name} can't use two-handed weapon and shield")
            shield = False

        super().__init__(
            name=name,
            St=St,
            Ge=Ge,
            In=In,
            Cha=Cha,
            subclass=subclass,
            beidhändig = beidhändig,
            shield = shield,
            upgrades = upgrades,
            level = level
        )
        
        
        
    def Attack(self, target):
        if not self.is_raging and self.rage > 0:
            self.is_raging = True
            self.rage -= 1
            
        vorteil = self.is_raging + (target.haltung == 0)
        damage = Roll(self.angriff + vorteil - target.Dodge())
        target.Block(0)
        
        if self.was_revived or self.HP < self.healed_by:
            self.excess_dmg += damage - target.block
        else:
            self.effective_dmg += damage - target.block
        
        
        
    def Block(self, damage, vorteil = 0):
        if not self.is_raging and self.rage > 0:
            self.is_raging = True
            self.rage -= 1
        block_bonus = - self.is_raging + self.is_raging * 2 * (self.subclass == 'Juggernaut')
        self.HP = max(0, self.HP - max(0, damage - Roll(self.block + block_bonus - vorteil)))
        
        if self.was_revived or self.HP < self.healed_by:
            self.excess_HP += damage
        else:
            self.effective_HP += damage
        
        
        

class KlerikerP(Kleriker):
    def __init__(self, name, St, Ge, In, Cha, subclass='None', beidhändig=False, shield=True, can_dodge=True, upgrades = [], level = 1):

        if beidhändig and shield:
            print(f"{name} can't use two-handed weapon and shield")
            shield = False

        super().__init__(
            name=name,
            St=St,
            Ge=Ge,
            In=In,
            Cha=Cha,
            subclass=subclass,
            beidhändig = beidhändig, 
            shield = shield, 
            can_ddge = can_dodge,
            upgrades = upgrades,
            level = level
        )
            


    def Attack(self, target):
        vorteil = 0
        if target.haltung == 0:
            vorteil += 1
        has_dodged = target.Dodge()
        damage = Roll(self.angriff + vorteil - has_dodged)
        target.Block(0)
        if self.was_revived or self.HP < self.healed_by:
            self.excess_dmg += damage - target.block
        else:
            self.effective_dmg += damage - target.block
            
        if self.subclass == 'Paladin':
            if self.haltung > 2 and (self.HP > 2 or target.HP == 2 or target.HP == 1):
                damage = Roll(self.charisma + vorteil - has_dodged)
                target.Resist(0)
                self.haltung -= 2
                
                if self.was_revived or self.HP < self.healed_by:
                    self.excess_dmg += damage - target.resist
                else:
                    self.effective_dmg += damage - target.resist


        
        
     
        
        
        

class Kämpfer(PC):
    def __init__(self, name, St, Ge, In, Cha, subclass='None', beidhändig=False, shield=True, can_dodge=False, upgrades = []):

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
            can_dodge=can_dodge,
            upgrades = upgrades
        )
        
        self.shield = shield
        
        self.taktik = 2
        self.taktik_dice = 1
        

    def Attack(self, target):   
        if self.shield and self.haltung > 2:
            self.Shield_Bash(target)
        vorteil = (target.haltung == 0)
        damage = Roll(self.angriff + vorteil - target.Dodge())
        if self.subclass == 'Krieger' and self.taktik > 0 and (target.HP + target.block == damage + 1 or damage + 2):
            damage += s()
            self.taktik -= 1
        target.Block(0)
        
        if self.was_revived or self.HP < self.healed_by:
            self.excess_dmg += damage - target.block
        else:
            self.effective_dmg += damage - target.block
            
            
    
    def Block(self, damage, vorteil = 0):
        damage -= Roll(self.block - vorteil)
        if self.was_revived or self.HP < self.healed_by:
            self.excess_HP += damage 
        else:
            self.effective_HP += damage
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage = max(damage - s(), 0)
            self.taktik -= 1
        self.HP = max(0, self.HP - max(0, damage))
        


    def Resist(self, damage, vorteil = 0):
        damage -= Roll(self.resist - vorteil)
        if self.was_revived or self.HP < self.healed_by:
            self.excess_HP += damage
        else:
            self.effective_HP += damage
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





class Zauberer(PC):
    
    def __init__(self, name, St, Ge, In, Cha, subclass = 'None', upgrades = []):
    
        
        super().__init__(name,
                        HP=4,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block= 0 + 1 * (subclass == 'Spellblade'),
                        resist= 1,
                        taunt= 2 + 2 * (subclass == 'Spellblade'),
                        haltung_max= 3,
                        angriff = In,
                        subclass = subclass,
                        upgrades = upgrades)

        
        self.dodge_cost = 2 - 1 * (subclass == 'Spellblade')
        
        self.spellcost = 1 - 1 * (subclass == 'Spellblade')
    
        self.channelcost = 2 - 1 * (subclass == 'Evoker')
        
        
        self.damage_stats = ['intelligenz']
   


    def Attack(self, target):        
        vorteil = (target.haltung == 0)
        if self.haltung < self.spellcost or self.haltung == self.spellcost and self.above_half:
            self.haltung = self.haltung_max
            return
        self.haltung -= self.spellcost
            
        if (self.haltung > self.channelcost and not self.above_half) or (self.haltung >= self.channelcost and self.above_half):
            vorteil += 1
            self.haltung -= self.channelcost

        damage = Roll(self.angriff + vorteil - target.Dodge())

        if self.subclass == 'Spellblade' and target.resist > target.block:
            target.Block(0)
            
            if self.was_revived or self.HP < self.healed_by:
                self.excess_dmg += damage - target.block
            else:
                self.effective_dmg += damage - target.block
            
        target.Resist(0)

        if self.was_revived or self.HP < self.healed_by:
            self.excess_dmg += damage - target.resist
        else:
            self.effective_dmg += damage - target.resist  
            
        
    def Subclasses(self):
        print('Possible subclasses:')
        print('Spellblade')
        print('Evoker')
    
    



