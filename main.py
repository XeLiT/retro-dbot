import threading
import logging
import config
from gui.master import MasterGUI
from ai.game_state import GameState
from ai.player import Player
from utils.admin import *
from network.network_sniffer import NetworkSniffer


if __name__ == '__main__':
    logging.basicConfig(level=config.LOGGING_LEVEL)
    ask_admin_access()
    gui = MasterGUI()
    gui.pack_slaves()
    game_state = GameState(gui, config.PLAYER_NAME)
    ns = NetworkSniffer(game_state)
    ns.start()
    player = Player(config.PLAYERS[0], game_state)
    player.start()
    gui.mainloop()
    if ns in threading.enumerate():
        interrupt_thread(ns.ident)
