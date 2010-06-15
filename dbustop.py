#!/usr/bin/python

import sys
#sys.path.append('.')
#print sys.path
import os
import line_handler

fd_r, fd_w = os.pipe()

try:
    rv = os.fork()
except OSError:
    print 'OSError'
    exit(1)

if rv == 0:
    os.dup2(fd_w, sys.stdout.fileno())
    child_name = '/usr/bin/dbus-monitor'
    os.execl(child_name, child_name, '--session')
else:
    os.dup2(fd_r, sys.stdin.fileno())
    dbusmon_output = os.fdopen(fd_r)
    while True:
        line = dbusmon_output.readline().rstrip()
        msg = line_handler.LineHandler.handle_line(line)
        if msg:
            print '=============================='
            #msg.print_msg()
