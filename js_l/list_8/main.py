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

def open_file(file_name:str) -> list[str]:
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines
    
    

class HttpLogsApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.title("HTTP logs app") # useless with i3 wm
        self.geometry("1200x700") # useless with i3 wm
        
        self.file : Optional[str] = None
        
        
        self.entry_log = ctk.CTkEntry(master=self, textvariable=tk.StringVar(value="/home/sliwek/Programowanie/sem4/js_l/list_8/NASA"))
        
        
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
        self.button_prev.configure(state=tk.NORMAL)
        if self.master_frame.select_next():
            print("selected next")
            if self.master_frame.selected_last():
                self.button_next["state"] = tk.DISABLED
                self.button_next.configure(state=tk.DISABLED)
                print("xd")
        else:
            print("no more logs")
    
    def prev_log(self):
        self.button_next.configure(state=tk.NORMAL)
        if self.master_frame.select_prev():
            print("selected prev")
            if self.master_frame.selected_first():
                self.button_prev.configure(state=tk.DISABLED)
                
        else:
            print("no more logs")
    
    def quit(self):
        sys.exit(0)
        
    def open_file(self):
        http_file = self.entry_log.get()
        if os.path.exists(http_file) and os.path.isfile(http_file):
            self.file = http_file
            print(f"File opened: {self.file}")
            self.master_frame.set_file(self.file)
        else: 
            print(f"File does not exist: {http_file}")
            
class MasterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_from = customtkinter.CTkLabel(self, text = "From")
        self.label_from.grid(row=0, column=0, pady = 20 ,padx=20)
        
        self.entry_date_from = ctk.CTkEntry(self)
        self.entry_date_from.grid(row = 0, column = 1, pady = 20, padx=20)
        
        self.file : Optional[str] = None
            
        self.label_to = customtkinter.CTkLabel(self,text = "To")
        self.label_to.grid(row=0, column=2, pady = 20 ,padx=20)

        self.entry_date_to = ctk.CTkEntry(self)
        self.entry_date_to.grid(row = 0, column = 3, pady = 20, padx=20)
        
        self.sitems = tk.StringVar()
        # self.sitems.set([1,2,3,4,132213312132312132312132312312,1,1,1,1,1,1,1,1,1,1,1,1,1])
        
        list_frame = ctk.CTkFrame(self)
        
        self.scroll = ttk.Scrollbar(list_frame, orient="vertical")
        self.scroll.grid(row = 0, column = 4, sticky="ns")
        self.listbox = tk.Listbox(master=list_frame, listvariable=self.sitems,yscrollcommand=self.scroll.set, width=70, height=15,exportselection=0)
        self.scroll.config(command=self.listbox.yview)
        list_frame.grid(row = 1, column = 0, sticky="NSEW", columnspan=4)
        
        self.listbox.grid(row = 0, column = 0, columnspan=1, sticky="NSEW")
    
    def set_file(self, file:str):
        self.file = file
        print(f"File set: {self.file}")
        self.set_items(open_file(file))
    
    def set_items(self, items: list[str]):
        self.sitems.set(items)
    
    def select_next(self) -> bool:
        index =  self.listbox.index("active")
        if index is not None:
            self.listbox.selection_clear(index)
            self.listbox.activate(index + 1)
            self.listbox.selection_set(index + 1)
            self.listbox.see(index + 1)
            return True
            
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            return True
    
    def selected_last(self) -> bool:
        index =  self.listbox.index("active")
        
        if index is not None:
            if index == self.listbox.size()-1:
                return True
            return False
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return False
        
    def select_prev(self):
        index =  self.listbox.index("active")
        if index is not None:
            self.listbox.selection_clear(index)
            self.listbox.activate(index - 1)
            self.listbox.selection_set(index - 1)
            self.listbox.see(index - 1)
            return True
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            return True
        
    def selected_first(self) -> bool:
        index =  self.listbox.index("active")
        if index is not None:
            if index == 0:
                return True
            return False
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            return True
        
        
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

