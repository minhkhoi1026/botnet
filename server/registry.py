from winreg import *

class registry:
    def __init__(self, path = None):
        self.key = self.get_reg_key(path)
        
    def __del__(self):
        CloseKey(self.key)
        
    def get_reg_key(self, path):
        try:
            tokens = path.split('\\')
            key =  eval(tokens[0])
            subkey = ''
            if (len(tokens) > 0): subkey = '\\'.join(tokens[1:])
            return OpenKeyEx(key, subkey, 0, KEY_ALL_ACCESS)
        except:
            return None

    def get_value(self, value_name):
        reg_val, reg_type = QueryValueEx(self.key, value_name)
        val = ''
        if (reg_type == REG_MULTI_SZ):
            val = '\n'.join(reg_val)
        elif (reg_type == REG_BINARY):
            for x in reg_val:
                val += str(x) + " "
        else:
            val = str(reg_val)
        return val

    def set_value(self, val_name, val_type, val):
        # change val_type from string to constant macro
        val_type = eval(val_type)
        print(val_type)
        # BINARY case
        if (val_type == REG_BINARY):
            tokens = val.split(' ')
            val = ''
            for token in tokens:
                if (token == ''):
                    continue
                if (not token.isnumeric()) or (int(token) > 127):
                    raise RuntimeError
                val += chr(int(token))
            val = bytes(val, encoding = "ascii")
        # DWORD and QWORD case, other case do nothing
        elif (val_type == REG_DWORD or val_type == REG_QWORD):
            val = int(val)
        elif (val_type == REG_MULTI_SZ):
            val = val.split('\\r\\n')
        print(val)
        # set value
        SetValueEx(self.key, val_name, 0, val_type, val)

    def delete_value(self, val_name):
        DeleteValue(self.key, val_name)

    def create_key(self, subkey):
        CreateKey(self.key, subkey)

    def delete_key(self, subkey):
        DeleteKeyEx(self.key,subkey)
        