import threading
from input.window import Window
from input.keyboard import Keyboard
from utils.helpers.collection import Collection
from utils.patterns.observable import Observable
from utils.patterns.observer import Observer
from ai.sequence.search_mob import SearchMob
from ai.sequence.sequence import Sequence

import config
import logging


class Player(threading.Thread, Observable, Observer, Sequence):
    def __init__(self, player_info, game_state) -> None:
        threading.Thread.__init__(self, daemon=True)
        Observable.__init__(self)
        Observer.__init__(self)
        self.player_info = player_info
        self.player_name = player_info['name']
        self.player_type = player_info['type']
        self.game_state = game_state
        self.window = None
        self.keyboard = None
        self.login = None
        self.flag_search_mob = False
        Sequence.__init__(self, self)

    def update(self, event, event_type):
        if event_type == "flag_search_mob":  # GUI events
            self.flag_search_mob = not self.flag_search_mob
            event["ref"].configure(text=f"Flag Searching Mob {str(self.flag_search_mob)}", background="green" if self.flag_search_mob else "white")

    def find_window(self, *arg):
        if self.window:
            return True
        windows = Window.list_windows()
        w = Collection(windows).find_one(callback=lambda x: self.player_name in x.name)
        if w:
            self.window = w
            self.window.resize()
            self.window.focus()
            self.keyboard = Keyboard(w)
            logging.info(f'Found window for {self.player_name} !')
            return True
        return False

    def run(self):
        while True:
            try:
                if not self.wait_until(self.find_window):
                    continue
                if not self.wait_until(lambda x: x.player_entity_id != 0 and x.map, self.game_state):
                    continue
                logging.info('Player found !')
                ai = SearchMob(self)
                ai.loop()
                self.tick()
            except Exception as e:
                logging.exception(e)
                self.tick(self.TICK * 10)

    def __repr__(self):
        return self.player_name


if __name__ == '__main__':
    p = Player(config.PLAYERS[0], None)
    p.find_window()