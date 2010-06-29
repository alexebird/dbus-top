import socket

def create_dbustop_socket(host, port):
    dbustop_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        dbustop_sock.connect((host, port))
        dbustop_sock.setblocking(0)  # Set to non-blocking mode
    except socket.error as e:
        print e
        dbustop_sock.close()
        return None
    return dbustop_sock

class ClientConnection():
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = create_dbustop_socket(host, port)

    #def do_run(self):
        #self.socket = create_dbustop_socket(self.host, self.port)
        #if not self.socket: return
        #while self.should_run == True:
            #if util.ready_for_read(self.socket):
                #dmessage_length = self.read_packet_length()
                #if util.ready_for_read(self.socket):
                    #data = self.socket.recv(dmessage_length)
                    ##if data == 'registered':
                        ##print 'registered with %s:%d' % \
                            ##(self.connection_args[0], self.connection_args[1])
                    #if len(data) > 0:
                        #try:
                            #msg = pickle.loads(data)
                            #self.fire_event('message_received', msg)
                        #except IndexError:
                            ## Occurs when Pickle can't parse the message.
                            ##print 'pickle: oops'
                            #pass
        #self.send_close()
    
    #def send_close(self):
        #self.socket.send('CLOSE')
        #self.socket.close()
