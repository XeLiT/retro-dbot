import logging

class Observer:
    def update(self, event):
        logging.debug(event)