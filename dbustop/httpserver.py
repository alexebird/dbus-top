from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import time

class DbusHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        resp = 'hi'
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Content-Length', len(resp))
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        self.request.send(resp)
