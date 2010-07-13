print 'IMPORTING:', __name__
import threading

class BaseThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name
