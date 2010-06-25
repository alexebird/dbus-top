import threading
from threading import Thread

class EventedThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        self.should_run_lock = threading.Lock()
        self.should_run = True
        self.running = False
        self.callbacks = {}
        self.shutdown_event = threading.Event()

    def run(self):
        self.running = True
        self.do_run()
        self.running = False

    def stop(self):
        #if self.running:
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()

    #
    # General purpose event mechanism methods
    #

    def add_callback(self, callback_name, method):
        try:
            self.callbacks[callback_name]
        except KeyError:
            self.callbacks[callback_name] = []
        self.callbacks[callback_name].append(method)

    def fire_event(self, event_name, data):
        for m in self.callbacks[event_name]:
            m(data)
