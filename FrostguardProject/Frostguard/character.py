# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 09:53:20 2025

@author: Admin
"""
import random as r

class Character:
    def __init__(self, name, St, Ge, In, Cha, HP, block, resist, angriff, haltung_max, haltung_reg = 1, can_dodge = True, ranged = False):
        
        self.name = name
        self.stärke = St
        self.geschicklichkeit = Ge
        self.intelligenz = In
        self.charisma = Cha

        self.HP = HP
        self.HP_max = HP
        self.Ini = Ge  # initiative roll base
        self.angriff = angriff
        self.block = block
        self.resist = resist

        self.haltung = haltung_max
        self.haltung_max = haltung_max
        self.haltung_reg = haltung_reg
        
        self.can_dodge = can_dodge
        self.dodge_cost = 2  # stamina cost for dodging
        
        self.move = 0
        self.ranged = ranged
        
        self.effects = {} # dictionary for effects
        
    

    
    def turn_start(self, battle):
        # Regenerate stamina/guard        
        self.round_vorteil = max(0, self.round_vorteil -1)
        
        self.resolve_effects()
        
        if not self.is_alive:
            return
        
        self.haltung = min(self.haltung + self.haltung_reg, self.haltung_max)
        
        if hasattr(self, 'fokus'):
            self.fokus = min(self.fokus + 1, self.fokus_max)
        
        self.turn(battle)
        
        
    def turn(self, battle):
        # Return List of Allies
        allies = battle.allies(self)
        
        # Do heal_allies() and if it returns False (default), continue with attack
        if not self.heal_allies(allies):
            # Default action: attack a target chosen by the battle system
            target = battle.choose_target(self)
            if target is None:
               return
            self.Attack(target)
        
        
        self.move = min(0, self.move + 1) # Reduce movement hindering Effects by 1
        
        
        
    def resolve_effects(self):
        for elem in list(self.effects):  # iterate over a copy
            effect_data = self.effects[elem]
            
            # Run the method of the effect
            effect_data["effect"](self, effect_data)
    
            # Check if effect has a timer
            if "duration" in effect_data:
                if effect_data["duration"] > 0:
                    effect_data["duration"] -= 1
                if effect_data["duration"] < 1:  # expired
                    self.effects.pop(elem)
                    continue  # move on to the next effect
    
    
    def gain_effect(self, name, effect):
        if name not in self.effects: # If effect is not on self, add it
            self.effects[name] = effect
            return
    
        i = 2
        while True: # If it is already there, rename new effect so no problems arise
            new_name = f"{name}{i}"
            if new_name not in self.effects:
                self.effects[new_name] = effect
                return
            i += 1
    

    def Block(self, damage, vorteil = 0):
        damage = self.class_block(damage, vorteil) # Look at class based Block method
        self.HP = max(0, self.HP - max(0, damage)) # Reduce HP by damage, or set to 0 if damage > HP


    def Resist(self, damage, vorteil = 0):
        damage = self.class_resist(damage, vorteil) # Look at class based Resist method
        self.HP = max(0, self.HP - max(0, damage))  # Reduce HP by damage, or set to 0 if damage > HP



    def defence_bonus(self, attacker=None):
        """
        Check all effects on character.
        If an effect has trigger 'on_hit' and is of type 'defence',
        run its effect function and return the resulting bonus.
        """
        total_bonus = 0
    
        for name, data in self.effects.items():
            if data.get("trigger") == "on_hit" and data.get("type") == "defence" and data.get('consumed') == True:
                return 0
            if data.get("trigger") == "on_hit" and data.get("type") == "defence":
                effect_func = data.get("effect")
                if callable(effect_func):
                    # Effect function should return a numeric value (bonus)
                    bonus = effect_func(self, data, attacker=attacker)
                    if bonus is not None:
                        total_bonus += bonus
                    print(f"rank increased by {total_bonus}")
        return total_bonus
    
    
    def damage_reduction(self, attacker=None):
        """
        Check all effects on character.
        If an effect has trigger 'on_hit' and is of type 'defence',
        run its effect function and return the resulting bonus.
        """
        total_bonus = 0
    
        for name, data in self.effects.items():
            if data.get("trigger") == "on_hit" and data.get("type") == "reduction":
                effect_func = data.get("effect")
                if callable(effect_func):
                    # Effect function should return a numeric value (bonus)
                    bonus = effect_func(self, data)
                    if bonus is not None:
                        total_bonus += bonus
                    print(f"total reduced by {total_bonus}")
    
        return total_bonus
    
    

    def heal_allies(self, allies):
        return False



    def is_alive(self):
        return self.HP > 0


    def Heal(self, amount):
        if amount <= 0:
            return
        if hasattr(self, "was_revived"):
            self.healed_by += amount
            if self.HP == 0:
                self.was_revived = True
        self.haltung = self.haltung * self.is_alive()  # reset guard if dead
        self.HP = min(self.HP + amount, self.HP_max)


    def Initiative(self):
        return self.Ini + r.random() * 12


    def Dodge(self):
        if self.can_dodge and self.haltung >= self.dodge_cost:
            self.haltung -= self.dodge_cost
            return True
        else:
            return False

    
    def above_half(self):
        return self.HP > 0.5 * self.HP_max


    def pure_damage(self, damage):
        if damage < 0:
            return
        self.HP = max(0, self.HP - damage)


    def reset(self):
        self.HP = self.HP_max
        self.haltung = self.haltung_max
        self.regen = 0
        self.move = 0
        self.vorteil = 0
        self.tmp_vorteil = 0
        self.round_vorteil = 0
        self.class_reset()
    
    
    def class_reset(self):
        return
    
    
    def advantage(self):
        vorteil = (self.haltung == 0) + self.vorteil + self.tmp_vorteil + self.round_vorteil
        self.tmp_vorteil = 0
        return vorteil
    

    def get_taunt(self):
        # 0 Taunt if dead
        if not self.is_alive():
            return 0
        
        if hasattr(self, 'taunt'):
            return self.taunt
        
        return max(0, 8 - self.HP) + self.angriff



    def __str__(self):
        """Pretty print basic stats when using print(obj)."""
        return (
            f"{self.name} | "
            f"HP: {self.HP}/{self.HP_max}, "
            f"Atk: {self.angriff}, "
            f"B: {self.block}, "
            f"R: {self.resist}, "
            f"Haltung: {self.haltung}/{self.haltung_max}, "
            f"Taunt: {getattr(self, 'taunt', '-')}"
        )

    def __repr__(self):
        """Unambiguous string (used in REPL or lists)."""
        return f"<{self.__class__.__name__} {self.name} HP:{self.HP}/{self.HP_max}>"
#______________________________________________________________________PC's___________________________________________________________________________

