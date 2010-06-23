import socket
import select
import threading
from threading import Thread
import client_registrar

class DbustopServer(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.host = ''                 # Symbolic name meaning all available interfaces
        self.port = port               # Arbitrary non-privileged port
        self.should_run_lock = threading.Lock()
        self.backlog = 5
        self.client_registrar = client_registrar.ClientRegistrar()
        self.should_run = True
        self.running = False
        print 'dbustop-server listening on %d' % self.port

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)  # Set to non-blocking mode
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        self.running = True
        while self.should_run == True:
            rv = select.select([self.socket], [], [], 0.2)
            if len(rv[0]) > 0:
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
                conn.send('registered')
                print 'registered client:', addr
        self.running = False

    def stop(self):
        if self.running:
            print 'stopping server'
            self.set_should_run_synced(False)

    def set_should_run_synced(self, newval):
        self.should_run_lock.acquire()
        self.should_run = False
        self.should_run_lock.release()

    def send_to_clients(self, msg):
        self.client_registrar.send_to_clients(msg.serialize())
