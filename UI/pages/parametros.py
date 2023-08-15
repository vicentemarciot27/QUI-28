# parametros_page.py
import customtkinter as ctk
from UI.components.sidebar import Sidebar

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

# Usage example:
if __name__ == '__main__':
    app = ParametrosPage()
    app.geometry("1024x576")
    app.title("Parâmetros Page")
    app.mainloop()
