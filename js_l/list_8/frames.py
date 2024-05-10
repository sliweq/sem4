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
from tmp import get_time_zone

def open_file(file_name:str) -> list[str]:
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines

class MasterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.label_from = customtkinter.CTkLabel(self, text = "From")
        self.label_from.grid(row=0, column=0, pady = 20 ,padx=20)
        
        self.entry_date_from = ctk.CTkEntry(self)
        self.entry_date_from.grid(row = 0, column = 1, pady = 20, padx=20)
        
        self.file : Optional[str] = None
        self.details_frame : Optional[DetailsFrame] = None
        
        self.label_to = customtkinter.CTkLabel(self,text = "To")
        self.label_to.grid(row=0, column=2, pady = 20 ,padx=20)

        self.entry_date_to = ctk.CTkEntry(self)
        self.entry_date_to.grid(row = 0, column = 3, pady = 20, padx=20)
        
        self.sitems = tk.StringVar()
        
        list_frame = ctk.CTkFrame(self)
        
        self.scroll = ttk.Scrollbar(list_frame, orient="vertical")
        self.scroll.grid(row = 0, column = 4, sticky="ns")
        self.listbox = tk.Listbox(master=list_frame, listvariable=self.sitems,yscrollcommand=self.scroll.set, width=70, height=15,exportselection=0)
        self.listbox.bind("<<ListboxSelect>>", self.xdd)
        self.scroll.config(command=self.listbox.yview)
        list_frame.grid(row = 1, column = 0, sticky="NSEW", columnspan=4)
        
        self.listbox.grid(row = 0, column = 0, columnspan=1, sticky="NSEW")

    def xdd(self,**kwargs):
        print("xdd")

    def set_details_frame(self, details_frame): 
        self.details_frame = details_frame
    
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
        
        self.stringVar_localhost = tk.StringVar()
        self.stringVar_localhost.set("localhost")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_localhost)
        self.entry_remote_host.grid(row = 0, column = 1, pady = 20, padx=20, columnspan=1)
        
        # Date
        self.label_date = customtkinter.CTkLabel(self, text = "Date")
        self.label_date.grid(row=1, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_date = tk.StringVar()
        self.stringVar_date.set("12.12.2021")
        self.entry_date = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_date)
        self.entry_date.grid(row = 1, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Time
        self.label_time = customtkinter.CTkLabel(self, text = "Time")
        self.label_time.grid(row=2, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_time = tk.StringVar()
        self.stringVar_time.set("21:37:69")
        self.entry_time = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_time)
        self.entry_time.grid(row = 2, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Timezone
        self.label_timezone = customtkinter.CTkLabel(self, text = "Timezone")
        self.label_timezone.grid(row=2, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_timezone = tk.StringVar()
        self.stringVar_timezone.set("21:37:69")
        self.entry_timezone = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_timezone)
        self.entry_timezone.grid(row = 2, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Status code
        self.label_status_code = customtkinter.CTkLabel(self, text = "Code")
        self.label_status_code.grid(row=3, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_status_code = tk.StringVar()
        self.stringVar_status_code.set("420")
        self.entry_status_code = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_status_code)
        self.entry_status_code.grid(row = 3, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Method
        
        self.label_method = customtkinter.CTkLabel(self, text = "Method")
        self.label_method.grid(row=3, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_method = tk.StringVar()
        self.stringVar_method.set("GET")
        self.entry_method = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_method)
        self.entry_method.grid(row = 3, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Resource
        
        self.label_resource = customtkinter.CTkLabel(self, text = "Resource")
        self.label_resource.grid(row=4, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_resource = tk.StringVar()
        self.stringVar_resource.set("/home/sliwek/tmp/tmp/tmp")
        self.entry_resource = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_resource)
        self.entry_resource.grid(row = 4, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Size
        
        self.label_size = customtkinter.CTkLabel(self, text = "Size")
        self.label_size.grid(row=5, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_size = tk.StringVar()
        self.stringVar_size.set(f"{2134} bytes")
        self.entry_size = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_size)
        self.entry_size.grid(row = 5, column = 1, pady = 20, padx=20,columnspan=1)
    
    def set_details(self, data: str):
        self.set_timezone(get_time_zone(data))
    
    def set_timezone(self, timezone:Optional[str]):
        if timezone is not None:
            self.stringVar_timezone.set(timezone)