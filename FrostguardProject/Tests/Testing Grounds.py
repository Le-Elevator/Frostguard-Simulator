# -*- coding: utf-8 -*-
"""
Created on Wed Sep 17 09:59:02 2025

@author: Admin
"""
import sys
import matplotlib.pyplot as plt
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from Frostguard.pc import Kämpfer, Zauberer, Kleriker
from Frostguard.battle import Battle
from Frostguard.spells import Shield



adan = Kämpfer('Adan', 2, 0, 1, 1, 'Verteidiger')
grandulf = Zauberer('Grandulf', 0, 2, 2, 1, 'Evoker')

eve = Kleriker('Eve', 0, 1, 1, 2)
marcon = Kleriker('Marcon', 2, 0, 1, 1, 'Paladin')



Shield(grandulf)







