import os
import socket
import select
import errno
import time
import urlparse
import shutil
from BaseHTTPServer import BaseHTTPRequestHandler
from Queue import Queue

import base_thread
import event
import dbus_helper

class MessageQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        def message_arrived_handler(event):
            self.put(event.data)
        event.mainloop.register_event_callback('dbus-message-received', message_arrived_handler)

message_queue = MessageQueue()

class DbusHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urlparse.urlparse(self.path)
        path = parsed_url.path
        query = parsed_url.query
        print '<%s %s>' % (path, query)
        if path != '/ajax':
            self.do_file_GET(path)
        else:
            parsed_query = urlparse.parse_qs(query)
            resp = self.handle_query(parsed_query)
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Content-Length', len(resp))
            self.send_header('Cache-Control', 'no-cache')
            self.send_header('Last-Modified', self.date_time_string(time.time()))
            self.end_headers()
            self.request.send(resp)

    def do_file_GET(self, path):
        f = None
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open('web' + path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        ctype = self.get_ctype(path)
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        shutil.copyfileobj(f, self.wfile)
        f.close()

    def get_ctype(self, fname):
        if fname.endswith('html'):
            return 'text/html'
        elif fname.endswith('css'):
            return 'text/css'
        elif fname.endswith('js'):
            return 'application/x-javascript'
        else:
            return 'text/plain'

    def handle_query(self, query):
        command = query['cmd'][0]
        if command == 'list':
            bus = query['bus'][0]
            return dbus_helper.list_services(bus)
        elif command == 'msg':
            json_resp = []
            while not message_queue.empty():
                json_resp.append(message_queue.get().json_str())
            print 'sent %d messages' % len(json_resp)
            return '[' + ', '.join(json_resp) + ']'
        elif command == 'ping':
            return 'pong'

class DbustopServer(base_thread.BaseThread):
    def __init__(self, host='localhost', port=8080):
        base_thread.BaseThread.__init__(self, 'DbustopServer_thread')
        self.host = host
        self.port = port

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
