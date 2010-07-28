import os
import sys
import re
import select
import signal

import base_thread
import event
import dbus_message

class DbusMonitorMonitor(base_thread.BaseThread):
    def __init__(self, description='default-bus', *dbus_monitor_args):
        base_thread.BaseThread.__init__(self, 'DbusMonitorMonitor_thread[%s]' % description)
        dbus_monitor_args = list(dbus_monitor_args)
        dbus_monitor_args.insert(0, '/usr/bin/dbus-monitor')
        self.dbus_monitor_args = dbus_monitor_args

    def run(self):
        fd_r, fd_w = os.pipe()
        child_pid = os.fork()
        if child_pid == 0:
            # Child process: exec dbus-monitor and pipe output to parent
            os.close(fd_r)
            os.dup2(fd_w, sys.stdout.fileno())
            os.execv(self.dbus_monitor_args[0], self.dbus_monitor_args)
        else:
            # Parent process: Read from the dbus-monitor pipe and parse dbus messages.
            os.close(fd_w)
            dbm_file = os.fdopen(fd_r)
            while True:
                ready_fds = select.select([fd_r, event.mainloop.child_thread_control_socket], [], [])
                if fd_r in ready_fds[0]:
                    line = dbm_file.readline().rstrip()
                    if line:
                        msg = dbus_message.parse(line)
                        print 'line:', line
                        if msg:
                            print 'message:', msg
                            event.mainloop.add_event(event.Event(self.name, 'dbus-message-received', msg))
                if event.mainloop.child_thread_control_socket in ready_fds[0]:
                    print 'exiting', self.name
                    break
            try:
                os.kill(child_pid, signal.SIGINT)
                os.wait()
            except OSError as e:
                print 'Error when killing dbus-monitor process from ' + self.name + ':', e
