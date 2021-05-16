from tkinter import *
from tkinter import ttk
from tkinter import Text
from PIL import ImageTk,Image
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True

from botnet_client import *

class windowApp(object):

    def __init__(self, master,client):
        self.master = Toplevel(master)
        self.client=client
        self.master.geometry("480x430")
        self.master.title("listApp")
        self.master.resizable(width=False,height=False)
        # Add some style
        self.style = ttk.Style()
        move_up = Button(self.master, text="Kill",padx=30,pady=20,command=self.killApp)
        move_up.place(x=30,y=10)

        move_down = Button(self.master, text="See",padx=30,pady=20,command=self.seeApp)
        move_down.place(x=135,y=10)

        select_button = Button(self.master, text="Delete",padx=30,pady=20,command=self.deleteApp)
        select_button.place(x=240,y=10)

        update_button = Button(self.master, text="Start",padx=30,pady=20,command=self.startApp)
        update_button.place(x=355,y=10)
        #Pick a theme
        self.style.theme_use("default")
        # Configure our treeview colors

        self.style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )
        # Change selected color
        self.style.map('Treeview', 
            background=[('selected', 'blue')])

        # Create Treeview Frame
        self.tree_frame = Frame(self.master)
        self.tree_frame.pack(pady=80)

        # Treeview Scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        # Pack to the screen
        self.my_tree.pack()

        #Configure the scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("Name", "ID", "Thread Count")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Name", anchor=W, width=140)
        self.my_tree.column("ID", anchor=CENTER, width=100)
        self.my_tree.column("Thread Count", anchor=W, width=140)

        # Create Headings 
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Name", text="Name", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Thread Count", text="Thread Count", anchor=W)
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")
    def seeApp(self):
        self.deleteApp()

        data = self.client.get_list_app()
        count=0
        for record in data:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))

            count += 1

    def killApp(self):
        ### START CODE HERE ###
        self.master2 = Toplevel(self.master)
        self.master2.geometry('400x50')
        self.val = Entry(self.master2, width=43, borderwidth=5)
        self.val.place(x=5,y=10)
        self.buttonConfirm = Button(self.master2,text="Kill",padx=18,pady=5,command=self.killCF)
        self.buttonConfirm.place(x=290,y=5)
        ### END CODE HERE ###
        return
    def killCF(self):
    	e=self.val.get()

    	messagebox.showinfo("Notification",self.client.kill_app(e))

    def startCF(self):
    	e=self.val.get()
    	### START CODE HERE ###

    	### END CODE HERE ###
    	messagebox.showinfo("Notification",self.client.start_app(e))
    def startApp(self):
        ### START CODE HERE ###
        self.master2 = Toplevel(self.master)
        self.master2.geometry('400x50')
        self.val = Entry(self.master2, width=43, borderwidth=5)
        self.val.place(x=5,y=10)
        self.buttonConfirm = Button(self.master2,text="Start",padx=18,pady=5,command=self.startCF)
        self.buttonConfirm.place(x=290,y=5)
        ### END CODE HERE ###
        return
    def deleteApp(self):
        ### START CODE HERE ###
        for record in self.my_tree.get_children():
        	self.my_tree.delete(record)
        ### END CODE HERE ###
        return

class windowProcess(object):

    def __init__(self, master,client):
        self.master = Toplevel(master)
        self.client=client
        self.master.geometry("480x430")
        self.master.title("Process")
        self.master.resizable(width=False,height=False)
        # Add some style
        self.style = ttk.Style()
        move_up = Button(self.master, text="Kill",padx=30,pady=20,command=self.killPS)
        move_up.place(x=30,y=10)

        move_down = Button(self.master, text="See",padx=30,pady=20,command=self.seePS)
        move_down.place(x=135,y=10)

        select_button = Button(self.master, text="Delete",padx=30,pady=20,command=self.deletePS)
        select_button.place(x=240,y=10)

        update_button = Button(self.master, text="Start",padx=30,pady=20,command=self.startPS)
        update_button.place(x=355,y=10)
        #Pick a theme
        self.style.theme_use("default")
        # Configure our treeview colors

        self.style.configure("Treeview", 
            background="#D3D3D3",
            foreground="black",
            rowheight=25,
            fieldbackground="#D3D3D3"
            )
        # Change selected color
        self.style.map('Treeview', 
            background=[('selected', 'blue')])

        # Create Treeview Frame
        self.tree_frame = Frame(self.master)
        self.tree_frame.pack(pady=80)

        # Treeview Scrollbar
        self.tree_scroll = Scrollbar(self.tree_frame)
        self.tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(self.tree_frame, yscrollcommand=self.tree_scroll.set, selectmode="extended")
        # Pack to the screen
        self.my_tree.pack()

        #Configure the scrollbar
        self.tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("Name", "ID", "Thread Count")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("Name", anchor=W, width=140)
        self.my_tree.column("ID", anchor=CENTER, width=100)
        self.my_tree.column("Thread Count", anchor=W, width=140)

        # Create Headings 
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("Name", text="Name", anchor=W)
        self.my_tree.heading("ID", text="ID", anchor=CENTER)
        self.my_tree.heading("Thread Count", text="Thread Count", anchor=W)
        self.my_tree.tag_configure('oddrow', background="white")
        self.my_tree.tag_configure('evenrow', background="lightblue")
    def seePS(self):
        self.deletePS()
        data = self.client.get_list_process()
        count=0
        for record in data:
            if count % 2 == 0:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('evenrow',))
            else:
                self.my_tree.insert(parent='', index='end', iid=count, text="", values=(record[0], record[1], record[2]), tags=('oddrow',))

            count += 1
        ### START CODE HERE ###
        
        ### END CODE HERE ###
    def killPS(self):
        ### START CODE HERE ###
        self.master2 = Toplevel(self.master)
        self.master2.geometry('400x50')
        self.val = Entry(self.master2, width=43, borderwidth=5)
        self.val.place(x=5,y=10)
        self.buttonConfirm = Button(self.master2,text="Kill",padx=18,pady=5,command=self.killCF)
        self.buttonConfirm.place(x=290,y=5)
        ### END CODE HERE ###
        return
    def killCF(self):
    	e=self.val.get()

    	self.master2.quit()
    	messagebox.showinfo("Notification",self.client.kill_process(e))

    def startCF(self):
    	e=self.val.get()
    	### START CODE HERE ###

    	### END CODE HERE ###
    	self.master2.quit()
    	messagebox.showinfo("Notification",self.client.start_process(e))
    def startPS(self):
        ### START CODE HERE ###
        self.master2 = Toplevel(self.master)
        self.master2.geometry('400x50')
        self.val = Entry(self.master2, width=43, borderwidth=5)
        self.val.place(x=5,y=10)
        self.buttonConfirm = Button(self.master2,text="Start",padx=18,pady=5,command=self.startCF)
        self.buttonConfirm.place(x=290,y=5)
        ### END CODE HERE ###
        return
    def deletePS(self):
        ### START CODE HERE ###
        for record in self.my_tree.get_children():
        	self.my_tree.delete(record)
        ### END CODE HERE ###
        return

class windowKey(object):
    def __init__(self, master,client):
        self.master = Toplevel(master)
        self.client=client
        self.master.geometry("480x430")
        self.master.title("Keystroke")
        self.master.resizable(width=False,height=False)
        # Add some style
        move_up = Button(self.master, text="Hook",padx=30,pady=20,command=self.Hook)
        move_up.place(x=30,y=10)

        move_down = Button(self.master, text="Unhook",padx=30,pady=20,command=self.unHook)
        move_down.place(x=130,y=10)

        select_button = Button(self.master, text="Print key",padx=30,pady=20,command=self.Print)
        select_button.place(x=245,y=10)

        update_button = Button(self.master, text="Delete",padx=30,pady=20,command=self.delete)
        update_button.place(x=365,y=10)
        #Pick a theme
        self.Key = Text(self.master, height=18, width=40)
        self.Key.place(x=80,y=100)
        self.Key.configure(state='disabled')
        

    def Hook(self):
        ### START CODE HERE ###
        self.client.hook_key()
        ### END CODE HERE ###
        return
    def unHook(self):
        ### START CODE HERE ###
        self.client.unhook_key()
        ### END CODE HERE ###
        return
    def Print(self):
        string=self.client.get_key_log()
        ### START CODE HERE ###
        self.Key.configure(state="normal")
        # self.Key.delete("1.0", END)
        self.Key.insert(END,string)
        self.Key.configure(state="disabled")
        ### END CODE HERE ###
        return
    def delete(self):
        ### START CODE HERE ###
        self.Key.configure(state="normal")
        self.Key.delete("1.0", END)
        self.Key.configure(state="disabled")
        ### END CODE HERE ###
        return

class windowReg(object):
    def __init__(self, master,client):
        self.master = Toplevel(master)
        self.client=client
        self.master.geometry("450x550")
        #self.master.resizable(width=False,height=False)

        self.pathFile = StringVar()
        self.pathFile.set('Path...')

        self.textfilename = Entry(self.master,textvariable=self.pathFile, state=DISABLED,width=50, borderwidth=5)
        self.textfilename.place(x=5,y=10)
        self.my_btn = Button(self.master, text="Browser...", command=self.open)
        self.my_btn.place(x=320,y=8)
        self.my_frame1 = Frame(self.master)
        self.my_scrollbar = Scrollbar(self.my_frame1, orient=VERTICAL)
        self.my_text = Text(self.my_frame1, width=50, yscrollcommand=self.my_scrollbar.set)
        self.my_scrollbar.config(command=self.my_text.yview)
        self.my_scrollbar.pack(side=RIGHT, fill=Y)
        self.my_frame1.place(x=10,y=50,width=300,height=150)
        self.my_text.pack(pady=15)
        self.buttonSend = Button(self.master,text="Send",padx=40,pady=50,command=self.Send1)
        self.buttonSend.place(x=320,y=60)

        self.my_frame2 = LabelFrame(self.master, text='Edit value directly',padx=20, pady=20)
        self.my_frame2.place(x=14,y=200)
        self.options = [
        "Get value", 
        "Set value", 
        "Delete value", 
        "Create key", 
        "Delete key"]

        self.dataType = [
        "String", 
        "Binary", 
        "DWORD", 
        "QWORD", 
        "Muti-string",
        "Expandabie String"
        ]
        self.choose = StringVar()
        self.choose.set("Select option")
        self.type = StringVar()
        self.type.set('Data type')
        self.drop1 = OptionMenu(self.my_frame2, self.choose, *self.options,command=self.option)
        self.drop2 = OptionMenu(self.my_frame2, self.type, *self.dataType)
        #print(clicked.get()) 
        self.pathSV=StringVar()
        self.pathSV.set('Path')
        self.NvalueSV=StringVar()
        self.NvalueSV.set('Name value')
        self.valueSV=StringVar()
        self.valueSV.set('value')
        self.path=Entry(self.my_frame2,textvariable=self.pathSV)
        self.Nvalue=Entry(self.my_frame2,textvariable=self.NvalueSV)
        self.Value=Entry(self.my_frame2,textvariable=self.valueSV)
        self.TEXT = Text(self.my_frame2,state='disabled', height=8, width=40)
        self.space=Label(self.my_frame2)
        self.drop1.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.path.grid(row=1, column=0, columnspan=3, sticky="nsew")
        self.Nvalue.grid(row=2, column=0, sticky="nsew")
        self.Value.grid(row=2, column=1, sticky="nsew")
        self.drop2.grid(row=2, column=2, sticky="nsew")
        self.space.grid(row=3, column=0)    
        self.TEXT.grid(row=4, column=0, columnspan=3)   
        self.buttonSend2 = Button(self.master,text="Send",command=self.Send2)   
        self.buttonSend2.place(x=100,y=500)
        self.buttonDelete = Button(self.master,text="Delete",command=self.Delete)   
        self.buttonDelete.place(x=250,y=500)  

    def option(self,ch):
        if ch in self.options[0:3:2]:
        	self.drop1.grid(row=0, column=0, columnspan=3, sticky="nsew")
        	self.path.grid(row=1, column=0, columnspan=3, sticky="nsew")
        	self.Nvalue.grid(row=2, column=0, sticky="nsew")
        	self.Value.grid(row=2, column=1, sticky="nsew")
        	self.drop2.grid(row=2, column=2, sticky="nsew")    	
        	self.space.grid(row=3, column=0)    	
        	self.TEXT.grid(row=4, column=0, columnspan=3)
        	self.drop2.grid_forget()
        	self.Value.grid_forget()
        elif ch == self.options[1]:
        	self.drop1.grid(row=0, column=0, columnspan=3, sticky="nsew")
        	self.path.grid(row=1, column=0, columnspan=3, sticky="nsew")
        	self.Nvalue.grid(row=2, column=0, sticky="nsew")
        	self.Value.grid(row=2, column=1, sticky="nsew")
        	self.drop2.grid(row=2, column=2, sticky="nsew")    	
        	self.space.grid(row=3, column=0)    	
        	self.TEXT.grid(row=4, column=0, columnspan=3)
        elif ch == self.options[3]:
        	self.drop1.grid(row=0, column=0, columnspan=3, sticky="nsew")
        	self.path.grid(row=1, column=0, columnspan=3, sticky="nsew")
        	self.Nvalue.grid(row=2, column=0, sticky="nsew")
        	self.Value.grid(row=2, column=1, sticky="nsew")
        	self.drop2.grid(row=2, column=2, sticky="nsew")    	
        	self.space.grid(row=3, column=0)    	
        	self.TEXT.grid(row=4, column=0, columnspan=3)
        	self.drop2.grid_forget()
        	self.Value.grid_forget()
        else:
            self.drop1.grid(row=0, column=0, columnspan=3, sticky="nsew")
            self.path.grid(row=1, column=0, columnspan=3, sticky="nsew")
            self.Nvalue.grid(row=2, column=0, sticky="nsew")
            self.Value.grid(row=2, column=1, sticky="nsew")
            self.drop2.grid(row=2, column=2, sticky="nsew")     
            self.space.grid(row=3, column=0)        
            self.TEXT.grid(row=4, column=0, columnspan=3)
            self.Nvalue.grid_forget()
            self.drop2.grid_forget()
            self.Value.grid_forget()

    def standardized(self, s):
        if s=='':
            return 'None'
        return s

    def open(self):
    	text_file = filedialog.askopenfilename(title="Open File", filetypes=(("REG Files", "*.reg"),("All Files", "*.*")))
    	file = open(text_file, 'r')
    	stuff = file.read()
    	self.my_text.delete("1.0", END)
    	self.my_text.insert(END, stuff)
    	self.pathFile.set(text_file)
    	self.textfilename.config(textvariable=self.pathFile)
    	self.my_text
    	file.close()
    def Send1(self):
        messagebox.showinfo("Notification",self.client.send_reg_text(self.my_text.get("1.0","end")))
        return
    def Send2(self):
        cmd=''
        T=''
        if self.choose.get()== self.options[0]:
            cmd="GETVAL"
        elif self.choose.get()== self.options[1]:
            cmd="SETVAL"
        elif self.choose.get()== self.options[2]:
            cmd="DELVAL"
        elif self.choose.get()== self.options[3]:
            cmd="CREKEY"
        elif self.choose.get()== self.options[4]:
            cmd="DELKEY"
        # type of data
        if self.type.get()== self.dataType[0]:
            T="REG_SZ"
        elif self.type.get()== self.dataType[1]:
            T="REG_BINARY"
        elif self.type.get()== self.dataType[2]:
            T="REG_DWORD"
        elif self.type.get()== self.dataType[3]:
            T = "REG_QWORD"
        elif self.type.get()== self.dataType[4]:
            T="REG_MULTI_SZ"
        elif self.type.get()== self.dataType[5]:
            T="REG_EXPAND_SZ"

        S=self.client.send_reg_cmd(self.standardized(cmd),
            self.standardized(self.pathSV.get()),
            self.standardized(self.NvalueSV.get()),
            self.standardized(self.valueSV.get()),
            self.standardized(T))
        self.Print(S)

    def Print(self,S):
        string=S
        ### START CODE HERE ###
        self.TEXT.configure(state="normal")
        self.TEXT.insert(END,string)
        self.TEXT.configure(state="disabled")
        ### END CODE HERE ###
        return
    def Delete(self):
        self.TEXT.configure(state="normal")
        self.TEXT.delete("1.0", END)
        self.TEXT.configure(state="disabled")
        return

class windowCap(object):
    def __init__(self, master,client):
        self.master = Toplevel(master)
        self.client=client
        self.master.geometry("500x300")
        self.image = self.client.get_screenshot()
        temp=self.image.resize((350, 250), Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(temp)
        self.my_label = Label(self.master,image=self.my_img)
        self.my_label.place(x=10,y=10)

        self.buttonShutdown = Button(self.master,text="Capture", command=self.cap,padx=20,pady=30)
        self.buttonShutdown.place(x=400,y=20)

        self.buttonCap = Button(self.master,text="Save", command=self.save,padx=30,pady=30)
        self.buttonCap.place(x=400,y=150)

    def save(self):
    	file = filedialog.asksaveasfile(mode='wb', defaultextension=".png", filetypes=(("PNG file", "*.png"),("All Files", "*.*") ))
    	if file:
    		self.image.save(file) # saves the image to the input file name. 

    def cap(self):
        self.image = self.client.get_screenshot()
        temp=self.image.resize((350, 250), Image.ANTIALIAS)
        self.my_img = ImageTk.PhotoImage(temp)
        self.my_label = Label(self.master,image=self.my_img)
        self.my_label.place(x=10,y=10)
        return

class windowMain(object):

    def __init__(self, master):
        self.master = master
        self.master.title("Client")
        self.master.geometry("430x350")
        self.client=botnet_client()
        self.master.resizable(width=False,height=False)

        self.val_id = StringVar()
        self.val_id.set('Enter IP')
        self.ip = Entry(self.master, width=50, borderwidth=5,textvariable=self.val_id)
        self.ip.place(x=5,y=10)

        self.buttonConnect = Button(self.master,text="Connect",padx=18,pady=5, command=self.Button_Connect)
        self.buttonConnect.place(x=330,y=5)

        self.buttonProcess = Button(self.master,text="Process\nRunning", command=self.Button_Process,padx=25,pady=130)
        self.buttonProcess.place(x=5,y=50)

        self.buttonApp = Button(self.master,text="App Running", command=self.Button_App,padx=60,pady=30)
        self.buttonApp.place(x=120,y=50)

        self.buttonShutdown = Button(self.master,text="Shutdown", command=self.Button_Shutdown,padx=10,pady=38)
        self.buttonShutdown.place(x=120,y=150)

        self.buttonCap = Button(self.master,text="Screen\ncapture", command=self.Button_Cap,padx=25,pady=30)
        self.buttonCap.place(x=220,y=150)

        self.buttonRegistry = Button(self.master,text="Registry", command=self.Button_Registry,padx=75,pady=30)
        self.buttonRegistry.place(x=120,y=260)

        self.buttonKey = Button(self.master,text="Keystroke", command=self.Button_Key,padx=15,pady=87)
        self.buttonKey.place(x=330,y=50)

        self.buttonQuit = Button(self.master,text="Quit", command=self.Button_Quit,padx=29,pady=30)
        self.buttonQuit.place(x=330,y=260)

    def Button_Connect(self):

        ### START CODE HERE ###
        self.client.set(self.ip.get())
        messagebox.showinfo("Notification",self.client.connect())
        ### END CODE HERE ###
        return
    def Button_Process(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        WP=windowProcess(self.master,self.client)
        self.master.wait_window(WP.master)
        ### END CODE HERE ###
        return
    def Button_App(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        WA=windowApp(self.master,self.client)
        self.master.wait_window(WA.master)
        ### END CODE HERE ###
        return
    def Button_Shutdown(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        self.client.shutdown()
        ### END CODE HERE ###
        return
    def Button_Cap(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        WC=windowCap(self.master,self.client)
        self.master.wait_window(WC.master)
        ### END CODE HERE ###
        return
    def Button_Key(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        WK=windowKey(self.master,self.client)
        self.master.wait_window(WK.master)
        ### END CODE HERE ###
        return
    def Button_Registry(self):
        if self.client.nr==None:
            messagebox.showinfo("Notification","Not connected to the server yet")
            return
        ### START CODE HERE ###
        WR=windowReg(self.master,self.client)
        self.master.wait_window(WR.master)
        ### END CODE HERE ###
        return
    def Button_Quit(self):
        ### START CODE HERE ###
        self.client.close_connect()
        self.master.quit()
        ### END CODE HERE ###
        return



if __name__ == "__main__":
    root = Tk()
    wd = windowMain(root)
    root.mainloop()