import socket
from client_registrar import ClientRegistrar
from common import util
from common.base_thread import BaseThread

class DbustopServer(BaseThread):
    def __init__(self, port):
        BaseThread.__init__(self, 'DbustopServer Thread')
        self.host = ''  # Symbolic name meaning all available interfaces
        self.port = port
        self.client_registrar = ClientRegistrar()
        self.listening = False
        print 'dbustop-server listening on %d' % self.port

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        backlog = 5
        self.socket.listen(backlog)
        self.socket.setblocking(0)  # Set to non-blocking mode
        self.listening = True

    def do_run(self):
        if not self.listening: return
        while self.should_run == True:
            if util.ready_for_read(self.socket):
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
        self.client_registrar.close_all()


    def send_to_clients(self, msg):
        self.client_registrar.send_to_clients(msg.packetize())

    def is_running(self):
        return self.running
