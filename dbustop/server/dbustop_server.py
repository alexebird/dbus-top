import socket
from client_registrar import ClientRegistrar
from dbustop.common import util
from dbustop.common.base_thread import BaseThread

class DbustopServer(BaseThread):
    def __init__(self, port):
        BaseThread.__init__(self, 'DbustopServerThread')
        self.host = ''  # Symbolic name meaning all available interfaces
        self.port = port
        self.client_registrar = ClientRegistrar()
        print 'dbustop-server listening on %d' % self.port

    def listen(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.bind((self.host, self.port))
        except socket.error as e:
            if e[0] == errno.EADDRINUSE:
                print 'Address is in use.'
                return False
        backlog = 5
        self.socket.listen(backlog)
        self.socket.setblocking(0)  # Set to non-blocking mode
        return True

    def run(self):
        while not self.shutdown_event.is_set():
            if util.ready_for_read(self.socket):
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
        self.client_registrar.close_all()
        self.socket.close()


    def send_to_clients(self, msg):
        self.client_registrar.send_to_clients(msg.packetize())
