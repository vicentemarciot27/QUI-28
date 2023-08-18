# internal imports
from UI.common import open_docs
# from UI.pages.parametros import open_parametros
# from UI.components.sidebar import Sidebar

# external imports

import tkinter as tk
import customtkinter as ctk

class ExtendedInput(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Labels
        ctk.CTkLabel(self, text="Nome da variável").grid(row=0, column=0, padx=5, pady=5)
        ctk.CTkLabel(self, text="Valor").grid(row=0, column=1, padx=5, pady=5)
        ctk.CTkLabel(self, text="Unidade de medida").grid(row=0, column=2, padx=5, pady=5)
        
        # Entries for first row
        self.var_name_entry1 = ctk.CTkEntry(self)
        self.var_name_entry1.grid(row=1, column=0, padx=5, pady=5)  
        
        self.value_entry1 = ctk.CTkEntry(self)
        self.value_entry1.grid(row=1, column=1, padx=5, pady=5)
        
        self.unit_entry1 = ctk.CTkEntry(self)
        self.unit_entry1.grid(row=1, column=2, padx=5, pady=5)
        
        # Entries for second row
        self.var_name_entry2 = ctk.CTkEntry(self)
        self.var_name_entry2.grid(row=2, column=0, padx=5, pady=5)
        
        self.value_entry2 = ctk.CTkEntry(self)
        self.value_entry2.grid(row=2, column=1, padx=5, pady=5)
        
        self.unit_entry2 = ctk.CTkEntry(self)
        self.unit_entry2.grid(row=2, column=2, padx=5, pady=5)
        
        # Hidden row for third variable
        self.var_name_entry3 = ctk.CTkEntry(self)
        self.value_entry3 = ctk.CTkEntry(self)
        self.unit_entry3 = ctk.CTkEntry(self)
        
        # Toggle button to show/hide third row
        self.toggle_btn = ctk.CTkButton(self, text="Toggle Third Variable", command=self.toggle_third_row)
        self.toggle_btn.grid(row=4, columnspan=3, pady=10)
        
        # Track the state of the third row (hidden by default)
        self.third_row_visible = False

    def toggle_third_row(self):
        if self.third_row_visible:
            self.var_name_entry3.grid_forget()
            self.value_entry3.grid_forget()
            self.unit_entry3.grid_forget()
            self.third_row_visible = False
        else:
            self.var_name_entry3.grid(row=3, column=0, padx=5, pady=5)
            self.value_entry3.grid(row=3, column=1, padx=5, pady=5)
            self.unit_entry3.grid(row=3, column=2, padx=5, pady=5)
            self.third_row_visible = True


class WelcomePage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Title
        self.title_label = ctk.CTkLabel(self, font=("Arial", 48), text="C.H.A.S.S.I.")
        self.title_label.place(x=400, y=100)

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self, font=("Arial", 16), text="Catalyst Hybrid And Single-propellant System design Interface")
        self.subtitle_label.place(x=300, y=200)

        # Link to documentation
        self.link_btn = ctk.CTkButton(self, text="Read the docs and get started", command=open_docs)
        self.link_btn.place(x=420, y=280)

class ModelagemPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Extended input section
        self.extended_input = ExtendedInput(self)
        self.extended_input.pack(pady=80)




class ParametrosPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        var_output = ""
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Extended input section
        self.extended_input = ExtendedInput(self)
        self.extended_input.pack(pady=80)
    
def open_parametros():
    # Open the Parâmetros page
    app = ParametrosPage()
    app.geometry("1024x576")
    app.title("Parâmetros Page")
    app.mainloop()

def open_welcome():
    welcome_app = WelcomePage()
    welcome_app.geometry("1024x576")
    welcome_app.title("Welcome Page")
    welcome_app.mainloop()

def open_modelagem():
    modelagem_app = ModelagemPage()
    modelagem_app.geometry("1024x576")
    modelagem_app.title("Modelagem Page")
    modelagem_app.mainloop()

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Set the properties for the navbar
        self.configure(width=1024, height=50, bg_color="#232323")
        self.place(y=0)
        
        # Configure columns for even distribution
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        
        # Add the Welcome button
        welcome_btn = ctk.CTkButton(self, text="Welcome", command=lambda: open_welcome())
        welcome_btn.grid(row=0, column=0, padx=20, pady=5, sticky='ew')
    
        # Add the Parâmetros button
        parametros_btn = ctk.CTkButton(self, text="Parâmetros", command=lambda: open_parametros())
        parametros_btn.grid(row=0, column=1, padx=20, pady=5, sticky='ew')
    
        # Add the Modelagem button
        modelagem_btn = ctk.CTkButton(self, text="Modelagem", command=lambda: open_modelagem())
        modelagem_btn.grid(row=0, column=2, padx=(20, 1000), pady=5, sticky='ew')

# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# App Frame
app = ctk.CTk()
app.geometry("1024x576")
app.title("C.H.A.S.S.I.")

# Title
title_label = ctk.CTkLabel(app, font=("Arial" , 48), text="C.H.A.S.S.I")  # Dark theme blue
title_label.place(x = 460, y = 100)

# Subtitle
subtitle_label = ctk.CTkLabel(app, font = ("Arial", 16), text="Catalyst Hybrid And Single-propellant System design Interface")
subtitle_label.place(x = 360, y = 200)

# Link to documentation
link_btn = ctk.CTkButton(app, text="Read the docs and get started", command=open_docs)
link_btn.place(x = 490, y = 280)

# # Sidebar
sidebar = Sidebar(app)

# App main loop
if __name__ == '__main__':
    app.mainloop()