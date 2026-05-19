# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:42:28 2025

@author: Admin
"""

from .character import Character  # relative import within the 

import Frostguard.dice as dice
import Frostguard.spells as s
import Frostguard.effects as eff

import random as r

# Example level ranges for tiers
TIER_LEVELS = {
    1: (1, 3),
    2: (4, 6),
    3: (7, 9),
    4: (10, 10),  # extend as needed
}

UPGRADE_TABLE = {
    "HP": {
        1: [1, 2],      
        2: [1, 1, 2],   
        3: [1, 1, 2],   
    },
    "Haltung": {
        1: [2],      
        2: [2],   
        3: [2],   
        },
    "Block": {
        1: [2],      
        2: [1, 2],
        3: [1, 1, 2]
    },
    "Resist": {
        1: [2],      
        2: [1, 2],
        3: [1, 1, 2]
    },
    "stärke": {
        1: [1],      
        2: [1, 2],
        3: [1, 2]
    },
    "geschicklichkeit": {
        1: [1],      
        2: [1, 2],
        3: [1, 2]
    },
    "intelligenz": {
        1: [1],      
        2: [1, 2],
        3: [1, 2]
    },
    "charisma": {
        1: [1],      
        2: [1, 2],
        3: [1, 2]
    },
    "Ini": {
        1: [1, 1, 1]
    },
    "subclass": {
        1: [2],      
        2: [2],
        3: [2]
    },
    "multiclass": {
        2: [3]
    },
    
    
}


        

    


class PC(Character):    
    
    def __init__(self, name, St, Ge, In, Cha, HP, block, resist, angriff, haltung_max=3, subclass = 'None', taunt = 1,  
                 can_dodge = True, level = 1, beidhändig = False, upgrades = [], ranged = False):
        
        super().__init__(name,
                        HP=HP,
                        St = St,
                        Ge=Ge,
                        In = In,
                        Cha = Cha,
                        block=block,
                        resist=resist,
                        haltung_max=haltung_max,
                        angriff = angriff,
                        can_dodge = can_dodge,
                        ranged = ranged)
        
        self.taunt = taunt
        self.subclass = subclass
        self.level = level
        self.echoes = level * 3 - 2 * (not subclass == 'None')
        self.beidhändig = beidhändig
        self.mana = 0
        
        self.fokus = 0
        self.fokus_max = 6
        

        
        self.multiclass = False
        
        self.damage_stats = ['stärke', 'geschicklichkeit']
        
        # track upgrades per stat
        self.upgrades = {stat: 0 for stat in UPGRADE_TABLE}
        
        self.spend_echoes(upgrades, silent = True)
    
    def Attack(self, target):
        target.Block(dice.Roll(self.angriff + target.advantage()))
    
    
    def class_block(self, damage, vorteil):
        return self.damage_calc(damage, self.block, vorteil)
    
    
    def class_resist(self, damage, vorteil):
        return self.damage_calc(damage, self.resist, vorteil)
    
    
    def level_up(self):
        if self.level < 10:
            self.echoes += 3
            self.level += 1
        else:
            print(f"{self.name} already level 10!")
        
    
    def get_current_tier(self):
        """Return the tier based on current level."""
        for tier, (min_level, max_level) in TIER_LEVELS.items():
            if min_level <= self.level <= max_level:
                return tier
        return max(TIER_LEVELS.keys())  
    
    

    def get_available_upgrades(self):
        """
        Return a list of tuples (stat, cost) for all upgrades the PC can currently take,
        considering all tiers for which the character is eligible based on level.
        """
        available = []
        for stat, tiers in UPGRADE_TABLE.items():
            for tier, costs in tiers.items():
                min_level, max_level = TIER_LEVELS.get(tier, (1, 100))
                if min_level <= self.level <= max_level:
                    taken = self.upgrades.get(stat, 0)
                    if taken < len(costs):
                        available.append((stat, costs[taken]))
        return available
    
    
    def apply_upgrade(self, stat_name):
        increment = 1  # fixed increase per upgrade
    
        if stat_name == "HP":
            # Increase max HP by 1
            self.HP_max += increment
            # Increase current HP by 1, not more
            self.HP = min(self.HP + increment, self.HP_max)
        else:
            # Increase other stats
            setattr(self, stat_name, getattr(self, stat_name) + increment)
    
            # If the stat affects attack, recalc
            if stat_name in getattr(self, "damage_stats", []):
                if self.damage_stats == ['stärke', 'geschicklichkeit']:
                    self.angriff = max(self.stärke + getattr(self, "beidhändig", 0), self.geschicklichkeit)
                else:
                    # For other classes, sum up all stats in damage_stats
                    self.angriff = sum(getattr(self, s) for s in self.damage_stats)
    
        # Track that this stat was upgraded
        self.upgrades[stat_name] += 1


    def spend_echoes(self, chosen_upgrades, silent = False):
        """
        Spend echoes to upgrade stats based on chosen upgrades.
        
        chosen_upgrades: list of stat names, e.g., ["HP", "stärke"]
        """
        if not chosen_upgrades:
            if not silent:
                print("No upgrades chosen.")
            return
    
        while self.echoes > 0 and chosen_upgrades:
            # Pick the next stat from the player’s choice
            upgrade_stat = chosen_upgrades.pop(0)
    
            # Check if this upgrade is available in the current tier
            possible_upgrades = self.get_available_upgrades()
            upgrade_info = next(((stat, cost) for stat, cost in possible_upgrades if stat == upgrade_stat), None)
    
            if upgrade_info is None:
                if not silent:
                    print(f"{upgrade_stat} is not available or cannot be upgraded now.")
                continue
    
            stat, cost = upgrade_info
    
            if cost > self.echoes:
                if not silent:
                    print(f"Not enough echoes to upgrade {stat}.")
                break
    
            # Apply the upgrade
            self.apply_upgrade(stat)
            self.echoes -= cost
            if not silent:
                print(f"Upgraded {stat} by 1! {self.echoes} echoes left.")


    
    def damage_calc(self, damage, attribute, vorteil):
        return damage - dice.Roll(attribute- vorteil + self.Dodge() + self.defence_bonus()) - self.damage_reduction()
    
#_____________________________________________________________________Classes_________________________________________________________________
        


        
class Berserker(PC):
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
            HP=7,
            block=1 + shield,
            resist=1 + shield,
            angriff=max(St + beidhändig, Ge),
            haltung_max=3,
            subclass=subclass,
            taunt=5,
            upgrades = upgrades,
            level = level
        )
    
        self.is_raging = False
        
        self.rage = 2
        
        
        
    def Attack(self, target):
        if not self.is_raging and self.rage > 0:
            self.is_raging = True
            self.rage -= 1
            self.vorteil += 1
        vorteil = self.is_raging + target.advantage()
        target.Block(dice.Roll(self.angriff + vorteil - target.Dodge()))
        
        
        
    def class_block(self, damage, vorteil):
        if not self.is_raging and self.rage > 0:
            self.is_raging = True
            self.rage -= 1
            self.vorteil += 1
        vorteil -= self.is_raging * 2 * (self.subclass == 'Juggernaut')
        return self.damage_calc(damage, self.block, vorteil)
        
        
        
    def class_reset(self):
        self.rage = 2
        self.is_raging = False
        
        
        

class Kleriker(PC):
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
            HP=5,
            block=1 + shield + (subclass == 'Paladin'),
            resist=1 + shield + (subclass == 'Paladin'),
            angriff=max(St + beidhändig, Ge),
            haltung_max=3,
            subclass=subclass,
            taunt=3 + (subclass == 'Paladin'),
            can_dodge= (not subclass == 'Paladin'),
            upgrades = upgrades,
            level = level,
            ranged = not (subclass == 'Paladin')
        )
        
        self.max_heals = self.level + self.charisma
        self.heals = self.max_heals
            
            
    def heal_allies(self, allies):
        if self.heals > 0:
            # Heal dead heroes first. Requires whole turn so returns True
            for ally in allies:
                if not ally.is_alive() and self.haltung >=2:
                    ally.Heal(dice.Roll(self.charisma))
                    self.haltung -= 2
                    self.heals -= 1
                    return True

            # Regen others if not Paladin. Requires whole turn so return True
            if not self.subclass == 'Paladin' and self.haltung > 1:

                for ally in allies:
                    if not ally.above_half():
                    
                        ally.gain_effect('regen', {'effect' : eff.regen, 'duration' : 3, 'power' : 1})
                        self.haltung -= 1
                        self.heals -= 1
                        return True
            
            # Heal self if Paladin. Doesn't require turn so will eventually return False
            if self.subclass == 'Paladin' and not self.above_half() and self.haltung > 2:
                self.Heal(dice.Roll(self.charisma))
                self.haltung -= 2
                self.heals -= 1
                
        return False
            
            
    def Attack(self, target):
        vorteil = target.advantage()
        has_dodged = target.Dodge()
        target.Block(dice.Roll(self.angriff + vorteil - has_dodged))
        if self.subclass == 'Paladin':
            if self.haltung > 2 and (self.HP > 2 or target.HP == 2 or target.HP == 1):
                target.Resist(dice.Roll(self.charisma + vorteil - has_dodged))
                self.haltung -= 2
        
        
        
     
        
    def class_reset(self):
        self.heals = self.max_heals
        

class Kämpfer(PC):
    def __init__(self, name, St, Ge, In, Cha, subclass='None', beidhändig=False, shield=True, can_dodge=False, upgrades = [], level = 1):

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
            upgrades = upgrades,
            level = level,
            ranged = not (subclass == 'Verteidiger')
        )
        
        self.shield = shield
        
        self.taktik_max = 2
        self.taktik = self.taktik_max
        self.taktik_dice = s
        

    def Attack(self, target):
        if self.shield and self.haltung > 2:
            self.Shield_Bash(target)
        vorteil = target.advantage()
        damage = dice.Roll(self.angriff + vorteil - target.Dodge())
        if self.subclass == 'Krieger' and self.taktik > 0 and (target.HP + target.block == damage + 1 or damage + 2):
            damage += self.taktik_dice()
            self.taktik -= 1
        target.Block(damage)
    
    
    def class_block(self, damage, vorteil):
        damage = self.damage_calc(damage, self.block, vorteil)
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage -= self.taktik_dice()
            self.taktik -= 1
        return damage


    def class_resist(self, damage, vorteil):
        damage = self.damage_calc(damage, self.resist, vorteil)
        if self.taktik > 0 and (damage > 1 or self.HP <= damage):
            damage -= self.taktik_dice()
            self.taktik -= 1
        return damage
    
    
    def Shield_Bash(self, target):
        self.haltung -= 1
        if dice.Roll(self.angriff) > target.block:
            target.haltung = max(0, target.haltung -1)

    
    def Subclasses(self):
        print('Possible subclasses:')
        print('Verteidiger')
        print('Krieger')
        
    
    def class_reset(self):
        self.taktik = self.taktik_max




class Zauberer(PC):
    
    def __init__(self, name, St, Ge, In, Cha, subclass = 'None', upgrades = [], level = 1, spells = ['Shield']):
    
        
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
                        upgrades = upgrades,
                        level = level,
                        ranged = True)

        
        self.dodge_cost = 2 - 1 * (subclass == 'Spellblade')
        
        self.spellcost = 1 - 1 * (subclass == 'Spellblade')
    
        self.channelcost = 2 - 1 * (subclass == 'Evoker')
        
        
        self.max_mana = self.level + self.intelligenz
        self.mana = self.max_mana
        
        self.damage_stats = ['intelligenz']
        
        self.spells = {}
        
        for spell in spells:
            s.get_spell(self, spell)
        
        
    def class_reset(self):
        self.mana = self.max_mana


    def Attack(self, target):
        vorteil = target.advantage()
            
        if (self.haltung > self.channelcost and not self.above_half) or (self.haltung >= self.channelcost and self.above_half):
            vorteil += 1
            self.haltung -= self.channelcost

        damage = dice.Roll(self.angriff + vorteil)

        if self.subclass == 'Spellblade' and target.resist > target.block:
            target.Block(damage)
            return
            
        target.Resist(damage)
    
    
    def class_block(self, damage, vorteil):
        if any(spell == 'shield' for spell in self.spells):
            if self.fokus > 0 and not self.above_half() or self.fokus > 2:
                s.Shield(self)
        return self.damage_calc(damage, self.block, vorteil)
        
    
    def class_resist(self, damage, vorteil):
        if any(spell == 'shield' for spell in self.spells):
            if self.fokus > 0 and not self.above_half() or self.fokus > 2:
                s.Shield(self)
        return self.damage_calc(damage, self.block, vorteil)
        
    
    def Subclasses(self):
        print('Possible subclasses:')
        print('Spellblade')
        print('Evoker')
    
    



