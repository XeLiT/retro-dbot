from network.game_action import *
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    GameAction().parse_action("GA;100;-1;80146042,-14")
    GameAction().parse_action("GA;100;250061785;-1,-4,2")
    GameAction().parse_action("GA;100;250062459;-1,-11,2")
    GameAction().parse_action("GA0;1;250062459;af6bgyagA")
    GameAction().parse_action("GA;1;-4;abnfa-")

