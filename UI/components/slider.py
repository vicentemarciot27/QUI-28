import tkinter as tk
import customtkinter as ctk

ctk.set_appearance_mode("dark")

class CustomSlider(tk.Frame):
    def __init__(self, _from = 2, _to = 3, discrete = True, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self._from = _from
        self._to = _to
        self.slider = ctk.CTkSlider(self, from_=self._from, to=self._to, command=self.on_slider_change)
        self.slider.set(self._from)
        self.slider.pack()
        self.slider._button_color = "#0a4b78"
        self.slider._button_hover_color = "#043959"
        self.slider._bg_color = "#242424"
        
        if(discrete):
            self.slider._number_of_steps = self._to - 1

        # Bind the function to the slider's change event
        self.slider.bind("<ButtonRelease-1>", self.on_button_release)
    
    def on_slider_change(self, value):
        # Convert the string value to integer
        slider_value = int(value)
    
        # Change color to red if value is 3, else default color
        if slider_value == self._to:
            self.slider._button_color = "#d63638"
            self.slider._button_hover_color = "#8a2424"
        else:
            self.slider._button_color = "#0a4b78"
            self.slider._button_hover_color = "#043959"
    
    def on_button_release(self, event):
        self.on_slider_change(self.slider.get())

    def get(self):
        return self.slider.get()

    def set(self, value):
        self.slider.set(value)


if __name__ == '__main__': 
    app = tk.Tk()
    app.title("Custom Slider Component")

    slider_component = CustomSlider(app)
    slider_component.pack()

    app.mainloop()
