# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 14:44:23 2025

@author: Admin
"""

import Frostguard.dice as dice
import Frostguard.spells as s


def level_of_success_passive(caster, target):
    return dice.Roll(max(caster.charisma, caster.intelligenz)) + target.resist



def regen(character, data):
    heal_amount = data.get("power", 1)
    character.HP = min(character.HP_max, character.HP + heal_amount)
    



def defence(character, data):
    if not data.get("consumed", False):
        bonus = data.get("bonus", 1)
        data["consumed"] = True   # mark as used
        data["duration"] = 0      # ensure it expires on resolve_effects
        return bonus
    return 0




def reflection(caster, aggressor, data):
    los = level_of_success_passive(caster, aggressor)
    s.harming(aggressor, los)
    return max(0, min(los, 3))



