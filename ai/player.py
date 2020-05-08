import threading
import time
from input.window import Window
from input.keyboard import Keyboard
from utils.collection import Collection
from input.login import Login
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
        self.login = Login(player_info)

    def find_window(self):
        windows = Window.list_windows()
        w = Collection(windows).find_one(callback=lambda x: self.player_name in x.name)
        if not w:
            self.login.login()
            self.window = self.login.window
            self.keyboard = self.login.kb
        else:
            self.window = w
            self.keyboard = Keyboard(w)
        logging.info(f'Found window for {self.player_name} !')

    def wait_until(self, callback, timeout=60):
        while timeout > 0:
            if callback(self.game_state):
                break
            time.sleep(TICK)
            timeout -= TICK
        return timeout > 0

    def run(self):
        try:
            self.find_window()
            self.wait_until(lambda x: x.player_entity_id != 0 and x.map)
            logging.info('Player found !')
        except Exception as e:
            logging.error(e)



if __name__ == '__main__':
    p = Player(config.PLAYERS[0], None)
    p.find_window()