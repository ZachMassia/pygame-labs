class EventManager(object):
    """Allows functions to subscribe to specific pygame events."""

    def __init__(self):
        self.subs = {}

    def dispatch(self, evts):
        """Dispatch the list of events to the subscribers."""
        for evt in evts:
            if evt.type in self.subs:
                for sub in self.subs[evt.type]:
                    sub(evt)

    def subscribe(self, evt_type, func):
        """Subscribe a function to a given event type."""
        if evt_type in self.subs:
            self.subs[evt_type].append(func)
        else:
            self.subs[evt_type] = [func]

    def unsubscribe(self, func):
        """Attempt to unsubscribe a function. No errors if not found."""
        for subList in self.subs:
            if func in subList:
                subList.remove(func)
