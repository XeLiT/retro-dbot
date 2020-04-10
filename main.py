import pyshark
import binascii
import struct
import logging
from sniffer.frames.map_frame import MapFrame
from config import NETWORK_INTERFACE, LOGGING_LEVEL

capture = pyshark.LiveCapture(interface=NETWORK_INTERFACE, bpf_filter='tcp port 5555 and len > 66')
logging.basicConfig(level=LOGGING_LEVEL)

for packet in capture.sniff_continuously():
    if not packet.data.len:
        continue
    binary = binascii.unhexlify(packet.data.data)
    data = list(filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00')))

    logging.debug('<TCP {}>{} L: {}'.format(packet.tcp.srcport, packet.tcp.dstport, packet.data.len))

    for action in data:
        logging.debug('   Data: {}'.format(action))
        if action.startswith('G'):
            if action[1] == 'M':
                mapFrame = MapFrame(action)
                print(mapFrame)
