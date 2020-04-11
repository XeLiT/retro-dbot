import pyshark
import binascii
import struct
import logging
from config import NETWORK_INTERFACE, LOGGING_LEVEL

# Frames
from frames.map_frame import MapFrame
from frames.map_change import MapChange
from frames.game_action import GameAction

# Ia
from ia.game_state import GameState

capture = pyshark.LiveCapture(interface=NETWORK_INTERFACE, bpf_filter='tcp port 5555 and len > 66')
logging.basicConfig(level=LOGGING_LEVEL)
game_state = GameState()

for packet in capture.sniff_continuously():
    if not packet.data.len:
        continue
    binary = binascii.unhexlify(packet.data.data)
    data = list(filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00')))
    logging.debug('<TCP {}>{} L: {}'.format(packet.tcp.srcport, packet.tcp.dstport, packet.data.len))

    for raw_data in data:
        logging.debug('   Data: {}'.format(raw_data))
        if raw_data.startswith('GM'):
            mapFrame = MapFrame(raw_data, game_state)
            logging.debug(mapFrame)
        elif raw_data.startswith('GDM'):
            m = MapChange(raw_data, game_state)
        elif raw_data.startswith('GA'):
            ga = GameAction(raw_data, game_state)