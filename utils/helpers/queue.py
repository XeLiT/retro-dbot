import queue
import time


class Queue(queue.Queue):
    def __init__(self, maxsize: int = ...) -> None:
        super().__init__(maxsize)

    def wait_until(self, callback, timeout=60):
        start = time.time()
        remaining_time = timeout
        while True:
            item = self.get(timeout=remaining_time)
            remaining_time -= int(time.time() - start)
            if callback(item):
                break
