#!/usr/bin/python

import sys
import os
import re
from dbus_message import *

class LineHandler:
    current_message = None

    @staticmethod
    def handle_line(line):
        if re.match('^\s{3,}\S+.*', line):
            if LineHandler.current_message:
                LineHandler.current_message.add_line(line)
        else:
            complete_msg = LineHandler.current_message
            LineHandler.current_message = DbusMessage(line)
            return complete_msg

fd_r, fd_w = os.pipe()

try:
    rv = os.fork()
except OSError:
    print 'OSError'
    exit(1)

if rv == 0:
    print 'child pid: %s' % os.getpid()
    os.dup2(fd_w, sys.stdout.fileno())
    child_name = '/usr/bin/dbus-monitor'
    os.execl(child_name, child_name, '--session')
else:
    print 'parent pid: %s' % os.getpid()
    os.dup2(fd_r, sys.stdin.fileno())
    dbusmon_output = os.fdopen(fd_r)
    while True:
        line = dbusmon_output.readline().rstrip()
        msg = LineHandler.handle_line(line)
        if msg:
            msg.print_msg()
            print '=============================='
