#!/usr/bin/python

# Echo client program
import sys
import socket
import signal
import select
import dbus_message
import pickle

#run = True

#def handler(signum, frame):
    #print 'Signal handler called with signal', signum
    #run = False

## Set the signal handler and a 5-second alarm
#signal.signal(signal.SIGINT, handler)
#signal.siginterrupt(signal.SIGINT, False)

if len(sys.argv) != 2:
    print 'Usage...'
    exit(1)

argport = int(sys.argv[1])

HOST = 'localhost'    # The remote host
PORT = argport          # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.setblocking(0)
#s.send(sys.argv[1])
while 1:
    rv = select.select([s], [], [], 0.2)
    if len(rv[0]) > 0:
        data = s.recv(4096 * 100)
        if data != 'registered':
            msg = pickle.loads(data)
            print msg
print 'sending close'
s.send('CLOSE')
s.close()

class DBusClient:
    def __init__(self):
        pass
