import threading
import logging
import config
from gui.master import MasterGUI
from network.game_state import GameState
from utils.helpers.admin import *
from network.network_sniffer import NetworkSniffer
from ai.player import Player

if __name__ == '__main__':
    logging.basicConfig(level=config.LOGGING_LEVEL)
    # ask_admin_access()
    gui = MasterGUI()
    gui.onAfter()
    game_state = GameState(gui, config.PLAYERS[0]['name'])
    lock = threading.Lock()
    ns = NetworkSniffer(game_state, lock)
    logging.info("Starting bot")
    ns.start()
    # player = Player(config.PLAYERS[0], game_state)
    # gui.attach(player, "flag_search_mob")
    # player.start()
    gui.mainloop()
    if ns in threading.enumerate():
        interrupt_thread(ns.ident)
