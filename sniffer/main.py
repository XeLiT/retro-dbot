import pyshark
import binascii
import struct
import logging
import frames.map_frame

logging.basicConfig(level=logging.DEBUG)
capture = pyshark.LiveCapture(interface='\\Device\\NPF_{F23B8BB9-F7D0-4D4B-8646-616C19D4390A}', bpf_filter='tcp port 5555 and len > 66')

for packet in capture.sniff_continuously():
    if not packet.data.len:
        continue
    binary = binascii.unhexlify(packet.data.data)
    data = list(filter(None, struct.unpack('!{}s'.format(len(binary)), binary)[0].decode('utf-8').replace('\n', '').split('\x00')))

    logging.debug('<TCP {}>{} L: {}'.format(packet.tcp.srcport, packet.tcp.dstport, packet.data.len))

    for action in data:
        action_code = action[:2]
        logging.debug('   Data: {}'.format(action))
        if action_code == 'GM':
            mapFrame = frames.map_frame.MapFrame(action)
            print(mapFrame)
