# internal imports
from UI.common import open_docs
from logica.duovar.testes import * 
from logica.duovar.Entregando_perifericos import *
# from UI.pages.parametros import open_parametros
# from UI.components.sidebar import Sidebar

# external imports

import tkinter as tk
import customtkinter as ctk

def create_parameter_from_data(variable_data):
    # Convert the data from string to appropriate types
    name = variable_data["name"]
    unit = variable_data["unit"]
    is_integer = variable_data["is_integer"]
    
    center = float(variable_data["value"]) if variable_data["value"] else 0.0
    lower_limit = float(variable_data["min_value"]) if variable_data["min_value"] else 0.0
    upper_limit = float(variable_data["max_value"]) if variable_data["max_value"] else 0.0
    delta = float(variable_data["delta"]) if variable_data["delta"] else 0.0
    
    # Create a Parameter object
    return Parameter(name, unit, is_integer, center, lower_limit, upper_limit, delta)



class ExtendedInput(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Labels for common headers
        headers = ["Nome da variável", "Valor", "Unidade de medida", 
                   "Max Value", "Min Value", "Delta", "Is Integer"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self, text=header).grid(row=0, column=col, padx=3, pady=3)

        # Entries and checkboxes for three rows
        self.entries = []
        for row in range(1, 4):
            row_entries = []
            for col in range(6):  # 6 for the six columns of Entry fields
                entry = ctk.CTkEntry(self)
                entry.grid(row=row, column=col, padx=3, pady=3)
                row_entries.append(entry)

            checkbox = ctk.CTkCheckBox(self, text="Is Integer")
            checkbox.grid(row=row, column=6, padx=3, pady=3)
            row_entries.append(checkbox)

            self.entries.append(row_entries)

        # Initially hide the third row
        for widget in self.entries[2]:
            widget.grid_remove()

        self.third_row_visible = False  # Track the state of the third row (hidden by default)

        # Toggle button to show/hide third row
        self.toggle_btn = ctk.CTkButton(self, text="Toggle Third Variable", command=self.toggle_third_row)
        self.toggle_btn.grid(row=5, column=2, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_data)
        self.send_button.grid(row=5, column=3, padx=5, pady=5)
        # Label to display the output
        self.output_label = ctk.CTkLabel(self, text="", wraplength=600)
        self.output_label.grid(row=6, columnspan=7, pady=10)

        


    def send_data(self):
        parameters_list = []
    
        for row_entries in self.entries:
            variable_data = {
                "name": row_entries[0].get(),
                "value": row_entries[1].get(),
                "unit": row_entries[2].get(),
                "max_value": row_entries[3].get(),
                "min_value": row_entries[4].get(),
                "delta": row_entries[5].get(),
                "is_integer": row_entries[6].get()
         }
            parameter = create_parameter_from_data(variable_data)
            print(parameter.unit)
            parameters_list.append(parameter)
        
        fatorial = FatorialPlan(len(parameters_list), math.sqrt(2))

        fatorial_plan_list = fatorial.fatorial

        real_plan = return_plan(parameters_list, fatorial_plan_list)

        
        output_strings = []
        for param in parameters_list:
            output_string = f"The variable {param.name} with unit of measure {param.unit} needs to use the following points: {real_plan}"
            output_strings.append(output_string)
            print(real_plan)
            print(param.unit)# Just for debugging.
        self.output_label.configure(text="\n".join(output_strings))
    



    def toggle_third_row(self):
        if self.third_row_visible:
            for widget in self.entries[2]:
                widget.grid_remove()
            self.third_row_visible = False
        else:
            for col, widget in enumerate(self.entries[2]):
                widget.grid(row=3, column=col, padx=5, pady=5)
            self.third_row_visible = True


class WelcomePage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add the sidebar
        self.sidebar = Sidebar(self)
        
        # Title
        self.title_label = ctk.CTkLabel(self, font=("Arial", 108), text="C.H.A.S.S.I.")
        self.title_label.pack(pady=100)

        # Subtitle
        self.subtitle_label = ctk.CTkLabel(self, font=("Arial", 16), text="Catalyst Hybrid And Single-propellant System design Interface")
        self.subtitle_label.pack()

        # Link to documentation
        self.link_btn = ctk.CTkButton(self, text="Read the docs and get started", command=open_docs)
        self.link_btn.pack(pady=20)

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
title_label = ctk.CTkLabel(app, font=("Arial" , 108), text="C.H.A.S.S.I")  # Dark theme blue
title_label.pack(pady=100)

# Subtitle
subtitle_label = ctk.CTkLabel(app, font = ("Arial", 16), text="Catalyst Hybrid And Single-propellant System design Interface")
subtitle_label.pack()

# Link to documentation
link_btn = ctk.CTkButton(app, text="Read the docs and get started", command=open_docs)
link_btn.pack(pady=20)

# # Sidebar
sidebar = Sidebar(app)

# App main loop
if __name__ == '__main__':
    app.mainloop()