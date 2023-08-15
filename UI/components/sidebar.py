import customtkinter as ctk

from UI.common import open_parametros

class Sidebar(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Set the properties for the sidebar
        self.configure(width=200, height=576, bg_color="#282828")
        self.place(x=0)
        
        # Add the Welcome button
        welcome_btn = ctk.CTkButton(self, text="Welcome")
        welcome_btn.pack(pady=40, padx=20)
        
        # Add the Parâmetros button
        another_page_btn = ctk.CTkButton(self, text="Parâmetros")
        another_page_btn.pack(pady=40, padx=20)
        
        # Add the Modelagem button
        modelagem_btn = ctk.CTkButton(self, text="Modelagem")
        modelagem_btn.pack(pady=(40, 400), padx=20)