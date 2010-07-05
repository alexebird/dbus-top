import socket
import select
import errno

from client_registrar import ClientRegistrar
from dbustop.common.base_thread import BaseThread
from dbustop.common.event import event_loop

class DbustopServer(BaseThread):
    def __init__(self, port):
        BaseThread.__init__(self, 'DbustopServer_thread')
        self.host = ''  # Symbolic name meaning all available interfaces
        self.port = port
        self.client_registrar = ClientRegistrar()
        def dbus_message_received_handler(event):
            self.client_registrar.send_to_clients(event.data.packetize())
        event_loop.loop.register_event_callback('DbusMonitorMonitor_thread', 'dbus-message-received', dbus_message_received_handler)
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
        while True:
            ready_fds = select.select([self.socket, event_loop.loop.child_thread_control_socket], [], [])
            if self.socket in ready_fds[0]:
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
            if event_loop.loop.child_thread_control_socket in ready_fds[0]:
                print 'exiting', self.name
                break
        self.client_registrar.close_all()
        self.socket.close()


    def send_to_clients(self, msg):
        self.client_registrar.send_to_clients(msg.packetize())
