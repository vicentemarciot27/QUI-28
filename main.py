import tkinter as tk
import customtkinter as ctk

# class Resposta:
#     def __init__(self):
#         self.respondeu = False
#         self.text = "Notext :("

# def send(resposta):
#     ans = (int(nvariaveis.get()) * 3)
#     resposta.text = customtkinter.CTkLabel(app, text="O dobro é " + str(ans))
#     resposta.text.pack(pady = 10)
#     resposta.respondeu = True

# # System Settings
# customtkinter.set_appearance_mode("System")
# customtkinter.set_default_color_theme("blue")

# # Our app Frame
# app = customtkinter.CTk()
# app.geometry("1024x576")
# app.title("C.H.A.S.S.I.")

# # Adding UI Elements
# title = customtkinter.CTkLabel(app, text="Catalyst Hybrid And Single-propellant System design Interface")
# title.pack(padx=20, pady=20)
# subtitle = customtkinter.CTkLabel(app, text="Insira o número de variáveis")
# subtitle.pack(padx=20, pady=20)

# # Input de numero
# nvariaveis = tkinter.StringVar()
# input = customtkinter.CTkEntry(app, width=350, height=40, textvariable=nvariaveis)
# input.pack(padx=20, pady=20)

# # Botao de ação
# resposta = Resposta()
# botao = customtkinter.CTkButton(app, text="Calcular", command=lambda: send(resposta))
# botao.pack(pady=10)

# # Run App
# app.mainloop()

class MainApplication(tk.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        
        
        # System Settings
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")


        # Our app Frame
        self.root = ctk.CTk()
        self.root.geometry("1280×720")
        self.root.title("C.H.A.S.S.I.")


        label = ctk.CTkLabel(self.root, text="Catalyst Hybrid And Single-propellant System design Interface")
        label.pack()








if __name__ == "__main__":
    root = tk.Tk()
    MainApplication(root).pack(side="top", fill="both", expand=True)
    root.mainloop()