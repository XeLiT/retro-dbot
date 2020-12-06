class Observable:
    def __init__(self):
        self.observers = set()
        self.event_type_index = {} # dict of sets, key is the event_type, value is a set of observers

    def attach(self, who, event_type=""):
        if event_type != "":
            if not event_type in self.event_type_index:
                self.event_type_index[event_type] = set()
            self.event_type_index[event_type].add(who)
        else:
            self.observers.add(who)

    def detach(self, who, event_type=""):
        if event_type != "" and event_type in self.event_type_index:
            self.event_type_index[event_type].discard(who)
        else:
            self.observers.discard(who)

    def dispatch(self, event, event_type=""):
        if event_type != "" and event_type in self.event_type_index:
            for observer in self.event_type_index[event_type]:
                observer.update(event)
        else:
            for observer in self.observers:
                observer.update(event)