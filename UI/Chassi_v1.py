# internal imports
from UI.common import open_docs
# from UI.pages.parametros import open_parametros
# from UI.components.sidebar import Sidebar

# external imports

import tkinter as tk
import customtkinter as ctk

def open_parametros():
    app.destroy()
    app

class WelcomePage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Title
        self.title_label = ctk.CTkLabel(self, font=("Arial", 48), text="C.H.A.S.S.I")
        self.title_label.place(x=460, y=100)

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self, font=("Arial", 16), text="Catalyst Hybrid And Single-propellant System design Interface")
        self.subtitle_label.place(x=360, y=200)

        # Link to documentation
        self.link_btn = ctk.CTkButton(self, text="Read the docs and get started", command=open_docs)
        self.link_btn.place(x=490, y=280)

class ModelagemPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Input slot
        self.input_label = ctk.CTkLabel(self, text="Input:")
        self.input_label.place(x=250, y=100)
        
        self.input_entry = ctk.CTkEntry(self, width=200)
        self.input_entry.place(x=300, y=100)
        
        # Output slot
        self.output_label = ctk.CTkLabel(self, text="Output:")
        self.output_label.place(x=250, y=200)
        
        self.output_entry = ctk.CTkEntry(self, width=200)
        self.output_entry.place(x=300, y=200)


class ParametrosPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Input slot
        self.input_label = ctk.CTkLabel(self, text="Input:")
        self.input_label.place(x=250, y=100)
        
        self.input_entry = ctk.CTkEntry(self, width=200)
        self.input_entry.place(x=300, y=100)
        
        # Output slot
        self.output_label = ctk.CTkLabel(self, text="Output:")
        self.output_label.place(x=250, y=200)
        
        self.output_entry = ctk.CTkEntry(self, width=200)
        self.output_entry.place(x=300, y=200)
    
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
        
        # Set the properties for the sidebar
        self.configure(width=200, height=576, bg_color="#282828")
        self.place(x=0)
        
        # Add the Welcome button
        welcome_btn = ctk.CTkButton(self, text="Welcome", command=lambda: open_welcome())
        welcome_btn.pack(pady=40, padx=20)
    
        # Add the Parâmetros button
        parametros_btn = ctk.CTkButton(self, text="Parâmetros", command=lambda: open_parametros())
        parametros_btn.pack(pady=40, padx=20)
    
        # Add the Modelagem button
        modelagem_btn = ctk.CTkButton(self, text="Modelagem", command=lambda: open_modelagem())
        modelagem_btn.pack(pady=(40, 400), padx=20)

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