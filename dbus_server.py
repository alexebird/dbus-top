#!/usr/bin/python

import socket
import select
from threading import Thread

class ClientRegistrar:
    def __init__(self):
        self.clients = []
        
    def register_client(self, conn, addr):
        self.clients.append((conn, addr))

    def send_to_clients(self, data):
        for c in self.clients:
            conn, addr = c[0], c[1]
            print 'sending to:', addr
            #conn.setblocking(0)
            #cmd = conn.recv(4096)
            #if cmd == 'CLOSE':
                #conn.close()
            #else:
                #conn.send(data)

class DbusServer(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.host = ''                 # Symbolic name meaning all available interfaces
        self.port = port               # Arbitrary non-privileged port
        self.backlog = 5
        self.client_registrar = ClientRegistrar()
        self.should_run = True

    def run(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(0)  # Set to non-blocking mode
        self.socket.bind((self.host, self.port))
        self.socket.listen(self.backlog)
        while self.should_run == True:
            rv = select.select([self.socket], [], [], 1.0)
            if len(rv[0]) > 0:
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
                print 'registered client:', addr

    def stop(self):
        print 'stop'
        self.should_run = False

    def send_to_clients(self, data):
        self.client_registrar.send_to_clients(data)
