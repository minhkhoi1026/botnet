import socket

def host_to_str(host, port):
    return host + ":" + str(port)
    
BUF_SIZE = 256
class socket_adapter:
    def __init__(self, conn):
        self.conn = conn

    def settimeout(self, t):
        self.conn.settimeout(t)
    
    def close(self):
        self.conn.close()

    def recv(self):
        bsize = self.conn.recv(4)
        size = int.from_bytes(bsize, 'big')
        chunks = []
        while size > 0:
            chunk = self.conn.recv(min(size, BUF_SIZE))
            if chunk == b'':
                raise socket.error("Socket connection broken!")
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)
        
    def send(self, data):
        bsize = len(data).to_bytes(4, 'big')
        self.conn.sendall(bsize)
        self.conn.sendall(data)