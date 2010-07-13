from threading import Thread

class BaseThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
