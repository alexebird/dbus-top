print 'IMPORTING:', __name__
import time
import select
import socket
from Queue import Queue

import base_thread

class Event:
    def __init__(self, origin, type, data):
        self.timestamp = time.time()
        self.origin = origin
        self.type = type
        self.data = data

    def __repr__(self):
        return '<Event: origin=%s, type=%s, data=%s>' % (self.origin, self.type, self.data.__class__)


class EventLoop(base_thread.BaseThread):
    def __init__(self):
        base_thread.BaseThread.__init__(self, 'EventLoop_thread')
        self.event_queue = EventQueue()
        # Sockets used to signal child threads to shutdown.
        self.my_child_thread_ctrl_sock, self.child_thread_control_socket = socket.socketpair()
        self.event_callback_dict = {}

    def run(self):
        while True:
            ready_fds = select.select([self.event_queue.queue_updated_sock], [], [])
            # Something has been put into the event queue
            if self.event_queue.queue_updated_sock in ready_fds[0]:
                self.event_queue.queue_updated_sock.recv(1)  # Clear the socket
                event = self.event_queue.get()
                if event.type == 'shutdown':
                    self.my_child_thread_ctrl_sock.send('\0')
                    break
                else:
                    key = (event.origin, event.type)
                    try:
                        callback_list = self.event_callback_dict[key]
                        for c in callback_list:
                            c(event)
                    except KeyError:
                        pass  # Don't care if the event doesn't have any registered callbacks.

    def add_event(self, new_event):
        self.event_queue.put(new_event)

    def register_event_callback(self, origin, type, callback):
        if origin == '':
            origin = None
        key = (origin, type)
        callback_list = None
        try:
            callback_list = self.event_callback_dict[key]
        except KeyError:
            self.event_callback_dict[key] = callback_list = []
        callback_list.append(callback)

class EventQueue(Queue):
    def __init__(self):
        Queue.__init__(self)
        self.event_q_sock, other_sock = socket.socketpair()
        self.queue_updated_sock = other_sock
    
    def put(self, item):
        Queue.put(self, item)
        self.event_q_sock.send('\0')

def add_event(new_event):
    __event_queue.put(new_event)

def next_event():
    try:
        return __event_queue.get(True, 0.1)
    except Queue.Empty:
        return None

__event_queue = Queue()
mainloop = EventLoop()
