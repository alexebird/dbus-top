import socket
import select

class ClientRegistrar:
    def __init__(self):
        self.clients = []
        
    def register_client(self, conn, addr):
        conn.setblocking(0)
        conn.send('registered')
        self.clients.append((conn, addr))
        print 'registered client:', addr

    def remove_client(self, conn):
        for c in self.clients:
            if conn == c[0]:
                self.clients.remove(c)
                print 'removed client:', c[1]
                break

    def send_to_clients(self, data):
        for c in self.clients:
            conn, addr = c[0], c[1]
            rv = select.select([conn], [conn], [], 0)
            if len(rv[0]) > 0:
                cmd = conn.recv(4096)
                if cmd == 'CLOSE':
                    print 'CLOSE received from ', addr
                else:
                    print 'unknown command: "%s"' % cmd
                conn.close()
                self.remove_client(conn)
            elif len(rv[1]) > 0:
                print 'sending to:', addr, '(%d bytes)' % len(data)
                conn.send(data)

    def close_all(self):
        for c in self.clients:
            c[0].close()
