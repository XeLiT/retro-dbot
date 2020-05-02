import threading
import time
from input.window import Window
from input.keyboard import Keyboard
from utils.collection import Collection
import config
import logging

TICK = 0.5


class Player(threading.Thread):
    def __init__(self, player_info, game_state) -> None:
        super().__init__(daemon=True)
        self.player_name = player_info['name']
        self.player_type = player_info['type']
        self.player_creds = open(player_info['secret']).read().split('\n')
        self.game_state = game_state
        self.window = None
        self.keyboard = None

    def find_window(self):
        while True:
            windows = Window.list_windows()
            w = Collection(windows).find_one(callback=lambda x: self.player_name in x.name)
            if w:
                self.window = w
                self.keyboard = Keyboard(w)
                break
            logging.debug(f'Finding window for {self.player_name}')
            time.sleep(1)

    def wait_until(self, callback, timeout=60):
        while timeout > 0:
            if callback(self.game_state):
                break
            time.sleep(TICK)
            timeout -= TICK
        return timeout > 0

    def run(self):
        self.find_window()
        logging.info(f'Found window for {self.player_name} !')
        self.wait_until(lambda x: x.player_entity_id != 0 and x.map)
        logging.info('Player found !')

if __name__ == '__main__':
    p = Player(config.PLAYERS[0], None)
    p.find_window()