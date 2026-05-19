# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:42:03 2025

@author: Admin
"""

import random as r


class Battle:
    def __init__(self, heroes, monsters):
        self.heroes = heroes
        self.monsters = monsters
        

    def run_turn(self, character):
        character.turn_start(self)  # delegate action logic to the character
            

    def choose_target(self, character):
        """Choose a target for the character based on taunt values."""
        enemies = [enemy for enemy in self.enemies(character) if enemy.is_alive()]
        
        # If character can't move and is melee combatant, introduce likelihood that no one is in range
        if character.move < 0 and not character.ranged and r.random() < 0.33:
            return None
        
        if not enemies:
            return None  # no valid targets
        
        taunts = [enemy.get_taunt() for enemy in enemies]
        
        # If ranged, invert the taunt list
        if getattr(character, "ranged", None) == True:
            taunt_min = min(taunts)
            taunt_max = max(taunts)
            taunts = [taunt_max + taunt_min - t for t in taunts]
    
        # Ensure weights are all positive
        taunts = [max(1, t) for t in taunts]
    
        return r.choices(enemies, weights=taunts, k=1)[0]
    
    
    def allies(self, character):
        if self.is_hero(character):
            return self.heroes
        else:
            return self.monsters
    
    
    
    def enemies(self, character):
        if self.is_hero(character):
            return self.monsters
        else:
            return self.heroes
    
    

    def is_hero(self, character):
        return character in self.heroes


