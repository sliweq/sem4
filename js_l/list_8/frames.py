import customtkinter as ctk
import customtkinter
import customtkinter
from CTkListbox import *
from typing import Optional
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import StringVar
import os
from datetime import datetime as dt, timedelta as td
from tmp import *

def open_file(file_name:str) -> list[str]:
    lines = []
    with open(file_name, "r") as f:
        lines = f.readlines()
    return lines

class MasterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.log_data = []
        
        self.label_from = customtkinter.CTkLabel(self, text = "From")
        self.label_from.grid(row=0, column=0, pady = 20 ,padx=20)
        
        self.entry_date_from = ctk.CTkEntry(self)
        self.entry_date_from.grid(row = 0, column = 1, pady = 20, padx=20)
        self.entry_date_from.bind("<Key>", lambda x: self.set_from_date())
        
        self.entry_date_to = ctk.CTkEntry(self)
        self.entry_date_to.grid(row = 0, column = 3, pady = 20, padx=20)
        self.entry_date_to.bind("<Key>", lambda x: self.set_to_date())
        
        self.date_from  : Optional[dt] = None
        self.date_to  : Optional[dt] = None
        
        
        
        self.file : Optional[str] = None
        self.details_frame : Optional[DetailsFrame] = None
        
        self.button_next : Optional[ctk.CTkButton] = None
        self.button_prev : Optional[ctk.CTkButton] = None 
        
        self.label_to = customtkinter.CTkLabel(self,text = "To")
        self.label_to.grid(row=0, column=2, pady = 20 ,padx=20)
        
        self.sitems = tk.StringVar()
        
        list_frame = ctk.CTkFrame(self)
        
        self.scroll = ttk.Scrollbar(list_frame, orient="vertical")
        self.scroll.grid(row = 0, column = 4, sticky="ns")
        self.listbox = tk.Listbox(master=list_frame, listvariable=self.sitems,yscrollcommand=self.scroll.set, width=70, height=15,exportselection=0)
        self.listbox.bind("<<ListboxSelect>>", self.set_details_command)
        self.scroll.config(command=self.listbox.yview)
        list_frame.grid(row = 1, column = 0, sticky="NSEW", columnspan=4)
        
        self.listbox.grid(row = 0, column = 0, columnspan=1, sticky="NSEW")

    def set_buttons(self, button_prev:ctk.CTkButton, button_next:ctk.CTkButton):
        self.button_prev = button_prev
        self.button_next = button_next

    def set_details_command(self,*args):
        self.details_frame.set_details(self.listbox.get(self.listbox.index("active")))
        if self.selected_first():
            self.button_prev.configure(state=tk.DISABLED)
            self.button_next.configure(state=tk.NORMAL)
        elif self.selected_last():
            self.button_prev.configure(state=tk.NORMAL)
            self.button_next.configure(state=tk.DISABLED)
        else:
            self.button_prev.configure(state=tk.NORMAL)
            self.button_next.configure(state=tk.NORMAL)
            
    def set_details_frame(self, details_frame): 
        self.details_frame = details_frame
    
    def set_file(self, file:str):
        self.file = file
        print(f"File set: {self.file}")
        self.log_data = open_file(self.file)
        self.set_items()
    
    def set_items(self):
        self.set_details_command()
        self.details_frame.clear_data()
        
        self.listbox.selection_set(0)
        self.listbox.activate(0)
        self.listbox.see(0)
        print("xd")
        
        if self.date_from is None:
            if self.date_to is None:
                self.sitems.set(self.log_data)
                return
            else:
                items = []
                for line in self.log_data:
                    if get_full_date(get_raw_date(line)) < self.date_to+ td(days=1):
                        items.append(line)
                    else: break
                self.sitems.set(items)
                return
        if self.date_to is None: 
            items = []
            index = 0
            while index < len(self.log_data) and get_full_date(get_raw_date(self.log_data[index])) < self.date_from:
                index += 1
            for line in self.log_data[index:]:
                if get_full_date(get_raw_date(line)) >= self.date_from:
                    items.append(line)
                else: 
                    break
            self.sitems.set(items)
            return
        
        items = []
        for line in self.log_data:
            if get_full_date(get_raw_date(line)) >= self.date_from and get_full_date(get_raw_date(line)) < self.date_to+ td(days=1):
                items.append(line)

        self.sitems.set(items)
    
    def select_next(self) -> bool:
        index =  self.listbox.index("active")
        if index is not None:
            self.listbox.selection_clear(index)
            self.listbox.activate(index + 1)
            self.listbox.selection_set(index + 1)
            self.listbox.see(index + 1)
            self.set_details_command()
            return True
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            self.set_details_command()
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
            self.set_details_command()
            return True
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            self.set_details_command()
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

    def clear_data(self):
        self.details_frame.clear_data()
        self.date_from = None
        self.date_to = None
        self.entry_date_from.delete(0, tk.END)
        self.entry_date_to.delete(0, tk.END)
        self.sitems.set([])
    
    def set_from_date(self):
        try:
            self.date_from = dt.strptime(self.entry_date_from.get(), "%d/%m/%Y")
            self.set_items()
        except ValueError:
            self.date_from = None
            
    def set_to_date(self):
        try:
            self.date_to = dt.strptime(self.entry_date_to.get(), "%d/%m/%Y")
            self.set_items()
        except ValueError:
            self.date_to = None
        
    
    

class DetailsFrame(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Remote host
        self.label_remote_host = customtkinter.CTkLabel(self, text = "Remote host")
        self.label_remote_host.grid(row=0, column=0, pady = 20 ,padx=20, columnspan=1)
        
        self.stringVar_localhost = tk.StringVar()
        self.stringVar_localhost.set("")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_localhost)
        self.entry_remote_host.grid(row = 0, column = 1, pady = 20, padx=20, columnspan=1)
        
        # Date
        self.label_date = customtkinter.CTkLabel(self, text = "Date")
        self.label_date.grid(row=1, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_date = tk.StringVar()
        self.stringVar_date.set("")
        self.entry_date = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_date)
        self.entry_date.grid(row = 1, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Time
        self.label_time = customtkinter.CTkLabel(self, text = "Time")
        self.label_time.grid(row=2, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_time = tk.StringVar()
        self.stringVar_time.set("")
        self.entry_time = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_time)
        self.entry_time.grid(row = 2, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Timezone
        self.label_timezone = customtkinter.CTkLabel(self, text = "Timezone")
        self.label_timezone.grid(row=2, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_timezone = tk.StringVar()
        self.stringVar_timezone.set("")
        self.entry_timezone = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_timezone)
        self.entry_timezone.grid(row = 2, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Status code
        self.label_status_code = customtkinter.CTkLabel(self, text = "Code")
        self.label_status_code.grid(row=3, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_status_code = tk.StringVar()
        self.stringVar_status_code.set("")
        self.entry_status_code = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_status_code)
        self.entry_status_code.grid(row = 3, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Method
        
        self.label_method = customtkinter.CTkLabel(self, text = "Method")
        self.label_method.grid(row=3, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_method = tk.StringVar()
        self.stringVar_method.set("")
        self.entry_method = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_method)
        self.entry_method.grid(row = 3, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Resource
        
        self.label_resource = customtkinter.CTkLabel(self, text = "Resource")
        self.label_resource.grid(row=4, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_resource = tk.StringVar()
        self.stringVar_resource.set("")
        self.entry_resource = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_resource)
        self.entry_resource.grid(row = 4, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Size
        
        self.label_size = customtkinter.CTkLabel(self, text = "Size")
        self.label_size.grid(row=5, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_size = tk.StringVar()
        self.stringVar_size.set(f"")
        self.entry_size = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_size)
        self.entry_size.grid(row = 5, column = 1, pady = 20, padx=20,columnspan=1)
    
    def set_details(self, data: str):
        self.set_timezone(get_time_zone(data))
        self.set_remote_host(get_ip_or_domain(data))
        self.set_date(get_full_date(get_raw_date(data)))
        self.set_time(get_full_date(get_raw_date(data)))
        self.set_status_code(get_code(data))
        self.set_method(get_method(data))
        self.set_resource(get_path_from_data(data))
        self.set_bytes(return_send_bytes(data))
    
    def set_timezone(self, timezone:Optional[str]):
        if timezone is not None:
            self.stringVar_timezone.set(timezone)
    
    def set_remote_host(self, remote_host:Optional[str]):
        if remote_host is not None:
            self.stringVar_localhost.set(remote_host)
        
    def set_date(self, date:Optional[str]):
        if date is not None:
            self.stringVar_date.set(str(date.date()))
    
    def set_time(self, time:Optional[str]):
        if time is not None:
            self.stringVar_time.set(str(time.time()))
    
    def set_status_code(self, status_code:Optional[str]):
        if status_code is not None:
            self.stringVar_status_code.set(status_code)
    
    def set_method(self, method:Optional[str]):
        if method is not None:
            self.stringVar_method.set(method)
        
    def set_resource(self, resource:Optional[str]):
        if resource is not None:
            self.stringVar_resource.set(resource)
            
    def set_bytes(self, time:Optional[int]):
        if time is not None:
            self.stringVar_size.set(f"{time} bytes")       
    
    def clear_data(self):
        self.stringVar_localhost.set("")
        self.stringVar_date.set("")
        self.stringVar_time.set("")
        self.stringVar_timezone.set("")
        self.stringVar_status_code.set("")
        self.stringVar_method.set("")
        self.stringVar_resource.set("")
        self.stringVar_size.set("")