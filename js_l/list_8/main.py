import customtkinter as ctk
import customtkinter
import customtkinter
from CTkListbox import *
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import os
from typing import Optional
customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

# app = customtkinter.CTk()  # create CTk window like you do with the Tk window

# app.grid_columnconfigure(0, weight=1)
# app.grid_columnconfigure(1, weight=3)

# https_logs_label = customtkinter.CTkLabel(master=app, text="http log file")
# https_logs_label.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = customtkinter.W)
# c =  customtkinter.CTkEntry(master=app)
# c.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = customtkinter.NSEW)


# def button_function():
#     print("button pressed")
#     if os.path.exists(c.get()):
#         print("File exists")
#     else:
#         print("File does not exist")

# button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_function)
# # button.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)
# button.grid(row = 0, column = 2, padx = 10, pady = 10, sticky = "ew")

# # Use CTkButton instead of tkinter Button


# app.mainloop()

class HttpLogsApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("HTTP logs app") # useless with i3 wm
        self.geometry("1200x700") # useless with i3 wm
        
        self.file : Optional[str] = None
        
        self.entry_log = ctk.CTkEntry(master=self)
        
        
        https_logs_label = customtkinter.CTkLabel(master=self, text="HTTP log browser", font=("Arial", 25) )
        https_logs_label.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "w")
        
        
        self.button_open = ctk.CTkButton(master=self, text="Open", command=self.open_file)
        
        self.entry_log.grid(row = 0, column = 1,columnspan=5, padx = 20, pady = 20, sticky = "ew")
        self.button_open.grid(row = 0, column = 7, padx = 10, pady = 10, sticky = "e")
        
        self.master_frame = MasterFrame(self)
        self.master_frame.grid(row = 1, column = 0, columnspan=4, padx = 20, pady = 20, sticky = "ew")
        
        self.details_frame = DetailsFrame(self)
        self.details_frame.grid(row = 1, column = 5, columnspan=4, pady = 20, padx=20)
        
        self.button_prev = ctk.CTkButton(master=self, text="Prev", command=self.prev_log)
        self.button_next = ctk.CTkButton(master=self, text="Next", command=self.next_log)
        self.button_quit = ctk.CTkButton(master=self, text="Quit", command=self.quit)
        
        self.button_quit.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "w")
        
        self.button_prev.grid(row = 2, column = 7, padx = 10, pady = 10, sticky = "ew")
        self.button_next.grid(row = 2, column = 8, padx = 10, pady = 10, sticky = "ew")
        
    def next_log(self):
        print("next log")
    
    def prev_log(self):
        print("prev log")
    
    def quit(self):
        sys.exit(0)
        
    def open_file(self):
        http_file = self.entry_log.get()
        if os.path.exists(http_file) and os.path.isfile(http_file):
            self.file = http_file
            print(f"File opened: {self.file}")
        else: 
            print(f"File does not exist: {http_file}")
            
class MasterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_from = customtkinter.CTkLabel(self, text = "From")
        self.label_from.grid(row=0, column=0, pady = 20 ,padx=20)
        
        self.entry_date_from = ctk.CTkEntry(self)
        self.entry_date_from.grid(row = 0, column = 1, pady = 20, padx=20)
        
        
        self.label_to = customtkinter.CTkLabel(self,text = "To")
        self.label_to.grid(row=0, column=2, pady = 20 ,padx=20)

        self.entry_date_to = ctk.CTkEntry(self)
        self.entry_date_to.grid(row = 0, column = 3, pady = 20, padx=20)
        
        # self.textbox_logs = ctk.CTkTextbox(self)
        # self.textbox_logs.grid(row = 1, column = 0, columnspan=4, pady = 20, padx=20)
        # self.textbox_logs_scroll = ctk.CTkScrollbar(self, command=self.textbox_logs.yview)
        # self.textbox_logs_scroll.grid(row = 1, column = 4, sticky="ns")
        
        items = tk.StringVar()
        items.set([1,2,3,4,132213312132312132312132312312,1,1,1,1,1,1,1,1,1,1,1,1,1])
        
        list_frame = ctk.CTkFrame(self)
        
        scroll = ttk.Scrollbar(list_frame, orient="vertical")
        scroll.grid(row = 0, column = 4, sticky="ns")
        listbox = tk.Listbox(master=list_frame, listvariable=items,yscrollcommand=scroll.set, width=70, height=15)
        scroll.config(command=listbox.yview)
        list_frame.grid(row = 1, column = 0, sticky="NSEW", columnspan=4)
        
        listbox.grid(row = 0, column = 0, columnspan=1, sticky="NSEW")
        
class DetailsFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Remote host
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Remote host")
        self.label_remote_host.grid(row=0, column=0, pady = 20 ,padx=20, columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("localhost")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 0, column = 1, pady = 20, padx=20, columnspan=1)
        
        # Date
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Date")
        self.label_remote_host.grid(row=1, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("12.12.2021")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 1, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Time
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Time")
        self.label_remote_host.grid(row=2, column=0, pady = 20 ,padx=20,columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("21:37:69")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 2, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Timezone
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Timezone")
        self.label_remote_host.grid(row=2, column=2, pady = 20 ,padx=20,columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("21:37:69")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 2, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Status code
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Code")
        self.label_remote_host.grid(row=3, column=0, pady = 20 ,padx=20,columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("420")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 3, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Method
        
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Method")
        self.label_remote_host.grid(row=3, column=2, pady = 20 ,padx=20,columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("GET")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 3, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Resource
        
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Resource")
        self.label_remote_host.grid(row=4, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set("/home/sliwek/tmp/tmp/tmp")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 4, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Size
        
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Size")
        self.label_remote_host.grid(row=5, column=0, pady = 20 ,padx=20,columnspan=1)
        
        stringVar_localhost = tk.StringVar()
        stringVar_localhost.set(f"{2134} bytes")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=stringVar_localhost)
        self.entry_remote_host.grid(row = 5, column = 1, pady = 20, padx=20,columnspan=1)
        
        
        
app = HttpLogsApp()
app.mainloop()

