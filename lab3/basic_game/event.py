import logging


class EventManager(object):
    """Allows functions to subscribe to specific pygame events."""

    def __init__(self):
        self.subs = {}
        self.logging_enabled = False

    def dispatch(self, evts):
        """Dispatch the list of events to the subscribers."""
        for evt in evts:
            if evt.type in self.subs:
                for sub in self.subs[evt.type]:
                    sub(evt)

    def subscribe(self, evt_type, func):
        """Subscribe a function to a given event type."""
        if evt_type not in self.subs:
            self.subs[evt_type] = list()
        self.subs[evt_type].append(func)

        if self.logging_enabled:
            logging.debug('EVT_MGR: binding func {} to {}'.format(func,
                                                                  evt_type))

    def subscribe_list(self, pairs):
        """Subscribe a list of function to event tuples."""
        for evt_type, func in pairs:
            self.subscribe(evt_type, func)

    def unsubscribe(self, func):
        """Attempt to unsubscribe a function. No errors if not found."""
        for subList in self.subs:
            if func in subList:
                subList.remove(func)
                if self.logging_enabled:
                    logging.debug('EVT_MGR: unbinding func {}'.format(func))
