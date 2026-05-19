# -*- coding: utf-8 -*-
"""
Created on Fri Sep 26 10:01:54 2025

@author: Admin
"""

import Frostguard.dice as dice
import Frostguard.effects as effects

def harming(target, los):
    target.pure_damage(los-1)



# =============================================================================
# class Spell:
#     def __init__(self, name, cost, reaction = False):
#         self.name = name
#         self.cost = cost
# 
#     def cast(self):
#         return
#     
#     
#     
# class Shield(Spell):
#     def __init__(self):
#         super().__init__("Shield", cost=1, reaction=True)
# 
#     def cast(self, caster, target, **kwargs):
#         target.temp_block_bonus = getattr(target, "temp_block_bonus", 0) + 1
#         print(f"{caster.name} casts {self.name} on {target.name}: +1 Block vs the next attack!")
# =============================================================================



def get_spell(character, spell_name):
    spell_func = globals().get(spell_name)
    if not callable(spell_func):
        raise ValueError(f"Spell '{spell_name}' not found or not callable")
        
    # store as dict, keyed by name
    character.spells[spell_name] = spell_func


    

def level_of_success(caster, target):
    return dice.Roll(max(caster.charisma, caster.intelligenz) + target.advantage() - target.Dodge()) - target.resist


def level_of_success_passive(caster, target):
    return dice.Roll(max(caster.charisma, caster.intelligenz)) + target.resist


def Shield(caster):
    caster.mana -= 1
    caster.gain_effect('shield', {'effect' : effects.defence, 'bonus' : 1, 'trigger' : 'on_hit', 'type': 'reduction', 'duration' : 1})



def Scourge(caster, target):
    if caster.mana > 2:
        caster.mana -= 2
        los = level_of_success(caster, target)
        
        target.harming(los)
        
        if los < 1:
            return
        if los == 1:
            target.tmp_vorteil = 1
            return
        if los > 1:
            target.round_vorteil += 1
            
        if los > 2:
            target.move -= 1
        
        if los > 3:
            target.round_vorteil += 1
            target.move -= 1


# =============================================================================
# def Chainbolt(target1, target2):
#     if 
# =============================================================================
    

    
def Frostguard(caster, target = None):
    if target == None:
        target = caster
    caster.focus -= 1
    target.gain_effect('frostguard', {'effect' : effects.reflection, 'trigger' : 'on_hit', 'duration' : 5})    
    
    
    


