import pyshark
import threading
import binascii
import struct
import config
import logging
from network.map_infos import MapInfos
from network.map_change import MapChange
from network.game_action import GameAction
from network.game_fight import GameFight


class NetworkSniffer(threading.Thread):
    def __init__(self, game_state, lock):
        super().__init__(daemon=True)
        self.game_state = game_state
        self.lock = lock

    def run(self):
        capture = pyshark.LiveCapture(interface=config.NETWORK_INTERFACE, bpf_filter='tcp port 5555 and len > 66')
        for packet in capture.sniff_continuously():
            try:
                self.parse(packet)
            except Exception as e:
                logging.exception(e)

    def parse(self, packet):
        if not packet.data.len:
            return
        binary = binascii.unhexlify(packet.data.data)
        data = filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00'))

        # self.lock.acquire()
        for raw_data in data:
            try:
                logging.debug('   Data: {}'.format(raw_data))

                # Map
                if raw_data.startswith('GM'):
                    self.game_state.update_map_infos(MapInfos(raw_data))
                elif raw_data.startswith('GDM'):
                    self.game_state.update_map(MapChange(raw_data))
                elif raw_data.startswith('GA'):
                    self.game_state.update_from_action(GameAction().parse_action(raw_data))

                # Player
                elif raw_data.startswith('Ow'):
                    self.game_state.player_infos.parse_pods(raw_data)

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
                elif raw_data.startswith('GCK'):  # and PLAYER_NAME in raw_data:                            # Fight end
                    self.game_state.set_fighting(False)
            except Exception as e:
                logging.error(f"Error parsing: {raw_data}")
                logging.exception(e)
        # self.lock.release()
