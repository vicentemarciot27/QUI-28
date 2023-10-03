import customtkinter as ctk

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
        self.toggle_btn.grid(row=4, columnspan=3, pady=10)

        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_data)
        self.send_button.grid(row=5, column=3, padx=5, pady=5)
        
    def send_data(self):
        # Implement the logic to handle data sending here
        pass

    def toggle_third_row(self):
        if self.third_row_visible:
            for widget in self.entries[2]:
                widget.grid_remove()
            self.third_row_visible = False
        else:
            for col, widget in enumerate(self.entries[2]):
                widget.grid(row=3, column=col, padx=5, pady=5)
            self.third_row_visible = True

class ExtendedInput(ctk.CTkFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        # Labels
        
        # Additional Labels and Inputs
        ctk.CTkLabel(self, text="Value").grid(row=0, column=3, padx=3, pady=3)
        self.value_entry = ctk.CTkEntry(self)
        self.value_entry.grid(row=1, column=1, padx=3, pady=3)

        ctk.CTkLabel(self, text="Max Value").grid(row=0, column=3, padx=3, pady=3)
        self.max_value_entry = ctk.CTkEntry(self)
        self.max_value_entry.grid(row=1, column=3, padx=3, pady=3)

        ctk.CTkLabel(self, text="Min Value").grid(row=0, column=4, padx=3, pady=3)
        self.min_value_entry = ctk.CTkEntry(self)
        self.min_value_entry.grid(row=1, column=4, padx=3, pady=3)

        ctk.CTkLabel(self, text="Delta").grid(row=0, column=5, padx=3, pady=3)
        self.delta_entry = ctk.CTkEntry(self)
        self.delta_entry.grid(row=1, column=3, padx=3, pady=3)

        self.is_integer_check = ctk.CTkCheckBox(self, text="Is Integer")
        self.is_integer_var1 = self.is_integer_check.get()
        self.is_integer_check.grid(row=1, column=8, columnspan=2, padx=3, pady=3)
        ctk.CTkLabel(self, text="Nome da variável").grid(row=0, column=0, padx=3, pady=3)
        ctk.CTkLabel(self, text="Valor").grid(row=0, column=1, padx=3, pady=3)
        ctk.CTkLabel(self, text="Unidade de medida").grid(row=0, column=2, padx=3, pady=3)
        
        # Entries for first row
        self.var_name_entry1 = ctk.CTkEntry(self)
        self.var_name_entry1.grid(row=1, column=0, padx=3, pady=3)  
        
        self.value_entry1 = ctk.CTkEntry(self)
        self.value_entry1.grid(row=1, column=1, padx=3, pady=3)
        
        self.unit_entry1 = ctk.CTkEntry(self)
        self.unit_entry1.grid(row=1, column=2, padx=3, pady=3)
        
        self.var_max_entry1 = ctk.CTkEntry(self)
        self.var_max_entry1.grid(row=1, column=3, padx=3, pady=3)  
        
        self.var_min_entry1 = ctk.CTkEntry(self)
        self.var_min_entry1.grid(row=1, column=4, padx=3, pady=3)
        
        self.var_delta_entry1 = ctk.CTkEntry(self)
        self.var_delta_entry1.grid(row=1, column=5, padx=3, pady=3)
        
        # Entries for second row
        self.var_name_entry2 = ctk.CTkEntry(self)
        self.var_name_entry2.grid(row=2, column=0, padx=3, pady=3)
        
        self.value_entry2 = ctk.CTkEntry(self)
        self.value_entry2.grid(row=2, column=1, padx=3, pady=3)
        
        self.unit_entry2 = ctk.CTkEntry(self)
        self.unit_entry2.grid(row=2, column=2, padx=3, pady=3)
        
        # Hidden row for third variable
        self.var_name_entry3 = ctk.CTkEntry(self)
        self.value_entry3 = ctk.CTkEntry(self)
        self.unit_entry3 = ctk.CTkEntry(self)
        
        # # Toggle button to show/hide third row
        # self.toggle_btn = ctk.CTkButton(self, text="Toggle Third Variable",
        #                                 command=self.toggle_third_row)
        # self.toggle_btn.grid(row=4, columnspan=3, pady=10)
        self.send_button = ctk.CTkButton(self, text="Send", command=self.send_data)
        self.send_button.grid(row=7, column=3, padx=5, pady=5)
        
    def send_data(self):
        # Implement the logic to handle data sending here
        pass
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
