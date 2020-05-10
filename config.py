import logging

# General
LOGGING_LEVEL = logging.DEBUG
VERSION = '1.32.0'
BINARY = "\"C:/Users/thomas/AppData/Local/Ankama/zaap/retro/Dofus Retro.exe\""
MAP_DIR = 'C:/Users/thomas/AppData/Local/Ankama/zaap/retro/resources/app/retroclient/data/maps'
MOTIF_DIR = 'utils/refs/'

# Sniffer
NETWORK_INTERFACE = 'Ethernet'

PLAYERS = [{
    'name': 'Xelit',
    'type': 'iop-air',
    'secret': 'C:/Users/thomas/xelit.txt',
    'spells': [{'name': 'épé céleste', 'index': 2, 'line': True, 'aoe': 2, 'range': [3, 3], 'priority': 100}]
}]