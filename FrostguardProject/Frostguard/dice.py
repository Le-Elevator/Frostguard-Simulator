# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 12:42:18 2025

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
    
    # For i < 1 use default
    if Rang < 1:
        return r.choice([0, 1])
    
    # For i > 10, use a default
    if Rang > 10:
        return o() + o() + o()
    
    # Get function from dict and call it
    return mapping[Rang]()

