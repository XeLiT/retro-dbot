class Observable:
    def __init__(self):
        self._observers = set([])

    def attach(self, observer):
        self._observers.add(observer)

    def detach(self, observer):
        self._observers.discard(observer)

    def dispatch(self, event, event_type=""):
        for observer in self._observers:
            observer.update(event, event_type)
