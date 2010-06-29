import os, socket, errno
from line_handler import LineHandler

class DbusMonitorMonitor:
    def __init__(self, dbusmonitor_fd):
        self.dbm_file = os.fdopen(dbusmonitor_fd)
        self.should_run = True

    def set_server(self, server):
        self.db_server = server

    def run(self):
        lh = LineHandler()
        if not self.db_server.listen(): return
        self.db_server.start()
        while self.should_run:
            try:
                line = self.read_dbm_line()
                msg = lh.handle_line(line)
                if msg:
                    print msg.to_string()
                    self.db_server.send_to_clients(msg)
            except IOError as ioe:
                #pass  # Don't care about missing dbus-monitor output.
                print 'IOError occured while reading from dbus-monitor'
        self.db_server.shutdown()
        print 'Ending dbus-monitor monitoring.'

    def read_dbm_line(self):
        return self.dbm_file.readline().rstrip()

    def stop(self):
        self.should_run = False
