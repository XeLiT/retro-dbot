import logging

# General
LOGGING_LEVEL = logging.DEBUG
VERSION = '1.33.6'
BINARY = "\"C:/Users/thomas/AppData/Local/Ankama/zaap/retro/Dofus Retro.exe\""
MAP_DIR = 'C:/Users/thomas/AppData/Local/Ankama/zaap/retro/resources/app/retroclient/data/maps'
MOTIF_DIR = 'utils/refs/'

# Sniffer
NETWORK_INTERFACE = 'Ethernet'

PLAYERS = [{
    'name': 'Xelit',
    'type': 'feca',
    'secret': 'C:/Users/thomas/xelit.txt',
    'spells': [{'name': 'Attaque Naturelle', 'index': 1, 'range': [1, 6], 'priority': 100}]
}]