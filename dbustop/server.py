import socket
import select
import errno

import base_thread
import event

class ClientRegistrar:
    def __init__(self):
        self.clients = []
        
    def register_client(self, conn, addr):
        conn.setblocking(0)  # set to non-blocking mode
        #conn.send('registered')
        self.clients.append((conn, addr))
        print 'registered client:', addr

    def remove_client(self, conn):
        for c in self.clients:
            if conn == c[0]:
                self.clients.remove(c)
                print 'removed client:', c[1]
                break

    def send_to_clients(self, data):
        for c in self.clients:
            conn, addr = c[0], c[1]
            ready_fds = select.select([conn], [conn], [])
            if conn in ready_fds[0]:
                cmd = conn.recv(4096)
                if cmd == 'CLOSE':
                    print 'CLOSE received from ', addr
                else:
                    print 'unknown command: "%s"' % cmd
                conn.close()
                self.remove_client(conn)
            if conn in ready_fds[1]:
                print 'sending to:', addr, '(%d bytes)' % len(data)
                try:
                    conn.send(data)
                except socket.error:
                    conn.close()
                    self.remove_client(conn)

    def close_all(self):
        for c in self.clients:
            c[0].close()

class DbustopServer(base_thread.BaseThread):
    def __init__(self, port):
        base_thread.BaseThread.__init__(self, 'DbustopServer_thread')
        self.host = ''  # Symbolic name meaning all available interfaces
        self.port = port
        self.client_registrar = ClientRegistrar()
        def dbus_message_received_handler(event):
            self.client_registrar.send_to_clients(event.data.packetize())
        event.mainloop.register_event_callback('DbusMonitorMonitor_thread', 'dbus-message-received', dbus_message_received_handler)
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
            ready_fds = select.select([self.socket, event.mainloop.child_thread_control_socket], [], [])
            if self.socket in ready_fds[0]:
                conn, addr = self.socket.accept()
                self.client_registrar.register_client(conn, addr)
            if event.mainloop.child_thread_control_socket in ready_fds[0]:
                print 'exiting', self.name
                break
        self.client_registrar.close_all()
        self.socket.close()

    def send_to_clients(self, msg):
        self.client_registrar.send_to_clients(msg.packetize())
