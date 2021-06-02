from tkinter import *
from botnet_server import *
from utils import *
from PIL import Image
import threading
import socket

root = Tk()
root.title('SERVER')
root.geometry("500x300")

# Keep track of the button state on/off
#global is_on
server = None
server_process = None
is_on = False

# Create Label
my_label = Label(root, 
	text="The Switch Is Off!", 
	fg="gray", 
	font=("Helvetica", 32))
my_label.pack(pady=20)


# Define our switch function
def switch():
	# Determine is on or off
	global is_on
	global server
	global server_process
	if is_on:
		on_button.config(image=off)
		my_label.config(text="The Switch is Off", fg="grey")
		if server and not server_process.is_stopped():
			server_process.stop()
			server = None
		is_on = False
	else:
		on_button.config(image=on)
		my_label.config(text="The Switch is On", fg="green")
		is_on = True
		server = botnet_server(host = get_host_ip())
		server_process = stoppabe_thread(target = server.run_server, daemon = True)
		server_process.start()

def get_host_ip():
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	return local_ip

# Define Our Images
on = PhotoImage(file='images/on.png')
off = PhotoImage(file='images/off.png')

# Create A Button
on_button = Button(root, image=off, bd=0, command=switch)
on_button.pack(pady=50)

root.mainloop()
