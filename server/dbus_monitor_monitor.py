import os
import line_handler

class DbusMonitorMonitor:
    def __init__(self, dbusmonitor_fd):
        #self.dbusmonitor_fd = dbusmonitor_fd
        self.dbm_file = os.fdopen(dbusmonitor_fd)
        self.should_run = True

    def set_server(self, server):
        self.db_server = server

    def run(self):
        lh = line_handler.LineHandler()
        #self.db_server.start()
        while self.should_run:
            try:
                line = self.read_dbm_line()
                msg = lh.handle_line(line)
                if msg:
                    msg.print_msg()
                    #self.db_server.send_to_clients(msg)
            except IOError as ioe:
                pass
        print 'Ending dbus-monitor monitoring.'
        #self.db_server.stop()
        #self.db_server.join()

    def read_dbm_line(self):
        return self.dbm_file.readline().rstrip()

    def stop(self):
        self.should_run = False
