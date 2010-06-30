import time

class Event:
    def __init__(self, origin, type, data):
        self.timestamp = time.time()
        self.origin = origin
        self.type = type
        self.data = data
