import socket
import select
import pickle
from common.evented_thread import EventedThread
from common import util

class NetworkThread(EventedThread):
    def __init__(self, host, port):
        EventedThread.__init__(self, 'NetworkThread')
        self.connection_args = (host, port)

    def do_run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect(self.connection_args)
            self.socket.setblocking(0)  # Set to non-blocking mode
        except socket.error as e:
            print e
            self.socket.close()
            return
        while self.should_run == True:
            if util.ready_for_read(self.socket):
                data = self.socket.recv(4096 * 100)
                #if data == 'registered':
                    #print 'registered with %s:%d' % \
                        #(self.connection_args[0], self.connection_args[1])
                if len(data) > 0:
                    try:
                        msg = pickle.loads(data)
                        self.fire_event('message_received', msg)
                    except IndexError:
                        # Occurs when Pickle can't parse the message.
                        pass
        #print 'sending close'
        self.socket.send('CLOSE')
        self.socket.close()

    def add_message_received_callback(self, method):
        self.add_callback('message_received', method)
