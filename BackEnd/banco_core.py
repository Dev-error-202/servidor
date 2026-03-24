"""
    Arquivo de manipulação direta do banco de dados
    gerencia a pasta de dados de cada usuario de maneira mas otimizada,
"""

import os
from random import randint
import sys
import sqlite3 as sql
import platform

if platform.system() == 'Windows':
    pastamain = 'C:/ProgramData/BancoSystem'
else:
    pastamain = '/var/BancoSystem'






class BancoCore:
    def __init__(self, user):
        self.pathuser = os.path.join(pastamain, user)




