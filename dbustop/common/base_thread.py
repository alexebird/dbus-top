import threading
from threading import Thread

class BaseThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.shutdown_event = threading.Event()

    #
    # Shutdown the thread.  Must call shutdown() from another thread.
    #
    def shutdown(self):
        self.shutdown_event.set()
        self.join()
