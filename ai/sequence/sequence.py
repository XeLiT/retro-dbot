import time
import logging

DEFAULT_TICK = 0.5


class Sequence:
    TICK = DEFAULT_TICK

    def __init__(self, player) -> None:
        self.player = player
        self.gs = self.player.game_state
        self.w = self.player.window
        self.kb = self.player.keyboard

    def loop(self):
        self.tick()

    def wait_until(self, callback, extra_arg=None, timeout=60):
        while timeout > 0:
            if callback(extra_arg):
                return True
            self.tick()
            timeout -= self.TICK
        logging.error(f"Timeout error for {str(callback)} {str(extra_arg)}")
        return timeout <= 0

    def tick(self, timeout=DEFAULT_TICK):
        time.sleep(timeout)