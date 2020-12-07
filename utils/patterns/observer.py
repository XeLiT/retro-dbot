import logging


class Observer:
    def update(self, event, event_type=None):
        logging.debug(event)