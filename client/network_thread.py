import socket
import select
import pickle
import threading
from threading import Thread
from common.dbus_message import DbusMessage

class NetworkThread(Thread):
    def __init__(self, host, port):
        Thread.__init__(self)
        self.name = 'NetworkThread'
        self.should_run_lock = threading.Lock()
        self.connection_args = (host, port)
        self.should_run = True
        self.running = False
        self.callbacks = {}

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
                #if data == 'registered':
                    #print 'registered with %s:%d' % \
                        #(self.connection_args[0], self.connection_args[1])
                if len(data) > 0:
                    try:
                        msg = pickle.loads(data)
                        self.__fire_event('message_received', msg)
                    except IndexError:
                        pass
        self.running = False
        #print 'sending close'
        self.socket.send('CLOSE')
        self.socket.close()

    def stop(self):
        print 'NetworkThread stopped',
        if self.running:
            #print 'stopping client'
            self.set_should_run_synced(False)

    def set_should_run_synced(self, newval):
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()

    def add_message_received_callback(self, method):
        self.__add_callback('message_received', method)

    #
    # General purpose event mechanism methods
    #

    def __add_callback(self, callback_name, method):
        try:
            self.callbacks[callback_name]
        except KeyError:
            self.callbacks[callback_name] = []
        self.callbacks[callback_name].append(method)

    def __fire_event(self, event_name, data):
        for m in self.callbacks[event_name]:
            m(data)
