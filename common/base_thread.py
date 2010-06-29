import threading
from threading import Thread

class BaseThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
        #self.should_run_lock = threading.Lock()
        #self.should_run = True
        #self.running = False
        #self.callbacks = {}
        self.shutdown_event = threading.Event()

    #
    # Shutdown the thread.  Must call shutdown() from another thread.
    #
    def shutdown(self):
        self.shutdown_event.set()
        self.join()

    #def run(self):
        ##self.running = True
        #self.do_run()
        ##self.running = False

    #def stop(self):
        #if self.running:
            #self.should_run_lock.acquire()
            #self.should_run = False
            #self.should_run_lock.release()
            #self.shutdown_event.set()
