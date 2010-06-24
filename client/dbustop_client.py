import socket
import select
import pickle
import threading
from threading import Thread
from common.dbus_message import DbusMessage

class DbustopClient(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.name = 'DbustopClient Thread'
        self.should_run_lock = threading.Lock()
        self.connection_args = (host, port)
        self.should_run = True
        self.running = False

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.connection_args)
            self.socket.setblocking(0)  # Set to non-blocking mode
        except socket.error as e:
            print e
            self.socket.close()
            return
        self.running = True
        while self.should_run == True:
            rv = select.select([self.socket], [], [], 0.1)
            if len(rv[0]) > 0:
                data = self.socket.recv(4096 * 100)
                if data == 'registered':
                    print 'registered with %s:%d' % \
                        (self.connection_args[0], self.connection_args[1])
                elif len(data) > 0:
                    msg = pickle.loads(data)
                    print msg
        self.running = False
        print 'sending close'
        self.socket.send('CLOSE')
        self.socket.close()

    def stop(self):
        if self.running:
            print 'stopping client'
            self.set_should_run_synced(False)

    def set_should_run_synced(self, newval):
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()
