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

        
    
        all_parameters = []
    
        # Check if the third row is visible
        third_row_visible = self.third_row_visible
    
        for index, row_entries in enumerate(self.entries):
            # Skip the third row if it's not visible
            if index == 2 and not third_row_visible:
                continue
            
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
            all_parameters.append(parameter)

        # Generate the fatorial plan and then convert it to a real plan using the return_plan function
        fatorial = FatorialPlan(len(all_parameters), math.sqrt(2))
        fatorial_plan_list = fatorial.fatorial
        real_plan = return_plan(all_parameters, fatorial_plan_list)
        
        output_strings = []
        for param in all_parameters:
            output_string = f"The variable {param.name} with unit of measure {param.unit} needs to use the following points: {real_plan}"
            output_strings.append(output_string)
        self.output_label.config(text="\n".join(output_strings))
print(param.upper_limit)  # Just for debugging.



    def toggle_third_row(self):
        if self.third_row_visible:
            for widget in self.entries[2]:
                widget.grid_remove()
            self.third_row_visible = False
        else:
            for col, widget in enumerate(self.entries[2]):
                widget.grid(row=3, column=col, padx=5, pady=5)
            self.third_row_visible = True


class