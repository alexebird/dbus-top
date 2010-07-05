import select
import socket

from dbustop.common.base_thread import BaseThread
from dbustop.common.event.event_queue import EventQueue

class EventLoop(BaseThread):
    def __init__(self):
        BaseThread.__init__(self, 'EventLoop_thread')
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

loop = EventLoop()
