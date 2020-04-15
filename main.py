import pyshark
import binascii
import struct
import logging
import threading
from gui.master import MasterGUI
from config import NETWORK_INTERFACE, LOGGING_LEVEL

# Frames
from frames.map_infos import MapInfos
from frames.map_change import MapChange
from frames.game_action import GameAction

# Ia
from ia.game_state import GameState

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
            data = list(filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00')))

            for raw_data in data:
                logging.debug('   Data: {}'.format(raw_data))
                if raw_data.startswith('GM'):
                    self.game_state.update_entities(MapInfos(raw_data))
                elif raw_data.startswith('GDM'):
                    self.game_state.update_map(MapChange(raw_data))
                elif raw_data.startswith('GA'):
                    self.game_state.update_entity(GameAction(raw_data))


if __name__ == '__main__':
    logging.basicConfig(level=LOGGING_LEVEL)
    ask_admin_access()
    gui = MasterGUI()
    game_state = GameState(gui)
    ns = NetworkSniffer(game_state)
    ns.start()
    gui.mainloop()
    if ns in threading.enumerate():
        interrupt_thread(ns.ident)
