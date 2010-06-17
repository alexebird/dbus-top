#!/usr/bin/python

import sys
import os
import line_handler
import dbus_server

if len(sys.argv) != 2:
    print 'Usage...'
    exit(1)

argport = int(sys.argv[1])

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
    lh = line_handler.LineHandler()
    server = dbus_server.DbusServer(argport)
    server.start()
    while True:
        line = dbusmon_output.readline().rstrip()
        msg = lh.handle_line(line)
        if msg:
            #print '=============================='
            #msg.print_msg()
            print 'got msg'
            server.send_to_clients(msg)
