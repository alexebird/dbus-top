import os
import sys
import re
import select

from dbustop.common.base_thread import BaseThread
from dbustop.common.dbus_message import DbusMessage
from dbustop.common.event import event_loop
from dbustop.common.event.event import Event

class DbusMonitorMonitor(BaseThread):
    def __init__(self):
        BaseThread.__init__(self, 'DbusMonitorMonitor_thread')

    def run(self):
        fd_r, fd_w = os.pipe()

        if os.fork() == 0:
            # Child process: exec dbus-monitor and pipe output to parent
            os.close(fd_r)
            os.dup2(fd_w, sys.stdout.fileno())
            child_name = '/usr/bin/dbus-monitor'
            os.execl(child_name, child_name, '--session')
        else:
            # Parent process: Read from the dbus-monitor pipe and parse dbus messages.
            os.close(fd_w)
            dbm_file = os.fdopen(fd_r)

        while True:
            ready_fds = select.select([fd_r, event_loop.loop.child_thread_control_socket], [], [])
            if fd_r in ready_fds[0]:
                line = dbm_file.readline().rstrip()
                # Make sure the line doesn't start with spaces
                if re.match('^\S.*', line):
                    msg = DbusMessage(line)
                    print msg
                    event_loop.loop.add_event(Event(self.name, 'dbus-message-received', msg))
            if event_loop.loop.child_thread_control_socket in ready_fds[0]:
                print 'exiting', self.name
                break
