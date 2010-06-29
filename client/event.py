import time

class Event:
    def __init__(self, origin, data):
        self.timestamp = time.time()
        self.data = data
        self.origin = origin
