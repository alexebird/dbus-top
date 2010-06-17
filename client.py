#!/usr/bin/python

# Echo client program
import sys
import socket

if len(sys.argv) != 2:
    print 'Usage...'
    exit(1)

HOST = 'localhost'    # The remote host
PORT = 50007          # The same port as used by the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.send(sys.argv[1])
while 1:
    data = s.recv(4096)
    if data:
        print data
s.close()
#print 'Received', repr(data)
