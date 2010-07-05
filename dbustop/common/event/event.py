import time

class Event:
    def __init__(self, origin, type, data):
        self.timestamp = time.time()
        self.origin = origin
        self.type = type
        self.data = data

    def __repr__(self):
        return '<Event: origin=%s, type=%s, data=%s>' % (self.origin, self.type, self.data.__class__)
