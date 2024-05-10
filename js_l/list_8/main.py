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
from frames import MasterFrame, DetailsFrame

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
        self.master_frame.set_details_frame(self.details_frame)
        
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
            
        
        
app = HttpLogsApp()
app.mainloop()

