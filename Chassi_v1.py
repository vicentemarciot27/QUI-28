# internal imports


# external imports

import tkinter as tk
import customtkinter as ctk


# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# App Frame
app = ctk.CTk()
app.geometry("1024x576")
app.title("C.H.A.S.S.I.")

# App main loop
if __name__ == '__main__':
    app.mainloop()