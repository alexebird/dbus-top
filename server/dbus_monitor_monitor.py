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
        if not self.__start_server(): return
        while self.should_run:
            try:
                line = self.read_dbm_line()
                msg = lh.handle_line(line)
                if msg:
                    msg.print_msg()
                    self.__send_msg_to_server(msg)
            except IOError as ioe:
                pass
                #print 'IOError occured while reading from dbus-monitor'
        self.__stop_server()
        print 'Ending dbus-monitor monitoring.'

    def read_dbm_line(self):
        return self.dbm_file.readline().rstrip()

    def stop(self):
        self.should_run = False

    #                                            #
    # Private methods for dbustop server control #
    #                                            #

    def __start_server(self):
        if self.db_server:
            try:
                self.db_server.listen()
            except socket.error as e:
                if e[0] == errno.EADDRINUSE:
                    print 'Address is in use.'
                    return False
            self.db_server.start()
        return True

    def __send_msg_to_server(self, msg):
        if self.db_server:
            self.db_server.send_to_clients(msg)

    def __stop_server(self):
        if self.db_server:
            self.db_server.stop()
            self.db_server.join()
