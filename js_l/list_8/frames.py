import customtkinter as ctk
from CTkListbox import *
from typing import Optional
import tkinter as tk
from tkinter import ttk
from datetime import datetime as dt, timedelta as td
from utils import *

class MasterFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.log_data = [] #contains all the data from the log file
        
        # Date from
        self.label_from = ctk.CTkLabel(self, text = "From")
        self.label_from.grid(row=0, column=0, pady = 20 ,padx=20)
        
        self.entry_date_from = ctk.CTkEntry(self)
        self.entry_date_from.grid(row = 0, column = 1, pady = 20, padx=20)
        self.entry_date_from.bind("<Key>", lambda x: self._set_from_date())
        
        # Date to
        self.label_to = ctk.CTkLabel(self,text = "To")
        self.label_to.grid(row=0, column=2, pady = 20 ,padx=20)
        
        self.entry_date_to = ctk.CTkEntry(self)
        self.entry_date_to.grid(row = 0, column = 3, pady = 20, padx=20)
        self.entry_date_to.bind("<Key>", lambda x: self._set_to_date())
        
        # Date variables
        self.date_from  : Optional[dt] = None
        self.date_to  : Optional[dt] = None
        
        # Filename
        self.file : Optional[str] = None
        
        # Detail frame
        self.details_frame : Optional[DetailsFrame] = None
        
        # buttons from main to navigate through the logs
        self.button_next : Optional[ctk.CTkButton] = None
        self.button_prev : Optional[ctk.CTkButton] = None 
        
        # Listbox with logs, scrollbar, stringvar
        self.sitems = tk.StringVar()
    
        list_frame = ctk.CTkFrame(self) 
        
        self.scroll = ttk.Scrollbar(list_frame, orient="vertical")
        self.listbox = tk.Listbox(master=list_frame, listvariable=self.sitems,yscrollcommand=self.scroll.set, width=70, height=15,exportselection=0)
        
        # bind 
        self.listbox.bind("<<ListboxSelect>>", self._set_details_command)
        self.scroll.config(command=self.listbox.yview)
        
        # layout
        list_frame.grid(row = 1, column = 0, sticky="NSEW", columnspan=4)
        self.scroll.grid(row = 0, column = 4, sticky="ns")
        self.listbox.grid(row = 0, column = 0, columnspan=1, sticky="NSEW")

    # setters for external usage
    def set_buttons(self, button_prev:ctk.CTkButton, button_next:ctk.CTkButton):
        """Set buttons to navigate through the logs"""
        self.button_prev = button_prev
        self.button_next = button_next
        
    def set_details_frame(self, details_frame): 
        """Set the details frame to display the details of the selected item"""
        self.details_frame = details_frame

    def set_file(self, file:str):
        """Set name of the file with logs"""
        self.file = file
        print(f"File set: {self.file}")
        self.log_data = open_file(self.file)
        self._set_items()
        
    #also external methods
    def select_next(self) -> bool:
        """return True if the next item is selected, False otherwise"""
        index =  self.listbox.index("active")
        if index is not None:
            self.listbox.selection_clear(index)
            self.listbox.activate(index + 1)
            self.listbox.selection_set(index + 1)
            self.listbox.see(index + 1)
            self._set_details_command()
            
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            self._set_details_command()
        return True
    
    def selected_last(self) -> bool:
        """Return True if the last item is selected, False otherwise"""
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
        """Select the previous item in the listbox, return True if the first item is selected, False otherwise"""
        index =  self.listbox.index("active")
        if index is not None:
            self.listbox.selection_clear(index)
            self.listbox.activate(index - 1)
            self.listbox.selection_set(index - 1)
            self.listbox.see(index - 1)
            self._set_details_command()
            
        else:
            self.listbox.selection_set(0)
            self.listbox.activate(0)
            self.listbox.see(0)
            self._set_details_command()
        return True
        
    def selected_first(self) -> bool:
        """return True if the first item is selected, False otherwise"""
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
        """clear all the data from the listbox and the details frame"""
        self.details_frame.clear_data()
        self.date_from = None
        self.date_to = None
        self.entry_date_from.delete(0, tk.END)
        self.entry_date_to.delete(0, tk.END)
        self.sitems.set([])

    # internal methods
    def _set_details_command(self,*args):
        """ Disable and enable buttons depending on the selected item """
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
    
    def _set_items(self):
        """Set items in the listbox, depending on the date_from and date_to, refreshes the listbox position"""
        self._set_details_command()
        self.details_frame.clear_data()
        
        self.listbox.selection_set(0)
        self.listbox.activate(0)
        self.listbox.see(0)
        
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
    
    def _set_from_date(self):
        """Set the date_from variable and refresh the listbox"""
        try:
            self.date_from = dt.strptime(self.entry_date_from.get(), "%d/%m/%Y")
            self._fix_date()
            self._set_items()
        except ValueError:
            self.date_from = None
            
    def _set_to_date(self):
        """Set the date_to variable and refresh the listbox"""
        try:
            self.date_to = dt.strptime(self.entry_date_to.get(), "%d/%m/%Y")
            self._fix_date()
            self._set_items()
        except ValueError:
            self.date_to = None
    
    def _fix_date(self) -> None:
        """Fix the date if the date_from is greater than date_to"""
        if self.date_from is not None and self.date_to is not None:
            if self.date_from > self.date_to:
                self.date_from, self.date_to = self.date_to, self.date_from
                self.entry_date_from.delete(0, tk.END)
                self.entry_date_from.insert(0, self.date_from.strftime("%d/%m/%Y"))
                self.entry_date_to.delete(0, tk.END)
                self.entry_date_to.insert(0, self.date_to.strftime("%d/%m/%Y"))
            
class DetailsFrame(ctk.CTkFrame):
    
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        # Remote host
        self.label_remote_host = ctk.CTkLabel(self, text = "Remote host")
        self.label_remote_host.grid(row=0, column=0, pady = 20 ,padx=20, columnspan=1)
        
        self.stringVar_localhost = tk.StringVar()
        self.stringVar_localhost.set("")
        self.entry_remote_host = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_localhost)
        self.entry_remote_host.grid(row = 0, column = 1, pady = 20, padx=20, columnspan=1)
        
        # Date
        self.label_date = ctk.CTkLabel(self, text = "Date")
        self.label_date.grid(row=1, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_date = tk.StringVar()
        self.stringVar_date.set("")
        self.entry_date = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_date)
        self.entry_date.grid(row = 1, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Time
        self.label_time = ctk.CTkLabel(self, text = "Time")
        self.label_time.grid(row=2, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_time = tk.StringVar()
        self.stringVar_time.set("")
        self.entry_time = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_time)
        self.entry_time.grid(row = 2, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Timezone
        self.label_timezone = ctk.CTkLabel(self, text = "Timezone")
        self.label_timezone.grid(row=2, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_timezone = tk.StringVar()
        self.stringVar_timezone.set("")
        self.entry_timezone = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_timezone)
        self.entry_timezone.grid(row = 2, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Status code
        self.label_status_code = ctk.CTkLabel(self, text = "Code")
        self.label_status_code.grid(row=3, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_status_code = tk.StringVar()
        self.stringVar_status_code.set("")
        self.entry_status_code = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_status_code)
        self.entry_status_code.grid(row = 3, column = 1, pady = 20, padx=20,columnspan=1)
        
        # Method
        
        self.label_method = ctk.CTkLabel(self, text = "Method")
        self.label_method.grid(row=3, column=2, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_method = tk.StringVar()
        self.stringVar_method.set("")
        self.entry_method = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_method)
        self.entry_method.grid(row = 3, column = 3, pady = 20, padx=20,columnspan=1)
        
        # Resource
        
        self.label_resource = ctk.CTkLabel(self, text = "Resource")
        self.label_resource.grid(row=4, column=0, pady = 20 ,padx=20,columnspan=1, sticky="ew")
        
        self.stringVar_resource = tk.StringVar()
        self.stringVar_resource.set("")
        self.entry_resource = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_resource)
        self.entry_resource.grid(row = 4, column = 1, pady = 20, padx=20,columnspan=3, sticky="ew")
        
        # Size
        
        self.label_size = ctk.CTkLabel(self, text = "Size")
        self.label_size.grid(row=5, column=0, pady = 20 ,padx=20,columnspan=1)
        
        self.stringVar_size = tk.StringVar()
        self.stringVar_size.set(f"")
        self.entry_size = ctk.CTkEntry(self, state="disabled",textvariable=self.stringVar_size)
        self.entry_size.grid(row = 5, column = 1, pady = 20, padx=20,columnspan=1)
    
    # setters for the details
    def set_details(self, data: str):
        self._set_timezone(get_time_zone(data))
        self._set_remote_host(get_ip_or_domain(data))
        self._set_date(get_full_date(get_raw_date(data)))
        self._set_time(get_full_date(get_raw_date(data)))
        self._set_status_code(get_code(data))
        self._set_method(get_method(data))
        self._set_resource(get_path_from_data(data))
        self._set_bytes(return_send_bytes(data))
    
    def _set_timezone(self, timezone:Optional[str]):
        if timezone is not None:
            self.stringVar_timezone.set(timezone)
        else:
            self.stringVar_timezone.set("")
    
    def _set_remote_host(self, remote_host:Optional[str]):
        if remote_host is not None:
            self.stringVar_localhost.set(remote_host)
        else: 
            self.stringVar_localhost.set("")
            
    def _set_date(self, date:Optional[str]):
        if date is not None:
            self.stringVar_date.set(str(date.date()))
        else:
            self.stringVar_date.set("")
    
    def _set_time(self, time:Optional[str]):
        if time is not None:
            self.stringVar_time.set(str(time.time()))
        else:
            self.stringVar_time.set("")
    
    def _set_status_code(self, status_code:Optional[str]):
        if status_code is not None:
            self.stringVar_status_code.set(status_code)
        else:
            self.stringVar_status_code.set("")
    
    def _set_method(self, method:Optional[str]):
        if method is not None:
            self.stringVar_method.set(method)
        else:
            self.stringVar_method.set("")
        
    def _set_resource(self, resource:Optional[str]):
        if resource is not None:
            self.stringVar_resource.set(resource)
        else:
            self.stringVar_resource.set("")
            
    def _set_bytes(self, time:Optional[int]):
        if time is not None:
            self.stringVar_size.set(f"{time} bytes") 
        else:
            self.stringVar_size.set("0 bytes")      
    
    # clear all the data
    def clear_data(self):
        self.stringVar_localhost.set("")
        self.stringVar_date.set("")
        self.stringVar_time.set("")
        self.stringVar_timezone.set("")
        self.stringVar_status_code.set("")
        self.stringVar_method.set("")
        self.stringVar_resource.set("")
        self.stringVar_size.set("")