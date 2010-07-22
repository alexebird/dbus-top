import socket
import select
import errno
import time
import urlparse
from BaseHTTPServer import BaseHTTPRequestHandler

import base_thread
import event
import dbus_helper

#class ClientRegistrar:
    #def __init__(self):
        #self.clients = []
        
    #def register_client(self, conn, addr):
        #conn.setblocking(0)  # set to non-blocking mode
        ##conn.send('registered')
        #self.clients.append((conn, addr))
        #print 'registered client:', addr

    #def remove_client(self, conn):
        #for c in self.clients:
            #if conn == c[0]:
                #self.clients.remove(c)
                #print 'removed client:', c[1]
                #break

    #def send_to_clients(self, data):
        #for c in self.clients:
            #conn, addr = c[0], c[1]
            #ready_fds = select.select([conn], [conn], [])
            #if conn in ready_fds[0]:
                #cmd = conn.recv(4096)
                #if cmd == 'CLOSE':
                    #print 'CLOSE received from ', addr
                #else:
                    #print 'unknown command: "%s"' % cmd
                #conn.close()
                #self.remove_client(conn)
            #if conn in ready_fds[1]:
                #print 'sending to:', addr, '(%d bytes)' % len(data)
                #try:
                    #conn.send(data)
                #except socket.error:
                    #conn.close()
                    #self.remove_client(conn)

    #def close_all(self):
        #for c in self.clients:
            #c[0].close()

class DbusHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = urlparse.parse_qs(urlparse.urlparse(self.path).query)
        resp = self.handle_query(query)
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(resp))
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        self.request.send(resp)

    def handle_query(self, query):
        command = query['cmd'][0]
        if command == 'register':
            pass
        elif command == 'list':
            bus = query['bus'][0]
            return dbus_helper.list_services(bus)
        elif command == 'update':
            pass
        elif command == 'close':
            pass

class DbustopServer(base_thread.BaseThread):
    def __init__(self, host='localhost', port=8080):
        base_thread.BaseThread.__init__(self, 'DbustopServer_thread')
        self.host = host
        self.port = port
        #self.client_registrar = ClientRegistrar()
        #def dbus_message_received_handler(event):
            #self.client_registrar.send_to_clients(event.data.packetize())
        #event.mainloop.register_event_callback('DbusMonitorMonitor_thread', 'dbus-message-received', dbus_message_received_handler)

    def bind_and_listen(self):
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
        print 'dbustop-server listening on %d' % self.port
        return True

    def run(self):
        while True:
            ready_fds = select.select([self.socket, event.mainloop.child_thread_control_socket], [], [])
            if self.socket in ready_fds[0]:
                request, client_addr = self.socket.accept()
                DbusHTTPRequestHandler(request, client_addr, None)
                request.close()
            if event.mainloop.child_thread_control_socket in ready_fds[0]:
                print 'exiting', self.name
                break
        self.socket.close()
