import logging

# General
LOGGING_LEVEL = logging.DEBUG
VERSION = '1.33.6'
BINARY = "\"C:/Users/thomas/AppData/Local/Ankama/zaap/retro/Dofus Retro.exe\""
MAP_DIR = 'C:/Users/thomas/AppData/Local/Ankama/zaap/retro/resources/app/retroclient/data/maps'
MOTIF_DIR = 'utils/motifs/'

# Sniffer
NETWORK_INTERFACE = 'Ethernet'

PLAYERS = [
    {
        'name': 'Panini',
        'type': 'cra',
        'spells': [{'name': 'Fleche Magique', 'index': 1, 'pa': 4, 'range': [1, 7], 'priority': 100}]
    }
]

IA = {
    "world": "search_mob",
    "fight": "hit_and_run",
}
MAX_MOB_GROUP_LEVEL = 9

AREA = [
    (2, 1), (3, 1),
    (2, 2), (3, 2),
]