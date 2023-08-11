import tkinter as tk
import customtkinter as ctk


class Resposta:
    def __init__(self):
        self.respondeu = False
        self.text = "Notext :("


def send(resposta):
    ans = int(nvariaveis.get()) * 2
    resposta.text = ctk.CTkLabel(app, text="O dobro é " + str(ans))
    resposta.text.pack(pady=10)
    resposta.respondeu = True


# System Settings
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Our app Frame
app = ctk.CTk()
app.geometry("1024x576")
# app.maxsize(width = 1024, height = 576)
app.title("C.H.A.S.S.I.")

# Adding UI Elements
title = ctk.CTkLabel(
    app, text="Catalyst Hybrid And Single-propellant System" "design Interface"
)
title.pack(padx=20, pady=20)
subtitle = ctk.CTkLabel(app, text="Insira o número de variáveis")
subtitle.pack(padx=20, pady=20)

# Input de numero
nvariaveis = tk.StringVar()
input = ctk.CTkEntry(app, width=350, height=40, textvariable=nvariaveis)
input.pack(padx=20, pady=20)

# Botao de ação
resposta = Resposta()
botao = ctk.CTkButton(app, text="Calcular", command=lambda: send(resposta))
botao.pack(pady=10)


# Como configurar multiplas janelas
def nova_tela():
    nova_janela = ctk.CTkToplevel(app)
    nova_janela.geometry("1024x576")

btn_novatela = ctk.CTkButton(app, text="Nova Tela", command=nova_tela)
btn_novatela.pack(pady=10)

#

# Run App
app.mainloop()
