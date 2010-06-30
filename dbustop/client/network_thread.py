import select
import socket
import pickle
import struct
from dbustop.common.base_thread import BaseThread
from dbustop.common import util
from dbustop.common import dbus_message
from dbustop.common.event.event import Event
#from dbustop.common.event.event_handler import EventHandler
from dbustop.common.event import event_handler

def create_dbustop_socket(host, port):
    dbustop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dbustop_sock.connect((host, port))
        dbustop_sock.setblocking(0)  # Set to non-blocking mode
    except socket.error as e:
        print e
        dbustop_sock.close()
        return None
    return dbustop_sock

class NetworkThread(BaseThread):
    def __init__(self, host, port):
        BaseThread.__init__(self, 'NetworkThread')
        self.host = host
        self.port = port

    def run(self):
        self.socket = create_dbustop_socket(self.host, self.port)
        if not self.socket: return
        while not self.shutdown_event.is_set():
            if util.ready_for_read(self.socket):
                msg = dbus_message.depacketize(self.socket)
                event_handler.add_event(Event(self.name, 'dbusmessage_received', msg))
        self.socket.close()
