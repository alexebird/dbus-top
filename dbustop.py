#!/usr/bin/python

import sys
import os
import line_handler
import dbus_server
import signal
import threading
import fcntl
import select

if len(sys.argv) != 2:
    print 'Usage...'
    exit(1)

def sigint_handler(signum, frame):
    global run_main_loop
    server.stop()
    run_main_loop = False
signal.signal(signal.SIGINT, sigint_handler)

argport = int(sys.argv[1])
fd_r, fd_w = os.pipe()
server_lock = threading.Lock()

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
    #fcntl.fcntl(fd_r, fcntl.F_SETFL, os.O_NONBLOCK)
    lh = line_handler.LineHandler()
    server = dbus_server.DbusServer(argport, server_lock)
    server.start()
    run_main_loop = True
    while run_main_loop == True:
        #rv = select.select([dbusmon_output], [], [], 0.1)
        #if len(rv[0]) > 1:
            #print 'selected'
        try:
            line = dbusmon_output.readline().rstrip()
            msg = lh.handle_line(line)
            if msg:
                msg.print_msg()
                server.send_to_clients(msg)
        except IOError as ioe:
            pass
    server.join()
    print 'exiting dbustop'
