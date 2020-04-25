import pyshark
import binascii
import struct
import threading
import logging
from gui.master import MasterGUI
from config import NETWORK_INTERFACE, LOGGING_LEVEL, PLAYER_NAME

# Frames
from frames.map_infos import MapInfos
from frames.map_change import MapChange
from frames.game_action import GameAction
from frames.game_fight import GameFight

# Ia
from ai.game_state import GameState

# Utils
from utils.admin import *


class NetworkSniffer(threading.Thread):
    def __init__(self, game_state):
        super().__init__(daemon=True)
        self.game_state = game_state

    def run(self):
        capture = pyshark.LiveCapture(interface=NETWORK_INTERFACE, bpf_filter='tcp port 5555 and len > 66')
        for packet in capture.sniff_continuously():
            if not packet.data.len:
                continue
            binary = binascii.unhexlify(packet.data.data)
            data = filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00'))

            for raw_data in data:
                logging.debug('   Data: {}'.format(raw_data))
                if raw_data.startswith('GM'):
                    self.game_state.update_map_infos(MapInfos(raw_data))
                elif raw_data.startswith('GDM'):
                    self.game_state.update_map(MapChange(raw_data))
                elif raw_data.startswith('GA'):
                    self.game_state.update_from_action(GameAction().parse_action(raw_data))

                # Fight
                elif raw_data.startswith('GP'):
                    self.game_state.game_fight.set_fight_start_cells(raw_data)
                elif raw_data.startswith('GIC'):
                    self.game_state.update_from_action(GameAction().parse_entity_start_cell(raw_data))
                elif raw_data.startswith('GR'):
                    self.game_state.set_player_ready(**GameFight.parse_fight_ready(raw_data))
                elif raw_data.startswith('GTS'):
                    self.game_state.game_fight.set_entity_turn(raw_data)
                elif raw_data.startswith('GTM'):
                    self.game_state.update_entities(GameFight.parse_fight_state(raw_data))
                elif raw_data.startswith('GCK') and PLAYER_NAME in raw_data:                            # Fight end
                    self.game_state.set_fighting(False)


if __name__ == '__main__':
    logging.basicConfig(level=LOGGING_LEVEL)
    ask_admin_access()
    gui = MasterGUI()
    gui.pack_slaves()
    game_state = GameState(gui, PLAYER_NAME)
    ns = NetworkSniffer(game_state)
    ns.start()
    gui.mainloop()
    if ns in threading.enumerate():
        interrupt_thread(ns.ident)
