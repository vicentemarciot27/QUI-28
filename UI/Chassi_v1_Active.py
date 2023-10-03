# internal imports
from UI.common import open_docs
from logica.duovar.Entregando_perifericos import *
import math
import numpy as np
import pandas as pd

# from UI.pages.parametros import open_parametros
# from UI.components.sidebar import Sidebar

# external imports

import tkinter as tk
import customtkinter as ctk


def beautify_matrix(mat):
    # Convert numpy array to list of lists
    mat_list = mat.tolist()
    
    # Find the maximum width needed for each column
    col_widths = [max(len(str(row[i])) for row in mat_list) for i in range(mat.shape[1])]
    
    # Format the matrix
    formatted_rows = []
    for row in mat_list:
        formatted_row = ' '.join([f"{val:>{col_widths[i]}}" for i, val in enumerate(row)])
        formatted_rows.append(formatted_row)
    
    return "\n".join(formatted_rows)

def create_parameter_from_data(variable_data):
    # Convert the data from string to appropriate types
    name = variable_data["name"]
    unit = variable_data["unit"]
    is_integer = variable_data["is_integer"]

    center = float(variable_data["value"]) if variable_data["value"] else 0.0
    lower_limit = (
        float(variable_data["min_value"]) if variable_data["min_value"] else 0.0
    )
    upper_limit = (
        float(variable_data["max_value"]) if variable_data["max_value"] else 0.0
    )
    delta = float(variable_data["delta"]) if variable_data["delta"] else 0.0

    # Create a Parameter object
    return Parameter(name, unit, is_integer, center, lower_limit, upper_limit, delta)


class ExtendedInput(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Labels for common headers
        headers = [
            "Nome da variável",
            "Valor",
            "Unidade de medida",
            "Max Value",
            "Min Value",
            "Delta",
            "Is Integer",
        ]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self, text=header).grid(row=0, column=col, padx=3, pady=3)


        default_values = ["Nome", 3, "Unidade", 10, 0, 1]
        
        # Entries and checkboxes for three rows
        self.entries = []
        for row in range(1, 4):
            row_entries = []
            for col in range(6):  # 6 for the six columns of Entry fields
                entry = ctk.CTkEntry(self)
                entry.grid(row=row, column=col, padx=3, pady=3)
                
                # Inserting default values into the entries
                entry.insert(0, default_values[col])
                
                row_entries.append(entry)
        
            checkbox = ctk.CTkCheckBox(self, text="Is Integer")
            checkbox.grid(row=row, column=6, padx=3, pady=3)
            row_entries.append(checkbox)

            self.entries.append(row_entries)

        # Initially hide the third row
        for widget in self.entries[2]:
            widget.grid_remove()

        self.third_row_visible = (
            False  # Track the state of the third row (hidden by default)
        )

        # Toggle button to show/hide third row
        self.toggle_btn = ctk.CTkButton(
            self, text="Toggle Third Variable", command=self.toggle_third_row
        )
        self.toggle_btn.grid(row=5, column=2, pady=5)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_data)
        self.send_button.grid(row=5, column=3, padx=5, pady=5)
        # Label to display the output
        self.output_label = ctk.CTkLabel(self, text="", wraplength=600)
        self.output_label.grid(row=6, columnspan=7, pady=10)

    def send_data(self):
        parameters_list = []
        is_integer = False

        num_rows = 3 if self.third_row_visible else 2

        for i in range(num_rows):
            row_entries = self.entries[i]
            variable_data = {
                "name": row_entries[0].get(),
                "value": row_entries[1].get(),
                "unit": row_entries[2].get(),
                "max_value": row_entries[3].get(),
                "min_value": row_entries[4].get(),
                "delta": row_entries[5].get(),
                "is_integer": row_entries[6].get(),
            }
            parameter = create_parameter_from_data(variable_data)
            if parameter.is_integer:
                is_integer = True
            print(parameter.unit)
            parameters_list.append(parameter)

        fatorial = FatorialPlan(parameters_list, math.sqrt(2), is_integer)

        output_strings = []

        output_strings.append(
            f"{beautify_matrix(return_real_plan(fatorial, fatorial.center))}\n Este é o ponto central do planejamento fatorial. "
            "Ele assim é chamado pois o planejamento é construido em volta dele."
            " Devem ser feitas de 3 a 5 repetições do experimento no ponto central,"
            " pois ele será importante para estimar a variância dos dados.\n\n"
        )
        output_strings.append(
            f"{beautify_matrix(return_real_plan(fatorial, fatorial.cubic))}\n Esses são os pontos cúbicos do planejamento fatorial. "
            " Eles assim são chamados pois no espaço de planejamento eles formam um quadrado"
            " (para 2 parâmetros), um cubo (para 3 parâmetros), ou um hypercubo (para mais"
            " de 3 parâmetros).\n\n"
        )
        output_strings.append(
            f"{beautify_matrix(return_real_plan(fatorial, fatorial.axial))}\n Esses são os pontos axiais do planejamento fatorial. "
            " Eles assim são chamados pois ficam sobre os eixos do espaço de planejamento.\n\n"
        )

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
        self.subtitle_label = ctk.CTkLabel(
            self,
            font=("Arial", 16),
            text="Catalyst Hybrid And Single-propellant System design Interface",
        )
        self.subtitle_label.pack()

        # Link to documentation
        self.link_btn = ctk.CTkButton(
            self, text="Read the docs and get started", command=open_docs
        )
        
        self.link_btn.pack(pady=20)
        
            
class ModelagemInput(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.num_vars_input_Label = ctk.CTkLabel(self, text="Número de variáveis\n do planejamento fatorial:").grid(row=0, column=0)
        
        self.num_vars_input = ctk.CTkEntry(self)
        self.num_vars_input.insert(0, "2")
        self.num_vars_input.grid(row=0, column=1)
        
        self.update_button = ctk.CTkButton(self, text="Update", command=self.update_entries)
        self.update_button.grid(row=0, column=2)
        
        num_vars = 2
        
        num_points = 3 + 2**num_vars + num_vars
        
        self.entries = []
        for i in range(num_points):
            self.entries.append([])
            for j in range(num_vars):
                self.entries[i].append(ctk.CTkEntry(self))
                self.entries[i][j].grid(row=i+2, column=j, padx=3, pady=3)
                
        # Instance variable to keep track of header labels
        self.headers_labels = []
        
        # Labels for common headers
        headers = ["Ponto", "Resultado"]
        ctk.CTkLabel(self, text="Ponto").grid(row=1, column=0, padx=3, pady=3)
        ctk.CTkLabel(self, text="Resultado").grid(row=1, column=num_vars, padx=3, pady=3)
        
        self.update_entries()
        
        # Add button to generate and display DataFrame
        self.print_df_button = ctk.CTkButton(self, text="Print DataFrame", command=self.print_dataframe)
        self.print_df_button.grid(row=2, column=num_vars+2)  # Adjust the grid position as needed

        # Label to display the DataFrame
        self.df_label = ctk.CTkLabel(self, text="")
        self.df_label.grid(row=3, column=0, columnspan=num_vars+2)  # Adjust the grid position as needed

        

    def update_entries(self):
        num_vars = int(self.num_vars_input.get())
        num_points = 3 + 2**num_vars + num_vars
    
        # Remove old entries
        for row in self.entries:
            for entry in row:
                entry.grid_forget()

        # Forget old header labels
        for label in self.headers_labels:
            label.grid_forget()

        # Clear the headers_labels list to prepare for new headers
        self.headers_labels = []

        default_value = 1
        self.entries = []
        for i in range(num_points):
            self.entries.append([])
            for j in range(num_vars+1):
                default_value = f"{i}.{j}"
                entry = ctk.CTkEntry(self)
                entry.insert(0, default_value)
                entry.grid(row=i+2, column=j, padx=3, pady=3)
                self.entries[i].append(entry)
    
        # Labels for common headers
        label_ponto = ctk.CTkLabel(self, text="Ponto")
        label_ponto.grid(row=1, column=0, padx=3, pady=3)
        self.headers_labels.append(label_ponto)

        label_resultado = ctk.CTkLabel(self, text="Resultado")
        label_resultado.grid(row=1, column=num_vars, padx=3, pady=3)
        self.headers_labels.append(label_resultado)
    
    def to_dataframe(self):
        num_vars = int(self.num_vars_input.get())
    
        # Prepare the column names
        columns = [f'Coordinate_{i}' for i in range(1, num_vars+1)] + ['Resultado']

        data = []

        for row in self.entries:
            # For each row of entries, extract the values and append to data
            row_data = [entry.get() for entry in row]
            data.append(row_data)

        df = pd.DataFrame(data, columns=columns)
        return df
    
    def print_dataframe(self):
        df = self.to_dataframe()
        # Convert the DataFrame to a string and set the label text
        self.df_label.configure(text=df.to_string())
    

        

class ModelagemPage(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Add the sidebar
        self.sidebar = Sidebar(self)

        # Extended input section
        self.extended_input = ModelagemInput(self)
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
    app.geometry("1024x1024")
    app.title("Parâmetros Page")
    app.mainloop()


def open_welcome():
    welcome_app = WelcomePage()
    welcome_app.geometry("1024x576")
    welcome_app.title("Welcome Page")
    welcome_app.mainloop()


def open_modelagem():
    modelagem_app = ModelagemPage()
    modelagem_app.geometry("1024x1024")
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
        welcome_btn = ctk.CTkButton(
            self, text="Welcome", command=lambda: open_welcome()
        )
        welcome_btn.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

        # Add the Parâmetros button
        parametros_btn = ctk.CTkButton(
            self, text="Parâmetros", command=lambda: open_parametros()
        )
        parametros_btn.grid(row=0, column=1, padx=20, pady=5, sticky="ew")

        # Add the Modelagem button
        modelagem_btn = ctk.CTkButton(
            self, text="Modelagem", command=lambda: open_modelagem()
        )
        modelagem_btn.grid(row=0, column=2, padx=(20, 1000), pady=5, sticky="ew")


# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# App Frame
app = ctk.CTk()
app.geometry("1024x576")
app.title("C.H.A.S.S.I.")

# Title
title_label = ctk.CTkLabel(
    app, font=("Arial", 108), text="C.H.A.S.S.I"
)  # Dark theme blue
title_label.pack(pady=100)

# Subtitle
subtitle_label = ctk.CTkLabel(
    app,
    font=("Arial", 16),
    text="Catalyst Hybrid And Single-propellant System design Interface",
)
subtitle_label.pack()

# Link to documentation
link_btn = ctk.CTkButton(app, text="Read the docs and get started", command=open_docs)
link_btn.pack(pady=20)

# # Sidebar
sidebar = Sidebar(app)

# App main loop
if __name__ == "__main__":
    app.mainloop()
