import customtkinter as ctk
import customtkinter
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
        self.geometry("800x800") # useless with i3 wm
        
        self.file : Optional[str] = None
        
        self.entry_log = ctk.CTkEntry(master=self)
        
        self.button_open = ctk.CTkButton(master=self, text="Open", command=self.open_file)
        self.entry_log.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = ctk.NSEW)
        self.button_open.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = ctk.NSEW)
        
    def open_file(self):
        http_file = self.entry_log.get()
        if os.path.exists(http_file):
            self.file = http_file
            print(f"File opened: {self.file}")
        
app = HttpLogsApp()
app.mainloop()