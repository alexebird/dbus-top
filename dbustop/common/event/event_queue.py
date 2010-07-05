import socket
from Queue import Queue

class EventQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        self.event_q_sock, other_sock = socket.socketpair()
        self.queue_updated_sock = other_sock
    
    def put(self, item):
        Queue.put(self, item)
        self.event_q_sock.send('\0')
