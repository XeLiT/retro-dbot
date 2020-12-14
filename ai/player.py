import threading
from input.window import Window
from input.keyboard import Keyboard
from utils.helpers.collection import Collection
from utils.patterns.observable import Observable
from utils.patterns.observer import Observer
from ai.sequence.search_mob import SearchMob
from ai.sequence.hit_and_run import HitAndRun
from ai.sequence.sequence import Sequence
from ai.eye import Eye

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
        self.eye = None
        self.flag_search_mob = False
        self.flag_debug_graph = False
        self.flag_debug_sight = False
        self.selected_cell = None
        self.last_computed_path = None
        Sequence.__init__(self, self)

    def update(self, event, event_type=None):
        if event_type == "flag_search_mob":  # GUI events
            self.flag_search_mob = not self.flag_search_mob
            event["ref"].configure(text=f"Searching Mob {str(self.flag_search_mob)}", background="green" if self.flag_search_mob else "white")

        elif event_type == "flag_debug_graph":  # GUI events
            self.flag_debug_graph = not self.flag_debug_graph
            self.game_state.map.graph.debug_edges()
            event["ref"].configure(text=f"Debug Graph {str(self.flag_debug_graph)}", background="green" if self.flag_debug_graph else "white")

        elif event_type == "flag_debug_sight":  # GUI events
            self.flag_debug_sight = not self.flag_debug_sight
            event["ref"].configure(text=f"Debug Sight {str(self.flag_debug_sight)}", background="green" if self.flag_debug_sight else "white")

        elif event_type == "cell_click_event":
            self.selected_cell = event["data"]
            logging.debug(self.selected_cell)

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
            self.eye = Eye(self.window)
            logging.info(f'Found window for {self.player_name} !')
            return True
        return False

    def debug_path(self):
        cell = self.selected_cell
        player_cell = self.game_state.get_entity_cell(self.game_state.get_player_entity())
        path = self.game_state.map.get_shortest_path(player_cell, cell)
        if len(path):
            self.game_state.map.graph.debug_path(path)

    def run(self):
        while True:
            try:
                if not self.wait_until(self.find_window):
                    continue
                if not self.wait_until(lambda x: x.player_entity_id != 0 and x.map, self.game_state):
                    continue
                world_ai = SearchMob(self)
                world_ai.loop()
                fight_ai = HitAndRun(self)
                fight_ai.loop()
                self.tick(1)
            except Exception as e:
                logging.exception(e)
                self.tick(self.TICK * 10)

    def __repr__(self):
        return self.player_name


if __name__ == '__main__':
    p = Player(config.PLAYERS[0], None)
    p.find_window()